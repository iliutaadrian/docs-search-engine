# Concurrent Indexing

Indexes on tables can be added using the concurrent algorithm; this allows indexing without any lock, thus excluding any app-level effects.

The only downside of running async indexes is that it takes a bit longer and can't run in transactions (meaning if an error occurs, there is no rollback possibility).


 
Example

```
class AddIndexToParametrizedJobs < ActiveRecord::Migration[5.1]
  disable_ddl_transaction! # Disable ddl transaction that Rails use by default

  def change
    add_index :parametrized_jobs, :job_id, algorithm: :concurrently # Specify custom alogirthm
  end
end
```

Postgres [docs](https://www.postgresql.org/docs/current/sql-createindex.html).