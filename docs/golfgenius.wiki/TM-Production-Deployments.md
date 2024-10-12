Deployments go through a two-step process, where a deployment is first prepared and documented by one person, and then reviewed by another one.

# Documenting Deployments

The initial deploy PR is prepared by Jira every weekday at 4:00 UTC.

If you are the Deployer, make sure it includes the following:

* Correct date
* All merged Jira Issues
* Other PRs/changes part of the changelog
* Latest test results - Check Jenkins email (GLG-Develop - Build)
* Any other information or console commands/migrations that should be run after the build finished

<img width="938" alt="Screenshot 2022-12-29 at 15 35 27" src="https://user-images.githubusercontent.com/16760229/209961341-783a55b1-cdd1-4088-9e4f-a069c902a539.png">

Fig. 1 - Example of a Deployment PR

# Reviewing a Successful Deployment

Deployments are checked for any breaking or intrusive changes. 

After a reviewer approved the deployment, it can be merged using GitHub's Merge Pull Request option. This will automatically trigger a deployment. Build monitoring is done through BuildBot and Kubernetes, and errors are monitored through HoneyBadger.

<img width="958" alt="Screenshot 2022-12-29 at 15 36 54" src="https://user-images.githubusercontent.com/16760229/209961438-2d729e12-89d9-49a3-98bd-fd48e018adf8.png">

Fig. 2 - Clicking the Merge button after the PR is approved triggers a Deployment

# After Deployments

After a successful deployment, use Jira's Releases function to notify everybody. Rename the latest Release to include the current date and click Release to mark it as complete.

1. Go to https://golfgenius.atlassian.net/projects/TM?selectedItem=com.atlassian.jira.jira-projects-plugin%3Arelease-page
1. Open Release (Clik on the name)
1. Blue "Release" button 
1. Orange "Release" button

<img width="1314" alt="Screenshot 2022-12-29 at 15 38 06" src="https://user-images.githubusercontent.com/16760229/209961569-ef24d226-fe8c-4802-a477-81bf5fa24214.png">

Fig. 3 - Jira Release Page (Clicking the blue Release button)

<img width="1314" alt="Screenshot 2022-12-29 at 15 38 29" src="https://user-images.githubusercontent.com/16760229/209961608-2cd314f6-12d5-46ce-90b2-293fa9180878.png">

Fig. 4 - Jira Release Page (Clicking the orange Release button)

# GitHub Setup

Add the deployment remote:

```sh
# SSH
git remote add deployment git@github.com:golfgenius/golfgenius_deployment.git
```

```sh
# HTTPS (Legacy)
git remote add deployment https://github.com/golfgenius/golfgenius_deployment.git
```

In case you need to rewrite the remote:

```sh
git remote rm deployment
```

Now, push the latest changes to the repository for production builds using the custom shell script.

```sh
sh ./dev_ops/deploy.sh
```

### (High Risk!) For Quick Deployments use the following:

```sh
git fetch deployment
git branch -D quick-deploy
git checkout -b quick-deploy deployment/production
git cherry-pick commit_hash
git push deployment quick-deploy:quick-deploy
```