#! /usr/bin/env python3
import argparse
import importlib
import logging
import os
import re
import shutil
import sys

from peewee import (Model, CharField, PostgresqlDatabase,
                    IntegrityError, ProgrammingError)
from playhouse.migrate import PostgresqlMigrator, migrate

from jambi.config import JambiConfig
from jambi.version import VERSION


_db = PostgresqlDatabase(None)
_schema = 'public'


class JambiModel(Model):
    """The model that keeps the database version."""
    ref = CharField(primary_key=True)

    class Meta:
        db_table = 'jambi'
        database = _db
        schema = _schema


class Jambi(object):
    """A database migration helper for peewee."""
    def __init__(self, config_file=None):
        self.version = VERSION
        self.config = JambiConfig()
        sys.path.append(os.getcwd())
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('peewee').setLevel(logging.INFO)
        self.logger = logging.getLogger('jambi')
        self.db, self.db_schema = self.__get_db_and_schema_from_config()

    def upgrade(self, ref):
        """Upgrade the database to the supplied version.

        Arguments:
        ref -- the version to upgrade the database to, or 'latest'
        """
        try:
            ref = int(ref)
        except:
            if ref != 'latest':
                self.logger.error('Unable to parse version "{}"'.format(ref))
                return

        # check the current db version
        current_ref = self.inspect()
        if current_ref is None:
            self.logger.error('Unable to inspect your database. '
                              'Perhaps you need to run \'jambi inpsect\'?')
            return

        # get the migrations
        migrations = self.find_migrations()
        latest_ref = migrations[-1][1] if any(migrations) else 0
        migrations = tuple(filter(lambda x: x[1] > current_ref, migrations))

        if current_ref > latest_ref:
            self.logger.error('Your database version is higher than the '
                              'current database version. '
                              '(current: {}, latest: {})'.format(current_ref,
                                                                 latest_ref))
        elif current_ref == latest_ref:
            self.logger.info('You are already up to date. '
                             '(version: {})'.format(current_ref))
            return

        # filter out migrations that are beyond the desired version
        if ref == 'latest':
            ref = latest_ref
        migrations = tuple(filter(lambda x: x[1] <= ref, migrations))
        if not any(migrations):
            self.logger.info('You are already up to date. '
                             '(version: {})'.format(current_ref))
            return

        # run the migrations
        self.logger.info('Migrating to version {}'.format(ref))
        self.db.connect()
        with self.db.atomic():
            for n, v, m in migrations:
                self.logger.info('Upgrading to version {}'.format(v))
                migrator = PostgresqlMigrator(self.db)
                upgrades = m.upgrade(migrator)
                migrate(*upgrades)
            self.__set_version(migrations[-1][1])
        self.db.close()
        return

    def downgrade(self, ref):
        """downgrade the db to the supplied version"""
        return NotImplemented

    def latest(self, quiet=False):
        """returns the latest version in the migrations folder"""
        ver = None
        migrations = self.find_migrations()
        if any(migrations):
            ver = migrations[-1][1]
            if not quiet:
                self.logger.info('Latest migration is at version '
                                 '{}'.format(ver))
        else:
            ver = 0
            if not quiet:
                self.logger.info('There are no migrations.')
        return ver

    def find_migrations(self):
        """find, import, and return all migration files as modules"""
        fileloc = self.config.get('migrate', 'location')
        fullpath = os.path.abspath(fileloc)
        try:
            filenames = os.listdir(fullpath)
        except FileNotFoundError:
            self.logger.error('Unable to find migration folder '
                              '"{}"'.format(fullpath))
            return []

        def is_valid_migration_name(n):
            return n.startswith('version_') and n.endswith('.py')
        filenames = filter(lambda x: is_valid_migration_name(x), filenames)
        filepaths = [(os.path.join(fullpath, f), f.replace('.py', ''))
                     for f in filenames]
        migrations = []
        for fp, mn in filepaths:
            module_name = '.'.join([fileloc.replace('/', '.').strip('.'), mn])
            try:
                ver = int(re.search(r'version_(\d+)', mn).group(1))
            except:
                self.logger.warning('Cannot parse version number from "{}", '
                                    'skipping'.format(mn))
                continue
            self.logger.debug('Found {} at version {}'.format(module_name,
                                                              ver))
            migrations.append(
                (module_name, ver, importlib.import_module(module_name))
            )
        return sorted(migrations, key=lambda x: x[1])

    def inspect(self):
        """inspect the database and report its version"""
        self.db.connect()
        result = None
        try:
            jambi_versions = JambiModel.select().limit(1)
            if any(jambi_versions):
                field = jambi_versions[0].ref
                try:
                    result = int(field)
                except ValueError:
                    self.logger.error('Database current version "{}" is not '
                                      'valid'.format(jambi_versions[0].ref))
                self.logger.info('Your database is at version '
                                 '{}'.format(field))
            else:
                self.logger.info('This database hasn\'t been migrated yet')
        except ProgrammingError:
            self.logger.info('Run "init" to create a jambi version table')
        finally:
            self.db.close()
        return result

    def __set_version(self, ref):
        """sets the jambi table version

        Note that this does not run the migrations, but is instead used by
        the migration logic to easily set the version after migrations have
        completed.
        """
        JambiModel.delete().execute()
        JambiModel.create(ref=str(ref))
        self.logger.debug('Set jambi version to {}'.format(ref))

    def init(self):
        """initialize the jambi database version table"""
        self.db.connect()
        try:
            self.db.create_tables([JambiModel], safe=True)
            JambiModel.create(ref='0')
            self.logger.info('Database initialized')
        except IntegrityError:
            self.logger.info('Database was already initialized')
        self.db.close()

    def makemigration(self):
        """create a new migration from template and place in migrate
        location
        """
        template = os.path.join(os.path.dirname(__file__),
                                'migration_template.py')
        ver = self.latest(quiet=True) + 1
        destination = os.path.abspath(self.config.get('migrate', 'location'))
        fname = 'version_{}.py'.format(ver)
        shutil.copyfile(template, os.path.join(destination, fname))
        self.logger.info('Migration \'{}\' created'.format(fname))
        self.latest()

    def wish_from_kwargs(self, **kwargs):
        """Processes keyword arguments in to a jambi wish."""
        try:
            wish = kwargs.pop('wish')
        except KeyError:
            self.logger.error('There was no wish to process')

        if wish == 'upgrade':
            result = self.upgrade(kwargs.pop('ref') or 'latest')
        elif wish == 'inspect':
            result = self.inspect()
        elif wish == 'latest':
            result = self.latest()
        elif wish == 'init':
            result = self.init()
        elif wish == 'makemigration':
            result = self.makemigration()
        else:
            self.logger.error('Unknown wish')
            result = None

        return result

    def __get_db_and_schema_from_config(self):
        _db.init(self.config.get('database', 'database'),
                 user=self.config.get('database', 'user'),
                 password=self.config.get('database', 'password'),
                 host=self.config.get('database', 'host'))
        _schema = self.config.get('database', 'schema')
        return _db, _schema


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog="jambi",
        description='Migration tools for peewee'
    )
    parser.add_argument(
        '--config',
        nargs='?',
        help='config file to use',
        type=str,
        default='jambi.conf',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(VERSION)
    )

    subparsers = parser.add_subparsers(title='actions', dest='wish')
    subparsers.add_parser('inspect', help='check database version')
    subparsers.add_parser('latest', help='get latest migration version')
    subparsers.add_parser('init', help='create jambi table')

    wish_make = subparsers.add_parser('makemigration',
                                      help='generate new migration')
    wish_make.add_argument('-l', type=str, help='migration label')

    wish_migrate = subparsers.add_parser('upgrade', help='run migrations')
    wish_migrate.add_argument('ref', type=str, help='db version', nargs='?')

    opts = parser.parse_args()

    if opts.wish is None:
        parser.print_help()
        sys.exit(1)

    # create jambi and process command
    jambi = Jambi(config_file=opts.config)
    jambi.wish_from_kwargs(**vars(opts))


if __name__ == '__main__':
    main()
