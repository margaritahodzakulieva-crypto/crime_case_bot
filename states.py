from aiogram.fsm.state import State,StatesGroup


# CRIME_CASE  (УДАЛЕНИЕ / ДОБАВЛЕНИЕ / ОБНОВЛЕНИЕ)
class AddCrimeCase(StatesGroup):
    title = State()
    country = State()
    year = State()
    category = State()
    description = State()

class DeleteCrimeCase(StatesGroup):
    title = State()

class UpdateCrimeCase(StatesGroup):
    title = State()
    choose_field = State()
    waiting_for_value = State()

# КОНТЕНТ  (УДАЛЕНИЕ / ДОБАВЛЕНИЕ / ОБНОВЛЕНИЕ)
class AddContent(StatesGroup):
    content_type = State()
    title = State()
    author = State()
    description = State()
    link = State()
    case_id = State()

class DeleteContent(StatesGroup):
    title = State()

class UpdateContent(StatesGroup):
    title = State()
    choose_field = State()
    waiting_for_value = State()