from hamcrest import *

class TestLights:

    def setUp(self):
        print("hello")

    def tearDown(self):
        print("good bye")

    def test_fail(self):
        # assert_that("abc", is_("def"))
        pass

    def test_pass(self):
        assert_that(["a", "b", "c"], has_item("a"))