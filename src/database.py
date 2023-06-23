from urllib.parse import quote_plus

import motor.motor_asyncio
from decouple import config


def get_client():
    host = config("MONGODB_HOST", default="127.0.0.1", cast=str)
    port = config("MONGODB_PORT", default=27017, cast=int)

    username = config("MONGODB_ROOT_USER", default="", cast=str)
    password = config("MONGODB_ROOT_PASSWORD", default="", cast=str)
    if username != "":
        user_pass = "{0}:{1}@".format(
            quote_plus(username), quote_plus(password)  # type: ignore
        )
    else:
        user_pass = ""

    endpoint = "mongodb://{0}{1}:{2}".format(user_pass, host, port)

    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(endpoint)
    return mongo_client


client = get_client()
admin = client.admin
geo = client.GeoData
climate_data = client.ClimateData
