""" юнит-тесты для NLP """
import unittest
from webapp.utils.nlp_util import truncate_or_pad, get_text_array, pad, \
    get_3_rand_indices, lemmatize, remove_stopwords, str_to_list, \
    get_random_synonyms


class TestRecommender(unittest.TestCase):
    """ юнит-тесты для Recommender system """

    def setUp(self):
        """ Инит TestRecommender """
        self.max_len = 500

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
        """ юнит-тест для get_3_rand_indices """
        words = ["aa", "aaa", "aaaa"]
        syn_map = {"aa": 1, "aaa": 2, "aaaa": 3}

        indices = get_3_rand_indices(words, syn_map)
        result = [words[i] for i in indices]

        self.assertIsNotNone(indices, "не пустой")
        self.assertIsNotNone(result, "не пустой")
        self.assertTrue("aa" in result, "aa")
        self.assertTrue("aaa" in result, "aaa")
        self.assertTrue("aaaa" in result, "aaaa")

    # process_synsets
    def test_lemmatize(self):
        """ юнит-тест для lemmatize """
        array = ["роза", "упала"]

        result = lemmatize(array)

        self.assertIsNotNone(result, "не пустой")
        self.assertEqual(result[0], "роза", "==")
        self.assertEqual(result[1], "упасть", "==")

    def test_remove_stopwords(self):
        """ юнит-тест для remove_stopwords """
        array = ["а", "роза", "и", "упала"]

        result = remove_stopwords(array)

        self.assertIsNotNone(result, "не пустой")
        self.assertEqual(result, "роза упала", "==")

    def test_str_to_list(self):
        """ юнит-тест для str_to_list function """
        array = "[а,роза,и,упала]\n"

        result = str_to_list(array)

        self.assertEqual(result, ["а", "роза", "и", "упала"], "==")

    def test_str_to_list_negatively(self):
        """ юнит-тест для str_to_list function """
        array = "\n"

        result = str_to_list(array)

        self.assertEqual(result, [""], "empty list")

    def test_get_random_synonyms(self):
        """ юнит-тест для get_random_synonyms """
        constants = ["b", "c", "d", "e"]
        indices = (0, 1)
        arr = ["a", "a"]
        similar = {"a": ["b", "c", "d", "e"]}

        synonyms = get_random_synonyms(arr, indices, similar)

        self.assertEqual(len(synonyms), 2, "== 2")
        self.assertEqual(synonyms[0][1], 0, "== 0")
        self.assertTrue(synonyms[0][0] in constants)
        self.assertEqual(synonyms[1][1], 1, "== 1")
        self.assertTrue(synonyms[1][0] in constants)

    def test_get_random_synonyms2(self):
        """ юнит-тест 2 для get_random_synonyms """
        constants = ["c", "d", "e"]
        indices = [0]
        arr = ["a"]
        similar = {"a": ["c", "d", "e"]}

        synonyms = get_random_synonyms(arr, indices, similar)

        self.assertEqual(len(synonyms), 1, "== 1")
        self.assertEqual(synonyms[0][1], 0, "== 0")
        self.assertTrue(synonyms[0][0] in constants)


if __name__ == "__main__":
    unittest.main()
