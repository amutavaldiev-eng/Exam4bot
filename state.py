from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from service import *
from callback import *
from keybords import * 

router = Router()



class AddProduct(StatesGroup):
    get_name = State()
    get_price = State()
    get_description = State()
    get_photo = State()


class ShowProduct(StatesGroup):
    get_id = State()


class SaveProduct(StatesGroup):
    get_id = State()


class MyProducts(StatesGroup):
    get_id = State()


class MarkProductSold(StatesGroup):
    get_id = State()


class DeleteSavedProduct(StatesGroup):
    get_id = State()
    

@router.message(F.text == "❌ Cancel")
@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Add Product cancelled!",reply_markup=main_kb)


@router.message(F.text == "➕ Add Product")
@router.message(Command("add_product"))
async def add_product_start(message: Message, state: FSMContext):
    await message.answer("Enter product name:",reply_markup=cancel_kb)
    await state.set_state(AddProduct.get_name)


@router.message(AddProduct.get_name)
async def get_product_title(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Enter product price:",reply_markup=cancel_kb)
    await state.set_state(AddProduct.get_price)


@router.message(AddProduct.get_price)
async def get_product_price(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        return await message.answer("Enter a valid price!")

    await state.update_data(price=int(message.text))
    await message.answer("Enter product description:",reply_markup=cancel_kb)
    await state.set_state(AddProduct.get_description)


@router.message(AddProduct.get_description)
async def get_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Send product photo:",reply_markup=cancel_kb)
    await state.set_state(AddProduct.get_photo)


@router.message(AddProduct.get_photo, F.photo)
async def get_product_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    result = await add_product(
        str(message.from_user.id),
        data["name"],
        data["price"],
        data["description"],
        message.photo[-1].file_id
    )
    if result:
        await message.answer("Product added successfully! ✅",reply_markup=main_kb)
    else:
        await message.answer("Error adding product! ❌",reply_markup=main_kb)
    await state.clear()
    
        
        
        
@router.message(F.text == "📦 Product")
async def show_products(message: Message):
    products = await get_all_products()
    if not products:
        return await message.answer("No products found! ❌")
    await message.answer("📦 Choose a product:",reply_markup=product_keyboard(products))
@router.callback_query(F.data.startswith("product_"))
async def product_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await get_product_by_id(product_id)
    if not product:
        await callback.message.answer("Product not found! ❌")
    else:
        await callback.message.answer_photo(
            photo=product["photo_file_id"],
            caption=f"""
📦 Name: {product["name"]}
💰 Price: {product["price"]} somoni
📝 Description: {product["description"]}
📌 Status: {product["status"]}
""",reply_markup=save_product_keyboard([product]))
    await callback.answer()
    
@router.message(F.text == "🛍 My Products")
@router.message(Command("my_products"))
async def show_my_products(message: Message):
    products = await get_my_products(message.from_user.id)
    if not products:
        return await message.answer("You have no products! ❌")
    await message.answer("Choose your product:",reply_markup=my_product_keyboard(products))

@router.callback_query(F.data.startswith("my_product_"))
async def my_product_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])
    product = await get_product_by_id(product_id)
    if not product:
        await callback.message.answer("Product not found! ❌")
    else:
        await callback.message.answer_photo(
            photo=product["photo_file_id"],
            caption=f"""
📦 Name: {product["name"]}
💰 Price: {product["price"]} somoni
📝 Description: {product["description"]}
📌 Status: {product["status"]}
""",reply_markup=sold_product_keyboard([product]))

    await callback.answer()
    
    
    
@router.message(F.text == "💾 Save Product")
@router.message(Command("save_product"))
async def save_product_start(message: Message):
    products = await get_all_products()
    if not products:
        return await message.answer("No products found! ❌")
    await message.answer("Choose product to save:",reply_markup=save_product_keyboard(products))
@router.callback_query(F.data.startswith("save_"))
async def save_product_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    result = await save_product(callback.from_user.id,product_id)
    if result:
        await callback.message.answer("Product saved successfully! ✅")
    else:
        await callback.message.answer("You can't save own Product! ❌")
    await callback.answer()

    
    
@router.message(F.text == "✅ Mark as Sold")
@router.message(Command("mark_sold"))
async def mark_sold_start(message: Message):
    products = await get_my_products(message.from_user.id)
    if not products:
        return await message.answer("You have no products! ❌")
    await message.answer("Choose product to mark as sold:",reply_markup=sold_product_keyboard(products))
    
@router.callback_query(F.data.startswith("sold_"))
async def sold_product_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    result = await mark_product_sold(callback.from_user.id,product_id)
    if result:
        await callback.message.answer("Product marked as sold! ✅")
    else:
        await callback.message.answer("Product not found or already sold! ❌")
    await callback.answer()
    
    
@router.message(F.text == "❌ Delete Saved")
@router.message(Command("delete_saved"))
async def delete_saved_start(message: Message):
    products = await get_saved_products(message.from_user.id)
    if not products:
        return await message.answer("You have no saved products! ❌")
    await message.answer("Choose product to delete:",reply_markup=delete_saved_keyboard(products))
@router.callback_query(F.data.startswith("delete_saved_"))
async def delete_saved_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])
    result = await delete_saved_product(callback.from_user.id,product_id)
    if result:
        await callback.message.answer("Product deleted successfully! ✅")
    else:
        await callback.message.answer("Product not found in saved! ❌")
    await callback.answer()
    
    
    
    