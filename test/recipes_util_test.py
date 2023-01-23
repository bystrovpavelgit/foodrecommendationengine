"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    recipes utility test cases
"""
import unittest
from webapp.utils.recipes_util import to_list


class TestRecipesUtil(unittest.TestCase):
    """ recipes util Test """
    def setUp(self) -> None:
        """ setUp """
        self.num = 5

    def test_to_list(self):
        """ юнит-тест для str_to_list function """
        array = "[а,роза,и,упала]\n"

        result = to_list(array)

        self.assertEqual(result, ["а", "роза", "и", "упала"], "==")
