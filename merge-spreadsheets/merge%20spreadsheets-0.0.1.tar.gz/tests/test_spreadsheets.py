from unittest import TestCase

from src.spreadsheets import Table


class TestTable(TestCase):

    EXAMPLE_TABLE_COLUMN_COUNT = 11
    EXAMPLE_TABLE_ROW_COUNT = 5

    def setUp(self):
        self.table = Table(
            headers=(
                'first column',
                'second column',
                'third column',
            ),
            rows=None,
        )

    def _table_from_file(self):
        import os
        filename = os.path.join(os.path.dirname(__file__), 'example.xlsx')
        return Table.from_xlsx(filename)

    def test_table_not_None(self):
        self.assertIsNotNone(self.table)

    def test_headers(self):
        self.assertEqual(self.table.headers, (
                'first column',
                'second column',
                'third column',
            )
        )

    def test_add_row(self):
        row = {
            'first column': 'first',
            'second column': 'second',
            'third column': 'third',
        }
        self.table.add(row)
        self.assertEqual(1, self.table.rows_count)

    def test_add_row_with_not_exists_column(self):
        row = {
            'first column': 'first',
            'second column': 'second',
            'third column not exists': 'third',
        }

        with self.assertRaises(Exception):
            self.table.add(row)

    def test_table_from_xlsx(self):
        table = self._table_from_file()

        self.assertIsNotNone(table)
        self.assertEqual(table.columns_count, self.EXAMPLE_TABLE_COLUMN_COUNT)
        self.assertEqual(table.rows_count, self.EXAMPLE_TABLE_ROW_COUNT)

    def test_merge_tables(self):
        table1 = self._table_from_file()
        table2 = self._table_from_file()

        table1.merge(table2)

        self.assertEqual(table1.columns_count, self.EXAMPLE_TABLE_COLUMN_COUNT)
        self.assertEqual(table1.rows_count, self.EXAMPLE_TABLE_ROW_COUNT*2)
