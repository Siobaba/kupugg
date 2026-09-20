import asyncio
import logging
import os
import sys
import urllib.request
import socket
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN
import database.db as db
from handlers import user, profile, shop, admin

# ==========================================
# --- ФИКСЫ СЕТИ ДЛЯ WINDOWS ---
# ==========================================
if sys.platform == "win32":
    # 1. Переключаем цикл событий, чтобы сокеты не зависали
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 2. Фикс ошибки таймаута: заставляем Python использовать только IPv4
orig_getaddrinfo = socket.getaddrinfo


def getaddrinfo_ipv4_only(*args, **kwargs):
    responses = orig_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]


socket.getaddrinfo = getaddrinfo_ipv4_only


# ==========================================


def get_system_proxy() -> str | None:
    """Автоматически достает прокси из настроек Windows (тот же, что использует браузер)."""
    proxies = urllib.request.getproxies()
    proxy = proxies.get("https") or proxies.get("http")
    if proxy and not proxy.startswith("http"):
        proxy = f"http://{proxy}"
    return proxy


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Инициализация базы данных PostgreSQL
    await db.init_db()

    # Проверяем системный прокси или переменную PROXY_URL из .env
    proxy = os.getenv("PROXY_URL") or get_system_proxy()

    if proxy:
        logging.info(f"Бот подключается через прокси: {proxy}")
        session = AiohttpSession(proxy=proxy)
        bot = Bot(token=BOT_TOKEN, session=session)
    else:
        logging.info("Прокси не обнаружен, подключение напрямую...")
        bot = Bot(token=BOT_TOKEN)

    # Инициализация диспетчера
    dp = Dispatcher()

    # Регистрация роутеров (обработчиков из папки handlers)
    dp.include_router(user.router)
    dp.include_router(profile.router)
    dp.include_router(shop.router)
    dp.include_router(admin.router)

    logging.info("Bot is starting...")

    # Очистка очереди обновлений (чтобы бот не отвечал на старые сообщения после перезапуска)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # Запуск поллинга (прослушивания сообщений)
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем пул подключений к БД при остановке скрипта
        if db.pool:
            await db.pool.close()
            logging.info("Пул соединений PostgreSQL закрыт.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен вручную.")