from distutils.core import setup
setup(
	name = 'mongo_remove_duplicate_indexes',
	version = '1.0.0',
	py_modules = ['mongo_dup_remover'],
	author = 'satyam',
	author_email = 'satyam.khare95@gmail.com',
	description = 'removes duplicates present in ur collection of particular index and return new collection with dups removed and that index uniquely indexed',
)