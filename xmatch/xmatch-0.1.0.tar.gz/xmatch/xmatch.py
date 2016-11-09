#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 IAS / CNRS / Univ. Paris-Sud
# LGPL License - see attached LICENSE file
# Author: Alexandre Beelen <alexandre.beelen@ias.u-psud.fr>

"""xmatch several catalogs on one or several positions"""

import logging
logging.basicConfig(
    format='%(asctime)s -- %(levelname)s: %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger('django')

import os
import sys
import argparse

import numpy as np

import astropy.units as u

from astropy.io import fits, ascii
from astropy import coordinates as coord

# from astropy.table import vstack as astvstack
# from astropy.table import hstack as asthstack
from astropy.table import Table, join

from astroquery.vizier import Vizier

try:  # pragma: py3
    PATTERN = None
    from configparser import ConfigParser, ExtendedInterpolation
except ImportError:  # pragma: py2
    import re
    from ConfigParser import ConfigParser
    PATTERN = re.compile(r"\$\{(.*?)\}")

try:  # pragma: py3
    FileNotFoundError
except NameError:  # pragma: py2
    FileNotFoundError = IOError


def check_config_vizier(config, cat):
    """Check that all basic options are set for a given vizier catalog

    Parameters
    ----------
    config : ~ConfigParser
        the ConfigParser object
    cat : str
        the name of the catalog/section

    Returns
    -------
    dict
        a dictionnary with all required data for the Vizier catalog :

        * catalog : the name of the Vizier catalog
        * fields : the name of the columns to output after the match
        * dist_threshold : the distance threshold for a match
    """

    opt = {}
    if config.has_option(cat, 'catalog'):
        opt['catalog'] = config.get(cat, 'catalog')
    else:
        raise ValueError("Missing 'catalog' option for [%s]" % cat)

    if config.has_option(cat, 'fields'):
        opt['fields'] = config.get(cat, 'fields').split()
    else:
        opt['fields'] = ['all']

    # xmatch catalogs has an additionnal option :
    if config.has_option(cat, 'dist_threshold'):
        opt['dist_threshold'] = config.getfloat(cat, 'dist_threshold')
    else:
        raise ValueError("Missing 'dist_threshold' option for [%s]" % cat)

    return opt


def check_config_cat(config, cat):
    """Check that all basic options are set for a given catalog

    Parameters
    ----------
    config : ~ConfigParser
        the ConfigParser object
    cat : str
        the name of the catalog/section

    Returns
    -------
    dict
        a dictionnary with all required data for the catalog :

        * filename : the filename of the catalog
        * ext : the extension number or name in the filename
        * lon, lat : the name of the columns for longitude and latitude
        * frame : the coordinate frame of longitude or latitude
        * fields : the name of the columns to output after the match

    """

    opt = {}
    if config.has_option(cat, 'filename'):
        opt['filename'] = config.get(cat, 'filename')
    else:
        raise ValueError("Missing 'filename' option for [%s]" % cat)

    if config.has_option(cat, 'ext'):
        ext = config.get(cat, 'ext')
        if ext.isdigit():
            ext = int(ext)
        opt['ext'] = ext
    else:
        raise ValueError("Missing 'ext' option for [%s]" % cat)

    if config.has_option(cat, 'lon'):
        opt['lon'] = config.get(cat, 'lon')
    else:
        raise ValueError("Missing 'lon' option for [%s]" % cat)

    if config.has_option(cat, 'lat'):
        opt['lat'] = config.get(cat, 'lat')
    else:
        raise ValueError("Missing 'lat' option for [%s]" % cat)

    if config.has_option(cat, 'frame'):
        opt['frame'] = config.get(cat, 'frame')
    else:
        raise ValueError("Missing 'frame' option for [%s]" % cat)

    if config.has_option(cat, 'fields'):
        opt['fields'] = config.get(cat, 'fields').split()
    else:
        opt['fields'] = ['all']

    return opt


def parse_config(conffile=None):
    """Parse options from a configuration file"""

    if PATTERN:  # pragma: py2
        config = ConfigParser()

        def rep_key(mesg):
            """replace keys in filenames"""
            section, key = re.split(':', mesg.group(1))
            return config.get(section, key)
    else:  # pragma: py3
        config = ConfigParser(interpolation=ExtendedInterpolation())

    conffiles = [os.path.join(directory, 'xmatch.cfg') for directory
                 in [os.curdir, os.path.join(os.path.expanduser("~"), '.config/xmatch')]]

    # If specifically ask for a config file, then put it at the
    # beginning ...
    if conffile:
        conffiles.insert(0, conffile)

    found = config.read(conffiles)

    if not found:
        raise FileNotFoundError

    options = {'cat_fits': [],
               'cat_vizier': []}

    # Take care of [inputs] if present
    if config.has_section('input'):
        # Check that all be basic options are set
        input_tab = check_config_cat(config, 'input')
        if PATTERN:  # pragma: py2
            input_tab['filename'] = PATTERN.sub(
                rep_key, input_tab['filename'])
        options['input_tab'] = input_tab

    if config.has_section('global') and \
       config.has_option('global', 'cat_list') and \
       config.get('global', 'cat_list'):

        for cat in str(config.get('global', 'cat_list')).split():
            if config.has_section(cat):

                opt = check_config_cat(config, cat)
                if PATTERN:  # pragma: py2
                    opt['filename'] = PATTERN.sub(rep_key, opt['filename'])

                # xmatch catalogs has an additionnal option :
                if config.has_option(cat, 'dist_threshold'):
                    opt['dist_threshold'] = config.getfloat(
                        cat, 'dist_threshold')
                else:
                    raise ValueError(
                        "Missing 'dist_threshold' option for [%s]" % cat)
                options['cat_fits'].append((cat, opt))
            else:
                raise ValueError("Missing [%s] section" % cat)

    if config.has_section('global') and \
       config.has_option('global', 'vizier_list') and \
       config.get('global', 'vizier_list'):

        for cat in str(config.get('global', 'vizier_list')).split():
            if config.has_section(cat):
                opt = check_config_vizier(config, cat)
                options['cat_vizier'].append((cat, opt))
            else:
                raise ValueError("Missing [%s] section" % cat)

    if options['cat_fits'] == options['cat_vizier'] == []:
        raise ValueError(
            "You must provide either a valid [global:cat_list] or [global:vizier_list]")

    if config.has_section('output'):
        if config.has_option('output', 'filename'):
            filename = config.get('output', 'filename')
            if PATTERN:  # pragma: py2
                filename = PATTERN.sub(rep_key, filename)
            options['filename'] = filename

        if config.has_option('output', 'outdir'):
            options['outdir'] = config.get('output', 'outdir')
        if config.has_option('output', 'verbosity'):
            level = str(config.get('output', 'verbosity')).lower()
            allowed_levels = {'verbose': logging.DEBUG,
                              'debug': logging.DEBUG,
                              'quiet': logging.ERROR,
                              'error': logging.ERROR,
                              'info': logging.INFO}
            if level in allowed_levels.keys():
                options['verbosity'] = allowed_levels[level]
            else:
                try:
                    options['verbosity'] = int(level)
                except ValueError:
                    options['verbosity'] = None

    return options


def parse_args(args):
    """Parse arguments from the command line"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Match position(s) with catalogs",
        epilog="""
configuration files:

The configuration file must contain a [global:cat_list] or
[global:vizier_list] option to list all the requested fits or vizier
catalogs. Each fits catalog description MUST list certain options :

---

[global]
cat_list: cat_name
vizier_list: vizier_name

[cat_name]            # catatlog name (no space)
filename: str         # full pathname to the vo-fits catalog
ext: int or str       # extension # or name within the above fits file
lon: str              # longitude and ...
lat: str              # ... latitude on a given ...
frame: str            # ... frame to be use for cross matching
fields: col1 col2     # columns to be selected for output
                      # (default: all)
dist_threshold: float # The distance threshold for a match to the
                      # reference position

[vizier_name]
catalog: str          # Vizier identifiant name of the catalog
fields: col1 col2     # columns to be selected for output
                      # (default: all)
dist_threshold: float # The distance threshold for a match to the
                      # reference position

---

Moreover, an input catalog can be given using [input] as a section
name, thus '--lonlat' is optionnal

"""
    )

    parser.add_argument(
        'conf', type=str, help='configuration file (see below)')
    parser.add_argument('--lonlat', type=float, nargs=2, required=False,
                        help='longitude and latitude to match with [deg] ')
    parser.add_argument('--coordframe', required=False,
                        help='coordinate frame of the lon. and lat.(default: galactic)',
                        choices=['galactic', 'icrs'], default='galactic')

    out = parser.add_argument_group('output')
    out.add_argument('--filename', required=False,
                     help='output file name (*.csv, *.txt, *.html, *.fits')
    out.add_argument('--outdir', required=False,
                     help='output directory (default:".")')

    general = parser.add_argument_group('general')
    verb = general.add_mutually_exclusive_group()
    verb.add_argument(
        '-v', '--verbose', action='store_true', help='verbose mode')
    verb.add_argument('-q', '--quiet', action='store_true', help='quiet mode')

    parsed_args = parser.parse_args(args)

    if parsed_args.verbose:
        parsed_args.verbosity = logging.DEBUG
    elif parsed_args.quiet:
        parsed_args.verbosity = logging.ERROR
    else:
        parsed_args.verbosity = None

    return parsed_args


def combine_args(args, config):
    """Combine the different sources of arguments (command line,
    configfile and default arguments
    """

    if config.get('input_tab') is None:
        if args.lonlat is None:
            raise ValueError(
                "Either [input] in %s or the '--lonlat' option is required" % args.conf)
        else:
            # Use the lonlat provided on the command line
            coord_in = coord.SkyCoord([args.lonlat[0]], [args.lonlat[1]],
                                      unit=u.deg,
                                      frame=args.coordframe)
            index = [0]
            tab_in = Table()
            tab_in.add_column(Table.Column(name='index', data=index))
            tab_in.add_column(
                Table.Column(name='glon', data=coord_in.galactic.l))
            tab_in.add_column(
                Table.Column(name='glat', data=coord_in.galactic.b))
            tab_in.add_column(Table.Column(name='RA', data=coord_in.icrs.ra))
            tab_in.add_column(
                Table.Column(name='DEC', data=coord_in.icrs.dec))
    else:
        # Use the input table by default
        input_tab = config.get('input_tab')
        tab_in = Table(fits.getdata(input_tab['filename'], input_tab['ext']))
        coord_in = coord.SkyCoord(
            tab_in[input_tab['lon']], tab_in[input_tab['lat']],
            unit=u.deg, frame=input_tab['frame'])
        try:
            tab_in.add_column(Table.Column(name='index',
                                           data=np.arange(len(tab_in))))
        except ValueError:
            # Tab already has an index column, use it !
            pass

    verbosity = args.verbosity or config.get('verbosity') or logging.INFO
    LOGGER.setLevel(verbosity)

    output = {}
    output['outdir'] = args.outdir or config.get('outdir') or '.'
    output['filename'] = args.filename or config.get('filename') or None

    return coord_in, tab_in,\
        config.get('cat_fits'), config.get('cat_vizier'), \
        output


def cross_match(config, lonlat=[0.0, 0.0], coordframe='galactic'):
    """Old interface"""

    coord_in = coord.SkyCoord(lonlat[0], lonlat[1],
                              unit="deg", frame=coordframe)

    matched_cat = {}
    if config.get('cat_fits'):
        matched_cat.update(xmatch_fits(coord_in, config.get('cat_fits')))
                           
    if config.get('cat_vizier'):
        matched_cat.update(xmatch_vizier(coord_in, config.get('cat_vizier')))
                           
    return matched_cat


def xmatch(coord_in, cat_table, cat_coord, opt):

    if coord_in.isscalar:
        index = np.array([0])
    else:
        index = np.arange(len(coord_in))

    temp_id, temp_sep, trash = coord_in.match_to_catalog_sky(cat_coord)

    # selecting associations with distance <  sz_dist_theshold_arcmin
    wheregood = temp_sep.arcmin < opt['dist_threshold']

    # To get consistent sizes with temp_sep...
    if temp_id.size == 1:
        temp_id = np.array([temp_id])

    # defining new columns related to the cross match
    if wheregood.any():
        x_id_in_cat = index[wheregood]
        x_id = temp_id[wheregood]
        x_sep = temp_sep[wheregood]

        # Extract the corresponding rows
        matched_tab = Table(cat_table[x_id])

        # Only keep the requested columns
        if opt['fields'] == ['all']:
            fields = matched_tab.columns.keys()
        else:
            fields = opt['fields']

        matched_tab.keep_columns(fields)  # extract the fields

        # for field in fields:
        #     matched_tab.rename_column(field, '_'+field)

        # adding columns related to the crossmatch
        matched_tab.add_column(Table.Column(name='index', data=x_id_in_cat))
        matched_tab.add_column(Table.Column(name='_id', data=x_id + 1))
        matched_tab.add_column(Table.Column(name='_sep', data=x_sep.arcmin))

    else:
        matched_tab = None

    return matched_tab


def xmatch_fits(coord_in, cat_fits):

    matched_fits = {}

    for cat, opt in cat_fits:

        cat_table = fits.getdata(opt['filename'], opt['ext'])

        cat_coord = coord.SkyCoord(cat_table[opt['lon']],
                                   cat_table[opt['lat']],
                                   unit=u.deg, frame=opt['frame'])

        matched_fits[cat] = xmatch(coord_in, cat_table, cat_coord, opt)

        LOGGER.debug('Results of cross correlation with ' + cat)
        LOGGER.debug(matched_fits[cat])

    return matched_fits


def xmatch_vizier(coord_in, cat_vizier):

    matched_vizier = {}

    for cat, opt in cat_vizier:

        # First query the catalog around input object (might have
        # several results per object)
        vizier = Vizier(columns=opt['fields'])
        cat_table = vizier.query_region(coord_in,
                                        catalog=opt['catalog'],
                                        radius=opt['dist_threshold'] * u.arcmin)

        # If we matched something, then match with the nearest object
        # in the catalog
        if len(cat_table) == 1:
            cat_table = cat_table[0]
            cat_coord = coord.SkyCoord(cat_table['_RAJ2000'],
                                       cat_table['_DEJ2000'],
                                       unit='deg', frame='icrs')

            # This is match to the nearest object
            matched_tab = xmatch(coord_in, cat_table, cat_coord, opt)

        else:
            matched_tab = None

        LOGGER.debug('Results of cross correlation with ' + cat)
        LOGGER.debug(matched_tab)

        matched_vizier[cat] = matched_tab

    return matched_vizier


def merge_tables(tab_in, matched_fits, rename_col=True):
    new = tab_in

    # put everything into the output table...
    for cat in matched_fits.keys():

        if matched_fits[cat]:
            matched_tab = matched_fits[cat]
        else:
            matched_tab = Table(masked=True)
            matched_tab.add_column(Table.Column(name='index', data=[0]))
            matched_tab.add_column(Table.Column(name='_id', data=[-1]))
            matched_tab.add_column(Table.Column(name='_sep', data=[np.nan]))


        if rename_col:
            # rename the columns according to cat (one way to do it)
            for field in matched_tab.columns.keys():
                if field not in ['index', '_id', '_sep']:
                    matched_tab.rename_column(field, cat + '_' + field)
                elif field in ['_id', '_sep']:
                    matched_tab.rename_column(field, cat + field)

        new = join(new, matched_tab, keys='index', join_type='outer')
        new[cat + '_id'].fill_value = -1
    return new


def main(argv=None):
    """The main routine for the command line program"""

    if argv is None:  # pragma: no cover
        argv = sys.argv[1:]

    try:
        args = parse_args(argv)
    except SystemExit:  # pragma: no cover
        sys.exit()

    try:
        config = parse_config(args.conf)
    except FileNotFoundError:  # pragma: no cover
        sys.exit()

    coord_in, tab_in, cat_fits, cat_vizier, output = combine_args(args, config)

    matched_cat = {}
    if cat_fits:
        matched_cat.update(xmatch_fits(coord_in, cat_fits))

    if cat_vizier:
        matched_cat.update(xmatch_vizier(coord_in, cat_vizier))

    merged_tab = merge_tables(tab_in, matched_cat)

    if output.get('filename'):
        filename = os.path.join(output.get('outdir'),
                                output.get('filename'))
        dummy, extension = os.path.splitext(filename)
        if extension == '.txt':
            ascii.write(merged_tab, filename,
                        format='commented_header', fast_writer=False)
        if extension == '.html':
            ascii.write(merged_tab, filename,
                        format='html', fast_writer=False)
        if extension == '.fits':
            merged_tab.write(filename, overwrite=True)

        if extension == '.csv':
            ascii.write(merged_tab, filename,
                        format='csv', fast_writer=False)


if __name__ == '__main__':
    main(sys.argv[1:])
