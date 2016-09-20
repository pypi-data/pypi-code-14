#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey, Sequence, select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from hive import HiveExecutor
from meta.entities import (ADCEngine, ADCAggregateFunc,
                           ADCDatasource, ADCTable, ADCTableColumn, ADCDataset, ADCDatasetField, ADCDatasetRelationship, ADCMetricType,ADCExtentionMetric)

from ConfigParser import ConfigParser


def build_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    adc_datasource = session.query(ADCDatasource).filter(
        ADCDatasource.name == '石家庄Hive数据源').one()

    #init table and columns data
    phoenix_datasource=session.query(ADCDatasource).filter(ADCDatasource.name == '石家庄Phoenix数据源').one()

    phoenix_tables=session.query(ADCTable).filter(ADCTable.datasource==phoenix_datasource)

    for table in phoenix_tables:
        if table.table_name.startswith('dim_'):
            adc_table = ADCTable(datasource=adc_datasource,db='ad', table_name=table.table_name, partitions="[('dt', 'string')]")
        else:
            adc_table = ADCTable(datasource=adc_datasource,db='ad', table_name=table.table_name, partitions=table.partitions)

        phoenix_table_columns=session.query(ADCTableColumn).filter(ADCTableColumn.table==table)
        for column in phoenix_table_columns:
            adc_table.columns.append(ADCTableColumn(column_name=column.column_name, column_title=column.column_title, data_type=column.data_type, position_rank=column.position_rank))
        session.add(adc_table)

        phoenix_datasets=session.query(ADCDataset).filter(ADCDataset.table==table)
        for dataset in table.datasets:
            adc_dataset=ADCDataset(table=adc_table, init_condition=dataset.init_condition, category=dataset.category,dataset_name=dataset.dataset_name,dataset_type=dataset.dataset_type)
        session.add(adc_dataset)

    session.commit()

    #init dataset fields data
    for table in phoenix_tables:
        adc_table=session.query(ADCTable).filter(ADCTable.table_name==table.table_name,ADCTable.datasource==adc_datasource).one()
        for dataset in table.datasets:
            adc_dataset=session.query(ADCDataset).filter(ADCDataset.table==adc_table,ADCDataset.dataset_name==dataset.dataset_name).one()
            for field in dataset.fields:
                adc_table_column=session.query(ADCTableColumn).filter(ADCTableColumn.table==adc_table,ADCTableColumn.column_name==field.table_column.column_name).one()
                session.add(ADCDatasetField(dataset=adc_dataset, table_column=adc_table_column,
                                                                  field_name=field.field_name, field_type=field.field_type, field_title=field.field_title))

    session.commit()

    #init dataset relationships data
    phoenix_relationships=session.query(ADCDatasetRelationship)

    for relation in phoenix_relationships:
        if relation.foreign_dataset.table.datasource==phoenix_datasource:

            adc_foreign_datasets=session.query(ADCDataset).filter(ADCDataset.dataset_name==relation.foreign_dataset.dataset_name);

            adc_foreign_dataset=None
            for adc_foreign_dataset in adc_foreign_datasets:
                if adc_foreign_dataset.table.datasource==adc_datasource:
                    break;

            adc_foreign_field=session.query(ADCDatasetField).filter(ADCDatasetField.dataset==adc_foreign_dataset,ADCDatasetField.field_name==relation.foreign_field.field_name).one()

            adc_primary_datasets=session.query(ADCDataset).filter(ADCDataset.dataset_name==relation.primary_dataset.dataset_name)
            adc_primary_dataset=None
            for adc_primary_dataset in adc_primary_datasets:
                if adc_primary_dataset.table.datasource==adc_datasource:
                    break;


            adc_primary_field=session.query(ADCDatasetField).filter(ADCDatasetField.dataset==adc_primary_dataset,ADCDatasetField.field_name==relation.primary_field.field_name).one()

            session.add(ADCDatasetRelationship(primary_dataset=adc_primary_dataset,primary_field=adc_primary_field,foreign_dataset=adc_foreign_dataset,foreign_field=adc_foreign_field))


    session.commit()


    session.close()


if __name__ == '__main__':


    connect_url = 'mysql://autoax:autoax@10.168.100.50:3306/adcloud?charset=utf8'
    connect_url = 'mysql://root:ad_tj2016@192.168.223.154:3306/adcloud?charset=utf8'
    engine = create_engine(connect_url, encoding="utf-8", echo=True)

    build_data(engine)

