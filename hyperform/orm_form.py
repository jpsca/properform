from .form import Form


__all__ = ("PonyForm", "SQLAForm")


class PonyForm(Form):
    def create_object(self, data):
        return self._model(**data)

    def delete_object(self):
        return self._object.delete()


class SQLAForm(Form):
    def create_object(self, data):
        object = self._model(**data)
        self._session.add(object)
        self._session.flush()
        return object

    def delete_object(self):
        result = self._session.delete(self._object)
        self._session.flush()
        return result
