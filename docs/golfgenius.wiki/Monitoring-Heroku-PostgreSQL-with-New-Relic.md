As of 5/1/2017, we have installed the PostgreSQL plugin to our New Relic dashboard.  This is available at https://rpm.newrelic.com/accounts/84565/plugins/29215.  Whenever a new database is added or removed, the monitoring proxy application will need to be updated.

## Instructions
Monitoring is facilitated by the golfgenius/postgresql-monitor application.  To update its config variables, issue the following command:

```
heroku config:set $(heroku config --shell --app golfleaguegenius | egrep 'NEW_RELIC_LICENSE_KEY|postgres://') --app postgresql-monitor
```
The monitoring app will restart and shortly start including data from new databases 