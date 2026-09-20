from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb() -> InlineKeyboardMarkup:
    """Главное меню точь-в-точь как на образце."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="㗊 Товары", callback_data="menu_shop")],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="menu_profile"),
            InlineKeyboardButton(text="💬 Поддержка", callback_data="menu_support")
        ],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="menu_info")],
        [InlineKeyboardButton(text="🌐 Язык", callback_data="menu_lang")]
    ])

def back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])

def info_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Политика конфиденциальности", callback_data="info_privacy")],
        [InlineKeyboardButton(text="📄 Пользовательское соглашение", callback_data="info_terms")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])

def languages_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])

def profile_kb(notifications_enabled: bool) -> InlineKeyboardMarkup:
    notif_text = "🔔 Уведомления: включены" if notifications_enabled else "🔕 Уведомления: выключены"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Баланс (Пополнить)", callback_data="profile_balance")],
        [InlineKeyboardButton(text="🛒 История покупок", callback_data="profile_purchases")],
        [InlineKeyboardButton(text="💳 История пополнений", callback_data="profile_deposits")],
        [InlineKeyboardButton(text="🎟 Промокоды", callback_data="profile_promo")],
        [InlineKeyboardButton(text=notif_text, callback_data="profile_notifications")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])

def shop_categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Подписки и нейросети", callback_data="cat_ai")],
        [InlineKeyboardButton(text="🎮 Карты и игры", callback_data="cat_games")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])