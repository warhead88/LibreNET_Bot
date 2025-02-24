import asyncpg
import asyncio

from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from dotenv import load_dotenv
import os

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            database="vpn_service",
            user="postgres",
            password=os.getenv("DATABASE_PASSWORD"),
            host="localhost",
            port="5432",
            min_size=1,
            max_size=10
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def add_user(self, telegram_id, username, first_name, sub_type):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                now = datetime.now(timezone.utc)
                if sub_type == 'month':
                    sub_end = now +  relativedelta(months=1)
                else:
                    sub_end = now + relativedelta(years=1)
                await conn.execute(f"INSERT INTO users (telegram_id, username, full_name, subscription_status, subscription_end) VALUES ({telegram_id}, '{username}', '{first_name}', 'active', '{sub_end}') ON CONFLICT DO NOTHING;")

    async def check_sub(self, telegram_id):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                sub_status = await conn.fetchval(f"SELECT subscription_status FROM users WHERE telegram_id = {telegram_id};")
                if sub_status == "active":
                    return True
                else:
                    return False
    async def check_date(self, telegram_id):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                sub_date = await conn.execute(f"SELECT subscription_end FROM users WHERE telegram_id = {telegram_id};")
                if sub_date != 'None':
                    return (sub_date - datetime.now()).days

async def main():
    load_dotenv()
    db = Database()
    await db.connect()
    logging.info(await db.check_sub(1))

if __name__ == "__main__":
    asyncio.run(main())
