from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import shop_categories_kb, back_to_main_kb

router = Router()

@router.callback_query(F.data == "menu_shop")
async def show_shop_categories(callback: CallbackQuery):
    text = "🛍 <b>Выберите категорию товаров:</b>"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=shop_categories_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=shop_categories_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("cat_"))
async def show_category_items(callback: CallbackQuery):
    text = "В этой категории пока нет доступных товаров."
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, reply_markup=back_to_main_kb())
    else:
        await callback.message.edit_text(text, reply_markup=back_to_main_kb())
    await callback.answer()