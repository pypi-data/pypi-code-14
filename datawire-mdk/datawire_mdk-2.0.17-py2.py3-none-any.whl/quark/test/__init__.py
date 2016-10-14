# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.test")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent
import quark.logging


class TestInitializer(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def getValue(self):
        return _cast(None, lambda: Test)

    def _getClass(self):
        return u"quark.test.TestInitializer"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
TestInitializer.quark_test_TestInitializer_ref = None

def red(str):
    return ((u"\x1b[31;1m") + (str)) + (u"\x1b[0m")


def green(str):
    return ((u"\x1b[32;1m") + (str)) + (u"\x1b[0m")


def bold(str):
    return ((u"\x1b[1m") + (str)) + (u"\x1b[0m")


def heading(str):
    padding = u"=";
    target_width = 78;
    res = (((padding) + (u" ")) + (str)) + (u" ");
    count = ((target_width) - (len(res))) // (len(padding));
    block = (padding) * ((count) // (2));
    extra = u"";
    if (((count) % (2)) == (1)):
        extra = padding

    return bold(((((block) + (res)) + (block)) + (extra)).strip())

class Test(_QObject):
    def _init(self):
        self.name = None
        self.checks = 0
        self.successes = _List([])
        self.failures = _List([])

    def __init__(self, name):
        self._init()
        (self).name = name

    @staticmethod
    def current():
        return (Test.ctx).getValue()

    def match(self, filters):
        if (((filters) == (None)) or ((len(filters)) == (0))):
            return True

        idx = 0;
        while ((idx) < (len(filters))):
            filter = (filters)[idx];
            if (((self.name).find(filter)) >= (0)):
                return True

            idx = (idx) + (1)

        return False

    def start(self):
        (Test.ctx).setValue(self);

    def stop(self):
        result = (((((self.name) + (u" [")) + (_toString(self.checks))) + (u" checks, ")) + (_toString(len(self.failures)))) + (u" failures]");
        if ((len(self.failures)) > (0)):
            _println(red(result));
        else:
            _println(bold(result));

        idx = 0;
        while ((idx) < (len(self.successes))):
            _println(green((u"  PASS: ") + ((self.successes)[idx])));
            idx = (idx) + (1)

        idx = 0
        while ((idx) < (len(self.failures))):
            _println(red((u"  FAIL: ") + ((self.failures)[idx])));
            idx = (idx) + (1)

        (Test.ctx).setValue(None);

    def check(self, value, message):
        self.checks = (self.checks) + (1)
        if (value):
            (self.successes).append(message);
        else:
            (self.failures).append(message);

        return value

    def fail(self, message):
        self.check(False, message);

    def run(self):
        pass

    def _getClass(self):
        return u"quark.test.Test"

    def _getField(self, name):
        if ((name) == (u"ctx")):
            return Test.ctx

        if ((name) == (u"name")):
            return (self).name

        if ((name) == (u"checks")):
            return (self).checks

        if ((name) == (u"successes")):
            return (self).successes

        if ((name) == (u"failures")):
            return (self).failures

        return None

    def _setField(self, name, value):
        if ((name) == (u"ctx")):
            Test.ctx = _cast(value, lambda: _TLS)

        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)

        if ((name) == (u"checks")):
            (self).checks = _cast(value, lambda: int)

        if ((name) == (u"successes")):
            (self).successes = _cast(value, lambda: _List)

        if ((name) == (u"failures")):
            (self).failures = _cast(value, lambda: _List)


Test.ctx = _TLS(TestInitializer())
Test.quark_test_Test_ref = None
class SafeMethodCaller(_QObject):
    def _init(self):
        self.method = None
        self.test = None

    def __init__(self, method, test):
        self._init()
        (self).method = method
        (self).test = test

    def call(self, ignore):
        (self.method).invoke(self.test, _List([]));
        return True

    @staticmethod
    def callMethod(method, test):
        if (SafeMethodCaller.useSafeCalls):
            callable = SafeMethodCaller(method, test);
            return _cast((quark.concurrent.Context.runtime()).callSafely(callable, False), lambda: bool)

        (method).invoke(test, _List([]));
        return True

    def _getClass(self):
        return u"quark.test.SafeMethodCaller"

    def _getField(self, name):
        if ((name) == (u"useSafeCalls")):
            return SafeMethodCaller.useSafeCalls

        if ((name) == (u"method")):
            return (self).method

        if ((name) == (u"test")):
            return (self).test

        return None

    def _setField(self, name, value):
        if ((name) == (u"useSafeCalls")):
            SafeMethodCaller.useSafeCalls = _cast(value, lambda: bool)

        if ((name) == (u"method")):
            (self).method = _cast(value, lambda: quark.reflect.Method)

        if ((name) == (u"test")):
            (self).test = value


SafeMethodCaller.useSafeCalls = True
SafeMethodCaller.quark_test_SafeMethodCaller_ref = None
class MethodTest(Test):
    def _init(self):
        Test._init(self)
        self.klass = None
        self.method = None

    def __init__(self, klass, method):
        super(MethodTest, self).__init__((((klass).getName()) + (u".")) + ((method).getName()));
        (self).klass = klass
        (self).method = method

    def run(self):
        setup = (self.klass).getMethod(u"setup");
        teardown = (self.klass).getMethod(u"teardown");
        test = (self.klass).construct(_List([]));
        if ((setup) != (None)):
            if (not (SafeMethodCaller.callMethod(setup, test))):
                fail(u"setup invocation crashed");

        if (not (SafeMethodCaller.callMethod(self.method, test))):
            fail(u"test invocation crashed");

        if ((teardown) != (None)):
            if (not (SafeMethodCaller.callMethod(teardown, test))):
                fail(u"teardown invocation crashed");

    def _getClass(self):
        return u"quark.test.MethodTest"

    def _getField(self, name):
        if ((name) == (u"ctx")):
            return Test.ctx

        if ((name) == (u"name")):
            return (self).name

        if ((name) == (u"checks")):
            return (self).checks

        if ((name) == (u"successes")):
            return (self).successes

        if ((name) == (u"failures")):
            return (self).failures

        if ((name) == (u"klass")):
            return (self).klass

        if ((name) == (u"method")):
            return (self).method

        return None

    def _setField(self, name, value):
        if ((name) == (u"ctx")):
            Test.ctx = _cast(value, lambda: _TLS)

        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)

        if ((name) == (u"checks")):
            (self).checks = _cast(value, lambda: int)

        if ((name) == (u"successes")):
            (self).successes = _cast(value, lambda: _List)

        if ((name) == (u"failures")):
            (self).failures = _cast(value, lambda: _List)

        if ((name) == (u"klass")):
            (self).klass = _cast(value, lambda: quark.reflect.Class)

        if ((name) == (u"method")):
            (self).method = _cast(value, lambda: quark.reflect.Method)


MethodTest.quark_test_MethodTest_ref = None

def check(value, message):
    return (Test.current()).check(value, message)


def checkEqual(expected, actual):
    return (Test.current()).check((expected) == (actual), (((u"expected ") + (_toString(expected))) + (u" got ")) + (_toString(actual)))


def fail(message):
    (Test.current()).check(False, message);


def checkOneOf(expected, actual):
    message = u"Expected one of [";
    idx = 0;
    success = False;
    while ((idx) < (len(expected))):
        if ((idx) != (0)):
            message = (message) + (u", ")

        message = (message) + (_toString((expected)[idx]))
        if (((expected)[idx]) == (actual)):
            success = True

        idx = (idx) + (1)

    message = ((message) + (u"] got ")) + (_toString(actual))
    return check(success, message)

class Harness(_QObject):
    def _init(self):
        self.pkg = None
        self.tests = _List([])
        self.filtered = 0

    def __init__(self, pkg):
        self._init()
        (self).pkg = pkg

    def collect(self, filters):
        names = _List(list((quark.reflect.Class.classes).keys()));
        (names).sort();
        idx = 0;
        pfx = (self.pkg) + (u".");
        while ((idx) < (len(names))):
            name = (names)[idx];
            if (((name).startswith(pfx)) and ((name).endswith(u"Test"))):
                klass = quark.reflect.Class.get(name);
                methods = (klass).getMethods();
                jdx = 0;
                while ((jdx) < (len(methods))):
                    meth = (methods)[jdx];
                    mname = (meth).getName();
                    if (((mname).startswith(u"test")) and ((len((meth).getParameters())) == (0))):
                        test = MethodTest(klass, meth);
                        if ((test).match(filters)):
                            (self.tests).append(test);
                        else:
                            self.filtered = (self.filtered) + (1)

                    jdx = (jdx) + (1)

            idx = (idx) + (1)

    def list(self):
        idx = 0;
        while ((idx) < (len(self.tests))):
            test = (self.tests)[idx];
            _println((test).name);
            idx = (idx) + (1)

    def run(self):
        """
        Run the tests, return number of failures.
        """
        _println(heading(u"starting tests"));
        idx = 0;
        failures = 0;
        while ((idx) < (len(self.tests))):
            test = (self.tests)[idx];
            (test).start();
            (test).run();
            (test).stop();
            if ((len((test).failures)) > (0)):
                failures = (failures) + (1)

            idx = (idx) + (1)

        passed = (len(self.tests)) - (failures);
        _println(heading(u"stopping tests"));
        result = (((((((u"Total: ") + (_toString((len(self.tests)) + (self.filtered)))) + (u", Filtered: ")) + (_toString(self.filtered))) + (u", Passed: ")) + (_toString(passed))) + (u", Failed: ")) + (_toString(failures));
        if ((failures) > (0)):
            _println(red(result));
        else:
            _println(green(result));

        return failures

    def json_report(self):
        _println(u"=============================== json report ===============================");
        idx = 0;
        report = _JSONObject();
        while ((idx) < (len(self.tests))):
            item = _JSONObject();
            test = (self.tests)[idx];
            f = 0;
            failures = _JSONObject();
            while ((f) < (len((test).failures))):
                (failures).setListItem(f, (_JSONObject()).setString(((test).failures)[f]));
                f = (f) + (1)

            (item).setObjectItem((u"name"), ((_JSONObject()).setString((test).name)));
            (item).setObjectItem((u"checks"), ((_JSONObject()).setNumber((test).checks)));
            (item).setObjectItem((u"failures"), (failures));
            (report).setListItem(idx, item);
            idx = (idx) + (1)

        _println((report).toString());

    def _getClass(self):
        return u"quark.test.Harness"

    def _getField(self, name):
        if ((name) == (u"pkg")):
            return (self).pkg

        if ((name) == (u"tests")):
            return (self).tests

        if ((name) == (u"filtered")):
            return (self).filtered

        return None

    def _setField(self, name, value):
        if ((name) == (u"pkg")):
            (self).pkg = _cast(value, lambda: unicode)

        if ((name) == (u"tests")):
            (self).tests = _cast(value, lambda: _List)

        if ((name) == (u"filtered")):
            (self).filtered = _cast(value, lambda: int)


Harness.quark_List_quark_test_Test__ref = None
Harness.quark_test_Harness_ref = None

def testPackages(packages, filters, emitJson):
    h = Harness(u"");
    total_failures = 0;
    idx = 0;
    while ((idx) < (len(packages))):
        (h).pkg = (packages)[idx]
        (h).collect(filters);
        idx = (idx) + (1)

    total_failures = (h).run()
    if (emitJson):
        (h).json_report();

    return total_failures


def run(args):
    ((quark.logging.makeConfig()).setLevel(u"INFO")).configure();
    pkg = (args)[0];
    filters = _List([]);
    qlist = False;
    json = False;
    idx = 1;
    while ((idx) < (len(args))):
        arg = (args)[idx];
        if ((arg) == (u"-l")):
            qlist = True
        else:
            if ((arg) == (u"--json")):
                json = True
            else:
                if ((arg) == (u"--unsafe")):
                    SafeMethodCaller.useSafeCalls = False
                else:
                    (filters).append(arg);

        idx = (idx) + (1)

    if (qlist):
        h = Harness(pkg);
        (h).collect(filters);
        (h).list();
    else:
        _println(bold((u"Running: ") + ((u" ").join(args))));
        failures = testPackages(_List([pkg]), filters, json);
        if ((failures) > (0)):
            (quark.concurrent.Context.runtime()).fail(u"Test run failed.");




def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.test")
