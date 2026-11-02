from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from state import router as state_router
from service import *
from connection import *
from keybords import *
from callback import *

import os
import asyncio

load_dotenv()


token_bot = os.getenv("BOT_TOKEN")

bot = Bot(token=token_bot)

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Hello {message.from_user.full_name}! 👋",reply_markup=main_kb)


        
@dp.message(F.text == "🆘 Help")
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""
🛍 Marketplace Bot

Available commands:

/add_product - Add product
/products - Show all products
/my_products - Show my products
/save_product - Save product
/mark_sold - Mark product as sold
/delete_saved - Delete saved product
/cancel - Cancel operation
/help - Help
""")



@dp.message(F.text == "📚 Saved Products")
async def show_saved_products(message: Message):
    products = await get_saved_products(message.from_user.id)
    if not products:
        return await message.answer("You have no saved products! ❌")
    for product in products:
        await message.answer_photo(
            photo=product["photo_file_id"],
            caption=f"""
📦 Name: {product["name"]}
💰 Price: {product["price"]} somoni
📝 Description: {product["description"]}
📌 Status: {product["status"]}
""",reply_markup=delete_saved_keyboard([product]))
        
        

@dp.message(F.text == "🗃 Products")
@dp.message(Command("products"))
async def show_all_products(message: Message):
    products = await get_all_products()
    if not products:
        return await message.answer("No products found! ❌")
    for product in products:
        await message.answer_photo(
            photo=product["photo_file_id"],
            caption=f"""
📦 Name: {product["name"]}
💰 Price: {product["price"]} somoni
📝 Description: {product["description"]}
📌 Status: {product["status"]}
""")
        
        
async def main():
    await create_table()
    dp.include_router(state_router)
    print("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())