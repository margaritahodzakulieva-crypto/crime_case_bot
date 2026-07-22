import keyboards as kb
import database.requests as rq

from aiogram import F,Router
from datetime import datetime, timezone
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from states import AddCrimeCase, AddContent, DeleteCrimeCase, DeleteContent, UpdateCrimeCase, UpdateContent, FoundCrimeCase


router = Router()

# СТАРТ И ПАНЕЛЬ АДМИНЕСТРАТОРА
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await rq.set_user(
        tg_id=message.from_user.id,
        registration_day=datetime.now(timezone.utc),
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name,
    )
    await message.answer(
        "🕵️ Добро пожаловать в архив True Crime.\n"
        "Выбери, что хочешь сделать.",
        reply_markup=kb.menu
    )

@router.message(Command("minlu"))
async def admin_panel(message: Message):
    if not await rq.is_admin(message.from_user.id):
        await message.answer("Нет доступа.")
        return
    await message.answer(
        "🔐 Доступ подтвержден.\nЧто будем делать?",
        reply_markup=kb.admin_menu
    )

# ВЕРНУТСЯ ДЛЯ АДМИНА
@router.message(F.text == 'Вернуться🔙')
async def back_to_admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        '↩️ Возвращаемся в главное меню.',
        reply_markup=kb.admin_menu
    )


# ДОБАВЛЕНИЕ CRIME CASE
@router.message(F.text == 'Добавить➕')
async def admin_menu(message: Message):
    await message.answer(
        'Ты нашел что-то новое? И что это?',
        reply_markup=kb.append_catalog
    )

@router.callback_query(F.data.startswith('crime_'))
async def check_brand_append(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(AddCrimeCase.title)
        await callback.message.answer(
            '🗂 Добавим новое дело.\nКак называется Crime Case?',
            reply_markup=kb.go_back_admin
        )
    elif crime_name == 'content':
        await state.set_state(AddContent.content_type)
        await callback.message.answer(
            '🎬 Что добавляем?\nФильм, сериал, книга, подкаст или что-то другое?',
            reply_markup=kb.go_back_admin
        )
    await callback.answer()

@router.message(AddCrimeCase.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddCrimeCase.country)
    await message.answer('🌍 В какой стране произошло это дело?', reply_markup=kb.go_back_admin)

@router.message(AddCrimeCase.country)
async def process_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text.strip())
    await state.set_state(AddCrimeCase.year)
    await message.answer('📅 В каком году произошли события?', reply_markup=kb.go_back_admin)

@router.message(AddCrimeCase.year)
async def process_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text.strip())
    await state.set_state(AddCrimeCase.category)
    await message.answer('⚖️ Какая основная категория преступления?', reply_markup=kb.go_back_admin)

@router.message(AddCrimeCase.category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text.strip())
    await state.set_state(AddCrimeCase.description)
    await message.answer(
        "📝 Теперь расскажи само дело.\nЧем подробнее описание, тем лучше.",
        reply_markup=kb.go_back_admin
    )

@router.message(AddCrimeCase.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())

    data = await state.get_data()
    try:
        await rq.append_crime_case(
            title=data['title'],
            country=data['country'],
            year=data['year'],
            category=data['category'],
            description=data['description'],
        )
        await message.answer('✅ Crime Case успешно добавлен в архив.', reply_markup=kb.admin_menu)
    except Exception as e:
        await message.answer('❌ Ошибка при добавлении дела.')
        print(f"Add crime error: {e}")

    await state.clear()

# ДОБАВЛЕНИЕ КОНТЕНТА
@router.message(AddContent.content_type)
async def content_type(message: Message, state: FSMContext):
    await state.update_data(content_type=message.text.strip())
    await state.set_state(AddContent.title)
    await message.answer('📌 Как называется этот материал?', reply_markup=kb.go_back_admin)

@router.message(AddContent.title)
async def content_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddContent.author)
    await message.answer('👤 Кто автор или создатель?', reply_markup=kb.go_back_admin)

@router.message(AddContent.author)
async def content_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text.strip())
    await state.set_state(AddContent.description)
    await message.answer('📝 Коротко расскажи, о чем он.', reply_markup=kb.go_back_admin)

@router.message(AddContent.description)
async def content_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddContent.link)
    await message.answer('🔗 Пришли ссылку.', reply_markup=kb.go_back_admin)

@router.message(AddContent.link)
async def content_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text.strip())
    await state.set_state(AddContent.case_id)
    await message.answer(
        '🗂 Укажи ID Crime Case, к которому относится этот материал.\nЕсли связи нет — отправь 0.',
        reply_markup=kb.go_back_admin
    )

@router.message(AddContent.case_id)
async def content_case_id(message: Message, state: FSMContext):
    await state.update_data(case_id=message.text.strip())
    data = await state.get_data()

    try:
        await rq.append_content(
            content_type=data['content_type'],
            title=data['title'],
            author=data['author'],
            link=data['link'],
            case=data['case_id'],
            description=data['description'],
        )
        await message.answer('✅ Контент успешно сохранен.', reply_markup=kb.admin_menu)
    except Exception as e:
        await message.answer('❌ Ошибка при сохранении контента.')
        print(f"Add content error: {e}")

    await state.clear()


# УДАЛЕНИЕ CRIME CASE И КОНТЕНТА
@router.message(F.text == 'Удалить➖')
async def admin_delete_menu(message: Message):
    await message.answer('🗑 Что будем удалять?', reply_markup=kb.delete_catalog)

@router.callback_query(F.data.startswith('delete_'))
async def check_brand_delete(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(DeleteCrimeCase.title)
        await callback.message.answer('🗂 Какой Crime Case удалить?\nНапиши его название.', reply_markup=kb.go_back_admin)
    elif crime_name == 'content':
        await state.set_state(DeleteContent.title)
        await callback.message.answer('🎬 Какой материал удалить?\nНапиши его название.', reply_markup=kb.go_back_admin)
    await callback.answer()

@router.message(DeleteContent.title)
async def content_delete(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())

    content = await state.get_data()
    await rq.delete_content(
        title=content['title']
    )

    await message.answer('✅ Контент удален.',
                         reply_markup=kb.admin_menu)
    await state.clear()

@router.message(DeleteCrimeCase.title)
async def crime_case_delete(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())

    crime_case = await state.get_data()
    await rq.delete_crime_case(
        title=crime_case['title']
    )

    await message.answer('✅ Crime Case удален из архива.',
                         reply_markup=kb.admin_menu)
    await state.clear()


# ОБНОВЛЕНИЕ CRIME CASE И КОНТЕНТ
@router.message(F.text == 'Отредактировать📝')
async def admin_update_menu(message: Message):
    await message.answer('Что ты решил отредактировать',
                         reply_markup=kb.update_catalog)

@router.callback_query(F.data.startswith('update_'))
async def chek_brand_update(callback: CallbackQuery, state: FSMContext):
    crime_name = callback.data.split('_')[1]
    if crime_name == 'сase':
        await state.set_state(UpdateCrimeCase.title)
        await callback.message.answer('🗂 Какой Crime Case нужно изменить?',
                                      reply_markup=kb.go_back_admin)
        await callback.answer()
    elif crime_name == 'content':
        await state.set_state(UpdateContent.title)
        await callback.message.answer('🎬 Какой материал нужно изменить?'
                                      ,reply_markup=kb.go_back_admin)
        await callback.answer()

@router.message(UpdateCrimeCase.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(UpdateCrimeCase.choose_field)
    await message.answer('✏️ Какое поле будем редактировать?\n(Название, страна, год, категория или описание.)'
                         ,reply_markup=kb.go_back_admin)

@router.message(UpdateCrimeCase.choose_field)
async def process_field(message: Message, state: FSMContext):
    await state.update_data(choose_field=message.text.strip())
    await state.set_state(UpdateCrimeCase.waiting_for_value)
    await message.answer('📝 Введи новое значение.',
                         reply_markup=kb.go_back_admin)

@router.message(UpdateCrimeCase.waiting_for_value)
async def crime_case_update(message: Message, state: FSMContext):
    await state.update_data(waiting_for_value=message.text.strip())

    crime_case = await state.get_data()
    await rq.update_crime_case(
        title=crime_case['title'],
        choose_field=crime_case['choose_field'],
        waiting_for_value=crime_case['waiting_for_value'],
    )

    await message.answer('✅ Crime Case обновлен.',
                         reply_markup=kb.admin_menu)
    await state.clear()

@router.message(UpdateContent.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(UpdateContent.choose_field)
    await message.answer('✏️ Какое поле будем редактировать?',
                         reply_markup=kb.go_back_admin)

@router.message(UpdateContent.choose_field)
async def process_field(message: Message, state: FSMContext):
    await state.update_data(choose_field=message.text.strip())
    await state.set_state(UpdateContent.waiting_for_value)
    await message.answer('📝 Введи новое значение.',
                         reply_markup=kb.go_back_admin)

@router.message(UpdateContent.waiting_for_value)
async def content_update(message: Message, state: FSMContext):
    await state.update_data(waiting_for_value=message.text.strip())

    content = await state.get_data()
    await rq.update_content(
        title=content['title'],
        choose_field=content['choose_field'],
        waiting_for_value=content['waiting_for_value'],
    )

    await message.answer('✅ Контент обновлен.',
                         reply_markup=kb.admin_menu)
    await state.clear()


# CRIME CASES И КОНТЕНТ
@router.message(F.text == 'Crime Case📂')
async def show_crime_cases(message: Message):
    await message.answer("📂 Загружаю архив Crime Case...")
    crime_list = await rq.get_crime_cases()

    if not crime_list:
        await message.answer("📭 Архив пока пуст.")
        return

    text = "📋 <b>Список криминальных дел:</b>\n\n"
    for case in crime_list:
        text += (
            f"🔹 <b>ID:</b> {case[0]}\n"
            f"📌 <b>Название:</b> {case[1]}\n"
            f"🌍 <b>Страна:</b> {case[2]}\n"
            f"📅 <b>Год:</b> {case[3]}\n"
            f"📂 <b>Категория:</b> {case[4]}\n"
            f"📝 <b>Описание:</b> {case[5][:300]}...\n"
            f"{'─' * 30}\n\n"
        )

    if len(text) > 4000:
        await message.answer("📚 Архив слишком большой. Показываю первые записи.")
        await message.answer(text[:4000], parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")

@router.message(F.text == 'Контент🎬')
async def show_content(message: Message):
    await message.answer("🎬 Загружаю каталог контента...")
    content_list = await rq.get_content()

    if not content_list:
        await message.answer("📭 Пока нет ни одного материала.")
        return

    text = "📋 <b>Список криминального контента:</b>\n\n"
    for content in content_list:
        text += (
            f"🔹 <b>ID:</b> {content[0]}\n"
            f"📌 <b>Название:</b> {content[1]}\n"
            f"🌍 <b>Тип контента:</b> {content[2]}\n"
            f"📅 <b>Автор:</b> {content[3]}\n"
            f"📂 <b>Ссылка:</b> {content[4]}\n"
            f"📝 <b>Описание:</b> {content[5][:300]}...\n"
            f"📂 <b>Crime case:</b> {content[6]}\n"
            f"{'─' * 30}\n\n"
        )

    if len(text) > 4000:
        await message.answer("📚 Материалов слишком много. Показываю первые записи.")
        await message.answer(text[:4000], parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")


# МЕНЮ ПОЛЬЗОВАТЕЛЯ
@router.message(F.text == 'menu')
async def menu(message: Message):
    await message.answer("📂 Выбери раздел.", reply_markup=kb.catalog)


# НАЙТИ CRIME CASE
@router.message(F.text == '🔍 Найти дело')
async def found_crime(message: Message, state: FSMContext):
    await state.set_state(FoundCrimeCase.title)
    await message.answer(
        '🔎 Введи название Crime Case, которое хочешь найти:',
        reply_markup=kb.menu
    )

@router.message(FoundCrimeCase.title, F.text == "Отмена")
async def cancel_search(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🚫 Поиск отменён.', reply_markup=kb.menu)

@router.message(FoundCrimeCase.title)
async def search_crime_by_title(message: Message, state: FSMContext):
    search_title = message.text.strip()
    if not search_title:
        await message.answer('⚠️ Название не может быть пустым.')
        return

    try:
        crime_case = await rq.get_crime_case_by_title(search_title)
        if crime_case:
            await message.answer(
                f'✅ <b>Crime Case найден!</b>\n\n'
                f'<b>Название:</b> {crime_case.title}\n'
                f'<b>ID:</b> {crime_case.id}\n'
                f'<b>Страна:</b> {crime_case.country}\n'
                f'<b>Год:</b> {crime_case.year}\n'
                f'<b>Категория:</b> {crime_case.category}\n\n'
                f'<b>Описание:</b>\n{crime_case.description or "—"}',
                parse_mode="HTML"
            )
        else:
            await message.answer(f'❌ Crime Case «{search_title}» не найден.', reply_markup=kb.menu)
    except Exception as e:
        await message.answer('❌ Ошибка при поиске.')
        print(f"Search error: {e}")

    await state.clear()

# @user.message(F.photo)
# async def photo(message: Message):
#     await message.answer(f'you send photo ,\n\n id:{message.photo[-1].file_id}')
#     await message.answer_photo(message.photo[-2].file_id)
#
# @user.message()
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.chat.id)