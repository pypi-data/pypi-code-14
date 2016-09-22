from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Table, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

postcode_restaurant = Table('postcode_restaurant', Base.metadata,
                            Column('postcode_id', Integer, ForeignKey('postcode.id')),
                            Column('restaurant_id', Integer, ForeignKey('restaurant.id'))
                            )


class Postcode(Base):
    __tablename__ = "postcode"
    id = Column(Integer, primary_key=True)
    postcode = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    restaurants = relationship("Restaurant", secondary=postcode_restaurant, back_populates="postcodes")

    def __repr__(self):
        return "<Postcode (country={}, postcode={}, url={})>".format(self.country, self.postcode, self.url)


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    postcodes = relationship('Postcode', secondary=postcode_restaurant, back_populates="restaurants")
    name = Column(String, nullable=False, index=True)
    url = Column(String(250), nullable=False, unique=True)
    info_url = Column(String(250))
    updated = Column(Date)
    info = relationship("Restaurant_info", uselist=False, cascade="all, delete, delete-orphan")
    open = relationship("Restaurant_open", uselist=False, cascade="all, delete, delete-orphan")
    category = relationship("Category", backref='restaurant', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Restaurant (name={}, url={})>".format(self.name, self.url)


class Restaurant_info(Base):
    __tablename__ = "restaurant_info"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    ratings = Column(Integer)
    delivery_fee = Column(String(250))
    minimum_delivery = Column(Integer)
    city = Column(String(500))
    street = Column(String(500))
    website = Column(String(250))
    description = Column(String)

    def __repr__(self):
        return "<Restaurant_info>"


class Restaurant_open(Base):
    __tablename__ = "restaurant_open"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    monday_am_open = Column(Time)
    monday_am_close = Column(Time)
    monday_pm_open = Column(Time)
    monday_pm_close = Column(Time)
    tuesday_am_open = Column(Time)
    tuesday_am_close = Column(Time)
    tuesday_pm_open = Column(Time)
    tuesday_pm_close = Column(Time)
    wednesday_am_open = Column(Time)
    wednesday_am_close = Column(Time)
    wednesday_pm_open = Column(Time)
    wednesday_pm_close = Column(Time)
    thursday_am_open = Column(Time)
    thursday_am_close = Column(Time)
    thursday_pm_open = Column(Time)
    thursday_pm_close = Column(Time)
    friday_am_open = Column(Time)
    friday_am_close = Column(Time)
    friday_pm_open = Column(Time)
    friday_pm_close = Column(Time)
    saturday_am_open = Column(Time)
    saturday_am_close = Column(Time)
    saturday_pm_open = Column(Time)
    saturday_pm_close = Column(Time)
    sunday_am_open = Column(Time)
    sunday_am_close = Column(Time)
    sunday_pm_open = Column(Time)
    sunday_pm_close = Column(Time)

    def __repr__(self):
        return "<Restaurant_open>"


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    name = Column(String, nullable=False, index=True)
    category_id = Column(String(250))
    meal = relationship("Meal", backref="category", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Category (name={}, category_id={}>".format(self.name, self.category_id)


class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String(250), nullable=False, index=True)
    price = Column(Float)
    product_id = Column(String(250))
    dom_id = Column(String(250))
    rest = Column(String(250))
    currency = Column(String(10))

    def __repr__(self):
        return "<meal (name={}, price={}, product_id={}>".format(self.name, self.price, self.product_id)


class UserTbl(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, index=True, unique=True)
    city = Column(String)
    postcode = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<User (username={}, name={}, email={}>".format(self.username, self.name, self.email)


if __name__ == "__main__":
    pass
