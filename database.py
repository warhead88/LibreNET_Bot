import asyncpg
import aiocron
import asyncio
import os
import logging

from asyncpg import Pool

from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Database:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create(cls):
        """Создаёт объект Database с уже готовым подключением."""
        load_dotenv()
        pool = await asyncpg.create_pool(
            database="vpn_service",
            user="postgres",
            password=os.getenv("DATABASE_PASSWORD"),
            host="localhost",
            port="5432",
            min_size=1,
            max_size=10
        )
        return cls(pool)

    async def add_user(self, telegram_id, username, first_name, sub_type):
        """Добавляет пользователя или обновляет подписку."""
        now = datetime.now(timezone.utc)
        sub_end = now + (relativedelta(months=1) if sub_type == 'month' else relativedelta(years=1))

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO users (telegram_id, username, full_name, subscription_status, subscription_end) 
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT DO NOTHING;""",
                    telegram_id, username, first_name, 'active', sub_end
                )

    from datetime import datetime, timezone

    async def get_subscription_info(self, telegram_id):
        """Возвращает (статус, количество дней до конца подписки)."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT subscription_status, subscription_end FROM users WHERE telegram_id = $1;",
                telegram_id
            )
            if not row:
                return "❌Неактивна", "У вас нет подписки :("

            status = "✅Активна" if row["subscription_status"] == "active" else "❌Неактивна"
            sub_end = row["subscription_end"]

            if not sub_end:
                return status, "Нет информации о сроке подписки."

            # Приведение к UTC, если datetime наивный (без tzinfo)
            if sub_end.tzinfo is None:
                sub_end = sub_end.replace(tzinfo=timezone.utc)  # Делаем осведомлённым

            # Вычисляем количество дней
            days_left = (sub_end - datetime.now(timezone.utc)).days
            return status, f"{days_left} дней." if days_left > 0 else "Срок подписки истёк."

class SubscriptionChecker:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def check_subscriptions(self):
        """Обновляет статус подписки, если срок истёк."""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET subscription_status = 'expired' WHERE subscription_end <= NOW();"
            )

# Функция для старта планировщика
async def start_subscription_checker(db_pool):
    checker = SubscriptionChecker(db_pool)
    aiocron.crontab('0 0 * * *', func=checker.check_subscriptions)  # Каждый день в 00:00
