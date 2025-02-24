from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

options_for_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Меню управления', callback_data='mainmenu')],
    [InlineKeyboardButton(text='Прайс-лист', callback_data='prices')],
    [InlineKeyboardButton(text='Справки и информация', callback_data='information')]
])

options_for_prices = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить на месяц', callback_data='buy_month')],
    [InlineKeyboardButton(text='Купить на год', callback_data='buy_year')],
    [InlineKeyboardButton(text='В меню', callback_data='homedir')]
])

information = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Серверы', callback_data='servers')],
    [InlineKeyboardButton(text='В меню', callback_data='homedir')]
])

menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='В меню', callback_data='homedir')]
])
