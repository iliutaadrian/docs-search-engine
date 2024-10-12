The dev_ops folder contains some useful scripts for automating repetitive actions.
[https://github.com/golfgenius/golfgenius/tree/master/dev_ops](https://github.com/golfgenius/golfgenius/tree/master/dev_ops)

# Setup

Use this script to make using the following tools easier.
It will install all dependencies and create aliases.

Run:

```
cd dev_ops
touch .db # add db config here
sh setup.sh
cd ..
zsh
```

!!! Make sure your terminal has the necessary permissions. 
You can go to Mac Settings > Security & Privacy > Privacy > Accessibility > Check Terminal.

Now you have the following command available
from the root of the project.

# Start server

Local database

```
start-local
```

Frankfurt database

```
start-frankfurt
```

Opens:
* console
* server
* rake
* queue
* memcached
* webpack

# Review

Use to checkout branches

```
review branch
# review hotfix/abc
# review feature/abc
```

# Merge

Use to merge hotfix/feature branches

```
merge branch
# merge hotfix/abc
# merge feature/abc
```

# Static analysis

Runs pronto with cached linters

```
analysis
```
