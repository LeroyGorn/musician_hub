import unittest

from hypothesis import given
from hypothesis import strategies as st


class Fibonacci:
    def __init__(self):
        self.cache = [0, 1]

    def __call__(self, n):
        # Validate the value of n
        if not (isinstance(n, int) and n >= 0):
            raise ValueError(f'Positive integer number expected, got "{n}"')

        # Check for computed Fibonacci numbers
        if n < len(self.cache):
            return self.cache[n]
        else:
            # Compute and cache the requested Fibonacci number
            fib_number = self(n - 1) + self(n - 2)
            self.cache.append(fib_number)

        return self.cache[n]


class TestFibonacci(unittest.TestCase):
    def setUp(self):
        self.fibonacci = Fibonacci()

    @given(
        x=st.integers(min_value=0, max_value=1),
    )
    def test_computed_numbers(self, x):
        self.assertEqual(self.fibonacci.__call__(x), x)

    def test_fibonacci(self):
        self.assertEqual(self.fibonacci.__call__(2), 1)
        self.assertEqual(self.fibonacci.__call__(3), 2)
        self.assertEqual(self.fibonacci.__call__(4), 3)
        self.assertEqual(self.fibonacci.__call__(5), 5)
        self.assertEqual(self.fibonacci.__call__(6), 8)
        self.assertEqual(self.fibonacci.__call__(7), 13)
        self.assertEqual(self.fibonacci.__call__(8), 21)
        self.assertEqual(self.fibonacci.__call__(9), 34)

    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(self.fibonacci.__call__(-1), 'Positive integer number expected, got "-1"')


def formatted_name(first_name, last_name, middle_name=""):
    if len(middle_name) > 0:
        full_name = first_name + " " + middle_name + " " + last_name
    else:
        full_name = first_name + " " + last_name
    return full_name.title()


class TestFormattedName(unittest.TestCase):
    def test_name(self):
        self.assertEqual(formatted_name("Michael", "Gorn", middle_name=""), "Michael Gorn")
        self.assertEqual(formatted_name("Michael", "Gorn", middle_name="Jordan"), "Michael Jordan Gorn")
        self.assertEqual(formatted_name("Michael", "Gorn"), "Michael Gorn")
        self.assertEqual(formatted_name("Michael", ""), "Michael ")
        self.assertEqual(formatted_name("", "Michael", "Jordan"), " Jordan Michael")
        self.assertEqual(formatted_name("", "Michael"), " Michael")

    @unittest.expectedFailure
    def test_exception(self):
        self.assertEqual(
            formatted_name("Michael"),
            'TypeError: formatted_name() missing 1 required positional argument: "last_name"',
        )
