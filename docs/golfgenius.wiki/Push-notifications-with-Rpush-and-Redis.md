**Rpush notifications and new Redis server setup**

In order to start a new Redis server in local environment: 
  - Create a duplicate file of this file: /usr/local/etc/redis.conf and name it redis1.conf
  - Edit this file and change the port to 6380
  - New redis server location is specified in development.rb - REDIS_PUSH_URL = "redis://127.0.0.1:6380/push"

On production:
  - We will need to specify the REDIS_PUSH_URL
  - "rake cleanup_push_notifications_redis" should be set to run daily in order to clear completed notifications 
  - "rake gc_am_tour_push_notifications" should be set to run once per hour in order to send 

On both local and production:
  - Before first run, we should create the Rpush App from rails console:

`Migrate.initialize_rpush_app`

  - Start Rpush server by running "rpush start" in terminal



After setting this up, following push notifications will be sent for GC Am Tour customer (18589)
- Send push notifications when opening the registration
- Send push notifications 8 hours before the event registration closes
- If the event is using tours, send notifications to all GC Am Tour App users with no player profile and to all members part of that tour
- If the event is using invitations list and the registration is opened for invitations, send notifications to all GC Am Tour App users with no player profile and to all members part of invitations list

Heroku setup:
https://github.com/rpush/rpush/wiki/Heroku

