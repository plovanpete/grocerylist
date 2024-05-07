from motor.motor_asyncio import AsyncIOMotorClient

url = 'INPUT YOUR LINK HERE!'

async def get_mongo_client() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(url)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise