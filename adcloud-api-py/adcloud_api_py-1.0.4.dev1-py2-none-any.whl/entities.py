#! /usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey, Sequence,select
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


#create database adcloud DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

Base = declarative_base()

class ADCEngine(Base):
    __tablename__="adc_engine"

    id=Column(Integer,primary_key=True)
    engine_name=Column(String(30),unique=True)
    engine_title=Column(String(40))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)


class ADCAggregateFunc(Base):
    __tablename__="adc_aggregate_func"

    id=Column(Integer,primary_key=True)
    engine_id=Column(Integer,ForeignKey('adc_engine.id'))
    func_name=Column(String(30))
    func_title=Column(String(50))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    adc_engine=relationship("ADCEngine",back_populates="agg_functions")


ADCEngine.agg_functions = relationship("ADCAggregateFunc", order_by=ADCAggregateFunc.id, back_populates="adc_engine")

class ADCMetricType(Base):
    __tablename__="adc_metric_type"

    id=Column(Integer,primary_key=True)
    type_name=Column(String(30))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

class ADCDatasource(Base):
    __tablename__="adc_datasource"
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    engine_id=Column(Integer,ForeignKey('adc_engine.id'))
    settings=Column(String(300))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    adc_engine=relationship("ADCEngine",back_populates="datasources")


ADCEngine.datasources = relationship("ADCDatasource", order_by=ADCDatasource.id, back_populates="adc_engine")


class ADCTable(Base):
    __tablename__="adc_table"
    id=Column(Integer,primary_key=True)
    datasource_id=Column(Integer,ForeignKey("adc_datasource.id"))
    db=Column(String(30))
    table_name=Column(String(50))
    partitions=Column(String(50))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    datasource=relationship("ADCDatasource",back_populates="tables")

ADCDatasource.tables=relationship("ADCTable",order_by=ADCTable.id,back_populates="datasource")

class ADCTableColumn(Base):
    __tablename__="adc_table_column"
    id=Column(Integer,primary_key=True)
    table_id=Column(Integer,ForeignKey("adc_table.id"))
    column_name=Column(String(30))
    column_title=Column(String(30))
    data_type=Column(String(30))
    comment=Column(String(100))
    position_rank=Column(Integer)
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    table=relationship("ADCTable",back_populates="columns")

ADCTable.columns=relationship("ADCTableColumn",order_by=ADCTableColumn.id,back_populates="table")


class ADCDataset(Base):
    __tablename__="adc_dataset"
    id=Column(Integer,primary_key=True)
    table_id=Column(Integer,ForeignKey("adc_table.id"))
    init_condition=Column(String(100))
    category=Column(String(50))
    dataset_name=Column(String(50))
    dataset_type=Column(String(5))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    table=relationship("ADCTable",back_populates="datasets")

ADCTable.datasets=relationship("ADCDataset",order_by=ADCDataset.id,back_populates="table")

class ADCDatasetField(Base):
    __tablename__="adc_dataset_field"
    id=Column(Integer,primary_key=True)
    dataset_id=Column(Integer,ForeignKey("adc_dataset.id"))
    column_id=Column(Integer,ForeignKey("adc_table_column.id"))
    field_name=Column(String(30))
    field_title=Column(String(30))
    field_type=Column(String(5))
    metric_type_id=Column(Integer,ForeignKey("adc_metric_type.id"))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    dataset=relationship("ADCDataset",back_populates="fields")
    table_column=relationship("ADCTableColumn",back_populates="fields")

    metric_type=relationship("ADCMetricType")

ADCDataset.fields=relationship("ADCDatasetField",order_by=ADCDatasetField.id,back_populates="dataset")
ADCTableColumn.fields=relationship("ADCDatasetField",order_by=ADCDatasetField.id,back_populates="table_column")

class ADCDatasetRelationship(Base):
    __tablename__="adc_dataset_relationship"
    id=Column(Integer,primary_key=True)
    primary_dataset_id=Column(Integer,ForeignKey("adc_dataset.id"))
    primary_field_id=Column(Integer,ForeignKey("adc_dataset_field.id"))
    foreign_dataset_id=Column(Integer,ForeignKey("adc_dataset.id"))
    foreign_field_id=Column(Integer,ForeignKey("adc_dataset_field.id"))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    primary_dataset=relationship("ADCDataset",foreign_keys="ADCDatasetRelationship.primary_dataset_id")
    foreign_dataset=relationship("ADCDataset",foreign_keys="ADCDatasetRelationship.foreign_dataset_id")

    primary_field=relationship("ADCDatasetField",foreign_keys="ADCDatasetRelationship.primary_field_id")
    foreign_field=relationship("ADCDatasetField",foreign_keys="ADCDatasetRelationship.foreign_field_id")


class ADCExtentionMetric(Base):
    __tablename__="adc_extention_metric"
    id=Column(Integer,primary_key=True)
    dataset_id=Column(Integer,ForeignKey("adc_dataset.id"))
    metric_name=Column(String(30))
    metric_title=Column(String(30))
    expression=Column(String(50))
    metric_type_id=Column(Integer,ForeignKey("adc_metric_type.id"))
    desc=Column(String(100))
    status=Column(Integer,default=1)
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

    dataset=relationship("ADCDataset",back_populates="extention_metrics")
    metric_type=relationship("ADCMetricType")

ADCDataset.extention_metrics=relationship("ADCExtentionMetric",order_by=ADCExtentionMetric.id,back_populates="dataset")

class ADCUserLogs(Base):
    __tablename__="adc_user_logs"
    id=Column(Integer,primary_key=True)
    job_id=Column(String(30))
    level=Column(String(10))
    log_type=Column(String(30))
    user=Column(String(30))
    host=Column(String(30))
    message=Column(String(2000))
    modify_time=Column(DateTime,default=datetime.now, onupdate=datetime.now)

def init_table_structure(engine):

    engine.execute('DROP DATABASE if exists adcloud;')
    engine.execute('create database adcloud DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;')
    engine.execute('use adcloud;')

    Base.metadata.create_all(engine)


if __name__=="__main__":

    connect_url='mysql://autoax:autoax@10.168.100.50:3306/adcloud?charset=utf8'
    connect_url='mysql://root:ad_tj2016@192.168.223.154:3306/adcloud?charset=utf8'
    engine = create_engine(connect_url, encoding="utf-8", echo=True)

    init_table_structure(engine)



