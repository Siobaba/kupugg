import os

# Список папок
folders = [
    "database",
    "keyboards",
    "states",
    "handlers"
]

# Список файлов и их базовое содержимое
files = {
    ".env": "BOT_TOKEN=\nADMIN_ID=\nMANAGER_USERNAME=\n",
    ".env.example": "BOT_TOKEN=\nADMIN_ID=\nMANAGER_USERNAME=\n",
    "requirements.txt": "aiogram>=3.4.0\naiosqlite>=0.20.0\npython-dotenv>=1.0.1\n",
    "README.md": "# KipuGG Bot\n",
    "bot.py": "",
    "config.py": "",
    "database/__init__.py": "",
    "database/db.py": "",
    "keyboards/__init__.py": "",
    "keyboards/inline.py": "",
    "keyboards/admin_kb.py": "",
    "states/__init__.py": "",
    "states/admin_states.py": "",
    "handlers/__init__.py": "",
    "handlers/user.py": "",
    "handlers/profile.py": "",
    "handlers/shop.py": "",
    "handlers/admin.py": ""
}

# Создаем папки
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Создаем файлы
for filepath, content in files.items():
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Структура проекта KipuGG успешно создана! Можно приступать к вставке кода.")