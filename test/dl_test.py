import unittest
import numpy as np
import pandas as pd
from webapp.dl import l2_norm, cosine_sim, average_rating, \
    get_actual_users, get_unique_user_map, get_users_items_matrix, \
    insert_users_and_recipes_into_df


class DeepLearningTest(unittest.TestCase):
    """ юнит-тесты для утилиты вычисления моделей dl.py """

    def setUp(self):
        self.ratings = pd.read_csv("data/users_ratings.csv")
        insert_users_and_recipes_into_df(self.ratings)
        self.ratings['rating'] =\
            self.ratings['rating'].values.astype(np.float32)
        self.user_dict = get_unique_user_map(self.ratings,
                                             get_actual_users(self.ratings))
        self.matrix = get_users_items_matrix(self.ratings)

    def test_l2_norm(self):
        """ l2_norm юнит-тест """
        vector1 = np.array([0.5, -0.5, 0.5, -0.5])
        vector2 = np.array([0.4, 0.3])

        norm1 = l2_norm(vector1)
        norm2 = l2_norm(vector2)

        self.assertEqual(norm1, 1., "равна 1")
        self.assertEqual(norm2, 0.5, "равна 0.5")

    def test_cosine_sim(self):
        """ cosine similarity юнит-тест """
        vector1 = np.array([0.5, -0.5, 0.5, -0.5])
        vector2 = np.array([0.4, -0.5, 0.5, 0.0])
        vector3 = np.array([1, -1, 1, -1])

        similarity1 = cosine_sim(vector1, vector3)
        similarity2 = cosine_sim(vector1, vector2)

        self.assertTrue(similarity1 > 0.99, "cosine similarity равна 1")
        self.assertTrue(similarity2 < 0.9, "cosine similarity меньше 0.9")

    def test_average_rating(self):
        """ """
        user_id = 3

        avg_rating = average_rating(self.user_dict[user_id], self.matrix)
        print(f"average_rating {avg_rating}")

        self.assertTrue(avg_rating > 0.01, "> 0.01")


if __name__ == "__main__":
    unittest.main()
