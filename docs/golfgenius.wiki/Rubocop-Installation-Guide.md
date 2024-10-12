We are setting this code standard to improve the review process, reduce refactoring comments and improve code quality all around from code clarity to speed improvements by suggesting some more optimal ways to do things in certain cases. Moreover, following the same coding conventions makes everyone’s code easier to read.

Not conforming to the new standard will result in you stepping into a puddle every time you put on socks.

We are using the rubocop extension in vs code using our custom config defined in .rubocop.yml and, for the moment, you need to manually install 3 gems globally, in the version that you are currently using (2.7.8):

```ruby
gem install rubocop
gem install rubocop-rails
gem install rubocop-performance
```

By restarting the VSCode editor, rubocop should resolve the paths and automatically check every file you're reading.

If you're using a different editor, it's your own responsibility to make rubocop functional for your IDE.

If the file is too big (leagues.rb), rubocop will either not work or be very slow. In that specific case, to check your correctness, you can use workarounds, like moving part of the method to another file, etc.

# THIS IS MANDATORY

For any issues about installing this, contact Aron.

## Addendum

In case you manually run the rubocop actions as such `rubocop some_path` you might be getting errors that look like this:

<img width="999" alt="Screenshot 2024-07-02 at 11 47 09" src="https://github.com/golfgenius/golfgenius/assets/81558783/e825dca7-4b8f-46bc-8242-7a3795850267">

This is a rubocop issue, caused by the lack of an `else` branch, in the presence of an `elsif` branch. More specifically:

Works
```ruby
if ...

elsif ...

else

end
```

Errors Rubocop
```ruby
if ...

elsif ...

end
```

You can ignore these errors, as rubocop functions in a modular way, meaning that other rules and checks will still be applied and returned.