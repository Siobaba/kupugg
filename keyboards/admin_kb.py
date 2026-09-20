from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="admin_products")]
    ])

def admin_products_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add_product")],
        [InlineKeyboardButton(text="📋 Список товаров (Удалить/Изменить)", callback_data="admin_list_products")],
        [InlineKeyboardButton(text="🔙 Закрыть панель", callback_data="admin_close")]
    ])

def confirm_delete_kb(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"del_yes_{product_id}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="admin_list_products")
        ]
    ])