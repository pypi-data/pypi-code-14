import unittest


class DecoratorsTestCase(unittest.TestCase):
    def test_anonymous_decorator(self):

        from rest_test import RestTestCase

        @RestTestCase.anonymous_user.can_create
        class DecoratedTest(RestTestCase):
            pass

        self.assertEqual(DecoratedTest.anonymous_user.allowed_operations, {'create'})

    def test_multiple_anonymous_decorators(self):

        from rest_test import RestTestCase

        @RestTestCase.anonymous_user.can_create
        @RestTestCase.anonymous_user.can_retrieve
        class DecoratedTest(RestTestCase):
            pass

        self.assertEqual(DecoratedTest.anonymous_user.allowed_operations, {'create', 'retrieve'})

    def test_inheritance_decorator(self):
        from rest_test import RestTestCase

        class MyTest(RestTestCase):
            pass

        @MyTest.anonymous_user.can_create
        class DecoratedTest(RestTestCase):
            pass

        self.assertEqual(MyTest.anonymous_user.allowed_operations, set())
        self.assertEqual(DecoratedTest.anonymous_user.allowed_operations, {'create'})

    def test_strange_inheritance_decorator(self):
        from rest_test import RestTestCase

        class MyTest(RestTestCase):
            pass

        @RestTestCase.anonymous_user.can_create
        class DecoratedTest(MyTest):
            pass

        self.assertEqual(MyTest.anonymous_user.allowed_operations, set())
        self.assertEqual(DecoratedTest.anonymous_user.allowed_operations, {'create'})


if __name__ == '__main__':
    unittest.main()
