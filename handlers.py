from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import keyboards as kb
from database import Database

db = Database()

router = Router()

introduction = """Привет! Это небольшой VPN-сервис, который даст тебе свободу в интернете. Вся необходимая информация есть ниже."""

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(introduction, reply_markup=kb.options_for_start)

@router.callback_query(F.data == 'homedir')
async def menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(introduction, reply_markup=kb.options_for_start)

@router.callback_query(F.data == 'mainmenu')
async def main_menu(callback: CallbackQuery):
    await db.connect()
    await callback.answer('')
    if await db.check_sub(callback.from_user.id) == True:
        status = 'Активна'
    else:
        status = 'Неактивна'
    await callback.message.edit_text(f"""Это основное меню управления, здесь вы можете всячески манипулировать с ботом.
Статус подписки: {status} """, reply_markup=kb.menu_button)
    await db.disconnect()

@router.callback_query(F.data == 'prices')
async def prices(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("""По ценам всё демократично :)
Месяц - 150 рублей;
Год - 1500 рублей.""", reply_markup=kb.options_for_prices)

@router.callback_query(F.data == 'buy_month')
async def buy_month(callback: CallbackQuery):
    await db.connect()
    id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    sub_type = 'month'
    await db.add_user(id, username, first_name, sub_type)
    await callback.answer('')
    await db.disconnect()
    await callback.message.edit_text("Пример покупки месячной подписки.", reply_markup=kb.menu_button)

@router.callback_query(F.data == 'buy_year')
async def buy_year(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Пример покупки годовой подписки.", reply_markup=kb.menu_button)

@router.callback_query(F.data == 'information')
async def info(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Тут будет приведена информация.", reply_markup=kb.information)

@router.callback_query(F.data == 'servers')
async def servers(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("""Серверы:
    🇫🇮 Финляндия - x1;
    🇳🇱 Нидерланды - x1.
Пока что, к сожалению, всё. Дальше планируем расширяться.""", reply_markup=kb.menu_button)
