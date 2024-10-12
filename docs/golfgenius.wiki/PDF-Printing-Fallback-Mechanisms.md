When DocRaptor is encountering issues, we have the following two fallback mechanisms:

* remove all jobs from the printing queue

```
Resque.redis.del "queue:printing"
```

* prevent any new printing jobs from being created

```
VariableSettings.create(league_id: -1, key: "disallow-printing")
```