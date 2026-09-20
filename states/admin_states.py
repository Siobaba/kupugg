from aiogram.fsm.state import StatesGroup, State

class AddProduct(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    is_active = State()