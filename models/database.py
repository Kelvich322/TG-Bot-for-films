import peewee as pw
from peewee import CharField

DATABASE_NAME = "telegram_bot.db"
db = pw.SqliteDatabase(DATABASE_NAME)


class BaseModel(pw.Model):
    class Meta:
        database = db


class Users(BaseModel):
    id = pw.PrimaryKeyField(primary_key=True)
    login = pw.CharField(unique=True)
    name = pw.CharField()


class Viewed_materials(BaseModel):
    user = pw.ForeignKeyField(Users, backref="Users")
    material_name = CharField()
    material_url = CharField()
    date = pw.TimestampField()


def init_db():
    db.connect()
    db.create_tables([Users, Viewed_materials], safe=True)
