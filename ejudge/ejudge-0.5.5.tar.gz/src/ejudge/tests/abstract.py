import pytest

from ejudge import functions
from iospec import parse_string, types, SimpleTestCase


def source_property(name):
    @property
    def source_property(self):
        return self.get_source(name)
    return source_property


class TestLanguageSupport:
    base_iospec_source = (
        'name: <foo>\n'
        'hello foo!\n'
        '\n'
        'name: <bar>\n'
        'hello bar!'
    )
    base_lang = None
    source_all = None
    source_ok = source_property('ok')
    source_wrong = source_property('wrong')
    source_syntax = source_property('syntax')
    source_recursive = source_property('recursive')
    source_error = source_property('error')

    @pytest.fixture
    def iospec(self):
        return parse_string(self.base_iospec_source)

    @pytest.fixture
    def lang(self):
        return self.base_lang

    @pytest.fixture
    def src_ok(self):
        return self.source_ok

    @pytest.fixture
    def src_wrong(self):
        return self.source_wrong

    @pytest.fixture
    def src_syntax(self):
        return self.source_syntax

    @pytest.fixture
    def src_recursive(self):
        return self.source_recursive

    @pytest.fixture
    def src_error(self):
        return self.source_error

    def get_source(self, name):
        if self.source_all is None:
            return None

        _, sep, data = self.source_all.partition('## %s\n' % name)
        if not sep:
            return None
        data, _, _ = data.partition('\n## ')
        return data.strip()

    # Test simple io.run() interactions
    def test_run_valid_source(self, src_ok, lang, timeout=None, sandbox=False):
        tree = functions.run(src_ok, ['foo'], lang=lang, sandbox=sandbox,
                             timeout=timeout,
                             raises=True)
        try:
            assert len(tree) == 1
            case = tree[0]
            assert isinstance(case, SimpleTestCase)
            assert case[0] == 'name: '
            assert case[1] == 'foo'
            assert case[2] == 'hello foo!'
        except Exception:
            tree.pprint()
            raise

    def test_run_valid_source_with_timeout(self, src_ok, lang):
        self.test_run_valid_source(src_ok, lang, timeout=1.0)

    @pytest.mark.sandbox
    def test_run_valid_source_with_sandbox(self, src_ok, lang):
        self.test_run_valid_source(src_ok, lang, sandbox=True)

    @pytest.mark.sandbox
    def test_run_valid_source_with_sandbox_and_timeout(self, src_ok, lang):
        self.test_run_valid_source(src_ok, lang, sandbox=True, timeout=1.0)

    def test_run_source_with_runtime_error(self, src_error, lang):
        tree = functions.run(src_error, ['foo'], lang=lang, sandbox=False)
        assert tree[0].error_type == 'runtime'

    def test_run_from_input_sequence(self, src_ok, lang):
        inputs = [['foo'], ['bar']]
        tree = functions.run(src_ok, inputs, lang=lang, sandbox=False)
        assert len(tree) == 2
        assert tree[0][2] == 'hello foo!'
        assert tree[1][2] == 'hello bar!'

    def test_run_valid_source_from_iospec_input(self, src_ok, lang):
        case1 = types.SimpleTestCase([types.In('foo'), types.Out('foo')])
        case2 = types.InputTestCase([types.In('bar')])
        inpt = types.IoSpec([case1, case2])
        tree = functions.run(src_ok, inpt, lang=lang, sandbox=False)
        assert len(tree) == 2
        assert tree[0][2] == 'hello foo!'
        assert tree[1][2] == 'hello bar!'

    def test_run_code_with_syntax_error(self, src_syntax, lang):
        ast = functions.run(src_syntax, ['foo'], lang=lang, sandbox=False)
        assert len(ast) == 1
        assert isinstance(ast[0], types.ErrorTestCase)
        assert ast[0].error_type == 'build'

    def test_run_recursive_function(self, src_recursive):
        result = functions.run(src_recursive, [()], lang='python', sandbox=False)
        assert list(result[0]) == ['120']

    @pytest.mark.sandbox
    def test_run_recursive_function_in_sandbox(self, src_recursive, lang):
        result = functions.run(src_recursive, [()], lang=lang, sandbox=True)
        assert list(result[0]) == ['120']

    # Test grading and check if the feedback is correct
    def test_valid_source_receives_maximum_grade(self, iospec, src_ok, lang):
        feedback = functions.grade(src_ok, iospec, lang=lang, sandbox=False)
        assert isinstance(feedback.answer_key, types.TestCase)
        assert isinstance(feedback.testcase, types.TestCase)
        assert feedback.grade == 1
        assert feedback.message is None
        assert feedback.status == 'ok'

    def test_wrong_source_receives_null_grade(self, iospec, src_wrong, lang):
        feedback = functions.grade(src_wrong, iospec, lang=lang, sandbox=False)
        assert feedback.grade == 0
        assert feedback.status == 'wrong-answer'
        assert feedback.title == 'Wrong Answer'
