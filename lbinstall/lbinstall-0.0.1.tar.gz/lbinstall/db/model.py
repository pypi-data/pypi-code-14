'''
Created on 9 Aug 2016

@author: Ben Couturier
'''

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
#from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()


class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    version = Column(String(250), nullable=False)
    release = Column(String(250), nullable=False)
    checksum = Column(String(250), nullable=True)
    checksum_type = Column(String(50), nullable=True)
    group = Column(String(250), nullable=False)
    location = Column(String(1000), nullable=True)
    relocatedLocation = Column(String(1000), nullable=True)
    postinstallrun = Column(String(1), nullable=True)
    UniqueConstraint('name', 'version', name='PackageDuplication') 
    
class Require(Base):
    __tablename__ = 'require'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    version = Column(String(250), nullable = True)
    release = Column(String(250), nullable = True)
    flags = Column(String(250), nullable=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    package = relationship(Package, backref="requires")

class Provide(Base):
    __tablename__ = 'provide'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    version = Column(String(250))
    release = Column(String(250), nullable = True)
    flags = Column(String(250), nullable=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    package = relationship(Package, backref="provides")


