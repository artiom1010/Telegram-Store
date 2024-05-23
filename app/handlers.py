from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Welcome to the sneaker store !", reply_markup=kb.main)


@router.message(F.text == "Catalog")
async def catalog(message: Message):
    await message.answer("Select a product category", reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer("You selected a category")
    await callback.message.answer("Select an item from the category", 
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_items(callback.data.split('_')[1])
    await callback.answer("You selected an item")
    await callback.message.answer(f"Title: {item_data.name}\nDescription: {item_data.description}\nPrice: {item_data.price} $", 
                                  reply_markup=await kb.items(callback.data.split('_')[1]))







# class Register (StatesGroup):
#     name = State()
#     age = State()
#     number = State()

# @router.message(Command("help"))
# async def cmd_help(message: Message):
#     await message.answer("Do you need help?")

# @router.message (F.text == "Каталог")
# async def catalog(message: Message):
#     await message.answer("Выберите категорию товара", reply_markup=kb.catalog)


# @router.callback_query(F.data == "t-shirt")
# async def t_shirt(callback: CallbackQuery):
#     await callback.answer("Вы выбрали категорю", show_alert=True)
#     await callback.message.answer("Вы выбрали футболки")


# @router.message (Command('register'))
# async def register(message: Message, state: FSMContext):
#     await state.set_state(Register.name)
#     await message.answer('Введите ваше имя')


# @router.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer('Введите ваш возраст')


# @router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.number)
#     await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)


# @router.message(Register.number, F.contact)
# async def register_number(message: Message, state: FSMContext):
#     await state.update_data(number=message.contact.phone_number)
#     data = await state.get_data()
#     await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер телефона: {data["number"]}')
#     await state.clear()