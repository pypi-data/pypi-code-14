import os
import os.path


def cache_busting_url_for(app, old_url_for, bust_extensions=True):
	'''
	Replace flask's url_for with one that supports cache busting of static files.
	'''

	def transform_filename(orig_filename):
		file_path = os.path.join(app.static_folder, orig_filename)
		if os.path.isfile(file_path):
			timestamp = int(os.stat(file_path).st_mtime)
			directory, filename = os.path.split(orig_filename)
			filename, extension = filename.split('.', 1)
			if bust_extensions is True or extension in bust_extensions or \
					extension.split('.')[-1] in bust_extensions:
				filename = '{}.{}.{}'.format(filename, timestamp, extension)
				return os.path.join(directory, filename)
		return orig_filename

	url_cache = {}

	def url_for_wrapper(endpoint, **values):
		if endpoint == 'static':
			filename = values.get('filename')
			if filename:
				if filename not in url_cache:
					url_cache[filename] = transform_filename(filename)
				values['filename'] = url_cache[filename]
		return old_url_for(endpoint, **values)

	return url_for_wrapper
