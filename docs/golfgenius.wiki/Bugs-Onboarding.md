### You need access to the following:
* (Legacy) GolfGenius GMail - you should receive emails from the support team and notifications regarding deployments
* Intercom - for additional intel on user-facing issues (you should be able to create an account using your GolfGenius email)
* HoneyBadger - to search for incidents when an issue is giving an error message or an Oops page (you should be able to connect using your TakeOffLabs email)
* Admin account - you should have a "+admin" account on the production database 
* Frankfurt Database - you need an admin account on the Frankfurt DB for debugging in a sandbox environment


### You should know how to use:
* [Bugs Tracking Project](https://github.com/golfgenius/golfgenius/projects/46) - kanban board for keeping track of bugs-related work
* [GitFlow](https://danielkummer.github.io/git-flow-cheatsheet/) - create a hotfix branch when preparing a fix for an Issue, create a Pull Request afterward following the template
* [Knowledge Base](http://docs.golfgenius.com/content) - user-facing articles about commonly misunderstood features
* [Feature Specs](https://drive.google.com/drive/u/2/folders/0BwpZoxRW--QlZUd5RnVsZ0lvVWM) - all the intel gathered before implementing new features, documentation for the intended behavior of a feature
* [HoneyBadger](https://github.com/golfgenius/golfgenius/wiki/Honeybadger-search-by-params) - how to find related incident information

### General Flow

![MES Flowchart (1)](https://user-images.githubusercontent.com/16760229/78232906-3ab4b980-74d5-11ea-9988-89493133d506.png)

The main activity on Bugs Watch is solving the incidents reported by our Support Team. When a support ticket is believed to be a bug, the support representative sends an email to bugs@golfgenius.com detailing the issue. We investigate these tickets and try to determine whether the reported problem is a bug (throws an error, confuses the user, doesn't work as expected, etc.) and then come up with a fix.

For every email that we receive from the Support Team, we automatically open an Issue on GitHub. Every morning, a list with the most important Issues is posted on Slack, including suggestions about the best person to investigate the issue and who could help with providing additional information to the team.

As a Guardian, your duty is to determine what is the source problem that created a bug and suggesting possible ways of fixing that problem. After your solution is discussed, you will create a Pull Request detailing your solution by following the default template. After creating a PR, you should add the `needs review` label to the corresponding Issue.

Your solution will be reviewed by someone from the team and, if it passes all the quality checks, it will be merged into the master branch. The `reply and close` label will be added to the related Issue and you will be asked to send an email back to the support team explaining what was causing the problem and how was it fixed. Keep in mind that fixes are only available on production after they are deployed.