from hamcrest import *
import unittest

class TestLights:

    def setUp(self):
        print("hello")

    def tearDown(self):
        print("good bye")

    def test_fail(self):
        assert_that("abc", is_("def"))

    def test_pass(self):
        assert_that(["a", "b", "c"], has_item("a"))