A build up of background jobs on the priority queue can cause delays for golf-critical operations such as printing PDFs, generating pairings, etc. This manifests by a slowness and waiting on background jobs to finish. Depending on severity, the background jobs may be finished very late. This symptom is generally raised as a 911 by support team.

# Example (October 31, 2019)

- 911 issue: can not add rounds.
- 1st check: is it a localized honeybadger or is it happening for other background job operations (e.g., printing). It happens for printing..
- 2nd check: what is the state of the background queues? Navigate to http://www.golfgenius.com/resque_metrics and we see number of background jobs in queue_printing more than 5,000

# Emergency Procedure:

- Log in to development console (ssh into kube, rails c per kubernetes procedures).
- Run `Resque.sample_queues` to see what is currently queued. In this case, we see many instances of `ResqueLibraries::ResqueSpecMapV2` for specific IDs
- Run commands to remove these processes from the Resque queue (e.g., `Resque::Job.destroy("priority", ResqueLibraries::ResqueSpecMapV2, 780326)`)
- Refresh /resque_metrics, re-run `Resque.sample_queues`, re-run commands above until situation is stable
- In a more aggressive case, we could use more drastic destroy commands (e.g., `Resque::Job.destroy("priority", ResqueLibraries::ResqueSpecMapV2` would remove all SpecMap commands from the queue)

