
import anvil.server

class Table:
	def __init__(self, id):
		self.id = id

	def search(self, _chunk_size=None, **kwargs):
		return anvil.server.call("anvil.private.tables.search", self.id, _chunk_size, **kwargs)

	def get_by_id(self, row_id):
		return anvil.server.call("anvil.private.tables.get_by_id", self.id, row_id)

	def add_row(self, **kwargs):
		return anvil.server.call("anvil.private.tables.add_row", self.id, **kwargs)

	def list_columns(self):
		return anvil.server.call("anvil.private.tables.list_columns", self.id)

	def delete_all_rows(self):
		return anvil.server.call("anvil.private.tables.delete_all_rows", self.id)

class AppTables:
	cache = {}

	def __getattr__(self, name):
		tbl = AppTables.cache.get(name)
		if tbl is not None:
			return tbl

		tid = anvil.server.call("anvil.private.tables.get_table_id", name)
		if tid is None:
			raise AttributeError("No such app table: '%s'" % name)

		tbl = Table(tid)
		AppTables.cache[name] = tbl
		return tbl

	def __setattr__(self, name, val):
		raise Exception("app_tables is read-only")

app_tables = AppTables()

def set_client_config(x):
    pass
