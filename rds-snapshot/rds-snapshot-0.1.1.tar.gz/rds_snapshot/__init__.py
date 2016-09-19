import argparse
import sys
from datetime import datetime, timedelta

import boto3
import botocore.exceptions

rds_client = None


def get_rds():
    """rds client singleton"""
    global rds_client

    if not rds_client:
        rds_client = boto3.client('rds')
    return rds_client


def listdbs(args):
    for db in get_rds().describe_db_instances()['DBInstances']:
        if not args.info:
            print db['DBInstanceIdentifier']
        else:
            print '%s (%s):\t%s:%d' % (
                db['DBInstanceIdentifier'],
                db['Engine'],
                db['Endpoint']['Address'],
                db['Endpoint']['Port']
            )


def lists(args):
    dbs = args.rds_instance

    # list all
    if args.all:
        dbs = [db['DBInstanceIdentifier'] for db in get_rds().describe_db_instances()['DBInstances']]

    # bail if no stacks to dump
    if not len(dbs):
        print 'this command needs a list of dbs, or the --all flag'
        sys.exit(1)

    for db in dbs:
        snaps = get_rds().describe_db_snapshots(DBInstanceIdentifier=db)['DBSnapshots']
        if len(dbs) > 1:
            print '---', db, '---'

        for snap in snaps:
            if not args.info:
                print snap['DBSnapshotIdentifier']
            else:
                try:
                    create_time = snap['SnapshotCreateTime']
                except KeyError:
                    create_time = 'progress: %d%%\t\t\t' % snap['PercentProgress']
                print '%s:%s\t%s\t%s\t%s' % (
                    snap['DBSnapshotIdentifier'],
                    ''.ljust(max([len(s['DBSnapshotIdentifier']) for s in snaps]) - len(snap['DBSnapshotIdentifier'])),
                    create_time,
                    snap['SnapshotType'],
                    snap['Status']
                )


def create(args):
    snap = get_rds().create_db_snapshot(
        DBSnapshotIdentifier='dbsnap-%s-%s' % (args.rds_instance, datetime.now().strftime('%Y%m%d-%H%M%S')),
        DBInstanceIdentifier=args.rds_instance
    )
    print snap['DBSnapshot']['DBSnapshotIdentifier']


def delete(args):
    get_rds().delete_db_snapshot(DBSnapshotIdentifier=args.snapshot)


def cleanup(args):
    for snap in get_rds().describe_db_snapshots(DBInstanceIdentifier=args.rds_instance)['DBSnapshots']:
        if snap['SnapshotType'] != 'manual' or snap['Status'] != 'available':
            continue

        if snap['DBSnapshotIdentifier'][:7] != 'dbsnap-':
            continue

        if snap['SnapshotCreateTime'].replace(tzinfo=None) < datetime.now() - timedelta(days=args.maxage):
            print 'delete', snap['DBSnapshotIdentifier']
            if not args.dry:
                get_rds().delete_db_snapshot(DBSnapshotIdentifier=snap['DBSnapshotIdentifier'])


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    listdbs_parser = subparsers.add_parser('dbs', help='list databases in account/region')
    listdbs_parser.add_argument('-i', '--info', action='store_true', help='show some info')
    listdbs_parser.set_defaults(func=listdbs)

    list_parser = subparsers.add_parser('list', help='list snapshots for db')
    list_parser.add_argument('-a', '--all', action='store_true', help='list snapshots for all dbs')
    list_parser.add_argument('-i', '--info', action='store_true', help='show some info')
    list_parser.add_argument('rds_instance', nargs='*', help='RDS instance name')
    list_parser.set_defaults(func=lists)

    create_parser = subparsers.add_parser('create', help='create snapshot for db')
    create_parser.add_argument('rds_instance', help='RDS instance name')
    create_parser.set_defaults(func=create)

    delete_parser = subparsers.add_parser('delete', help='delete snapshot')
    delete_parser.add_argument('snapshot', help='snapshot name')
    delete_parser.set_defaults(func=delete)

    cleanup_parser = subparsers.add_parser('cleanup', help='cleanup old snapshots')
    cleanup_parser.add_argument('-d', '--dry', action='store_true', help='dry-run, show what would be cleaned up')
    cleanup_parser.add_argument('--maxage', type=int, default=90, help='maximum age of snapshots (days, default:90)')
    cleanup_parser.add_argument('rds_instance', help='RDS instance name')
    cleanup_parser.set_defaults(func=cleanup)

    args = parser.parse_args()
    try:
        args.func(args)
    except botocore.exceptions.NoRegionError as err:
        print str(err)
        sys.exit(1)
    except botocore.exceptions.ClientError as err:
        print str(err)
        sys.exit(1)
