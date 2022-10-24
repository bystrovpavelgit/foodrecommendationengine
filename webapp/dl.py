"""DL constants"""
import pickle
import numpy as np
from tensorflow import keras
from webapp.utils.nlp_util import tokenize_recipe, truncate_or_pad

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
    """ predict_types """
    with open("models/vocabulary.pkl", "rb") as v_file:
        vocab = pickle.load(v_file)
    part1, part2 = tokenize_recipe(recipe, "еос")
    dirs = truncate_or_pad([vocab.get(w) if w in vocab else 0 for w in part1], 0)
    ingredients = truncate_or_pad([vocab.get(w) if w in vocab else 0 for w in part2], 0)[:100]
    res = dirs + ingredients

    model = keras.models.load_model("models/rnn2_with_embed.h5")
    arr = np.array([res])
    pred = model.predict(arr[..., None])
    cuisine = np.argmax(pred)
    model = keras.models.load_model("models/rnn2_dish_pred7.h5")
    arr = np.array([res])
    pred = model.predict(arr[..., None])
    type_pred = np.argmax(pred)
    print("result", CUISINES[int(cuisine)], TYPE_MAP[int(type_pred)])
    return CUISINES[int(cuisine)], TYPE_MAP[int(type_pred)]
