# -*- coding: utf-8 -*-

from playhouse.migrate import *
import config


def run_migrate():
    print('Begin migrate ...')
    migrator = PostgresqlMigrator(config.dbconnect)
    status_field = IntegerField(null=False, default=0)
    try:
        migrate(migrator.add_column('tabapp', 'valid', status_field))
    except:
        pass

    ################################################################################################

    try:
        migrate(migrator.drop_column('cabpagehist', 'cnt_html'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabpagehist', 'time_create'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabpagehist', 'date'))
    except:
        pass

    try:
        migrate(migrator.rename_column('cabpagehist', 'id_user', 'user_name'))
    except:
        pass

    ###################################################################################################

    try:
        migrate(migrator.drop_column('cabwikihist', 'date'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabwikihist', 'time_create'))
    except:
        pass

    ##########################################################################################

    try:
        migrate(migrator.drop_column('cabposthist', 'id_spec'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabposthist', 'id_cats'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabposthist', 'date'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabposthist', 'time_create'))
    except:
        pass


    ##########################################################################################
    try:
        migrate(migrator.drop_column('cabpost', 'id_cats', status_field))
    except:
        pass
    try:
        migrate(migrator.drop_column('tabapp', 'id_cats', status_field))
    except:
        pass
    try:
        migrate(migrator.add_column('cabpost', 'valid', status_field))
    except:
        pass
    try:
        migrate(migrator.drop_column('cabmember', 'valid'))
    except:
        pass





    try:
        migrate(migrator.drop_column('cabwiki', 'src_type'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabpage', 'src_type'))
    except:
        pass

    try:
        migrate(migrator.drop_column('cabpost', 'src_type'))
    except:
        pass

    try:
        migrate(migrator.add_column('cabmember', 'time_email', status_field))
    except:
        pass

    try:
        migrate(migrator.add_column('cabmember', 'time_login', status_field))
    except:
        pass
    try:
        migrate(migrator.add_column('cabmember', 'time_create', status_field))
    except:
        pass

    try:
        migrate(migrator.add_column('cabmember', 'time_update', status_field))
    except:
        pass

    try:
        migrate(
            migrator.rename_column('cabmember', 'reset_passwd_timestamp', 'time_reset_passwd')
        )
    except:
        pass

    print('QED')
