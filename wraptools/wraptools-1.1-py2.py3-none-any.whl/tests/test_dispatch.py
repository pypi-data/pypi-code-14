import unittest


from wraptools import dispatch


def even(n):
    return n % 2 == 0


def multiple_three(n):
    return n % 3 == 0


class TestDispatch(unittest.TestCase):
    def test__dispatched(self):
        target = dispatch.dispatch(
            (even, lambda n: "even"),
            (multiple_three, lambda n: "multiple three"),
        )
        self.assertEqual(target(2), "even")
        self.assertEqual(target(3), "multiple three")
        self.assertEqual(target(4), "even")

    def test__default(self):
        target = dispatch.dispatch(
            (even, lambda n: "even"),
            default=lambda n: "anything else"
        )
        self.assertEqual(target(1), "anything else")
        self.assertEqual(target(2), "even")

    def test__default_but_without_func(self):
        target = dispatch.dispatch(
            (even, lambda n: "even"),
        )
        self.assertEqual(target(1), None)


class TestAll(unittest.TestCase):
    def test(self):
        target = dispatch.all_(even, multiple_three)
        self.assertEqual(target(2), False)
        self.assertEqual(target(3), False)
        self.assertEqual(target(5), False)
        self.assertEqual(target(6), True)


class TestAny(unittest.TestCase):
    def test(self):
        target = dispatch.any_(even, multiple_three)
        self.assertEqual(target(2), True)
        self.assertEqual(target(3), True)
        self.assertEqual(target(5), False)
        self.assertEqual(target(6), True)


class TestNot(unittest.TestCase):
    def test(self):
        target = dispatch.not_(even)
        self.assertEqual(target(2), False)
        self.assertEqual(target(3), True)
        self.assertEqual(target(5), True)
        self.assertEqual(target(6), False)


class TestDispatcher(unittest.TestCase):
    def test__wrap(self):
        @dispatch.dispatcher
        def wrapped(mail):
            return mail.endswith("@admin.com")

        self.assertEqual(wrapped("me@admin.com"), True)
        self.assertEqual(wrapped("me@other.com"), False)

    def test__and(self):
        w_even = dispatch.dispatcher(even)
        w_multiple_three = dispatch.dispatcher(multiple_three)
        target = w_even & w_multiple_three
        self.assertEqual(target(2), False)
        self.assertEqual(target(3), False)
        self.assertEqual(target(5), False)
        self.assertEqual(target(6), True)

    def test__or(self):
        w_even = dispatch.dispatcher(even)
        w_multiple_three = dispatch.dispatcher(multiple_three)
        target = w_even | w_multiple_three
        self.assertEqual(target(2), True)
        self.assertEqual(target(3), True)
        self.assertEqual(target(5), False)
        self.assertEqual(target(6), True)

    def test__not(self):
        w_even = dispatch.dispatcher(even)
        target = ~w_even
        self.assertEqual(target(2), False)
        self.assertEqual(target(3), True)
        self.assertEqual(target(5), True)
        self.assertEqual(target(6), False)
