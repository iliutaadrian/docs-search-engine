# Introduction
The scheduler is a multi-threaded C++ binary that is responsible for quickly generating pairings.  This article deals with compilation for production/staging environments (Heroku) and development (OSX).  

## Development
1.  Ensure that your local copy is up to date in the golfgenius/scheduler repository / league-mods branch:
```
    git reset --hard
    git pull
```
2.  Edit main.cpp and verify the first three lines:
```
    #define mac 0
    #define num_threads 8
    #define debugx 0
```
3.  From the scheduler directory:
```
$ mkdir bin; ./compile.sh
$ cp bin/golf_scheduler <GOLFGENIUS_APP_DIR>/bin/scheduler_development
$ cp bin/golf_scheduler <GOLFGENIUS_APP_DIR>/bin/scheduler_test
```

## Production
1. The underlying architecture of Heroku uses Ubuntu Linux.  You can find out what Heroku stack is in use by typing the following from the golfgenius repository, and looking for the "Stack:" line.
```
    heroku apps:info 
```
  At time of writing, we are using the cedar-14 stack.  Then check [on the Heroku DevCenter](https://devcenter.heroku.com/articles/stack) to see what version of Ubuntu linux that corresponds to.  This is currently Ubuntu 14.04
2.  If you do not already have it, download the GGS Scheduler Compile VMWare Image from the Golf Genius google drive account.  It is in the "Virtual Machines" folder.
3.  The username and password for the single user is "golfgenius"
4.  Ensure that your local copy is up to date in the golfgenius/scheduler repository / league-mods branch.  You will be prompted for your github username and password.
```
    cd ~/scheduler
    git reset --hard
    git pull
```
2.  Edit main.cpp and verify the first three lines:
```
    #define mac 0
    #define num_threads 12
    #define debugx 0
```
3.  From the scheduler directory:
```
    $ g++ -O3 -finline-fuctions -ffast-math -funroll-all-loops -msse3 -D_REENTRANT -pthread -o bin/golf_scheduler main.cpp
    $ . chmod u+rx bin/golf_scheduler
```
4.  Copy the file from your virtual machine to your desktop's golfgenius git repo (using scp, for example).
```
    scp golfgenius@172.16.41.129:scheduler/bin/golf_scheduler ~/Downloads
```
5.  Replace the existing scheduler binaries.
```
    $ cp ~/Downloads/golf_scheduler <PROJECT_DIR>/bin/scheduler_staging
    $ cp ~/Downloads/golf_scheduler <PROJECT_DIR>/bin/scheduler_production
```
6.  Verify the scheduler works in staging prior to deploying to production.