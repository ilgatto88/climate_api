# climATe API

Climate API for Austria

# Plan

https://orf.at/stories/3316936/

# Setup

Upgrade pip with `python3 -m pip install --upgrade pip`  
Install virtualenv `python3 -m pip install --user virtualenv`
Install virtualenv step2 `sudo apt install python3.10-venv`
Install Python modules with `pip install -r requirements.txt`
Add this to your bashrc `export PYTHONPATH="/home/jtordai/projects/climate_api/:$PYTHONPATH"`

## MongoDB installation

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
`sudo apt-get install gnupg`
`curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor`
`echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list`
`sudo apt-get update`
`sudo apt-get install -y mongodb-org libkrb5-dev`
`sudo chown mongodb:mongodb /var/run/mongod.pid`

## MongoDB startup

https://askubuntu.com/questions/1203689/cannot-start-mongodb-on-wsl
https://stackoverflow.com/questions/25903980/error-cannot-write-pid-file-to-var-run-mongodb-mongod-pid-no-such-file-or-dir

## MongoDB useful commands

`sudo service mongod start` start mongodb
`sudo service mongod status` check mongodb status

`sudo cat /var/log/mongodb/mongod.log` check logs if database won't start up

## Install mongosh (MongoDB shell)

`cd ~`
`wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -`
`sudo apt-get update`
`sudo apt-get install -y mongodb-mongosh`

## MongoDB shell useful commands

`mongosh`: start MongoDB shell  
`db`: display current database  
`use <database>`: switch databases  
`show dbs`: list available databases  
`use <database>`: create a new database  
`db.dropDatabase()`: delete current database  
`db.createCollection("<collection>")`: create a new collection  
`show collections`: list all collections  
`db.<collection>.drop()`: delete a collection  
`db.<collection>.insertOne({key1: "Value1", key2: "Value2", key3: 3, key4: ["Value4", "Value5"], date: Date()})`: insert one new document into collection  
`db.<collection>.insertMany([{key1: "Value1", key2: "Value2", key3: 3, key4: ["Value4", "Value5"], date: Date()}, {key1: "Value1", key2: "Value2", key3: 3, key4: ["Value4", "Value5"], date: Date()}])`: insert multiple new documents into collection  
`db.municipalityData.find( { key: value } )`: select data from collection  
`db.<collection>.findOne()`: select only one document from collection  
`db.<collection>.updateOne( { key1: "Post Title 1" }, { $set: { key3: 2 } } ) `: update a document  
`db.<collection>.deleteOne( { key: value } )`: delete one document from a collection  
`db.<collection>.deleteMany({})`: delete all documents in a collection

### Comparison

The following operators can be used in queries to compare values:

`$eq`: Values are equal
`$ne`: Values are not equal
`$gt`: Value is greater than another value
`$gte`: Value is greater than or equal to another value
`$lt`: Value is less than another value
`$lte`: Value is less than or equal to another value
`$in`: Value is matched within an array

### Logical

The following operators can logically compare multiple queries.

`$and`: Returns documents where both queries match
`$or`: Returns documents where either query matches
`$nor`: Returns documents where both queries fail to match
`$not`: Returns documents where the query does not match

### Evaluation

The following operators assist in evaluating documents.

`$regex`: Allows the use of regular expressions when evaluating field values
`$text`: Performs a text search
`$where`: Uses a JavaScript expression to match documents

# Starting the application

`docker-compose build --no-cache && docker-compose up -d`: build the images and start the containers

# Further tutorials to read

https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable
https://github.com/vinissimus/async-asgi-testclient
https://github.com/petrgazarov/FastAPI-app
https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/
https://fastapi.tiangolo.com/tutorial/testing/
