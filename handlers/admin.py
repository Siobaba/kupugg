from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from keyboards.admin_kb import admin_main_kb, admin_products_kb, confirm_delete_kb
from keyboards.inline import back_to_main_kb
from database.db import add_product, get_products, delete_product
from states.admin_states import AddProduct

router = Router()


# Фильтр для админа: можно вынести в отдельный файл, но для лаконичности оставим здесь
async def is_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if await is_admin(message):
        await message.answer("Добро пожаловать в Админ-панель", reply_markup=admin_main_kb())


@router.callback_query(F.data == "admin_close")
async def admin_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "admin_products")
async def admin_products_menu(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    await callback.message.edit_text("📦 Управление товарами", reply_markup=admin_products_kb())
    await callback.answer()


# --- ДОБАВЛЕНИЕ ТОВАРА ---
@router.callback_query(F.data == "admin_add_product")
async def add_product_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID: return
    await callback.message.edit_text("Введите категорию (например, 'Подписки' или 'Игры'):")
    await state.set_state(AddProduct.category)
    await callback.answer()


@router.message(AddProduct.category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите название товара:")
    await state.set_state(AddProduct.name)


@router.message(AddProduct.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(AddProduct.description)


@router.message(AddProduct.description)
async def process_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену товара (только число):")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        data = await state.get_data()
        await add_product(data['category'], data['name'], data['description'], price, True)
        await message.answer("✅ Товар успешно добавлен!", reply_markup=admin_main_kb())
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")


# --- СПИСОК И УДАЛЕНИЕ ---
@router.callback_query(F.data == "admin_list_products")
async def list_products(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    products = await get_products()
    if not products:
        await callback.message.edit_text("Товаров пока нет.", reply_markup=admin_products_kb())
        return

    # Для простоты первого этапа выводим текстом.
    # В идеале нужно делать Inline-пагинацию.
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()

    text = "📋 Список товаров:\n\n"
    for p in products:
        text += f"ID: {p[0]} | {p[2]} ({p[4]}₽)\n"
        builder.button(text=f"🗑 Удал. {p[2]}", callback_data=f"del_ask_{p[0]}")

    builder.button(text="🔙 Назад", callback_data="admin_products")
    builder.adjust(1)

    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("del_ask_"))
async def ask_delete_product(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    product_id = int(callback.data.split("_")[2])
    await callback.message.edit_text("Вы уверены, что хотите удалить этот товар?",
                                     reply_markup=confirm_delete_kb(product_id))
    await callback.answer()


@router.callback_query(F.data.startswith("del_yes_"))
async def confirm_delete(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    product_id = int(callback.data.split("_")[2])
    await delete_product(product_id)
    await callback.message.edit_text("✅ Товар удален.", reply_markup=admin_products_kb())
    await callback.answer()