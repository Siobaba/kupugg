import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from database.db import get_or_create_user
from keyboards.inline import (
    main_menu_kb,
    back_to_main_kb,
    info_kb,
    shop_categories_kb,
    languages_kb
)
from config import MANAGER_USERNAME

router = Router()
BANNER_PATH = "banner.jpg"


async def send_welcome_banner(target, is_callback: bool = False):
    """Отправляет баннер с кнопками либо возвращает экран в исходное состояние."""
    caption = "👋 <b>Добро пожаловать!</b>"

    if os.path.exists(BANNER_PATH):
        photo = FSInputFile(BANNER_PATH)
        if is_callback:
            try:
                # Если сообщение уже было с фото, просто восстанавливаем подпись и меню
                await target.message.edit_caption(caption=caption, parse_mode="HTML", reply_markup=main_menu_kb())
                return
            except Exception:
                await target.message.delete()
        await (target.message.answer_photo if is_callback else target.answer_photo)(
            photo=photo,
            caption=caption,
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
    else:
        # Резервный вариант, если banner.jpg еще не загружен
        if is_callback:
            await target.message.edit_text(caption, parse_mode="HTML", reply_markup=main_menu_kb())
        else:
            await target.answer(caption, parse_mode="HTML", reply_markup=main_menu_kb())


@router.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user(message.from_user.id, message.from_user.username)
    await send_welcome_banner(message, is_callback=False)


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await send_welcome_banner(callback, is_callback=True)
    await callback.answer()


@router.callback_query(F.data == "menu_support")
async def support_menu(callback: CallbackQuery):
    text = f"🎧 <b>Поддержка</b>\n\nЕсли у вас возникли вопросы, обратитесь к менеджеру: @{MANAGER_USERNAME}"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=back_to_main_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
    await callback.answer()


@router.callback_query(F.data == "menu_info")
async def info_menu(callback: CallbackQuery):
    text = "ℹ️ <b>Раздел информации:</b>\nВыберите интересующий пункт ниже:"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=info_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=info_kb())
    await callback.answer()


@router.callback_query(F.data == "menu_lang")
async def language_menu(callback: CallbackQuery):
    text = "🌐 <b>Выберите язык интерфейса / Select language:</b>"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=languages_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=languages_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: CallbackQuery):
    lang_code = callback.data.split("_")[2]
    lang_name = "Русский 🇷🇺" if lang_code == "ru" else "English 🇬🇧"
    text = f"✅ Язык успешно изменен на: <b>{lang_name}</b>"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=back_to_main_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("info_"))
async def info_pages(callback: CallbackQuery):
    if callback.data == "info_privacy":
        text = "🔒 <b>Политика конфиденциальности</b>\n\nТекст политики безопасности данных..."
    else:
        text = "📄 <b>Пользовательское соглашение</b>\n\nТекст пользовательского соглашения и правил покупки..."

    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=back_to_main_kb())
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
    await callback.answer()