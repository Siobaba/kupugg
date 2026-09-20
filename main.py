# --- Добавьте этот блок перед функцией main() ---
async def handle_ping(request):
    return web.Response(text="Бот работает!")


async def start_dummy_server():
    """Запускает фиктивный веб-сервер, чтобы Render не выдавал ошибку развертывания."""
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Web-сервер запущен на порту {port}")


# ------------------------------------------------

async def main():
    # ... (ваш текущий код) ...

    logging.info("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # ЗАПУСКАЕМ СЕРВЕР ДЛЯ RENDER ЗДЕСЬ:
        await start_dummy_server()

        # Запуск поллинга
        await dp.start_polling(bot)
    finally:
        if db.pool:
            await db.pool.close()