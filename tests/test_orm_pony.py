try:
    from pony import orm
except ImportError:
    orm = None

import proper_form as f
from proper_form.constants import SEP, NEW, DELETED

if orm:
    db = orm.Database()

    class Person(db.Entity):
        name = orm.Required(str)
        age = orm.Required(int)
        cars = orm.Set("Car")

    class Car(db.Entity):
        make = orm.Required(str)
        model = orm.Required(str)
        owner = orm.Required(Person)

    db.bind(provider="sqlite", filename=":memory:")
    db.generate_mapping(create_tables=True)
    orm.set_sql_debug(True)

    class CarForm(f.PonyForm):
        _model = Car

        make = f.Text(required=True)
        model = f.Text(required=True)

    class PersonForm(f.PonyForm):
        _model = Person

        name = f.Text(required=True)
        age = f.Integer(required=True)
        cars = f.FormSet(CarForm, backref="owner")

    @orm.db_session
    def test_orm_save():
        input_data = {
            "name": "Jesse Montgomery III",
            "age": 23,
            f"cars{SEP}{NEW}1{SEP}make": "Renault",
            f"cars{SEP}{NEW}1{SEP}model": "Le Car",
            f"cars{SEP}{NEW}2{SEP}make": "Aspire",
            f"cars{SEP}{NEW}2{SEP}model": "RS",
        }
        form = PersonForm(input_data)

        assert form.validate()
        obj = form.save()
        assert isinstance(obj, Person)
        assert obj.name == input_data["name"]

        cars = list(obj.cars)
        assert len(cars) == 2
        assert isinstance(cars[0], Car)
        assert cars[0].make in ("Renault", "Aspire")
        assert cars[0].model in ("Le Car", "RS")

    @orm.db_session
    def test_orm_save_update_and_delete():
        input_data = {
            "name": "John",
            "age": 20,
            f"cars{SEP}100{SEP}make": "Renault",
            f"cars{SEP}100{SEP}model": "Le Car",
            f"cars{SEP}101{SEP}{DELETED}": "1",
        }

        p1 = Person(name="John", age=20)
        Car(id=100, make="Toyota", model="Prius", owner=p1)
        Car(id=101, make="Ford", model="Explorer", owner=p1)
        orm.commit()

        form = PersonForm(input_data, p1)

        assert form.validate()
        obj = form.save()
        assert isinstance(obj, Person)
        cars = list(obj.cars)
        assert len(cars) == 1
        assert isinstance(cars[0], Car)
        assert cars[0].make == "Renault"
        assert cars[0].model == "Le Car"
