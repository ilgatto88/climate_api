from pymongo import MongoClient

import dbconfig


def db_client():
    return MongoClient(dbconfig.CONNECTION_STRING)


def get_database():
    client = db_client()
    return client[dbconfig.DB_NAME]


def reset_database():
    print("Deleting database and collections...")
    client = db_client()
    db = get_database()
    for collection in dbconfig.COLLECTIONS:
        db.drop_collection(collection)
    print("All collections deleted...")

    client.drop_database(dbconfig.DB_NAME)
    print(f"Database {dbconfig.DB_NAME} deleted...")


if __name__ == "__main__":
    dbname = get_database()
    print(dbname)
    # reset_database()
