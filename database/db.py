import asyncpg
import logging
from config import DATABASE_URL

# Глобальный пул соединений
pool = None

async def init_db():
    global pool
    try:
        # Создаем пул подключений к PostgreSQL
        pool = await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        logging.error(f"Ошибка подключения к PostgreSQL: {e}")
        raise e

    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username TEXT,
                balance REAL DEFAULT 0.0,
                language TEXT DEFAULT 'ru',
                notifications_enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                category TEXT,
                name TEXT,
                description TEXT,
                price REAL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                price REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS deposits (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS promo_codes (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE,
                discount REAL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logging.info("Таблицы PostgreSQL успешно инициализированы.")

async def get_or_create_user(telegram_id: int, username: str):
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
        if not user:
            await conn.execute(
                "INSERT INTO users (telegram_id, username) VALUES ($1, $2)",
                telegram_id, username
            )
            user = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
        return user

async def toggle_notifications(telegram_id: int):
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE users SET notifications_enabled = NOT notifications_enabled 
            WHERE telegram_id = $1
        """, telegram_id)

async def add_product(category: str, name: str, description: str, price: float, is_active: bool):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO products (category, name, description, price, is_active)
            VALUES ($1, $2, $3, $4, $5)
        """, category, name, description, price, is_active)

async def get_products():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM products")

async def delete_product(product_id: int):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM products WHERE id = $1", product_id)