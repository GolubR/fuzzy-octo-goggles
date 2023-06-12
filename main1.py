from funct_test import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token = token)
dp = Dispatcher(bot, storage=MemoryStorage())

name = ""
age = ""

@dp.message_handler(commands=["start", "help"], state = "*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Hi!\nI'm InfoBot!\nPowered by myself.\nPlease, say your name")
    await state.set_state("q1")


@dp.message_handler(state="q1")
async def process_name(message: types.Message, state: FSMContext):
    global name
    name = message.text
    await state.update_data({"name": name})
    await state.set_state("q2")
    await message.answer("Say your age")

@dp.message_handler(state="q2")
async def process_age(message: types.Message, state: FSMContext):
    global age
    age = message.text
    if age.isdigit():
        await state.update_data({"age": int(age)})
        await message.answer("Now you can ask me about information you entered by sending /info command")
        await state.set_state("**")
    else:
        await message.answer("Send a number")

@dp.message_handler(commands = ["info"], state = "**")
async def n_age(message: Message, state: FSMContext):
    global name
    global age
    await message.answer("Ваше имя " + name + ", ваш возраст " + str(age))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)