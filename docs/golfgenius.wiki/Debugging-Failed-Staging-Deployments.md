1. BuildBot failure

Click the link shown in the message below.

<img width="567" alt="Screenshot 2024-07-11 at 17 04 38" src="https://github.com/golfgenius/golfgenius/assets/81558783/3b91bef7-7f58-4017-9515-186c662788aa">

Go to the latest failed step and make the dropdown visible

<img width="1476" alt="image" src="https://github.com/golfgenius/golfgenius/assets/81558783/6fe36eeb-7abe-4af2-9105-7f83ff9585fc">

Hit View all lines to see the full logs:

<img width="1453" alt="image" src="https://github.com/golfgenius/golfgenius/assets/81558783/8efd58c3-18db-45d9-962a-e1541cd41ad8">

Look for the error and fix it:

<img width="1480" alt="Screenshot 2024-07-11 at 17 07 12" src="https://github.com/golfgenius/golfgenius/assets/81558783/03a2151d-8671-4d41-9a3d-580def7b708a">

2. Pod not starting:

Check the channel for the error to find out what pod is not starting:

![image](https://github.com/golfgenius/golfgenius/assets/81558783/9b56b726-b57f-48c3-9a05-371943c0a13d)

Go to https://dash-kube.dev.tms.internal.golf-genius.com/#/log/dev-golfgenius and log in with the credentials.

Go to the namespace that interests you:

### dev = ggstest.com
### dsg = ggstest2.com
### dtg = dtg.ggstest.com

![image](https://github.com/golfgenius/golfgenius/assets/81558783/592f1eec-9cc8-4c55-9d41-43da4aa4d1a1)

Go to the pods section

![image](https://github.com/golfgenius/golfgenius/assets/81558783/99ec2a2e-d5b4-4bbe-ae2b-0dcf1b9d37c3)

Look for the `frontend` pods, as that's what the error states as crash looping, and then click it.

![image](https://github.com/golfgenius/golfgenius/assets/81558783/262d22de-f217-4369-b41b-be41aa428215)

Scroll down and see that the pod is indeed still unhealthy:

![image](https://github.com/golfgenius/golfgenius/assets/81558783/f36df85a-2aa1-4abc-99a6-28566f86270b)

Hit the 3 lines in the upper right column to see the pod logs:

![image](https://github.com/golfgenius/golfgenius/assets/81558783/4ebce59c-c298-4206-aee7-32a46a0606d7)

Select the unicorn container instead of the nginx one:

![image](https://github.com/golfgenius/golfgenius/assets/81558783/4ad1ecff-88fd-440c-8083-d0c14cbcbbdc)

Watch the logs and find the errors:

![image](https://github.com/golfgenius/golfgenius/assets/81558783/99075655-cfcf-402d-a5c7-a8651c4d3634)

3. The usual suspects:
- Files not recognised (new gems/ old files that have been deleted), should be fixed by a Base + Current rebuild.
- JavaScript out of heap memory - should re-run whatever build was being attempted.
- resque worker/ scheduler crash looping due to redis constraints - should check AWS to see redis values - very likely due to some new job which fills the redis queue.