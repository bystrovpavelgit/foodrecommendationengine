"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    recipes utility test cases
"""
import unittest
from webapp.utils.recipes_util import to_list, \
    reorder_ids_by_index, find_enough_recommended_recipes


class TestRecipesUtil(unittest.TestCase):
    """ recipes util Test """

    def test_to_list(self):
        """ юнит-тест для str_to_list function """
        array = "[а,роза,и,упала]\n"

        result = to_list(array)

        self.assertEqual(result, ["а", "роза", "и", "упала"], "==")

    def test_reorder_ids_by_index_negatively1(self):
        """negative test of reorder_ids_by_index() when inputs are empty"""
        indices = []
        msg = []
        ids = []

        msg1, ids1 = reorder_ids_by_index(indices, [""], [0])
        msg2, ids2 = reorder_ids_by_index([1], msg, [0])
        msg3, ids3 = reorder_ids_by_index([1], [""], ids)

        self.assertEqual(msg1, [], "empty")
        self.assertEqual(msg2, [], "empty")
        self.assertEqual(msg3, [], "empty")
        self.assertEqual(ids1, [], "empty")
        self.assertEqual(ids2, [], "empty")
        self.assertEqual(ids3, [], "empty")

    def test_reorder_ids_by_index_negatively2(self):
        """
            negative test of reorder_ids_by_index function
            when inputs have different size
        """
        indices = [0]
        msg = ["", ""]
        ids = [1, 2]

        msg1, ids1 = reorder_ids_by_index(indices, msg, ids)

        self.assertEqual(msg1, [], "empty")
        self.assertEqual(ids1, [], "empty")

    def test_reorder_ids_by_index_negatively3(self):
        """ negative test of reorder_ids_by_index function
            when indices greater than length of list
        """
        indices = [5, 6]
        msg = ["", ""]
        ids = [1, 2]

        msg1, ids1 = reorder_ids_by_index(indices, msg, ids)

        self.assertEqual(msg1, [], "empty")
        self.assertEqual(ids1, [], "empty")

    def test_reorder_ids_by_index(self):
        """ test of reorder_ids_by_index function
            when indices greater than length of list
        """
        indices = [2, 1, 0]
        msg = ["m1", "m2", "m3"]
        ids = [0, 1, 2]

        msg1, ids1 = reorder_ids_by_index(indices, msg, ids)

        self.assertEqual(msg1[0], "m3", "== m3")
        self.assertEqual(msg1[2], "m1", "== m1")
        self.assertEqual(ids1[0], 2, "== 2")
        self.assertEqual(ids1[2], 0, "== 0")

    def test_find_enough_recommended_recipes_negatively(self):
        """ test of find_enough_recommended_recipes function
            when cuisine and ish type are None
        """
        cuisine, dish = None, None

        msg1, ids1 = find_enough_recommended_recipes(0, cuisine, dish)

        self.assertEqual(msg1, [], "empty")
        self.assertEqual(ids1, [], "empty")
