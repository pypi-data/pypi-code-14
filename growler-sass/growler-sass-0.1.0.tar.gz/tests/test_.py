#
# tests/test.py
#

import pytest
from unittest.mock import MagicMock
from growler_sass import SassMiddleware


@pytest.fixture
def mw(tmpdir):
    return SassMiddleware(tmpdir, "/bar")

@pytest.fixture
def req(req_path):
    m = MagicMock()
    m.path = req_path
    return m

@pytest.fixture
def res():
    m = MagicMock()
    m.headers = {}
    return m


def test_growler_ext():
    'test the growler_ext extension file'
    from growler_ext import SassMiddleware as MW
    assert SassMiddleware is MW


def test_mw_fixture(mw, tmpdir):
    assert isinstance(mw, SassMiddleware)
    assert str(mw.source_dir) == str(tmpdir)
    assert mw.dest == '/bar/'


def test_constructor_non_exist():
    with pytest.raises(FileNotFoundError):
        SassMiddleware("/notadir", "/doesnot/matter")


def test_constructor_bad_dir():
    with pytest.raises(NotADirectoryError):
        SassMiddleware(__file__, "/doesnot/matter")


@pytest.mark.parametrize("path, ex", [
    ("/bar/spam.css", 'spam.sass'),
    ("/bar/spam/a/lot.css", 'spam/a/lot.sass'),
    ("bar/spam/a/lot.css", None),
    ("zoomba", None),
    ("nothing.css", None),
    ("/bar/css.csss", None),
    ("/bar/css.notcss", None),
])
def test_matches_request_pattern(mw, path, ex):
    assert mw.matches_request_pattern(path) == ex



@pytest.mark.parametrize("path, ex", [
    ("/bar/spam.css", 'spam.sass'),
    ("/bar/spam/a/lot.css.sass", 'spam/a/lot.sass'),
    ("bar/spam/a/lot.css", None),
])
def test_matches_request_pattern_extension_tuple(mw, path, ex):
    mw.MATCHING_SUFFIX = ('.css', '.css.sass')
    assert mw.matches_request_pattern(path) == ex


@pytest.mark.parametrize("req_path, files, sent", [
    ("/bar/spam.css", [], None),
    ("/spam.css", [], None),
    ("/bar/spam.css", [("spam.sas", "")], None),
    ("/bar/spam.css", [("spam.sass", "")], b''),
    ("/bar//spam.css", [("spam.sass", "")], b''),
    ("/bar/foo/../spam.css", [("spam.sass", "")], None),
    ("/bar/spam.css", [("spam.sass", "foo\n a: b")], b'foo {\n  a: b; }\n'),
])
def test_call(mw, tmpdir,files , req, res, sent):
    for f, data in files:
        tmpdir.join(f).write(data)
    mw(req, res)
    if sent is None:
        assert not res.send.called
    else:
        assert res.headers['Content-Type'] == 'text/css; charset=UTF-8'
        res.send.assert_called_with(sent)
