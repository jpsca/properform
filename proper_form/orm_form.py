from .form import Form


__all__ = ("PonyForm", "SQLAForm")


class PonyForm(Form):
    def create_object(self, **data):
        return self._model(**data)

    def delete_object(self, object):
        return object.delete()


class SQLAForm(Form):
    @property
    def db_session(self):
        return self._model.sa.session()

    def create_object(self, **data):
        object = self._model(**data)
        self.db_session.add(object)
        return object

    def delete_object(self, object):
        return self.db_session.delete(object)
