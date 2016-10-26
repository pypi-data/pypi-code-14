#!/usr/bin/env python

import argparse
import subprocess


def main():
	args = get_args()
	layouts = args.layouts.split(',')
	check_valid_layouts(layouts)
	rotate_layout(layouts)


def rotate_layout(layouts):
	current_layout = get_current_layout()
	current_index = 0
	try:
		current_index = layouts.index(current_layout)
	except:
		print('Current language not in rotation, setting to first language')

	next_layout = (current_index + 1) % len(layouts)

	set_layout(layouts[next_layout])


def get_current_layout():
	cmd = ['setxkbmap', '-query']
	check_output = subprocess.check_output(cmd)
	for line in check_output.split('\n'):
		if line.startswith('layout:'):
			layout = line.split(':', 1)[1]
			return layout.strip()


def check_valid_layouts(layouts):
	valid_layouts = get_all_valid_layouts()
	for layout in layouts:
		if not layout in valid_layouts:
			raise ValueError('"%s" is not a valid keyboard layout' % layout)


def get_all_valid_layouts():
	cmd = ['localectl', 'list-x11-keymap-layouts']
	output = subprocess.check_output(cmd)
	layouts = set()
	for line in output.split('\n'):
		layouts.add(line.strip())
	return layouts


def set_layout(layout):
	cmd = ['setxkbmap', '-layout', layout]
	subprocess.check_call(cmd)


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('layouts', help='Comma-separated list of the layouts to rotate')
	return parser.parse_args()


if __name__ == '__main__':
	main()