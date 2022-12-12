from datetime import datetime
from asyncpg import UniqueViolationError
from gino import Gino
from aiohttp import web

db = Gino()


class BaseModelMixin:

    @classmethod
    async def by_id(cls, obj_id):
        obj = await cls.get(obj_id)
        if obj:
            return obj
        else:
            raise web.HTTPNotFound()

    @classmethod
    async def create_model(cls, **kwargs):
        try:
            obj = await cls.create(**kwargs)
            return obj

        except UniqueViolationError:
            raise web.HTTPBadRequest()

    @classmethod
    async def update_model(cls, obj_id, **kwargs):
        get = await cls.by_id(obj_id)
        await get.update(**kwargs).apply()
        response = await cls.by_id(obj_id)
        return response


class Users(db.Model, BaseModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)

    idx = db.Index("users_user_username", "username", unique=True)

    def to_dict(self):
        dict_user = super().to_dict()
        dict_user.pop("password")
        return dict_user


class AD(db.Model, BaseModelMixin):

    __tablename__ = "ad"

    id = db.Column(db.Integer, primary_key=True)
    owners = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        ads = {
            "id": self.id,
            "owners": self.owners,
            "title": self.title,
            "text": self.text,
            "date": str(self.date),
        }
        return ads


async def return_all_posts():
    get = await AD.query.gino.all()
    some_list = []
    for adss in get:
        some_list.append({"id": adss.id, "owners": adss.owners, "title": adss.title, "text": adss.text,
                          "date": str(adss.date)})
    return some_list