"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    DL constants
"""
from copy import copy
from functools import reduce
import pickle
import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from webapp.utils.nlp_util import tokenize_recipe, truncate_or_pad
from keras.layers import Add, Activation, Lambda, Input, Embedding
from keras.layers import Reshape, Flatten, Dot
from tensorflow.keras.models import Sequential, Model, load_model, save_model
from keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

TYPE_MAP = {0: "вторые блюда",
            1: "десерты",
            2: "завтраки",
            3: "закуски",
            4: "салаты",
            5: "соусы",
            6: "супы и первые блюда"}
CUISINES = {0: "европейская",
            1: "русская",
            2: "азиатская",
            3: "африканская",
            4: "мексиканская"}


def predict_types(recipe):
    """ predict types """
    with open("models/vocabulary.pkl", "rb") as v_file:
        vocab = pickle.load(v_file)
    part1, part2 = tokenize_recipe(recipe, "еос")
    dirs = truncate_or_pad([vocab.get(w) if w in vocab else 0 for w in part1], 0)
    ingredients = truncate_or_pad([vocab.get(w) if w in vocab else 0 for w in part2], 0)[:100]
    res = dirs + ingredients

    model = keras.models.load_model("models/new_rnn_cuisine.h5")
    arr = np.array([res])
    pred = model.predict(arr[..., None])
    cuisine = np.argmax(pred)
    model = keras.models.load_model("models/new_rnn2_dish_type.h5")
    arr = np.array([res])
    pred = model.predict(arr[..., None])
    type_pred = np.argmax(pred)
    print("result", CUISINES[int(cuisine)], TYPE_MAP[int(type_pred)])
    return CUISINES[int(cuisine)], TYPE_MAP[int(type_pred)]


def get_actual_items(ratings):
    """ get_actual_items """
    actual_items = list(set(ratings['recipeId'].values.tolist()))
    return actual_items


def get_actual_users(ratings):
    """ get_actual_users """
    actual_users = list(set(ratings['userId'].values.tolist()))
    return actual_users


def get_unique_user_map(ratings, actual_users):
    """ get_unique_user_map """
    user_enc = LabelEncoder()
    user_enc.fit(ratings['userId'].values)
    res = {el: user_enc.transform([el])[0] for el in actual_users}
    del user_enc
    return res


def get_unique_item_map(ratings, actual_items):
    """ get_unique_item_map """
    item_enc = LabelEncoder()
    item_enc.fit(ratings['recipeId'].values)
    res = {el: item_enc.transform([el])[0] for el in actual_items}
    del item_enc
    return res


def insert_users_and_recipes_into_df(df):
    """ insert users and recipes into dataframe"""
    user_enc = LabelEncoder()
    df['user'] = user_enc.fit_transform(df['userId'].values)
    item_enc = LabelEncoder()
    df['recipe'] = item_enc.fit_transform(df['recipeId'].values)
    del user_enc, item_enc


def load_users_and_ratings_as_x_y_df(users_csv="data/users_ratings.csv"):
    """ load users and ratings as x, y, dataframe """
    ratings = pd.read_csv(users_csv)
    insert_users_and_recipes_into_df(ratings)
    ratings['rating'] = ratings['rating'].values.astype(np.float32)
    x = ratings[['user', 'recipe']].values
    y = ratings['rating'].values
    return x, y, ratings


def get_train_test_arrays(x_train, x_test):
    """ get train test arrays """
    x_train_array = [x_train[:, 0], x_train[:, 1]]
    x_test_array = [x_test[:, 0], x_test[:, 1]]
    return x_train_array, x_test_array


class EmbeddingLayer:
    """ Embedding Layer """
    def __init__(self, n_items, n_factors):
        self.n_items = n_items
        self.n_factors = n_factors

    def __call__(self, x):
        x = Embedding(self.n_items, self.n_factors, embeddings_initializer='he_normal',
                      embeddings_regularizer=l2(1e-6))(x)
        x = Reshape((self.n_factors,))(x)
        return x


def recommender_v2(n_users, n_items, n_factors, min_rating, max_rating):
    """ Recommender V2 """
    user = Input(shape=(1,))
    u = EmbeddingLayer(n_users, n_factors)(user)
    ub = EmbeddingLayer(n_users, 1)(user)
    movie = Input(shape=(1,))
    m = EmbeddingLayer(n_items, n_factors)(movie)
    mb = EmbeddingLayer(n_items, 1)(movie)
    x = Dot(axes=1)([u, m])
    x = Add()([x, ub, mb])
    x = Activation('sigmoid')(x)
    x = Lambda(lambda t: t * (max_rating - min_rating) + min_rating)(x)
    model = Model(inputs=[user, movie], outputs=x)
    opt = Adam(learning_rate=0.001)
    model.compile(loss='mean_squared_error', optimizer=opt)
    return model


def extract_and_save_embeddings(model):
    """ extract and save users embeddings """
    w1 = None
    for layer in model.layers:
        num = str(layer.name)[-2:]
        if isinstance(layer, Embedding):  # (1, 3076, 60)
            w1 = layer
            print(f"layer {num}", np.array(w1.get_weights()).shape)
            break
    users_embedding = np.array(w1.get_weights())
    with open("models/users_embedding.pkl", "wb") as out_file:
        pickle.dump(users_embedding, out_file)
    return users_embedding


def l2_norm(vect):
    """ l2 norm """
    tmp = [x * x for x in vect.tolist()]
    res = np.sqrt(reduce(lambda x, y: x + y, tmp))
    return res


def cosine_sim(v1, v2, eps1=1e-5, eps2=1e-5):
    """ cosine similarity """
    div = (l2_norm(v1) + eps1) * (l2_norm(v2) + eps2)
    res = np.dot(v1, v2) / div
    return res


def find_n_closest(id_, ids, users_dict, embed, n=20):
    """ find the N-nearest vectors """
    minus_one = copy(ids)
    minus_one.remove(id_)
    k = users_dict[id_]
    encoded_ids = list(map(lambda x: users_dict[x], minus_one))
    vect = embed[0][k][...]
    res = [(i, cosine_sim(vect, embed[0][encoded_ids[i]][...])) for i in range(len(minus_one))]
    sort = sorted(res, key=lambda x: x[1], reverse=True)[:200]
    print(minus_one[sort[0][0]], minus_one[sort[1][0]])
    sort = sort[:n]
    similars = [elem[1] for elem in sort]
    actuals = [minus_one[elem[0]] for elem in sort]
    return actuals, similars


def get_users_items_matrix_and_popularities(ratings):
    """ Construct sparse matrix """
    X = ratings[['user', 'recipe']].values
    y = ratings['rating'].values
    n_users = ratings['user'].nunique()
    n_items = ratings['recipe'].nunique()
    mat = sp.dok_matrix((n_users + 1, n_items + 1), dtype=np.float32)
    for i in range(len(y)):
        if y[i] > 0:
            mat[X[i][0], X[i][1]] = y[i]
    popular = np.zeros((n_items,))
    for i in range(len(y)):
        popular[X[i][1]] += 1
    return mat, popular


def average_rating(k, ratings):
    """ average_rating """
    vals = dict(ratings[k])
    sum_ = reduce(lambda x, y: x + y, vals.values()) / ratings.shape[0]
    return sum_


class CFRecommender:
    """ Recommender of dishes using collaborative filtration """
    def __init__(self, users_csv="data/users_ratings.csv", n_factors=60):
        x, y, ratings = load_users_and_ratings_as_x_y_df(users_csv=users_csv)
        self.ratings = ratings
        X_train, X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.1, random_state=17)
        self.X_train_array, self.X_test_array = get_train_test_arrays(X_train, X_test)
        self.n_users = ratings['user'].nunique()
        self.n_items = ratings['recipe'].nunique()
        self.n_factors = n_factors
        self.actual_items = get_actual_items(self.ratings)
        self.users_embedding = None
        self.matr = None
        self.popularity = None
        self.closest_users = None
        self.similarities = None
        self.closest_users = None
        self.similarities = None

    def get_pretrained_embeddings(self, pickle_file="models/users_embedding.pkl"):
        """ get pretrained embeddings """
        with open(pickle_file, "rb") as pkl_file:
            self.users_embedding = pickle.load(pkl_file)

    def train_model_and_get_embeddings(self, epochs=2000):
        """ train model and get embeddings """
        model = recommender_v2(self.n_users, self.n_items, self.n_factors,
                               min(self.ratings['rating']), max(self.ratings['rating']))
        model.fit(x=self.X_train_array, y=self.y_train,
                  batch_size=128,
                  epochs=epochs,
                  shuffle=True,
                  verbose=1,
                  validation_data=(self.X_test_array, self.y_test))
        model.save("models/new_rnn_cuisine.h5")
        self.users_embedding = extract_and_save_embeddings(model)

    def find_rating_for_dish(self, user_id, item_id, user_enc, item_enc):
        """ Вычисление оценки рейтинга по схожим клиентам
            (User based Collaborative Filtering)
            arguments user_id and item_id
        """
        dish = item_enc[item_id]
        avg_u = average_rating(user_enc[user_id], self.matr)
        weighted_sum = 0.
        sum_ = 0.
        for k in range(len(self.closest_users)):
            j = user_enc[self.closest_users[k]]
            if self.matr[j, dish] > 0:
                rate = self.matr[j, dish]
                avg_v = average_rating(j, self.matr)
                weighted_sum += self.similarities[k] * (rate - avg_v)
                sum_ += self.similarities[k]
        if sum_ > 0:
            return int(avg_u + (weighted_sum / sum_))
        return 1

    def find_100_closest_ratings_for_user(self, user_id, user_dict, item_dict):
        """ find 100 closest ratings for user """
        del self.matr, self.popularity
        self.matr, self.popularity = get_users_items_matrix_and_popularities(
            self.ratings)
        all_users = get_actual_users(self.ratings)
        self.closest_users, self.similarities = find_n_closest(user_id,
                                                               all_users,
                                                               user_dict,
                                                               self.users_embedding,
                                                               n=20)
        actual_items = get_actual_items(self.ratings)
        rating_list = [self.find_rating_for_dish(user_id,
                                                 i,
                                                 user_dict,
                                                 item_dict) for i in actual_items]
        return rating_list

    def find_top_items_for_rating(self, rating_list):
        """ find top 9 for ratings with rate_value """
        zipped = zip(rating_list, self.popularity, list(range(len(rating_list))))
        sorted_ratings = sorted(list(zipped), key=lambda x: x[0], reverse=True)
        top_ratings = [(self.actual_items[el[2]], el[0], el[1]) for el in sorted_ratings]
        print(top_ratings[:10])
        return top_ratings


RECOMMEND = CFRecommender(users_csv="data/users_ratings.csv", n_factors=60)
RECOMMEND.get_pretrained_embeddings()


def prepare_embeddings_and_get_top_items(user_id, load_pretrained=True):
    """ do calculations and return top items with rating = 5 """
    recommender = RECOMMEND
    if not load_pretrained:
        recommender.train_model_and_get_embeddings(epochs=2222)
    user_dict = get_unique_user_map(recommender.ratings,
                                    get_actual_users(recommender.ratings))
    item_dict = get_unique_item_map(recommender.ratings,
                                    recommender.actual_items)
    rating_list = recommender.find_100_closest_ratings_for_user(user_id,
                                                                user_dict,
                                                                item_dict)
    top_items_with_rating_and_popularity = recommender.find_top_items_for_rating(
        rating_list)
    print(f"TOP 7: {top_items_with_rating_and_popularity[:8]}")
    return top_items_with_rating_and_popularity
