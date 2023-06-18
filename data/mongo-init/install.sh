#!/bin/bash
set -e

echo CREATING ROOT USER
mongosh << EOF
use admin
db.createCollection("Users")
db.Users.insertOne(
    {
        fullname: "${MONGO_INITDB_ROOT_USERNAME}",
        password: "${MONGODB_ROOT_HASHED_PASSWORD}",
        email: "${MONGO_INITDB_ROOT_USERNAME}@admin.com",
    }
)
EOF

echo IMPORTING MUNICIPALITY COLLECTION
cp /docker-entrypoint-initdb.d/municipalities.json /tmp/municipalities.json
mongoimport --authenticationDatabase admin --username $MONGO_INITDB_ROOT_USERNAME --password $MONGODB_ROOT_PASSWORD --db GeoData --collection Municipality --file /tmp/municipalities.json --jsonArray
echo “CLEANING UP”
rm /tmp/municipalities.json
echo DONE IMPORTING


