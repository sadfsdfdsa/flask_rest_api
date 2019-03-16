from app import db
import psycopg2


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return str({"id": self.id, "username": self.username, "email": self.email, "password": self.password})

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            # This is an example how to deal with Many2Many relations
            'email': self.email,
            #'password': self.password
        }

    @property
    def serialize_many2many(self):
        """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
        return [item.serialize for item in self.many2many]

    @classmethod
    def return_columns(cls):
        return [cls.username, cls.email, cls.password]


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(120), nullable=False)
    text = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return str({"id": self.id, "url": self.url, "text": self.text})

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            # This is an example how to deal with Many2Many relations
            'text': self.text,
            #'password': self.password
        }

    @property
    def serialize_many2many(self):
        """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
        return [item.serialize for item in self.many2many]

    @classmethod
    def return_columns(cls):
        return [cls.url, cls.text]
#db.metadata.clear()
#db.create_all()

"""
try:
    user = User.query.filter_by(nickname=user.nickname).one()
except NoResultFound:
    # ник уникален
    pass
else:
    # ник не уникален
    pass
    
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
                                lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
"""