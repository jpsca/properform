from .form import Form


__all__ = ("PonyForm", "SQLAForm")


class PonyForm(Form):
    def create_object(self, data):
        return self._model(**data)

    def delete_object(self):
        return self.object.delete()


class SQLAForm(Form):
    def create_object(self, data):
        object = self._model(**data)
        self._session.add(object)
        return object

    def delete_object(self):
        return self._session.delete(self.object)
