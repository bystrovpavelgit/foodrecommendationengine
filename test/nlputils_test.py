""" юнит-тесты для NLP """
import unittest
from webapp.utils.nlp_util import truncate_or_pad, get_text_array, pad, \
    get_3_rand_indices, lemmatize, remove_stopwords, str_to_list, \
    get_random_synonyms, process_synsets, get_similar_directions, \
    remove_duplicates


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
        self.assertEqual(res[400:], [0] * 100, "добавлено 100 нулей к array")
        self.assertEqual(res2, list(range(500)), "result2 size == 500")

    def test_truncate_or_pad_negatively(self):
        """ юнит-тест для truncate_or_pad """
        try:
            res = truncate_or_pad(None, None, max_len=self.max_len)

            self.assertIsNotNone(res, "не пустой")
        except ValueError as err:
            self.assertIsNotNone(err, "не пустой")

    def test_get_array(self):
        """ юнит-тест для pad """
        array = list(range(300))

        res = pad(array, 0, max_len=self.max_len)

        self.assertIsNotNone(res, "не пустой")
        self.assertEqual(res[:300], list(range(300)), "result size > 300")
        self.assertEqual(res[300:], [0] * 200, "добавлено 200 нулей к array")

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
        result = [words[index] for index in indices]

        self.assertIsNotNone(indices, "не пустой")
        self.assertIsNotNone(result, "не пустой")
        self.assertTrue("aa" in result, "aa")
        self.assertTrue("aaa" in result, "aaa")
        self.assertTrue("aaaa" in result, "aaaa")

    def test_get_3_rand_indices_negatively2(self):
        """ юнит-тест для get_3_rand_indices """
        syn_map = {"aa": 1, "aaa": 2, "aaaa": 3}

        indices = get_3_rand_indices(None, syn_map)

        self.assertEqual(indices, [])

    def test_get_3_rand_indices_negatively3(self):
        """ юнит-тест для get_3_rand_indices """
        words = ["aa", "aaa", "aaaa"]

        indices = get_3_rand_indices(words, None)

        self.assertEqual(indices, [])

    # process_synsets
    def test_lemmatize(self):
        """ юнит-тест для lemmatize """
        array = ["роза", "упала"]

        result = lemmatize(array)

        self.assertEqual(result[0], "роза", "==")
        self.assertEqual(result[1], "упасть", "==")

    def test_lemmatize_negatively(self):
        """ юнит-тест для lemmatize """
        array = []

        result = lemmatize(array)

        self.assertEqual(result, [], "Empty")

    def test_remove_stopwords(self):
        """ юнит-тест для remove_stopwords """
        array = ["а", "роза", "и", "упала"]

        result = remove_stopwords(array)

        self.assertEqual(result, "роза упала", "==")

    def test_remove_stopwords_negatively(self):
        """ юнит-тест для remove_stopwords """
        array = []

        result = remove_stopwords(array)

        self.assertEqual(result, "", "Empty")

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

    def test_get_random_synonyms3(self):
        """ юнит-тест 3 для get_random_synonyms """
        similar = {"a": ["c", "d", "e"]}

        synonyms = get_random_synonyms(None, None, similar)

        self.assertEqual(synonyms, [])

    def test_get_random_synonyms4(self):
        """ юнит-тест 4 для get_random_synonyms """
        indices = [0]
        arr = ["a"]

        synonyms = get_random_synonyms(arr, indices, None)

        self.assertEqual(synonyms, [])

    def test_process_synsets_negatively(self):
        """ юнит-тест для process_synsets """
        result = process_synsets(csvfile=None)

        self.assertEqual(result, {})

    def test_get_similar_directions_negatively2(self):
        """ юнит-тест для get_similar_directions """
        try:
            result = get_similar_directions(None, None)

            self.assertIsNotNone(result, "не пустой")
        except ValueError as err:
            self.assertIsNotNone(err)

    def test_get_similar_directions_negatively3(self):
        """ юнит-тест для get_similar_directions """
        try:
            result = get_similar_directions([], {})

            self.assertIsNotNone(result, "не пустой")
        except ValueError as err:
            self.assertIsNotNone(err)

    def test_remove_duplicates_negatively1(self):
        """ юнит-тест для remove_duplicates """
        try:
            result = remove_duplicates(None, None)

            self.assertIsNotNone(result, "не пустой")
        except ValueError as err:
            self.assertIsNotNone(err)

    def test_remove_duplicates_negatively2(self):
        """ юнит-тест для remove_duplicates """
        try:
            result = remove_duplicates([], [])

            self.assertIsNotNone(result, "не пустой")
        except ValueError as err:
            self.assertIsNotNone(err)


if __name__ == "__main__":
    unittest.main()
