from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from service import *


def product_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(text=product["name"], callback_data=f'product_{product["products_id"]}')])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keybor



def my_product_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=product["name"],callback_data=f'my_product_{product["products_id"]}') ])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keybor

def save_product_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(text=f'{product["name"]} — 💾 Save', callback_data=f'save_{product["products_id"]}')])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keybor


def sold_product_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{product["name"]} — 💰 Sell',
                callback_data=f'sold_{product["products_id"]}')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def delete_saved_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(text=product["name"], callback_data=f'delete_saved_{product["products_id"]}')])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keybor