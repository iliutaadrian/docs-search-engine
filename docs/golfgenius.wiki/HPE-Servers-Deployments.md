This Wiki covers a short description and the process of deploying changes to Golf Genius [HPE Servers](http://hpe.golfgenius.com/). 


## HPE Servers Summary
HPE Servers are a copy of the TMS Application running on a separate instance. This entails separate servers, databases, caching, workers, etc., completely segregated from the regular TMS. 

They have been designed to be the most stable version of the TMS Application. This was done to run our most noteworthy tournaments from the PGA, USGA, etc., alleviating the need for deployment freezes on regular TMS. 

### Branches
HPE Servers have 3 main branches in this repository: 
* **hpe_dev** - this contains the develop code(similar to **develop**)
* **hpe_staging** - this points to the HPE Staging(similar to feature/ggstest) [Server](http://hpe.ggstest.com/)
* **hpe_production** - this contains production code and is similar  to the HPE Production [Server](https://hpe.golfgenius.com/)

## Prerequisites
* Go through the HPE Version Control [Document](https://docs.google.com/document/d/1PkjpcULMBE6pvpy3SN3pwJyAagP3YpqDGWAROY_Ek4E/edit?pli=1). 
* [Install](https://docs.google.com/document/d/1PkjpcULMBE6pvpy3SN3pwJyAagP3YpqDGWAROY_Ek4E/edit?pli=1#heading=h.lm44vrtf83p0) the `git hpe` extension. 
* Obtain access to HPE Deployment [Repo](https://github.com/golfgenius/hpe_deployment) and HPE VPN. (ping @Mircea or @Mihail.Muscalita)


## Releases
![Screenshot 2024-04-09 at 15 24 37](https://github.com/golfgenius/golfgenius/assets/29895369/5569a54e-d19d-4fdd-ae4e-86a70ca5c288)


### TMS ➡️ HPE
Step by step process to release from **master** to **hpe_production**. 
1. Create an **hpe_update** PR <br/>
`git hpe update start jan_23`<br/>
OR<br/>
`git checkout feature/develop_regular_hpe`<br/>
`git checkout -b hpe_update/jan_23`<br/>
Example [PR](https://github.com/golfgenius/golfgenius/pull/43324).<br/> 
🚨  In the PR Description get all commands that need to be run. 🚨 
2. Merge in **hpe_dev**
3. Deploy to HPE Staging. This step is **mandatory**(see [Deployments](#deployments)).<br/>
`git checkout hpe_staging`<br/>
`git merge hpe_dev`<br/>
`git push origin hpe_staging`<br/>
`git push hpe_deployment hpe_staging:dev`<br/>
4. Create **hpe_release** PR. <br/>
`git hpe release start jan_23`<br/>
Example [PR](https://github.com/golfgenius/golfgenius/pull/43329). <br/>
🚨  In the PR Description copy all commands that need to be run. 🚨 
5. Merge in **hpe_production**.
6. Deploy to HPE Prod. (see [Deployments](#deployments))

### HPE ➡️ TMS
Step by step process to release from **hpe_production** to **master**. 
1. Create an **feature** PR into **develop** <br/>
`git checkout hpe_production`<br/>
`git checkout -b feature/merge_hpe_mar_23`<br/>
Example [PR](https://github.com/golfgenius/golfgenius/pull/43491).<br/> 
🚨  In the PR Description get all commands that need to be run. 🚨 <br/>
After this, the **Merge HPE** is considered to be a function in the TMS Development cycle. <br/>
All processes like Code Reviews, Scheduling, Tests, QA, Release branches, etc. apply to it in the same way as any TMS Function. 

## Deployments <a id='deployments'></a>

### HPE Deployments Repo
HPE Servers are deployed in this [repo](https://github.com/golfgenius/hpe_deployment).
There are two branches of importance: 
* **dev** -> this points to the HPE Staging [Server](http://hpe.ggstest.com/)
* **prod** -> this points to the HPE Production [Server](https://hpe.golfgenius.com/)

Any changes in these branches will trigger a deployment through the CI/CD. 

### Deployments 
#### Staging
* Have everything merged in the `hpe_staging` branch 
* Push to the HPE Deployment Repo: `git push hpe_deployment hpe_staging:dev`

#### Production
* Have everything merged in the `hpe_production` branch 
* Push to the deploy branch in the HPE Deployment Repo: `git push hpe_deployment hpe_production:deploy`
* Create PR to prod; Get at least one approval (Example [PR](https://github.com/golfgenius/hpe_deployment/pull/11) ) 
* Merge in prod to start deployment

### Access
In order to deploy, you need access to the following: 
* HPE Deployment [repo](https://github.com/golfgenius/hpe_deployment) - to deploy 
* HPE Prod VPN - console access for migrations etc. 

To obtain access ping @Mircea and @Mihail Muscalita. 

### Restrictions
* No deployments during HPE Deployment Freezes
* Just as TMS, only deployers have access to deploy
* Deployments must happen before 1 PM Ro Time (6 AM EST). 











