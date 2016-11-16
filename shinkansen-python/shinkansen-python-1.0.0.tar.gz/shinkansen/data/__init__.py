class TableConfig(object):
    def __init__(
        self, table_name, partition_col, chunk_col,
        delta_col=None, join=None, table_alias=None,
        trim_column=None, trim_timedelta=None,
        ignore_columns=None
    ):
        self.table_name = table_name
        self.partition_col = partition_col
        self.chunk_col = chunk_col
        self.delta_col = delta_col
        self.join = join if join is not None else ''
        self.table_alias = table_alias if table_alias is not None else ''
        self.trim_column = trim_column
        self.trim_timedelta = trim_timedelta
        self.ignore_columns = [] if ignore_columns is None else [col.lower() for col in ignore_columns]

    def __eq__(self, b):
        return (
            self is b
            or (
                b is not None
                and self.table_name == b.table_name
                and self.partition_col == b.partition_col
                and self.chunk_col == b.chunk_col
                and self.delta_col == b.delta_col
                and self.join == b.join
                and self.table_alias == b.table_alias
                and self.trim_column == b.trim_column
                and self.trim_timedelta == b.trim_timedelta
                and self.ignore_columns == b.ignore_columns
            )
        )

    def __repr__(self):
        return '%s(%r, %r, %r, %r, %r, %r, %r, %r, %r)' % (
            self.__class__.__name__,
            self.table_name, self.partition_col, self.chunk_col,
            self.delta_col, self.join, self.table_alias,
            self.trim_column, self.trim_timedelta,
            self.ignore_columns
        )
