from sqlalchemy.orm import Session
from models import Guest, Dish
from schemas import GuestCreate, DishCreate


def create_guest(db: Session, data: GuestCreate):
    guest = Guest(**data.dict())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


def get_guests(db: Session):
    return db.query(Guest).all()


def create_dish(db: Session, data: DishCreate):
    dish = Dish(**data.dict())
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


def get_dishes(db: Session):
    return db.query(Dish).all()