import motor.motor_asyncio

from core import dbconfig

client = motor.motor_asyncio.AsyncIOMotorClient(dbconfig.DB_URI)

climate_data_database = client.ClimateData
geo = client.GeoData
climate_data = client.ClimateData
