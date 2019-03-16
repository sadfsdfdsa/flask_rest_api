from models import *


class ApiV1:
    api_objects = {
        'users': User,
        'urls': Url
    }

    api_objects_columns = {
        'users': ['id', 'username', 'email', 'password'],
        'urls': ['id', 'url', 'text']
    }

    @classmethod
    def get_all(cls, object, *args, **kwargs):
        return [i.serialize for i in cls.api_objects[object].query.all()]

    @classmethod
    def get_by_id(cls, object, id, *args, **kwargs):
        return [i.serialize for i in cls.api_objects[object].query.filter_by(id=id).all()]

    @classmethod
    def post_object(cls, object, db, *args, **kwargs):
        object = cls.api_objects[object](**kwargs)
        db.session.add(object)
        db.session.commit()
        return object

    @classmethod
    def put_object_by_id(cls, object, db, id, *args, **kwargs):
        db_object = cls.api_objects[object].query.filter_by(id=id).first()
        if db_object is None:
            return None
        for key in kwargs.keys():
            setattr(db_object, key, kwargs[key])
        db.session.commit()
        return [i.serialize for i in cls.api_objects[object].query.filter_by(id=id).all()]

    @classmethod
    def delete_object_by_id(cls, object, db, id, *args, **kwargs):
        if len(cls.api_objects[object].query.filter_by(id=id).all()) != 0:
            cls.api_objects[object].query.filter_by(id=id).delete()
            db.session.commit()
            return True
        else:
            return False


Apis_version_dict = {
    'v1': ApiV1
}
