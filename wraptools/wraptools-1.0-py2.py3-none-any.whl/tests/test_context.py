import unittest


from wraptools import context


class TestContext(unittest.TestCase):
    def test__decorator(self):
        def context_function(i):
            return {1: 'user1', 2: 'user2'}.get(i)

        def view(i, user):
            return i, user

        wrapped_func = context.context(context_function)(view)
        self.assertEqual(wrapped_func(1), (1, 'user1'))
        self.assertEqual(wrapped_func(2), (2, 'user2'))
        self.assertEqual(wrapped_func(3), (3, None))
