from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db import get_or_create_user, toggle_notifications
from keyboards.inline import profile_kb, back_to_main_kb

router = Router()


@router.callback_query(F.data == "menu_profile")
async def show_profile(callback: CallbackQuery):
    user = await get_or_create_user(callback.from_user.id, callback.from_user.username)
    notif_status = bool(user[5])

    text = (
        f"👤 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{user[1]}</code>\n"
        f"💰 Баланс: <b>{user[3]} ₽</b>\n"
        f"🌐 Язык: <b>{'Русский' if user[4] == 'ru' else 'English'}</b>\n"
    )
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=profile_kb(notif_status))
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=profile_kb(notif_status))
    await callback.answer()


@router.callback_query(F.data == "profile_notifications")
async def switch_notifications(callback: CallbackQuery):
    await toggle_notifications(callback.from_user.id)
    await show_profile(callback)


@router.callback_query(F.data.in_(["profile_purchases", "profile_deposits", "profile_promo"]))
async def profile_placeholders(callback: CallbackQuery):
    if callback.data == "profile_purchases":
        text = "🛒 История покупок пуста."
    elif callback.data == "profile_deposits":
        text = "💳 История пополнений пуста."
    else:
        text = "🎟 Введите промокод (раздел в разработке)."

    if callback.message.photo:
        await callback.message.edit_caption(caption=text, reply_markup=back_to_main_kb())
    else:
        await callback.message.edit_text(text, reply_markup=back_to_main_kb())
    await callback.answer()