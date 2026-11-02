import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

        print("Neon connected successfully! ✅")

        result = await conn.fetchval("SELECT current_database()")
        print("Database:", result)

        await conn.close()

    except Exception as error:
        print("Connection error:", error)


asyncio.run(test_connection())