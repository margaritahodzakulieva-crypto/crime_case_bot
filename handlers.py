import keyboards as kb
import database.requests as rq

from aiogram import F,Router
from datetime import datetime, timezone
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from states import AddCrimeCase, AddContent, DeleteCrimeCase, DeleteContent, UpdateCrimeCase, UpdateContent


router = Router()

# СТАРТ И ПАНЕЛЬ АДМИНЕСТРАТОРА
@router.message(CommandStart())
async def start(message: Message,state: FSMContext):
    await rq.set_user(tg_id=message.from_user.id,
                      registration_day=datetime.now(timezone.utc),
                      username=message.from_user.username,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      )
    await message.answer('Hello!',
                         reply_markup=kb.menu)

@router.message(Command("minlu"))
async def admin_panel(message: Message):
    if not await rq.is_admin(message.from_user.id):
        await message.answer("Нет доступа.")
        return
    await message.answer('привет маргош у тебя есть что-то новое!?!?',
                         reply_markup=kb.admin_menu)


# ДОБАВЛЕНИЕ CRIME CASE
@router.message(F.text == 'добавить')
async def admin_menu(message: Message):
    await message.answer('что ты хочешь добавить',
                         reply_markup=kb.append_catalog)

@router.callback_query(F.data.startswith('crime_'))
async def chek_brand_append(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(AddCrimeCase.title)
        await callback.message.answer('отправь название crime case..')
        await callback.answer()
    elif crime_name == 'content':
        await state.set_state(AddContent.content_type)
        await callback.message.answer('какой контенты ты хочешь добавить..')
        await callback.answer()

@router.message(AddCrimeCase.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddCrimeCase.country)
    await message.answer('в какой стране это было..')

@router.message(AddCrimeCase.country)
async def process_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text.strip())
    await state.set_state(AddCrimeCase.year)
    await message.answer('в каком году это было..')

@router.message(AddCrimeCase.year)
async def process_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text.strip())
    await state.set_state(AddCrimeCase.category)
    await message.answer('В какую категорию входит дело?')

@router.message(AddCrimeCase.category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text.strip())
    await state.set_state(AddCrimeCase.description)
    await message.answer('Расскажи подробнее про это дело:')

@router.message(AddCrimeCase.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())

    crime_case = await state.get_data()
    await rq.append_crime_case(
        title=crime_case['title'],
        country=crime_case['country'],
        year=crime_case['year'],
        category=crime_case['category'],
        description=crime_case['description'],
    )

    await message.answer('все я запомнил про это дело')
    await state.clear()

# ДОБАВЛЕНИЕ КОНТЕНТА
@router.message(AddContent.content_type)
async def content_type(message: Message, state: FSMContext):
    await state.update_data(content_type=message.text.strip())
    await state.set_state(AddContent.title)
    await message.answer('отправь название..')

@router.message(AddContent.title)
async def content_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddContent.author)
    await message.answer('кто автор..')

@router.message(AddContent.author)
async def content_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text.strip())
    await state.set_state(AddContent.description)
    await message.answer('про что там..')

@router.message(AddContent.description)
async def content_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddContent.link)
    await message.answer('где можно посмотреть..')

@router.message(AddContent.link)
async def content_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text.strip())
    await state.set_state(AddContent.case_id)
    await message.answer('что за crime case..')

@router.message(AddContent.case_id)
async def content_case_id(message: Message, state: FSMContext):
    await state.update_data(case_id=message.text.strip())

    content = await state.get_data()
    await rq.append_content(
        content_type=content['content_type'],
        title=content['title'],
        author=content['author'],
        link=content['link'],
        case=content['case_id'],
        description=content['description'],
    )

    await message.answer('хорошая находка')
    await state.clear()


# УДАЛЕНИЕ CRIME CASE И КОНТЕНТА
@router.message(F.text == 'удалить')
async def admin_delete_menu(message: Message):
    await message.answer('что ты хочешь удалить',
                         reply_markup=kb.delete_catalog)

@router.callback_query(F.data.startswith('delete_'))
async def chek_brand_delete(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(DeleteCrimeCase.title)
        await callback.message.answer('отправь название crime case..')
        await callback.answer()
    elif crime_name == 'content':
        await state.set_state(DeleteContent.title)
        await callback.message.answer('отправь название контента..')
        await callback.answer()

@router.message(DeleteContent.title)
async def content_delete(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())

    content = await state.get_data()
    await rq.delete_content(
        title=content['title']
    )

    await message.answer('этот контент удален',
                         reply_markup=kb.admin_menu)
    await state.clear()

@router.message(DeleteCrimeCase.title)
async def crime_case_delete(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())

    crime_case = await state.get_data()
    await rq.delete_crime_case(
        title=crime_case['title']
    )

    await message.answer('этот crime case удален',
                         reply_markup=kb.admin_menu)
    await state.clear()


# ОБНОВЛЕНИЕ CRIME CASE И КОНТЕНТ
@router.message(F.text == 'отредактировать')
async def admin_update_menu(message: Message):
    await message.answer('что ты хочешь обновить',
                         reply_markup=kb.update_catalog)

@router.callback_query(F.data.startswith('update_'))
async def chek_brand_update(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(UpdateCrimeCase.title)
        await callback.message.answer('отправь название crime case..')
        await callback.answer()
    elif crime_name == 'content':
        await state.set_state(UpdateContent.title)
        await callback.message.answer('отправь название контента..')
        await callback.answer()

@router.message(UpdateCrimeCase.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(UpdateCrimeCase.choose_field)
    await message.answer('что будем менять')

@router.message(UpdateCrimeCase.choose_field)
async def process_field(message: Message, state: FSMContext):
    await state.update_data(choose_field=message.text.strip())
    await state.set_state(UpdateCrimeCase.waiting_for_value)
    await message.answer('на что будем менять..')

@router.message(UpdateCrimeCase.waiting_for_value)
async def crime_case_update(message: Message, state: FSMContext):
    await state.update_data(waiting_for_value=message.text.strip())

    crime_case = await state.get_data()
    await rq.update_crime_case(
        title=crime_case['title'],
        choose_field=crime_case['choose_field'],
        waiting_for_value=crime_case['waiting_for_value'],
    )

    await message.answer('этот crime case изменен',
                         reply_markup=kb.admin_menu)
    await state.clear()



# МЕНЮ ПОЛЬЗОВАТЕЛЯ
@router.message(F.text == 'menu')
async def menu(message: Message):
    await message.answer('select a category',
                         reply_markup=kb.catalog)

# @user.message(F.photo)
# async def photo(message: Message):
#     await message.answer(f'you send photo ,\n\n id:{message.photo[-1].file_id}')
#     await message.answer_photo(message.photo[-2].file_id)
#
# @user.message()
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.chat.id)