from pony import orm

import proper_form as f


db = orm.Database()


class Person(db.Entity):
    name = orm.Required(str)
    age = orm.Required(int)
    cars = orm.Set('Car')


class Car(db.Entity):
    make = orm.Required(str)
    model = orm.Required(str)
    owner = orm.Required(Person)


db.bind(provider='sqlite', filename=':memory:')
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
