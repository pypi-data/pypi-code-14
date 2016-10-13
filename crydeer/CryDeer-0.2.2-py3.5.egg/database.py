#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# import sqlite3
import os
from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    nu = Column(String)
    description = Column(String)
    comCode = Column(String)
    state = Column(Integer)
    status = Column(Integer)
    lastUpdateTime = Column(String, primary_key=True)
    lastUpdateInfo = Column(String)

    def __init__(self, id, nu, description, comCode, state, status, lastUpdateTime, lastUpdateInfo):
        self.id = id
        self.nu = nu
        self.description = description
        self.comCode = comCode
        self.state = state
        self.status = status
        self.lastUpdateTime = lastUpdateTime
        self.lastUpdateInfo = lastUpdateInfo

    def __repr__(self):
        return "<Item('%d','%s','%s','%s','%d','%d','%s','%s')"\
               % (self.id, self.nu, self.description, self.comCode, self.state,\
                  self.status, self.lastUpdateTime, self.lastUpdateInfo)


class Info(Base):

    __tablename__ = "infos"

    id = Column(Integer, primary_key=True)
    nu = Column(String)
    time = Column(String)
    context = Column(String)

    def __init__(self, id, nu, time, context):
        self.nu = nu
        self.time = time
        self.context = context

    def __repr__(self):
        return "<Info(time='%s',context='%s')" % (self.time, self.context)

class Database:

    items_table = Item.__table__
    metadata = Base.metadata
    engine = ""
    db_location = ""
    db_name = ""
    session = ""
    infos = []

    def __init__(self, db_name=".items.db"):
        self.db_name = db_name
        self.db_location = "sqlite:///" + os.path.expanduser("~") +"/" + db_name
        self.engine = create_engine(self.db_location, echo=False)
        self.metadata = MetaData(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.items_table = Item.__table__
        if not database_exists(self.db_location):
            create_database(self.engine.url)
        Base.metadata.create_all(self.engine)

    def get_all_nu(self):
        return [item.nu for item in self.session.query(Item)]

    def get_full_nu(self, short_nu):
        nus = []
        for nu in self.get_all_nu():
            if nu[:len(short_nu)] == short_nu:
                nus.append(nu)
        return nus

    def has_item(self, nu):
        query = self.session.query(Item).filter(Item.nu == nu)
        return query.count() > 0

    def insert_item(self, id, nu, description, comCode, state, status, lastUpdateTime, lastUpdateInfo):
        query = self.session.query(Item).filter(Item.nu == nu);
        if query.count() == 0:
            self.session.add(Item(id, nu, description, comCode, state, status, lastUpdateTime, lastUpdateInfo))
            self.session.commit()

    def insert_info(self, id, nu, time, context):
        query = self.session.query(Info).filter(Info.time == time);
        if query.count() == 0:
            self.session.add(Info(id, nu, time, context))
            self.session.commit()

    def get_new_item_id(self):
        query =   self.session.query(Item)\
                                    .order_by(Item.id)
        if (query.count() > 0):
            return query[-1].id + 1
        else:
            return 0

    def get_new_info_id(self):
        query =   self.session.query(Info)\
                                    .order_by(Info.id)
        if (query.count() > 0):
            return query[-1].id + 1
        else:
            return 0

    def find_item(self, nu):
        try:
            item = self.session.query(Item)\
                       .filter(Item.nu == nu)\
                       .one()
            return item
        except NoResultFound:
            print("无法找到")

    def update_item(self, nu, state, status, lastUpdateTime, lastUpdateInfo):
        try:
            item = self.session.query(Item)\
                       .filter(Item.nu == nu)\
                       .one()
            item.state = state
            item.status = status
            item.lastUpdateTime = lastUpdateTime
            item.lastUpdateInfo = lastUpdateInfo
            self.session.commit()
        except NoResultFound:
            print("无法找到")

    def delete_item(self, nu):
        try:
            item = self.session.query(Item)\
                       .filter(Item.nu == nu)\
                       .one()
            self.session.delete(item)
            self.session.commit()
        except NoResultFound:
            print("无法找到")

    def delete_info(self, nu):
        try:
            query = self.session.query(Info)\
                       .filter(Info.nu == nu)
            for info in query:
                self.session.delete(info)
            self.session.commit()
        except NoResultFound:
            print("无法找到")

    def get_item_query(self):
        return self.session.query(Item)

    def get_info_query(self, nu):
        return self.session.query(Info).filter(Info.nu == nu).order_by(Info.time)

    def display(self):
        for instance in self.session.query(Item)\
                                    .order_by(Item.id):
            print(instance)

if __name__ == "__main__":
    db = Database()
    print(db.get_all_nu())
