""" юнит-тесты для Recommender system """
import unittest
from webapp.dl import CFRecommender, get_unique_user_map, get_actual_users, \
    get_unique_item_map, find_n_closest_users, get_users_items_matrix, \
    get_items_popularities


class TestRecommender(unittest.TestCase):
    """ юнит-тесты для Recommender system """

    def setUp(self):
        """ Инит TestRecommender """
        self.recommender = CFRecommender()

    def prepare_data(self):
        """ подготовка данных """
        self.recommender.get_pretrained_embeddings()
        embed = self.recommender.users_embedding
        ratings = self.recommender.get_ratings()
        user_dict = get_unique_user_map(ratings, get_actual_users(ratings))
        self.recommender.set_user_dict(user_dict)
        item_dict = get_unique_item_map(ratings,
                                        self.recommender.get_actual_items())
        self.recommender.set_item_dict(item_dict)
        all_users = get_actual_users(ratings)
        tupl_ = find_n_closest_users(2,
                               all_users,
                               user_dict,
                               embed,
                               n=20)
        self.recommender.closest_users = tupl_[0]
        self.recommender.similarities = tupl_[1]
        self.recommender.matr = get_users_items_matrix(
            self.recommender.get_ratings())
        self.recommender.popularity = get_items_popularities(
            self.recommender.get_ratings())

    def test_get_pretrained_embeddings(self):
        """ get_pretrained_embeddings юнит-тест """
        print("юнит-тест get_pretrained_embeddings")
        self.assertIsNotNone(self.recommender,
                             "recommender не инициализирован")
        self.assertIsNone(self.recommender.users_embedding,
                          "users_embedding не пустой")

        self.recommender.get_pretrained_embeddings()

        self.assertIsNotNone(self.recommender.users_embedding,
                             "users_embedding не инициализирован")
        self.assertTrue(self.recommender.users_embedding.shape[0] > 0,
                        "users_embedding не пустой")

    def test_find_rating_for_dish(self):
        """ test_find_rating_for_dish юнит-тест """
        print("юнит-тест find_rating_for_dish")
        self.assertIsNone(self.recommender.users_embedding,
                          "users_embedding не пустой")

        self.prepare_data()
        rate = self.recommender.find_rating_for_dish(2, 350)

        self.assertEqual(rate, 1., "item_rating для блюда 350 = 1.")

    def test_find_top_items_for_rating(self):
        """ test_find_top_items_for_rating юнит-тест """
        print("юнит-тест find_top_items_for_rating")
        self.assertIsNone(self.recommender.users_embedding,
                          "users_embedding не пустой")

        self.prepare_data()
        rating_list = self.recommender.find_100_closest_ratings_for_user(2)
        top_items = self.recommender.find_top_items_for_rating(rating_list)

        self.assertGreaterEqual(len(rating_list), 100, "длина ratings >= 100")
        self.assertGreaterEqual(len(top_items), 100, "длина top_items >= 100")


if __name__ == "__main__":
    """ unittest """
    unittest.main()
