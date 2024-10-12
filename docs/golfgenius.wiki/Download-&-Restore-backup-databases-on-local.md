1.  * download golfgenius0_development on local ex:

`aws s3 sync s3://golfgenius-dev/backups/YYYY-MM-DD/glg0.dump/ ../backups/glg0.dump/`

where YYYY-MM-DD can be 2019-10-28
    
    * restore golfgenius0_development on local ex:

* dropdb golfgenius0_development
* createdb golfgenius0_development
* pg_restore --verbose --clean --no-acl --no-owner -h localhost -d golfgenius0_development ../backups/glg0.dump -j 16

2.  * download golfgenius1_development on local ex:

* aws s3 cp s3://golfgenius-dev/backups/YYYY-MM-DD/glg_short.backup ../backups/glg_short.backup

where YYYY-MM-DD can be 2019-10-28

    * restore golfgenius1_development on local ex:

* dropdb golfgenius1_development
* createdb golfgenius1_development
* pg_restore --verbose --clean --no-acl --no-owner -h localhost -d golfgenius1_development ../backups/glg_short.backup -j 16

3.  * download and restore public schema for golfgenius2_development and golfgenius3_development

* aws s3 cp s3://golfgenius-dev/backups/YYYY-MM-DD/public_shard2.dump ../backups/public_shard2.dump
* aws s3 cp s3://golfgenius-dev/backups/YYYY-MM-DD/public_shard3.dump ../backups/public_shard3.dump 

    * restore

* pg_restore --port 5432 --dbname "golfgenius2_development" --no-password --schema public --no-acl --no-owner ../backups/public_shard2.dump
* pg_restore --port 5432 --no-acl --no-owner --dbname "golfgenius3_development" --no-password --clean --schema public --verbose ../backups/public_shard3.dump

4.  * download an restore schema from 3 to 102 ex:

* aws s3 cp s3://golfgenius-dev/backups/YYYY-MM-DD/c22.dump ../backups/c22.dump
* ruby script/restore.rb 22

 
