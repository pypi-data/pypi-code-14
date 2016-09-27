import os, glob, json, collections, zipfile, shlex, subprocess


def ZipNormalize(*args):
	path = os.path.join(*args)
	return os.path.normpath(path).replace('\\', '/')


def ExpandConfig(target_config, target_settings, project):
	target_config['name'] = project['name']
	target_config['version'] = project['version']

	extensions = {
		'windows': 'pyd',
		'linux': 'so',
	}
	
	prefix = 'cp{0}-cp{0}m'.format(target_config['pyver'][2:])

	suffix = {
		('windows', 'x86'): 'win32',
		('windows', 'x64'): 'win_amd64',
		('linux', 'x86'): 'manylinux1-i686',
		('linux', 'x64'): 'manylinux1-x86_64',
	}

	bits = {
		'x86': 32,
		'x64': 64,
	}

	pair = target_config['platform'], target_config['arch']

	target_config['bits'] = bits[target_config['arch']]
	target_config['ext'] = extensions[target_config['platform']]
	target_config['tag'] = '{}-{}'.format(prefix, suffix[pair])
	target_config['wheel'] = '{name}-{version}-{tag}.whl'.format_map(target_config)
	target_config.update(target_settings)


cwd = os.getcwd()

def Compile(project):
	if os.path.isdir(project):
		project = os.path.join(project, 'project.json')

	with open(project) as settings_file:
		project = json.load(settings_file, object_pairs_hook = collections.OrderedDict)

		wheel_folder = os.path.join(cwd, os.path.normpath(project['output']))
		module_folder = os.path.join(cwd, os.path.normpath(project['module']))

		if not os.path.isdir(wheel_folder):
			os.makedirs(wheel_folder)

		for target_name, target_settings in project['targets'].items():
			if 'skip' in target_settings and target_settings['skip']:
				print('Skipping %s' % target_name)
				continue

			target_parts = ('pyver', 'platform', 'arch')
			target_config = dict(zip(target_parts, target_name.split('-')))

			ExpandConfig(target_config, target_settings, project)
			wheel_path = os.path.join(wheel_folder, target_config['wheel'])

			pack = zipfile.ZipFile(wheel_path, 'w')

			module_search = os.path.normpath(os.path.join(module_folder, '**/*.py'))
			for filename in glob.glob(module_search, recursive = True):
				relative_path = os.path.relpath(filename, module_folder)
				zip_py = ZipNormalize(project['name'], relative_path)

				with open(filename) as py_file:
					content = py_file.read()

				pack.writestr(zip_py, content)

			for ext_name, ext_settings in project['extensions'].items():
				ext_output = ext_settings['output'].format_map(target_config)
				target_config['output'] = ext_output
				
				ext_build = ext_settings['build'].format_map(target_config)
				ext_path = ext_settings['path'].format_map(target_config)

				ext_path = os.path.normpath(os.path.join(cwd, ext_path))
				ext_output = os.path.normpath(os.path.join(ext_path, ext_output))

				zip_ext = '{}.{}'.format(ext_name, target_config['ext'])
				zip_ext = ZipNormalize(project['name'], zip_ext)

				print(ext_build)
				proc = subprocess.Popen(shlex.split(ext_build), cwd = ext_path)
				proc.wait()

				with open(ext_output) as ext_file:
					content = ext_file.read()

				pack.writestr(zip_ext, content)

			pack.close()
