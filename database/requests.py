from database.models import User,CrimeCase,Content,Favorite
from database.models import async_session
from sqlalchemy import select


ADMIN_ID = [1935020407]

# СОХРАНЕНИЕ ПОЛЬЗОВАТЕЛЯ / ПРОВЕРКА АДМИНА
async def set_user(tg_id,registration_day,username,firstname,lastname):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(
                User(
                    tg_id=tg_id,
                    username=username,
                    firstname=firstname or '',
                    lastname=lastname or '',
                    registration_day=registration_day
                )
            )
            await session.commit()

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_ID

# CRIME CASE  (ДОБАВЛЕНИЕ / УДАЛЕНИЕ)
async def append_crime_case(title,country,year,category,description):
    async with async_session() as session:
        crime_case = await session.scalar(select(CrimeCase).where(CrimeCase.title == title))

        if not crime_case:
            session.add(
                CrimeCase(
                    title=title,
                    country=country,
                    year=year,
                    category=category or '',
                    description=description or ''
                )
            )
            await session.commit()

async def delete_crime_case(title):
    async with async_session() as session:
        crime_case = await session.scalar(select(CrimeCase).where(CrimeCase.title == title))
        if crime_case is not None:
            await session.delete(crime_case)
            await session.commit()

async def update_crime_case(title,choose_field,waiting_for_value):
    async with async_session() as session:
        crime_case = await session.scalar(select(CrimeCase).where(CrimeCase.title == title))
        if crime_case is not None:
            match choose_field:
                case 'title':
                    crime_case.title = waiting_for_value
                case 'country':
                    crime_case.country = waiting_for_value
                case 'year':
                    crime_case.year = waiting_for_value
                case 'category':
                    crime_case.category = waiting_for_value
                case 'description':
                    crime_case.description = waiting_for_value
            await session.commit()



# КОНТЕНТ (ДОБАВЛЕНИЕ / УДАЛЕНИЕ)
async def append_content(content_type,title,author,link,case,description):
    async with async_session() as session:
        content = await session.scalar(select(Content).where((Content.title == title)&(Content.content_type == content_type)))

        case_id = await session.scalar(select(CrimeCase.id).where(CrimeCase.title == case))

        if not content:
            session.add(
                Content(
                    content_type=content_type,
                    title=title,
                    author=author or '',
                    link=link or '',
                    case_id=case_id or '',
                    description=description or ''
                )
            )
            await session.commit()

async def delete_content(title):
    async with async_session() as session:
        content = await session.scalar(select(Content).where(Content.title == title))
        if content is not None:
            await session.delete(content)
            await session.commit()



