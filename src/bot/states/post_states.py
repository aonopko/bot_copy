from aiogram.fsm.state import State, StatesGroup

class PostStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_topic = State()
    waiting_for_photo = State() 