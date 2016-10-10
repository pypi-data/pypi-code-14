import os.path
import subprocess

import click
import MySQLdb


class MySQLBisect:
    def __init__(self, host, user, password, db, query, verbose):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.query = query
        self.conn = None
        self.verbose = verbose

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password)

    def _load_dump(self, fname):
        if self.verbose:
            print("Re-creating database...")
        cur = self.conn.cursor()
        cur.execute('DROP DATABASE IF EXISTS `{}`;'.format(self.db))
        cur.execute('CREATE DATABASE `{}`;'.format(self.db))
        cur.close()

        if self.verbose:
            print("Importing database dump {}...".format(fname))

        args = ['mysql', '-u', self.user]
        if self.password:
            args.append('-p' + self.password)
        args.append(self.db)

        if fname.endswith('.gz'):
            p1 = subprocess.Popen(["zcat", fname], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(args, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p1.stdout.close()
            out = p2.communicate()[0]
            if p2.returncode != 0:
                raise click.ClickException('MySQL returned an error: {}'.format(out))
        else:
            with open(fname, 'r') as f:
                subprocess.check_output(args, stdin=f)

    def check(self, fname):
        self._load_dump(fname)
        self.conn.select_db(self.db)
        cur = self.conn.cursor()
        cur.execute(self.query)
        res = cur.fetchone()
        return res and any(res)

    def bisect(self, filenames):
        max_known_good = 0
        min_known_bad = len(filenames) - 1

        if not self.check(filenames[0]):
            raise click.ClickException('Query does not return any results in the first file, can\'t bisect this!')

        if self.check(filenames[-1]):
            raise click.ClickException('Query returns results in the last file, can\'t bisect this!')

        while min_known_bad - max_known_good > 1:
            i = int((max_known_good + min_known_bad) / 2)
            if self.check(filenames[i]):
                if self.verbose:
                    print("File {} was good".format(filenames[i]))
                max_known_good = i
            else:
                if self.verbose:
                    print("File {} was bad".format(filenames[i]))
                min_known_bad = i

        if self.verbose:
            print("Cleanup...")
        cur = self.conn.cursor()
        cur.execute('DROP DATABASE IF EXISTS `{}`;'.format(self.db))
        cur.close()

        print("Done bisecting!")
        print("The file {} is the last one to be known as good".format(filenames[max_known_good]))
        print("The file {} is the first one to be known as bad".format(filenames[min_known_bad]))
        return min_known_bad


@click.command(help='Takes a number of SQL dumps, imports them into a temporary database and runs a query '
               'on them. Then it performs a binary search on them to find the EARLIEST dump where the query '
               'returns a result. The SQL dumps are processed in alphabetical filename order. If a query '
               'returns a row consisting only of 0 and NULL, it will be counted as "no result".')
@click.option('--host', '-h', default='localhost', help='MySQL host to use for temporary databases')
@click.option('--user', '-u', default='root', help='MySQL user to use for temporary databases. '
              'Needs permission to create and drop databases of the name specified with --db.')
@click.option('--password', '-p', default='', prompt=True, hide_input=True, help='MySQL user password')
@click.option('--db', default='bisect_tmp', help='MySQL database name scheme for temporary database. '
              'Default: bisect_tmp')
@click.option('--query', '-q', required='True', help='MySQL query to check in each file.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output.')
@click.argument('filename', nargs=-1, type=click.Path(exists=True))
def bisect(host, user, password, db, filename, query, verbose):
    mb = MySQLBisect(host, user, password, db, query, verbose)
    mb.connect()
    mb.bisect(sorted(filename, key=os.path.basename))


if __name__ == '__main__':
    bisect()
