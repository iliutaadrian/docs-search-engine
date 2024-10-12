CloudWatch returns increased usage of the redis cluster.

Can be resolved via:

```
Resque::Failure.count
Resque::Failure.clear
```