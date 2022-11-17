import peewee

from config import settings


database = peewee.SqliteDatabase(settings.DATABASE_NAME)
