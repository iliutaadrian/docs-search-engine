`install yarn: https://yarnpkg.com/lang/en/docs/install/`  

Install the items below; when it tries to override files, say no: n

`bundle exec rails webpacker:install`  
`bundle exec rails webpacker:install:react`  
`npm install (to update libraries and modules)`  
`./bin/webpack-dev-server`

To migrate to the new Customer Center (remove this logic after release)

`rake db:migrate`  
`Sharding::TenantManagement.migration_new_table("sharded_lists")`  
`Sharding::TenantManagement.migration_new_table("sharded_leagues_lists")`  

Once you are do with this, the Customer Center will be empty for all your customers; you can repopulate them in 2 ways - by running a migration over all customers which will take a substantial amount of time, or you can migrate the customers you need to work with, both options provided below

`Migrate.compute_league_positions`  
`Migrate.move_lists_to_shards`  

Migrate a specific customer

`ResqueLibraries::ResqueComputeLeaguePositions.perform(9215)`  
`ResqueLibraries::ResqueCopyListsToShards.perform(9215)`  