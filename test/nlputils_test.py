import unittest
from webapp.utils.nlp_util import truncate_or_pad


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

        res = truncate_or_pad(array, 0, max_len=self.max_len)

        self.assertIsNotNone(res, "array не пустой")
        self.assertEqual(res[:400], list(range(400)), "array size > 400")
        self.assertEqual(res[400:], [0]*100, "добавлено 100 нулей к array")
