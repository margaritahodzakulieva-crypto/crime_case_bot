from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column( primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(25))
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    registration_day = mapped_column(DateTime(timezone=True))

class CrimeCase(Base):
    __tablename__ = 'crime_cases'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(70))
    country: Mapped[str] = mapped_column(String(50))
    year: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(50))

class Content(Base):
    __tablename__ = 'contents'
    id: Mapped[int] = mapped_column(primary_key=True)
    content_type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(120))
    link  = mapped_column(String(120))
    case_id: Mapped[int] = mapped_column(ForeignKey('crime_cases.id'))

class Favorite(Base):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    case_id: Mapped[int] = mapped_column(ForeignKey('crime_cases.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)