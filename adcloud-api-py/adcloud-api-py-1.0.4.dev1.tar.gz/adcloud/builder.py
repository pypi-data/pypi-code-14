#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import logging
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hive import HiveExecutor
from phoenix.client import PhoenixClient
from pipelinedb.client import PipelineDBClient

_logger = logging.getLogger(__name__)

class SQLSessionBuilder(object):

    def __init__(self, **kwargs):
        self.db_connect_url = kwargs['db_connect_url']

        if kwargs.has_key('db_encoding'):
            self.db_encoding = kwargs['db_encoding']
        else:
            self.db_encoding = "utf-8"

        if kwargs.has_key('db_echo_switch'):
            self.db_echo_swith = kwargs['db_echo_switch']
        else:
            self.db_echo_switch = False

        self._db_engine = create_engine(
            self.db_connect_url, encoding=self.db_encoding, echo=self.db_echo_switch)
        self._session = None

    def getSession(self):
        if not self._session:
            Session = sessionmaker(bind=self._db_engine)
            self._session = Session()

        return self._session


class DefaultExecutor(object):

    def __init__(self,api_settings, **kwargs):
        self._api_settings=api_settings

    def _build_sql(self):        
        sql="select"
        final_query_fields=[]
        final_aggr_fields=[]
        query_fields=[]
        group_fields=[]
        foreign_fields=[]
        required_foreign_fields=[]
        required_primary_fields=[]
        required_primary_relations={}
        filter=None
        if self._api_settings.api_config['filter']:
            filter=self._api_settings.api_config['filter']
        for field in self._api_settings.fields:
            if field.dataset==self._api_settings.adc_dataset:
                required_foreign_fields.append(field)
                if filter:
                    filter=filter.replace(field.field_name,field.table_column.column_name)
            else:
                required_primary_fields.append(field)
                for relation in self._api_settings.dataset_relations:
                    if relation.primary_dataset==field.dataset:
                        foreign_fields.append(relation.foreign_field)
                        required_primary_relations[field.dataset]={"foreign_field":relation.foreign_field,"primary_field":relation.primary_field}

        if self._api_settings.adc_dataset.init_condition:
            if filter:
                filter="%s and %s" %(self._api_settings.adc_dataset.init_condition,filter)
            else:
                filter="%s" %(self._api_settings.adc_dataset.init_condition)

        for field in foreign_fields:
            if field not in required_foreign_fields:
                required_foreign_fields.append(field)
                #query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))

        for field in required_foreign_fields:
            query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))
            if len(self._api_settings.groups)>0:
                group_fields.append(field.table_column.column_name)

        for field,aggr_func in self._api_settings.aggregates:
            query_fields.append(" %s(%s) as %s" %(aggr_func,field.table_column.column_name,field.field_name))
            if len(required_primary_fields)>0:
                final_aggr_fields.append(field.field_name)

        sql=sql+",".join(query_fields)+"\n"

        if self._api_settings.adc_dataset.table.db:
            sql=sql+"from %s.%s" %(self._api_settings.adc_dataset.table.db,self._api_settings.adc_dataset.table.table_name)
        else:
            sql=sql+"from %s" %(self._api_settings.adc_dataset.table.table_name)

        sql=sql+"\n"

        if filter:
            sql=sql+"where %s" %(filter)

        if len(self._api_settings.groups)>0:
            sql=sql+"\n"
            sql=sql+"group by %s" %(",".join(group_fields))

    
        if len(required_primary_fields)>0:
            for field in self._api_settings.fields:
                final_query_fields.append("t%s.%s" %(field.dataset.id,field.field_name))
            
            sql="(\n"+sql+"\n) t%s" %(self._api_settings.adc_dataset.id)
            sql="select %s \nfrom\n%s" %(",".join(final_query_fields+final_aggr_fields),sql)

            for primary_dataset,relation in required_primary_relations.items():
                sql=sql+"\ninner join \n"
                if primary_dataset.table.db:
                    sql=sql+"%s.%s t%s" %(primary_dataset.table.db,primary_dataset.table.table_name,primary_dataset.id)
                else:
                    sql=sql+"%s t%s" %(primary_dataset.table.table_name,primary_dataset.id)

                sql=sql+"\n"

                foreign_field_data_type=relation['foreign_field'].table_column.data_type.lower()
                primary_field_data_type=relation['primary_field'].table_column.data_type.lower()

                if foreign_field_data_type.find("char")>=0 and primary_field_data_type.find("char")==-1:
                    sql=sql+"on t%s.%s=to_char(t%s.%s)" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)
                elif foreign_field_data_type.find("char")==-1 and primary_field_data_type.find("char")>=0:
                    sql=sql+"on to_char(t%s.%s)=t%s.%s" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)
                else:
                    sql=sql+"on t%s.%s=t%s.%s" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)


        if len(self._api_settings.sorts)>0:
            sql=sql+"\n"
            sorts=[]
            for field,sort_type in self._api_settings.sorts:
                if len(required_primary_relations)>0:
                    sorts.append("t%s.%s %s" %(field.dataset.id,field.field_name,sort_type))
                else:
                    sorts.append("%s %s" %(field.field_name,sort_type))

            sql=sql+"order by %s" %(",".join(sorts))

        if self._api_settings.limits:
            sql=sql+"\n"
            sql=sql+"limit %s" %(self._api_settings.limits)

        return sql

class PhoenixClientExecutor(DefaultExecutor):

    def __init__(self,api_settings, **kwargs):
        super(PhoenixClientExecutor,self).__init__(api_settings,**kwargs)
        self.client=PhoenixClient(**self._api_settings.datasource_settings)
        self.sql=self._build_sql()
        

    def execute(self):
        self._result_generator=self.client.fetch(self.sql)
        return self._result_generator

    def executeAndSave(self,path):
        self._result_generator=self.client.fetch(self.sql)
        if self._result_generator:
            with open(path,"w") as file:
                for row in self._result_generator:
                    file.write("%s\n" %(",".join(row)))


    def _build_sql(self):
        sql="select"
        final_query_fields=[]
        final_aggr_fields=[]
        query_fields=[]
        group_fields=[]
        foreign_fields=[]
        required_foreign_fields=[]
        required_primary_fields=[]
        required_primary_relations={}
        filter=None
        if self._api_settings.api_config['filter']:
            filter=self._api_settings.api_config['filter']
        for field in self._api_settings.fields:
            if field.dataset==self._api_settings.adc_dataset:
                required_foreign_fields.append(field)
                if filter:
                    filter=filter.replace(field.field_name,field.table_column.column_name)
            else:
                required_primary_fields.append(field)
                for relation in self._api_settings.dataset_relations:
                    if relation.primary_dataset==field.dataset:
                        foreign_fields.append(relation.foreign_field)
                        required_primary_relations[field.dataset]={"foreign_field":relation.foreign_field,"primary_field":relation.primary_field}

        if self._api_settings.adc_dataset.init_condition:
            if filter:
                filter="%s and %s" %(self._api_settings.adc_dataset.init_condition,filter)
            else:
                filter="%s" %(self._api_settings.adc_dataset.init_condition)

        for field in foreign_fields:
            if field not in required_foreign_fields:
                required_foreign_fields.append(field)
                #query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))

        for field in required_foreign_fields:
            query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))
            if len(self._api_settings.groups)>0:
                group_fields.append(field.table_column.column_name)

        for field,aggr_func in self._api_settings.aggregates:
            query_fields.append(" %s(%s) as %s" %(aggr_func,field.table_column.column_name,field.field_name))
            if len(required_primary_fields)>0:
                final_aggr_fields.append(field.field_name)

        sql=sql+",".join(query_fields)+"\n"

        if self._api_settings.adc_dataset.table.db:
            sql=sql+"from %s.%s" %(self._api_settings.adc_dataset.table.db,self._api_settings.adc_dataset.table.table_name)
        else:
            sql=sql+"from %s" %(self._api_settings.adc_dataset.table.table_name)

        sql=sql+"\n"

        if filter:
            sql=sql+"where %s" %(filter)

        if len(self._api_settings.groups)>0:
            sql=sql+"\n"
            sql=sql+"group by %s" %(",".join(group_fields))


        if len(required_primary_fields)>0:
            for field in self._api_settings.fields:
                final_query_fields.append("t%s.%s" %(field.dataset.id,field.field_name))
            
            sql="(\n"+sql+"\n) t%s" %(self._api_settings.adc_dataset.id)
            sql="select %s \nfrom\n%s" %(",".join(final_query_fields+final_aggr_fields),sql)

            for primary_dataset,relation in required_primary_relations.items():
                sql=sql+"\ninner join \n"
                if primary_dataset.table.db:
                    sql=sql+"%s.%s t%s" %(primary_dataset.table.db,primary_dataset.table.table_name,primary_dataset.id)
                else:
                    sql=sql+"%s t%s" %(primary_dataset.table.table_name,primary_dataset.id)

                sql=sql+"\n"

                foreign_field_data_type=relation['foreign_field'].table_column.data_type.lower()
                primary_field_data_type=relation['primary_field'].table_column.data_type.lower()

                if foreign_field_data_type.find("char")>=0 and primary_field_data_type.find("char")==-1:
                    sql=sql+"on t%s.%s=to_char(t%s.%s)" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)
                elif foreign_field_data_type.find("char")==-1 and primary_field_data_type.find("char")>=0:
                    sql=sql+"on to_char(t%s.%s)=t%s.%s" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)
                else:
                    sql=sql+"on t%s.%s=t%s.%s" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)


        if len(self._api_settings.sorts)>0:
            sql=sql+"\n"
            sorts=[]
            for field,sort_type in self._api_settings.sorts:
                if len(required_primary_relations)>0:
                    sorts.append("t%s.%s %s" %(field.dataset.id,field.field_name,sort_type))
                else:
                    sorts.append("%s %s" %(field.field_name,sort_type))

            sql=sql+"order by %s" %(",".join(sorts))

        if self._api_settings.limits:
            sql=sql+"\n"
            sql=sql+"limit %s" %(self._api_settings.limits)

        return sql


class PipelineDBClientExecutor(DefaultExecutor):

    def __init__(self,api_settings, **kwargs):
        super(PipelineDBClientExecutor,self).__init__(api_settings,**kwargs)


class HiveClientExecutor(DefaultExecutor):

    def __init__(self,api_settings, **kwargs):
        super(HiveClientExecutor,self).__init__(api_settings,**kwargs)
        self.client=HiveExecutor(**self._api_settings.datasource_settings)
        self.sql=self._build_sql()
        

    def execute(self):
        cr=self.client.execute(sql=self.sql)
        return (row.split('\t') for row in cr.stdout_text.split("\n"))


    def executeAndSave(self,path):
        self.client.execute(sql=self.sql,output_file=path)

    def _build_partition_filter(self,dataset):
        partition_filter=None

        if dataset.dataset_type=='b':
            last_partition=self.client.last_partitions(dataset.table.db,dataset.table.table_name)
            partition_info=self.client.desc_table(dataset.table.db,dataset.table.table_name)

            if partition_info.has_key('partitions'):
                partition_info['partitions']
                if last_partition and len(last_partition)>0:
                    column_name=partition_info['partitions'][0][0]
                    column_type=partition_info['partitions'][0][1]

                    if column_name and column_type:
                        if column_type in ['tinyint','smallint','int','bigint','float','double','decimal']:
                            partition_filter="%s=%s" %(column_name,last_partition[column_name])
                        else:
                            partition_filter="%s='%s'" %(column_name,last_partition[column_name])
        return partition_filter


    def _build_sql(self):
        sql="select"
        final_query_fields=[]
        final_aggr_fields=[]
        query_fields=[]
        group_fields=[]
        foreign_fields=[]
        required_foreign_fields=[]
        required_primary_fields=[]
        required_primary_relations={}
        filter=None
        if self._api_settings.api_config['filter']:
            filter=self._api_settings.api_config['filter']
        for field in self._api_settings.fields:
            if field.dataset==self._api_settings.adc_dataset:
                required_foreign_fields.append(field)
                if filter:
                    filter=filter.replace(field.field_name,field.table_column.column_name)
            else:
                required_primary_fields.append(field)
                for relation in self._api_settings.dataset_relations:
                    if relation.primary_dataset==field.dataset:
                        foreign_fields.append(relation.foreign_field)
                        required_primary_relations[field.dataset]={"foreign_field":relation.foreign_field,"primary_field":relation.primary_field}

        if self._api_settings.adc_dataset.init_condition:
            if filter:
                filter="%s and %s" %(self._api_settings.adc_dataset.init_condition,filter)
            else:
                filter="%s" %(self._api_settings.adc_dataset.init_condition)

        for field in foreign_fields:
            if field not in required_foreign_fields:
                required_foreign_fields.append(field)
                #query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))

        for field in required_foreign_fields:
            query_fields.append(" %s as %s" %(field.table_column.column_name,field.field_name))
            if len(self._api_settings.groups)>0:
                group_fields.append(field.table_column.column_name)

        for field,aggr_func in self._api_settings.aggregates:
            query_fields.append(" %s(%s) as %s" %(aggr_func,field.table_column.column_name,field.field_name))
            if len(required_primary_fields)>0:
                final_aggr_fields.append(field.field_name)

        sql=sql+",".join(query_fields)+"\n"

        sql=sql+"from %s.%s" %(self._api_settings.adc_dataset.table.db,self._api_settings.adc_dataset.table.table_name)

        sql=sql+"\n"

        partition_filter=self._build_partition_filter(self._api_settings.adc_dataset)

        if filter:
            if partition_filter:
                sql=sql+"where %s and %s" %(partition_filter,filter)
            else:
                sql=sql+"where %s" %(filter)

        if len(self._api_settings.groups)>0:
            sql=sql+"\n"
            sql=sql+"group by %s" %(",".join(group_fields))


        if len(required_primary_fields)>0:
            for field in self._api_settings.fields:
                final_query_fields.append("t%s.%s" %(field.dataset.id,field.field_name))
            
            sql="(\n"+sql+"\n) t%s" %(self._api_settings.adc_dataset.id)
            sql="select %s \nfrom\n%s" %(",".join(final_query_fields+final_aggr_fields),sql)

            for primary_dataset,relation in required_primary_relations.items():

                sql=sql+"\ninner join \n"
                if primary_dataset.table.db:
                    sql=sql+"%s.%s t%s" %(primary_dataset.table.db,primary_dataset.table.table_name,primary_dataset.id)
                else:
                    sql=sql+"%s t%s" %(primary_dataset.table.table_name,primary_dataset.id)

                sql=sql+"\n"

                partition_filter=None
                partition_filter=self._build_partition_filter(primary_dataset)

                if partition_filter:
                    sql=sql+"on t%s.%s and t%s.%s=t%s.%s" %(primary_dataset.id,partition_filter,self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)
                else:
                    sql=sql+"on t%s.%s=t%s.%s" %(self._api_settings.adc_dataset.id,relation['foreign_field'].field_name,primary_dataset.id,relation['primary_field'].field_name)

        if len(self._api_settings.sorts)>0:
            sql=sql+"\n"
            sorts=[]
            for field,sort_type in self._api_settings.sorts:
                if len(required_primary_relations)>0:
                    sorts.append("t%s.%s %s" %(field.dataset.id,field.field_name,sort_type))
                else:
                    sorts.append("%s %s" %(field.field_name,sort_type))

            sql=sql+"order by %s" %(",".join(sorts))

        if self._api_settings.limits:
            sql=sql+"\n"
            sql=sql+"limit %s" %(self._api_settings.limits)

        return sql


class ExecutorBuilder(object):

    @staticmethod
    def build(api_settings, **kwargs):
        if api_settings.adc_engine.engine_name == 'phoenix':
            return PhoenixClientExecutor(api_settings,**kwargs)
        elif api_settings.adc_engine.engine_name == 'hive':
            return HiveClientExecutor(api_settings,**kwargs)
        elif api_settings.adc_engine.engine_name == 'pipelinedb':
            return PipelineDBClientExecutor(api_settings,**kwargs)
