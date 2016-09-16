"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        conftest.py

    FIRST RELEASE
        2016-07-06  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import json
import os.path
import pytest
from cuebung_helper import Make, Command, emit, set_emit

DIRNAME = os.path.dirname(os.path.realpath(__file__))
LIBDIR = os.path.realpath(os.path.join(DIRNAME, '..', 'lib'))

LD_PRELOAD = []
LD_PRELOAD.append(os.path.join(LIBDIR, 'emit.so'))
GFORBIDDEN = os.environ.get('GENERAL_FORBIDDEN', None)
if GFORBIDDEN is not None:
    LD_PRELOAD.append(GFORBIDDEN)
LD_PRELOAD.append(os.path.join(DIRNAME, "forbidden.so"))


def my_emit(msg):
    """Write msg as json dump to file"""
    assert isinstance(msg, dict)
    with open('output', 'a') as outputfile:
        outputfile.write(json.dumps(msg) + '\n')

set_emit(my_emit)


@pytest.fixture(scope="module")
def filename(request):
    """Fixture compiles the c program and do some prechecks"""
    program = getattr(request.module, 'PROGRAM_NAME', 'cmd')
    ignore_warnings = getattr(request.module, 'IGNORE_COMPILER_WARNINGS',
                              False)
    no_ld_pre = getattr(request.module, 'NO_LD_PRELOAD', False)
    make = Make(ignore_warnings=ignore_warnings, timeout=30)
    assert make.clean()
    assert make.test()
    fname = os.path.join(DIRNAME, program)
    if not os.path.isfile(fname):
        msg = {'msg': 'Das Program "%s" wurde nicht erstellt.' % (program)}
        emit(msg)
        assert False

    def fin():
        """finalizer"""
        emit({'msg': 'Alle Tests durchlaufen'})

    request.addfinalizer(fin)
    if no_ld_pre:
        ldp = ''
    else:
        ldp = 'LD_PRELOAD=%s' % (':'.join(LD_PRELOAD))
    return Command(ldp, fname)


# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
