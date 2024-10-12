Ability to search honeybadger errors by parameters is important for debugging.
Searching by request params or resque job arguments does **not** work by just typing the key in the search box.


You need to select params in the search popup and use the following convention
> params.key:"*value*" 

Example: Search by player_id: 123 in params
> params.player_id:"* 123 *"

For resque jobs with arrays you can use, similarly
> params.job_arguments:"* 123 *"

**Note: For resque jobs, search seems to be working only with the first argument in the array**

Example HB search query link:
[https://heroku.honeybadger.io/projects/55816/faults?q=params.player_id%3A%225886431110262451977%22](https://heroku.honeybadger.io/projects/55816/faults?q=params.player_id%3A%225886431110262451977%22)


Reference: [https://docs.honeybadger.io/guides/search.html#search-by-request](https://docs.honeybadger.io/guides/search.html#search-by-request)

