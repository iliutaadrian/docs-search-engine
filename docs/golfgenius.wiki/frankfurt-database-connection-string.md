# Connecting to Frankfurt DB

**insert this definitions in .envrc**
    
    export START_TENANT=4765
    export MAX_SHARD=5

    export DATABASE1_STATUS=on
    export DATABASE2_STATUS=on
    export DATABASE3_STATUS=on
    export DATABASE4_STATUS=on
    export DATABASE5_STATUS=on

    # coment the next line if you want to use local database
    
    export DATABASE0_URL=postgres://ubuntu:qaz321fwsx@ec2-18-185-239-187.eu-central-1.compute.amazonaws.com:5432/golfgenius0_development
    export DATABASE1_URL=postgres://ubuntu:qaz321fwsx@ec2-18-157-79-154.eu-central-1.compute.amazonaws.com:5432/golfgenius1_development
    export DATABASE2_URL=postgres://ubuntu:qaz321fwsx@ec2-3-127-27-86.eu-central-1.compute.amazonaws.com:5432/golfgenius2_development
    export DATABASE3_URL=postgres://ubuntu:qaz321fwsx@ec2-3-123-29-144.eu-central-1.compute.amazonaws.com:5432/golfgenius3_development
    export DATABASE4_URL=postgres://ubuntu:qaz321fwsx@ec2-18-195-225-38.eu-central-1.compute.amazonaws.com:5432/golfgenius2_development
    export DATABASE5_URL=postgres://ubuntu:qaz321fwsx@ec2-3-125-156-231.eu-central-1.compute.amazonaws.com:5432/golfgenius3_development
    export DATABASE_URL=postgres://ubuntu:qaz321fwsx@ec2-18-185-239-187.eu-central-1.compute.amazonaws.com:5432/golfgenius0_development    




`

**run `direnv allow`**

**use the proper database definition in config/database.yml**

    development:
      adapter:    postgresql
      host:       ec2-18-185-239-187.eu-central-1.compute.amazonaws.com
      database:   golfgenius0_development
      username:   ubuntu
      password:   qaz321fwsx
      timeout:    5000
      encoding:   utf8
      pool:       5
      reconnect:  true

     DATABASE0 => golfgenius0_development => public, c103
     DATABASE1 => golfgenius1_development
     DATABASE2 => golfgenius2_development => c3-c27
     DATABASE3 => golfgenius3_development => c53-c77
     DATABASE4 => golfgenius2_development => c28-c52
     DATABASE5 => golfgenius3_development => c78-c102

# To use local database
* remove the lines above from .envrc
* change config/database.yml to use the local DB settings
* restart rails s, rails c, and redis queues