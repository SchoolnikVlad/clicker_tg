from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from database import get_user
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start(message: types.Message):
    webapp_url = f"{config.WEBAPP_URL}?user_id={message.from_user.id}"
    await message.answer(
        "🎮 Играть",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(
                    text="🎮 Играть",
                    web_app=types.WebAppInfo(url=webapp_url)
                )]
            ],
            resize_keyboard=True
        )
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))