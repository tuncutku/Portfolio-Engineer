from src.extensions import db
from sqlalchemy_serializer import SerializerMixin


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
