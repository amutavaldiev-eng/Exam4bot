from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Add Product"),
            KeyboardButton(text="📦 Product")
        ],
        [
            KeyboardButton(text="🛍 My Products"),
            KeyboardButton(text="🗃 Products")
        ],
        [
            KeyboardButton(text="💾 Save Product"),
            KeyboardButton(text="📚 Saved Products")
        ],
        [
            KeyboardButton(text="✅ Mark as Sold"),
            KeyboardButton(text="❌ Delete Saved")
        ],
        [
            KeyboardButton(text="🆘 Help")
        ]
    ],
    resize_keyboard=True
)



cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Cancel")]
    ],
    resize_keyboard=True
)