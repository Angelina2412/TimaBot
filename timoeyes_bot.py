from aiogram import Bot, Dispatcher, executor, types
import logging
import os

API_TOKEN = '7866296094:AAG-2Bczn1v5najl_DyqPJN45KZEocugP8M'
CHANNEL_USERNAME = '@timoeyes'
FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSczQIWgLgMmMHzMM6I5mlmc5EydHy5t1LSQh-h0J6hFMIPpNA/viewform'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer(f"Вы подписаны ✅\nВот ваша ссылка на форму: {FORM_LINK}")
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        keyboard.add(types.InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription"))

        await message.answer("Сначала подпишитесь на канал, чтобы получить доступ к форме:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if await is_subscribed(user_id):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=user_id, text=f"Вы подписаны ✅\nВот ваша ссылка на форму: {FORM_LINK}")
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=user_id, text="Вы пока не подписаны ❌ Подпишитесь на канал и нажмите 'Проверить подписку' ещё раз.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
