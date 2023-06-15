import motor.motor_asyncio

from core import dbconfig

client = motor.motor_asyncio.AsyncIOMotorClient(dbconfig.DB_URI)

admin = client.admin
geo = client.GeoData
climate_data = client.ClimateData
