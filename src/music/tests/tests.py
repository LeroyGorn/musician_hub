import unittest
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from hypothesis import given
from hypothesis import strategies as st

from music.models import ForumCategory, ForumComments, ForumPosted


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


def sample_forum_posted(title, **params):
    defaults = {
        "description": "Some text",
        "category": ForumCategory.objects.create(name="Misha"),
    }
    defaults.update(params)
    return ForumPosted.objects.create(title=title, **defaults)


def sample_forum_comments(**params):
    defaults = {
        "text": "text",
        "messages": sample_forum_posted(title="Test"),
    }
    defaults.update(params)
    return ForumComments.objects.create(**defaults)


class TestForumModel(TestCase):
    def setUp(self) -> None:
        self.category = ForumCategory.objects.create(name="Misha")
        self.messages_count = 1
        self.test_forum_posted = sample_forum_posted(title="test_mytest")
        self.test_forum_comments = sample_forum_comments(
            text="test_text", messages=sample_forum_posted(title="Test"), date=date(2022, 6, 8)
        )
        for i in range(self.messages_count):
            sample_forum_comments(messages=self.test_forum_posted, text="test")

    def tearDown(self) -> None:
        self.test_forum_posted.delete()

    def test_messages_count_normal_case(self):
        self.assertEqual(self.messages_count, self.test_forum_posted.messages_count())

    def test_title_limit(self):
        post_wrong_value = sample_forum_posted(title="i" * 2000)
        with self.assertRaises(ValidationError):
            post_wrong_value.full_clean()

    def test_description_limit(self):
        desc_wrong_value = sample_forum_posted(title="3", description="i" * 2000)
        with self.assertRaises(ValidationError):
            desc_wrong_value.full_clean()

    def test_category_name(self):
        self.assertEqual(str(self.category), "Misha")

    def test_date_field(self):
        with self.assertRaises(ValueError):
            self.assertEqual(
                self.test_forum_comments,
                sample_forum_comments(
                    text="test_text", messages=sample_forum_posted(title="Test"), date=date(6, 2022, 8)
                ),
            )
