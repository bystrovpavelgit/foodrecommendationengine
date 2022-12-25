""" юнит-тесты для NLP """
import unittest
from webapp.utils.nlp_util import truncate_or_pad, get_text_array, pad, \
    get_3_rand_indices


class TestRecommender(unittest.TestCase):
    """ юнит-тесты для Recommender system """

    def setUp(self):
        """ Инит TestRecommender """
        self.max_len = 500

    def test_sum(self):
        """ summation юнит-тест """
        print("юнит-тест summation")
        self.assertEqual(sum([2, 7]), 9, "равен 9")
        self.assertEqual(sum([2, 7, 9]), 18, "равен 18")
        self.assertEqual(sum([6, 1]), 7, "равен 7")

    def test_truncate_or_pad(self):
        """ юнит-тест для truncate_or_pad """
        array = list(range(400))
        array2 = list(range(600))

        res = truncate_or_pad(array, 0, max_len=self.max_len)
        res2 = truncate_or_pad(array2, 0, max_len=self.max_len)

        self.assertIsNotNone(res, "не пустой")
        self.assertIsNotNone(res2, "не пустой")
        self.assertEqual(res[:400], list(range(400)), "result size > 400")
        self.assertEqual(res[400:], [0]*100, "добавлено 100 нулей к array")
        self.assertEqual(res2, list(range(500)), "result2 size == 500")

    def test_get_array(self):
        """ юнит-тест для pad """
        array = list(range(300))

        res = pad(array, 0, max_len=self.max_len)

        self.assertIsNotNone(res, "не пустой")
        self.assertEqual(res[:300], list(range(300)), "result size > 300")
        self.assertEqual(res[300:], [0]*200, "добавлено 200 нулей к array")

    def test_get_text_array(self):
        """ юнит-тест для get_text_array """
        data = "'0,1,2,3,4'"

        result = get_text_array(data)

        self.assertIsNotNone(result, "не пустой")
        self.assertEqual(result, ["0", "1", "2", "3", "4"], "result size == 5")

    def test_get_3_rand_indices(self):
        """ test get_3_rand_indices """
        words = ["aa", "aaa", "aaaa"]
        syn_map = {"aa": 1, "aaa": 2, "aaaa": 3}

        indices = get_3_rand_indices(words, syn_map)
        result = [words[i] for i in indices]

        self.assertIsNotNone(indices, "не пустой")
        self.assertIsNotNone(result, "не пустой")
        self.assertTrue("aa" in result, "aa")
        self.assertTrue("aaa" in result, "aaa")
        self.assertTrue("aaaa" in result, "aaaa")
