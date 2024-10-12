## What is LDS?

LDS (Local Data Storage) is a per-request caching mechanism implemented through a combination of Ruby's internal `Thread.current` data storage with Ruby's OOP instance variables belonging to an instance of a class.

## How is it used?

Most of it use cases appear when some data should be communicated to multiple parts of the application without having to pass them through all the methods' callstack.

Other use cases is actually similar to a cache, where you store already computed data to make sure you don't have to process it again. (Some of this functionality would also be taken care of by the ActiveRecord query caching)

A clear example of this would be in the scoring part of the application:

```ruby
  def self.prepare_lds(basis)
    Lds.ds.invalidate!
  
    round_ids = basis.map { |event|
      event.round_id.presence || event.children_events.map(&:round_id)
    }.flatten.compact.uniq

    players = Player.where(round_id: round_ids) \
                    .where("foursome_id is not null").to_a

    foursomes = Foursome.where(id: players.pluck(:foursome_id)).to_a

    Lds.ds.store_array(players)
    Lds.ds.store_array(foursomes)
    Lds.ds.store_array(Score.where(player_id: players.collect(&:id)))
    Lds.ds.store_array(PlayoffScore.where(player_id: players.collect(&:id)))
    
    Lds.ds.add_index(Score, "player_id")
    Lds.ds.add_index(PlayoffScore, "player_id")
  end
```

The function above stores 4 arrays and adds 2 indexes in the Lds, which are then called further down the road in the scoring process, thus making the whole calling chain easier to manage and understand.

```ruby
...
foursome_id = Lds.ds.find(Player, round_aggregate.nets&.first&.player_id)&.foursome_id
tee_time = 
  if foursome_id.present?
    Lds.ds.find(Foursome, foursome_id)&.official_tee_at
  else
    nil
  end || round_aggregate.start_tee_time
...
```

The snippet of code above is used in the `display_order` function in the `new_aggregate.rb` file. Due to the previously-stored variables in the Lds, the queries for foursomes and players based on their associated IDs are not run anymore, and the objects are extracted directly from the memory.

## Core Principles

In staging and production, our current application is running on unicorn. This means that it's a single-thread multi-process server. A unicorn server, has multiple workers, each of them staying alive until they run out of memory (?MEMORY LEAK WARNING?), they get killed by the unicorn-worker-killer trying to prevent memory leaks, or they just restart due to deployments. This means that each forked process owns a single thread upon which everything server-side is executed.

The single-threaded part of the paragraph above is essential for the current Lds implementation to function. The reason for that being that whenever we want to use the per-request functionality, we call a `Lds.ds.ANY_GENERIC_METHOD`. What `Lds.ds` does is:

```ruby
  def self.ds
    Thread.current[:ds] ||= Lds.new
  end
```

Which will always return the current Lds class instance stored in the thread, or create a new one.

Then comes the instance variables part. Most of the methods in the `lds.rb` file are just abstractions over one basic method that is called `get_local_store`. What this method does is:

```ruby
  def get_local_store(name)
    local_store = instance_variable_get(name)
    if local_store.blank?
      instance_variable_set(name, {})
      local_store = instance_variable_get(name)
    end
    return local_store
  end
```

Which checks for the name, that acts as a cache key, using ruby's [instance_variable_get](https://apidock.com/ruby/Object/instance_variable_get). If it doesn't find an instance variable (store) with the mentioned name, it creates one using [instance_variable_set](https://apidock.com/ruby/Object/instance_variable_set) that defaults to an empty hash and then returns it. This hash then gets filled with key/value pairs representing IDs and their associated objects.

So, what Lds does is basically storing an instance of the Lds class in the current thread, and then attaching instance variables to the aforementioned instance, in either their raw form or through stores, that can be easily accessible through wrapper methods.

## Wait, is this safe?

Two very important facts that do not go well together have been mentioned above. We mentioned unicorn has multiple workers which stay alive, using their own main thread. But then we said that Lds should be a per-request caching mechanism, right? So, given the current setup, are we not creating an infinitely growing store that will just keep adding more and more objects to the same thread?

Well, yes, but no.

On the server side, before each request gets processed, the `load_data_store` hook is called:
```ruby
  def load_data_store
    Thread.current[:ds] = Lds.new
  end
```
which removes the reference to the old Lds instance from the thread, thus leaving it to be collected by the garbage collector.

As for the async jobs, given that resque forks a new process for each job that gets processed on a worker, they each get a new thread, so the data does not get passed around or it does not end in the wrong place.

## A few step-by-step method explanations

Given that most method in that file already have indicative comments before them, we will take a more detailed look at only a few of them

### find

```ruby
  # Find an object, either in local store or from SQL
  #
  # Lds.ds.find(Tee, 7286)
  def find(class_name, id)
    return nil if id.blank?
    variable = get_variable_for_class(class_name)
    store = get_local_store(variable)
    
    store[id] = class_name.find_by_id(id) if store[id].blank?
    return store[id]
  end
```

The method accepts the class_name and an associated ID as parameters.

1. It returns nil if no id is given.
2. It creates an instance variable name based on the class name using string interpolation `"@#{cls.to_s.downcase.gsub(":", "_")}_by_id"`. In the example given in the comments, it would bee `"@tee_by_id`.
3. It looks for the current Lds store for the variable.
4. If there is currently no object inside the store associated with that id, it uses the MODEL.find_by_id(id) ActiveRecord specific method to run an SQL query and then place the object in the store.
5. The object is returned and is now saved in the cache.

The LDS would look like
```ruby
Lds.ds
> #<Lds:someid @tee_by_id={ID_1 => TeeObjectWithId1, ID_2 => TeeObjectWithId2 ...}>
```

### store_array

```ruby
  # Store an array of objects, not necessarly the same class,
  # in the Lds
  #
  # Lds.ds.store_array(League.find(1140).courses)
  def store_array(array_of_objects, class_name = nil)
    array_of_objects.each do |obj|
      store_object(obj, class_name) if obj.present?
    end
  end
```

The above code basically allows storing an array of objects (very likely designed to be exclusively Model objects) **who have an associated id**, regardless of their classes.

The function iterates through the array and then uses the `store_object` method

```ruby
  def store_object(obj, class_name = nil)
    name = class_name.present? ? class_name : obj.class
    variable = get_variable_for_class(name)
    store = get_local_store(variable)
    store[obj.id] = obj
  end
```

to find or create a store and then place the `obj` object inside it, if `obj` is present.

The above bolded constraint about IDs is exactly because of the `store_object` method which would throw an error if the passed objects do not have an id accessible instance variable/ method.

### set_in_cache & get_from_cache

```ruby
  # Per request cache
  def get_from_cache(name)
    instance_variable_get("@#{name}")
  end
  
  def set_in_cache(name, value)
    instance_variable_set("@#{name}", value)
  end
```

All of the other functions in the Lds implementation are based on a store which uses hash. However, in case you do not want to be bound by the constraints of the wrapper, you can directly use the above functions to create your own instance variables on the Lds.

## VERY IMPORTANT INFORMATION

The current implementation does not serialize and deserialize the objects.

While this might be the faster way of implementing this, one should proceed with caution when writing code using the Lds.

### The SAME(not a copy or clone or a newly initialized one) Object:

#### Example

```ruby
test_variable = Customer.last
test_variable.name == 'Customer Name' # => true
Lds.ds.set_in_cache('test_123', test_variable)
test_variable == Lds.ds.get_from_cache('test_123') # => true
test_variable.name = 'New Name for LDS Test'
Lds.ds.get_from_cache('test_123').name == 'New Name for LDS Test' => TRUE.
```

This basically means that if in a hypothetical scenario, we could modify things about the object stored in memory which could then end up in places where it should not have been.

A good example is to think of it as
```ruby
test_obj_1 = {}
test_obj_2 = test_obj_1
test_obj_3 = test_obj_1.clone
test_obj_1[:test] = 32
test_obj_1 # {:test => 32}
test_obj_2 # {:test => 32}
test_obj_3 # {}
```

The Lds would behave like `test_obj_1` and `test_obj_2`.

### Everything gets saved

When saving objects in the Lds (either through `store_array`, or `set_in_cache`, or `store_variable`), EVERYTHING about the objects gets added to memory. So if the objects you are trying to save also have models preloaded on them, then the associated preloaded model objects will also be saved.

#### Example
```ruby
test_variable = Customer.where(id: 19059).includes(:text_messaging_setting).last # Runs 2 queries, one for `Customer`, one for `CustomerTextMessagingSetting`.
Lds.ds.store_array([test_variable])
Lds.ds.find(Customer, 19059) # Finds the test_variable.
Lds.ds.find(Customer, 19059).text_messaging_setting # Directly loads the object, and does not run a query anymore.
```

While the above might seem like a warning, the initial Lds design was done with this in mind. So, while it can be potentially dangerous, as long as we are aware of what we are doing, we can avoid creating weird-13-hours-looking-for-the-line-of-code-for-it-to-lead-to-lds bugs.