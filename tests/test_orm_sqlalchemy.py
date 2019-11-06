from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import proper_form as f
from proper_form.constants import SEP, NEW, DELETED


engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    cars = relationship("Car", back_populates="owner")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('people.id'))
    owner = relationship("Person", back_populates="cars")


Base.metadata.create_all(engine)


class CarForm(f.SQLAForm):
    _model = Car
    _session = session

    make = f.Text(required=True)
    model = f.Text(required=True)


class PersonForm(f.SQLAForm):
    _model = Person
    _session = session

    name = f.Text(required=True)
    age = f.Integer(required=True)
    cars = f.FormSet(CarForm, backref="owner")


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
    session.commit()

    assert isinstance(obj, Person)
    assert obj.name == input_data["name"]

    cars = list(obj.cars)
    assert len(cars) == 2
    assert isinstance(cars[0], Car)
    assert cars[0].make in ("Renault", "Aspire")
    assert cars[0].model in ("Le Car", "RS")


def test_orm_save_update_and_delete():
    input_data = {
        "name": "John",
        "age": 20,
        f"cars{SEP}100{SEP}make": "Renault",
        f"cars{SEP}100{SEP}model": "Le Car",
        f"cars{SEP}101{SEP}{DELETED}": "1",
    }

    p1 = Person(name="John", age=20)
    c1 = Car(id=100, make="Toyota", model="Prius", owner=p1)
    c2 = Car(id=101, make="Ford", model="Explorer", owner=p1)
    session.add(p1)
    session.add(c1)
    session.add(c2)
    session.commit()

    form = PersonForm(input_data, p1)

    assert form.validate()
    obj = form.save()
    session.commit()

    assert isinstance(obj, Person)
    cars = list(obj.cars)
    assert len(cars) == 1
    assert isinstance(cars[0], Car)
    assert cars[0].make == "Renault"
    assert cars[0].model == "Le Car"
