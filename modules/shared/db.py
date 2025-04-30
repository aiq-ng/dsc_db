import asyncio
import os
from typing import Optional

import asyncpg
from dotenv import load_dotenv

load_dotenv()


class DatabaseError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self):
        for _ in range(5):  # Retry 5 times
            try:
                self.pool = await asyncpg.create_pool(
                    user=os.getenv("POSTGRES_USER", "postgres"),
                    password=os.getenv("POSTGRES_PASSWORD", "password"),
                    database=os.getenv("POSTGRES_DB", "dsc_db"),
                    host=os.getenv("POSTGRES_HOST", "db"),
                    port=int(os.getenv("POSTGRES_PORT", "5432")),
                )
                print("Database connection established")
                break
            except (
                asyncpg.exceptions.ConnectionDoesNotExistError,
                ConnectionRefusedError,
            ) as e:
                print(f"Connection failed: {e}, retrying in 2 seconds...")
                await asyncio.sleep(2)
        else:
            raise Exception("Failed to connect to database after retries")

    async def close_pool(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        try:
            async with self.pool.acquire() as connection:
                return await connection.execute(query, *args)
        except Exception as e:
            raise DatabaseError("Failed to execute query") from e

    async def fetch(self, query: str, *args):
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetch(query, *args)
        except Exception as e:
            raise DatabaseError("Failed to fetch records") from e

    async def fetchrow(self, query: str, *args):
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetchrow(query, *args)
        except Exception as e:
            raise DatabaseError("Failed to fetch single record") from e

    async def fetchval(self, query: str, *args):
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetchval(query, *args)
        except Exception as e:
            raise DatabaseError("Failed to fetch value") from e


db = Database()


async def create_db_pool():
    await db.create_pool()


async def close_db_pool():
    await db.close_pool()
