from src.extensions import db
from sqlalchemy_serializer import SerializerMixin


class BaseModel(db.Model):
    __abstract__ = True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
