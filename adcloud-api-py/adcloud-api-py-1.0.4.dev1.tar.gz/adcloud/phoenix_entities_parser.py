#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey, Sequence, select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
sys.path.append("..")
from hive.executor import HiveExecutor
from meta.entities import (ADCEngine, ADCAggregateFunc,
                           ADCDatasource, ADCTable, ADCTableColumn, ADCDataset, ADCDatasetField, ADCDatasetRelationship, ADCMetricType,ADCExtentionMetric)
from phoenix.client import PhoenixClient
from ConfigParser import ConfigParser


def parse_precompute_config(path, keywords_mapping):
    config = ConfigParser()
    config.read(path)

    results = []
    for section in config.sections():
        if section.startswith('pre') and config.get(section, 'target_db').find('phoenix') >= 0 and section.find('adx') == -1 and section.find('publish') == -1:
            keywords = section.split('_')
            flag = True
            for idx, word in enumerate(keywords):
                if idx > 0 and keywords_mapping.has_key(word) == False:
                    flag = False
                    break

            if flag == True:
                for option in config.options(section):
                    if option.startswith('dims'):
                        dims = config.get(section, option).strip().split(',')
                        dim_titles = []
                        dim_keys = []
                        for dim in dims:
                            dim_keys.append(dim.replace('t1.', ''))
                            dim_titles.append(
                                keywords_mapping[dim.replace('t1.', '')]['title'])

                results.append((section, 'x'.join(dim_titles), dim_keys, config.get(
                    section, 'interval').strip().split(',')))
    return results


def build_table_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    adc_datasource = session.query(ADCDatasource).filter(
        ADCDatasource.name == '石家庄Phoenix数据源').one()

    parameters = eval(adc_datasource.settings)

    client = PhoenixClient(**parameters)

    dbs = client.show_databases()

    for index, pattern in enumerate(['ADWISE_%', 'DIM_AD_PS%','DIM_AD_CREATIVE']):
        for table in client.show_tables(table_pattern=pattern):
            table_info = client.desc_table(db_name=None, table_name=table)
            if table.find('ADX') == -1 and table.find('CONVERSION') == -1 and table.find('PUBLISH') == -1:
                if index == 0:
                    if table.find('HOUR') >= 0:
                        adc_table = ADCTable(
                            db=None, table_name=table.lower(), partitions="[('sdate', 'string'), ('hour', 'string')]")
                    else:
                        adc_table = ADCTable(
                            db=None, table_name=table.lower(), partitions="[('sdate', 'string')]")
                else:
                    adc_table = ADCTable(
                        db=None, table_name=table.lower(), partitions="[('dt', 'string')]")
                    
                adc_table.datasource = adc_datasource
                adc_table.columns = []
                for idx, col in enumerate(table_info['fields']):
                    adc_table.columns.append(ADCTableColumn(column_name=col['name'].lower(), column_title=col[
                                             'name'].lower(), data_type=col['type'].lower(), position_rank=idx))

                session.add(adc_table)
                session.commit()

    session.close()


def build_dataset_data(engine, precompute_structure, keywords_mapping):
    Session = sessionmaker(bind=engine)
    session = Session()

    for pre_table in precompute_structure:
        pre_table_name = pre_table[0]
        pre_table_title = pre_table[1]
        for interval in pre_table[3]:
            suffix = ''
            if interval == 'hour':
                suffix = '_HOUR'
            category = pre_table_title.split('x')[0]
            table_name = 'ADWISE_%s_DIM_RESULT%s' % (len(pre_table[2]), suffix)
            adc_table = session.query(ADCTable).filter(
                ADCTable.table_name == table_name.lower()).one()

            if interval=='hour':
                adc_dataset = ADCDataset(table=adc_table, init_condition="pre_table='%s'" % (
                    pre_table_name), category='%s相关分小时数据集' % (category), dataset_name='%s(每天,每小时)' %(pre_table_title), dataset_type='d')
            else:
                adc_dataset = ADCDataset(table=adc_table, init_condition="pre_table='%s'" % (
                    pre_table_name), category='%s相关数据集' % (category), dataset_name='%s(每天)' %(pre_table_title), dataset_type='d')

            for idx, dim in enumerate(pre_table[2]):
                for adc_table_column in adc_table.columns:
                    if adc_table_column.column_name.startswith('dim%s' % (idx + 1)):
                        adc_dataset.fields.append(ADCDatasetField(dataset=adc_dataset, table_column=adc_table_column,
                                                                  field_name=dim, field_type='d', field_title=keywords_mapping[dim]['title']))

            for adc_table_column in adc_table.columns:
                col_name = adc_table_column.column_name
                if col_name.lower() != 'pre_table' and col_name.startswith('dim') != True:

                    adc_dataset.fields.append(ADCDatasetField(dataset=adc_dataset, table_column=adc_table_column, field_name=col_name, field_type=keywords_mapping[
                                              col_name]['type'], field_title=keywords_mapping[col_name]['title'],metric_type_id=keywords_mapping[col_name]['metric_type_id']))

            session.add(adc_dataset)
            session.commit()

    dim_tables = session.query(ADCTable).filter(ADCTable.table_name.like('dim_%'))

    for adc_table in dim_tables:
        adc_table_name = ''
        for key, value in keywords_mapping.items():
            if adc_table.table_name.find(key.lower()) >= 0:
                adc_table_name = value['title']
                break

        adc_dataset = ADCDataset(table=adc_table, init_condition='', category='业务集',
                                 dataset_name='%s业务集' % (adc_table_name), dataset_type='b')

        dim_table_columns = session.query(ADCTableColumn).filter(
            ADCTableColumn.table == adc_table)
        for adc_table_column in dim_table_columns:
            adc_dataset.fields.append(ADCDatasetField(dataset=adc_dataset, table_column=adc_table_column,
                                                      field_name=adc_table_column.column_name, field_type='d', field_title=keywords_mapping[adc_table_column.column_title]['title']))

        session.add(adc_dataset)
        session.commit()

def init_field_relationship(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    adc_table=session.query(ADCTable).filter(ADCTable.table_name=='ADWISE_2_DIM_RESULT_HOUR'.lower()).one()

    adc_dataset=session.query(ADCDataset).filter(ADCDataset.table==adc_table,ADCDataset.dataset_name=='广告位x广告素材(每天,每小时)').one()

    adc_dataset_field=None
    data_campaign_field=None
    data_adpos_field=None
    data_display_num_field=None
    data_click_num_field=None
    data_lands_num_field=None

    fields=session.query(ADCDatasetField).filter(ADCDatasetField.dataset==adc_dataset)

    for adc_dataset_field in fields:
        if adc_dataset_field.field_name.lower()=='creative_id':
            data_creative_field=adc_dataset_field
        if adc_dataset_field.field_name.lower()=='adpos_id':
            data_adpos_field=adc_dataset_field
        if adc_dataset_field.field_name.lower()=='vis_display_num':
            data_display_num_field=adc_dataset_field
        if adc_dataset_field.field_name.lower()=='click_num':
            data_click_num_field=adc_dataset_field
        if adc_dataset_field.field_name.lower()=='lands_num':
            data_lands_num_field=adc_dataset_field


    dim_adpos_table=session.query(ADCTable).filter(ADCTable.table_name=='DIM_AD_PS'.lower()).one()
    dim_creative_table=session.query(ADCTable).filter(ADCTable.table_name=='DIM_AD_CREATIVE'.lower()).one()

    dim_adpos_dataset=session.query(ADCDataset).filter(ADCDataset.table==dim_adpos_table).one()
    dim_creative_dataset=session.query(ADCDataset).filter(ADCDataset.table==dim_creative_table).one()


    fields=session.query(ADCDatasetField).filter(ADCDatasetField.dataset==dim_creative_dataset)

    adc_dataset_field=None
    for adc_dataset_field in fields:
        if adc_dataset_field.field_name.lower()=='creative_id':
            break

    if adc_dataset_field:
        session.add(ADCDatasetRelationship(primary_dataset=dim_creative_dataset,primary_field=adc_dataset_field,foreign_dataset=adc_dataset,foreign_field=data_creative_field))
        session.commit()

    fields=session.query(ADCDatasetField).filter(ADCDatasetField.dataset==dim_adpos_dataset)

    adc_dataset_field=None
    for adc_dataset_field in fields:
         if adc_dataset_field.field_name.lower()=='adpos_id':
            break

    if adc_dataset_field:
        session.add(ADCDatasetRelationship(primary_dataset=dim_adpos_dataset,primary_field=adc_dataset_field,foreign_dataset=adc_dataset,foreign_field=data_adpos_field))
        session.commit()

    if data_display_num_field and data_click_num_field:
        session.add(ADCExtentionMetric(dataset=adc_dataset,metric_name='CTR',metric_title='点击率(CTR)',metric_type_id=3,expression='${%s}*1000/${%s}' %(data_click_num_field.id,data_display_num_field.id)))

    if data_lands_num_field and data_click_num_field:
        session.add(ADCExtentionMetric(dataset=adc_dataset,metric_name='CVR',metric_title='线索转化率(CVR)',metric_type_id=3,expression='${%s}*100/${%s}' %(data_lands_num_field.id,data_click_num_field.id)))

    session.commit()

def init_base_data(engine):

    Session = sessionmaker(bind=engine)

    session = Session()

    clear_tables = ['adc_dataset', 'adc_table',
                    'adc_table_column', 'adc_dataset_field', 'adc_dataset_relationship',
                    'adc_aggregate_func', 'adc_engine', 'adc_datasource', 'adc_metric_type','adc_extention_metric']

    engine.execute('SET foreign_key_checks=0;')
    for table in clear_tables:
        engine.execute('truncate table adcloud.%s' % (table))

    engine.execute('SET foreign_key_checks=1;')


    # init adc_engine and adc_aggregate_func data
    adc_engine = ADCEngine(engine_name='phoenix',
                           engine_title='Phoenix引擎', desc='')
    adc_engine.agg_functions = [
        ADCAggregateFunc(func_name='sum', func_title='sum'),
        ADCAggregateFunc(func_name='avg', func_title='avg'),
        ADCAggregateFunc(func_name='max', func_title='max'),
        ADCAggregateFunc(func_name='min', func_title='min'),
    ]

    adc_engine.datasources = [
        ADCDatasource(name='石家庄Phoenix数据源',
                      settings="{'url':'http://192.168.223.199:8765/?v=1.6','max_retries':3,'readOnly':False}")
    ]

    session.add(adc_engine)

    adc_engine = ADCEngine(
        engine_name='hive', engine_title='Hive存储引擎', desc='')

    adc_engine.agg_functions = [
        ADCAggregateFunc(func_name='sum', func_title='sum'),
        ADCAggregateFunc(func_name='avg', func_title='avg'),
        ADCAggregateFunc(func_name='max', func_title='max'),
        ADCAggregateFunc(func_name='min', func_title='min'),
    ]

    adc_engine.datasources = [
        ADCDatasource(name='石家庄Hive数据源',
                      settings="{'hive_cmd_path':'hive','verbose':False,'hive_init_settings':['set mapred.job.queue.name=q_guanggao.q_adlog']}")
    ]

    session.add(adc_engine)
    adc_engine = ADCEngine(engine_name='pipelinedb',
                           engine_title='PipelineDB存储引擎', desc='')
    adc_engine.agg_functions = [
        ADCAggregateFunc(func_name='sum', func_title='sum'),
        ADCAggregateFunc(func_name='avg', func_title='avg'),
        ADCAggregateFunc(func_name='max', func_title='max'),
        ADCAggregateFunc(func_name='min', func_title='min'),
    ]

    adc_engine.datasources = [
        ADCDatasource(name='PipelineDB数据源',
                      settings="{'dbname':'pipeline','user':'pipeline','host':'192.168.223.154','port':5888}")
    ]

    session.add(adc_engine)

    adc_metric_type = ADCMetricType(type_name='流量指标', desc='流量指标')
    session.add(adc_metric_type)

    adc_metric_type = ADCMetricType(type_name='销售指标', desc='销售指标')
    session.add(adc_metric_type)

    adc_metric_type = ADCMetricType(type_name='转化指标', desc='转化指标')
    session.add(adc_metric_type)

    adc_metric_type = ADCMetricType(type_name='计算指标', desc='计算指标')
    session.add(adc_metric_type)

    session.commit()


if __name__ == '__main__':

    keywords_mapping = {'sdate': {'title': '日期', 'type': 'd','metric_type_id':None},
                        'hour': {'title': '小时', 'type': 'd','metric_type_id':None},
                        'adpos': {'title': '广告位', 'type': 'd','metric_type_id':None},
                        'advert': {'title': '广告类型', 'type': 'd','metric_type_id':None},
                        'browser': {'title': '浏览器', 'type': 'd','metric_type_id':None},
                        'campaign': {'title': '广告计划', 'type': 'd','metric_type_id':None},
                        'carousel': {'title': '轮播号', 'type': 'd','metric_type_id':None},
                        'contract': {'title': '合同号', 'type': 'd','metric_type_id':None},
                        'creative': {'title': '广告素材', 'type': 'd','metric_type_id':None},
                        'group': {'title': '广告组', 'type': 'd','metric_type_id':None},
                        'groupadpos': {'title': '广告位组', 'type': 'd','metric_type_id':None},
                        'plat_from': {'title': '平台', 'type': 'd','metric_type_id':None},
                        'oplatform': {'title': '平台', 'type': 'd','metric_type_id':None},
                        'order': {'title': '订单', 'type': 'd','metric_type_id':None},
                        'ordertype': {'title': '订单类型', 'type': 'd','metric_type_id':None},
                        'platform': {'title': '平台', 'type': 'd','metric_type_id':None},
                        'purpose': {'title': '投放目的', 'type': 'd','metric_type_id':None},
                        'region': {'title': '投放地域', 'type': 'd','metric_type_id':None},
                        'sellmode': {'title': '计费方式', 'type': 'd','metric_type_id':None},
                        'adpos_id': {'title': '广告位', 'type': 'd','metric_type_id':None},
                        'ps': {'title': '广告位', 'type': 'd','metric_type_id':None},
                        'advert_type': {'title': '广告类型', 'type': 'd','metric_type_id':None},
                        'campaign_id': {'title': '广告计划', 'type': 'd','metric_type_id':None},
                        'carousel_id': {'title': '轮播号', 'type': 'd','metric_type_id':None},
                        'contract_id': {'title': '合同', 'type': 'd','metric_type_id':None},
                        'contract_no': {'title': '合同号', 'type': 'd','metric_type_id':None},
                        'creative_id': {'title': '广告素材', 'type': 'd','metric_type_id':None},
                        'group_id': {'title': '广告组', 'type': 'd','metric_type_id':None},
                        'adpos_group_id': {'title': '广告位组', 'type': 'd','metric_type_id':None},
                        'platform_id': {'title': '平台', 'type': 'd','metric_type_id':None},
                        'order_id': {'title': '订单', 'type': 'd','metric_type_id':None},
                        'order_type': {'title': '订单类型', 'type': 'd','metric_type_id':None},
                        'platform_id': {'title': '平台', 'type': 'd','metric_type_id':None},
                        'purpose_id': {'title': '投放用途', 'type': 'd','metric_type_id':None},
                        'billing_id': {'title': '计费方式', 'type': 'd','metric_type_id':None},
                        'req_num': {'title': '请求量', 'type': 'm','metric_type_id':1},
                        'imp_filter_pv': {'title': '展现过滤PV', 'type': 'm','metric_type_id':1},
                        'click_filter_pv': {'title': '点击过滤PV', 'type': 'm','metric_type_id':1},
                        'imp_num': {'title': '曝光量', 'type': 'm','metric_type_id':1},
                        'vis_req_num': {'title': '可见请求量', 'type': 'm','metric_type_id':1},
                        'vis_imp_num': {'title': '可见曝光量', 'type': 'm','metric_type_id':1},
                        'vis_display_num': {'title': '可见展现', 'type': 'm','metric_type_id':1},
                        'click_num': {'title': '点击量', 'type': 'm','metric_type_id':1},
                        'lands_num': {'title': '线索量', 'type': 'm','metric_type_id':1},
                        'req_num': {'title': '请求UV', 'type': 'm','metric_type_id':1},
                        'imp_uv': {'title': '曝光UV', 'type': 'm','metric_type_id':1},
                        'imp_login_uv': {'title': '曝光会员数', 'type': 'm','metric_type_id':1},
                        'req_uv': {'title': '请求UV', 'type': 'm','metric_type_id':1},
                        'vis_req_uv': {'title': '可见请求UV', 'type': 'm','metric_type_id':1},
                        'vis_imp_uv': {'title': '可见曝光UV', 'type': 'm','metric_type_id':1},
                        'vis_imp_login_uv': {'title': '可见曝光会员数', 'type': 'm','metric_type_id':1},
                        'lands_uv': {'title': '线索UV', 'type': 'm','metric_type_id':1},
                        'click_uv': {'title': '点击UV', 'type': 'm','metric_type_id':1},
                        'lands_login_uv': {'title': '线索会员数', 'type': 'm','metric_type_id':1},
                        'order_type': {'title': '订单类型', 'type': 'd','metric_type_id':None},
                        'order_name': {'title': '订单名称', 'type': 'd','metric_type_id':None},
                        'advert_type': {'title': '广告类型', 'type': 'd','metric_type_id':None},
                        'group_id': {'title': '广告素材组ID', 'type': 'd','metric_type_id':None},
                        'group_name': {'title': '广告素材组名称', 'type': 'd','metric_type_id':None},
                        'adpos_name': {'title': '广告位名称', 'type': 'd','metric_type_id':None},
                        'channelsecond': {'title': '广告位所属二级频道', 'type': 'd','metric_type_id':None},
                        'channelsecond_id': {'title': '广告位所属二级频道ID', 'type': 'd','metric_type_id':None},
                        'page': {'title': '广告位所属页面', 'type': 'd','metric_type_id':None},
                        'page_id': {'title': '广告位所属页面ID', 'type': 'd','metric_type_id':None},
                        'channelfirst': {'title': '广告位所属一级频道', 'type': 'd','metric_type_id':None},
                        'channelfirst_id': {'title': '广告位所属一级频道ID', 'type': 'd','metric_type_id':None},
                        'website': {'title': '广告位所属站点', 'type': 'd','metric_type_id':None},
                        'website_id': {'title': '广告位所属站点ID', 'type': 'd','metric_type_id':None},
                        'group_adpos_id': {'title': '广告位组', 'type': 'd','metric_type_id':None},
                        'group_adpos_name': {'title': '广告位组名称', 'type': 'd','metric_type_id':None},
                        'customer_name': {'title': '合同名称', 'type': 'd','metric_type_id':None},
                        'sell_mode_name': {'title': '计费方式', 'type': 'd','metric_type_id':None},
                        'campaign_name': {'title': '计划名称', 'type': 'd','metric_type_id':None},
                        'company_name': {'title': '签约公司名称', 'type': 'd','metric_type_id':None},
                        'purpose_name': {'title': '投放目的', 'type': 'd','metric_type_id':None},
                        'facility': {'title': '投放设备', 'type': 'd','metric_type_id':None},
                        'sales_man_name': {'title': '业务员名称', 'type': 'd','metric_type_id':None},
                        }

    connect_url = 'mysql://autoax:autoax@10.168.100.50:3306/adcloud?charset=utf8'
    connect_url = 'mysql://root:ad_tj2016@192.168.223.154:3306/adcloud?charset=utf8'
    engine = create_engine(connect_url, encoding="utf-8", echo=True)

   
    init_base_data(engine)

    precompute_config = '../../../adlogx/precompute/config.cfg'
    results = parse_precompute_config(precompute_config, keywords_mapping)
    build_table_data(engine)
    build_dataset_data(engine, results, keywords_mapping)

    init_field_relationship(engine)
