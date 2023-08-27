from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN_FOR_BOT = os.getenv('TOKEN_FOR_BOT')

bot = Bot(token=TOKEN_FOR_BOT)
dp = Dispatcher(bot)


@dp.message_handler(text='Старт')
async def hell_func(message: Message):
    text: str = f'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text)


@dp.message_handler(text='Стоп')
async def while_func(message: Message):
    text: str = f'До свиданья, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text)


@dp.message_handler()
async def echo_func(message: Message):
    answer: str
    if "ты кто" in message.text.lower():
        answer: str = 'Я твое эхо ...'
    else:
        answer = f'{message.text} '
    await message.answer(text=answer)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)