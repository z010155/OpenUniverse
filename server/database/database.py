from datetime import datetime
from typing import Optional

import bcrypt
from peewee import PostgresqlDatabase, Model, CharField, BooleanField, ForeignKeyField, BigAutoField, DoesNotExist, \
    SmallIntegerField, IntegerField, BigIntegerField, DateTimeField

db = PostgresqlDatabase('openlu', user='postgres', password='postgres')

db.connect()


class InvalidPasswordException(Exception):
    pass


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = BigAutoField(primary_key=True)
    username = CharField(33)
    password = CharField(60)
    first_login_sub = BooleanField(default=True)
    free_to_play = BooleanField(default=False)
    front_character = SmallIntegerField(default=0)


class Character(BaseModel):
    character_id = BigAutoField(primary_key=True)
    user = ForeignKeyField(User, backref='characters')
    name = CharField(33)
    unapproved_name = CharField(33, default="")
    name_rejected = BooleanField(default=False)
    free_to_play = BooleanField(default=False)
    shirt_color = BigIntegerField()
    shirt_style = BigIntegerField()
    pants_color = BigIntegerField()
    hair_style = BigIntegerField()
    hair_color = BigIntegerField()
    lh = BigIntegerField()
    rh = BigIntegerField()
    eyebrow_style = BigIntegerField()
    eye_style = BigIntegerField()
    mouth_style = BigIntegerField()
    last_zone = IntegerField(default=0)
    last_instance = IntegerField(default=0)
    last_clone = BigIntegerField(default=0)
    last_login = DateTimeField(default=datetime.now)


class Inventory(BaseModel):
    object_id = BigIntegerField()
    lot = SmallIntegerField()
    character = ForeignKeyField(Character, backref='items')
    bound = BooleanField(default=False)
    amount = SmallIntegerField(default=1)
    slot = SmallIntegerField()


db.create_tables([User, Character, Inventory])


class Database:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        user = User(username=username,
                    password=bcrypt.hashpw(password.encode('latin1'), bcrypt.gensalt()).decode('latin1'))

        user.save()

        return user

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        try:
            return User.get(User.user_id == user_id)
        except DoesNotExist:
            return None

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        try:
            user = User.get(User.username == username)

            if bcrypt.checkpw(password.encode('latin1'), user.password.encode('latin1')):
                return user

            raise InvalidPasswordException()
        except DoesNotExist:
            return None
