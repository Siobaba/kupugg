import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
PROXY_URL = os.getenv("PROXY_URL", "").strip()

raw_admin_id = os.getenv("ADMIN_ID", "0").strip()
ADMIN_ID = int(raw_admin_id) if raw_admin_id.isdigit() else 0

MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "manager").replace("@", "")

# Добавляем URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "")