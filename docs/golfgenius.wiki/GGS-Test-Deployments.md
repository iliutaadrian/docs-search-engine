This document outlines the procedures for Deployments on https://ggstest.com/
![Screenshot 2024-06-21 at 16 48 36](https://github.com/golfgenius/golfgenius/assets/29895369/a5ddac70-1a6f-40dd-9a15-bec61ad03481)

### Branching model
The relevant branches are the following ones: 
* **feature/ggstest#golfgenius** - branch contains all the code that gets to ggstest from the `golfgenius` repo
* **ggstest_deploy#golfgenius_deployment** - branch in `golfgenius_deployment` repo, place to prepare all the code for the deployment 
* **ggstest#golfgenius_deployment** - branch in `golfgenius_deployment` repo that goes directy to deployment; branch protected and can only be pushed through with with 1 approval

### Deployment Process
The deployment will have the following steps: 
1. Push code to **feature/ggstest** branch 
2. Solve any conflicts 
3. Push code to **ggstest_deploy** branch on `golfgenius_deployment` repo. PR should be automatically created
4. Get at least one approval. 
5. Merge PR in **ggstest** branch. 
6. Wait for Deploy to finish, check if successful and run migrations/extra commands if applicable.

Commands:<br/>
`git checkout feature/ggstest`<br/>
`git merge feature/yourFeature`<br/>
`git push origin feature/ggstest`<br/>
`git push deployment feature/ggstest:ggstest_deploy`<br/>


### Revert in case of errors
1. Recreate **feature/ggstest** branch <br/>
`#delete remote branch`<br/>
`git push -d origin feature/ggstest `<br/>
`#delete local branch`<br/>
`git branch -D feature/ggstest`<br/>
`#recreate branch`<br/>
`git fetch deployment`<br/>
`git checkout -b feature/ggstest deployment/ggstest`<br/>
`git push origin feature/ggstest`<br/>

2. Recreate **ggstest_deploy** branch<br/>
`#delete remote branch`<br/>
`git push -d deployment ggstest_deploy`<br/>
`#delete local branch`<br/>
`git branch -D ggstest_deploy`<br/>
`#recreate branch`<br/>
`git fetch deployment`<br/>
`git checkout -b ggstest_deploy deployment/ggstest`<br/>
`git push deployment ggstest_deploy:ggstest_deploy`<br/>



