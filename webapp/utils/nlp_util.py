"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    nlp utilities
"""
import csv
from copy import copy
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem

my_stopwords = stopwords.words('russian')
MAX_LEN = 400
TYPE_MAP = {"вторые блюда": 1,
            "десерты": 2,
            "завтраки": 3,
            "закуски": 4,
            "салаты": 5,
            "соусы": 6,
            "супы и первые блюда": 7,
            }
CUISINES = {"европейская": 1,
            "русская": 2,
            "венгерская": 1,
            "сербская": 1,
            "азиатская": 3,
            "африканская": 4,
            "мексиканская": 5,
            }


def replace_special_chars(text):
    """ replace special chars:  """
    specials = [("¼", "четверть"), ("½", "половина"), ("⅓", "треть"), ("¾", "три четверти")]
    for tuple_ in specials:
        text = text.replace(tuple_[0], tuple_[1])
    return text


def str_to_list(text: str) -> list:
    """ convert text with comma-delimiters to list and
    replace special chars as spaces """
    txt = text.replace("[", "") \
        .replace("]", "") \
        .replace("'", "") \
        .replace("\n", "")
    result = [elem.strip() for elem in txt.split(",")]
    return result


def tokenize(text: str) -> list:
    """ tokenize function """
    txt = text.replace(".", " ЕОС ") \
        .replace(";", " ЕОС ") \
        .replace("!", " ЕОС ") \
        .replace("?", " ЕОС ") \
        .replace('\n', "")
    tokenizer = RegexpTokenizer(r'[0-9A-Fa-fА-Яа-я\-\`\,ё]+')
    txt = tokenizer.tokenize(txt)
    return txt


def remove_stopwords(words: list) -> str:
    """ remove stopwords """
    the_stopwords = my_stopwords
    res = " ".join([token for token in words
                    if token not in the_stopwords]).strip()
    return res


def lemmatize(text: list) -> list:
    """ lemmatize """
    mystem = Mystem()
    text = " ".join(text)
    return [wo for wo in mystem.lemmatize(text) if wo not in [" ", "\n"]]


def process_synsets(csvfile="./data/yarn-synsets.csv"):
    """ process YARN synonyms """
    syn_map = {"": []}
    with open(csvfile, "r") as csvf:
        fields = ['id', 'words', 'grammar', 'domain']
        data = csv.DictReader(csvf, fields, delimiter=',')
        for row in data:
            if row["words"] is None:
                continue
            words = row["words"].split(";")
            if len(words) > 1:
                for word in words:
                    tmp = copy(words)
                    tmp.remove(word)
                    syn_map[word] = tmp
    print(f"map len = {len(syn_map)}")
    return syn_map


def get_3_rand_indices(lemmas, syn_map):
    """ get 3 random indices """
    num = len(lemmas)
    synonyms_exist = np.array([ndx for ndx in range(num) if lemmas[ndx] in syn_map])
    np.random.shuffle(synonyms_exist)
    return synonyms_exist.tolist()[:3]


def get_random_synonyms(lemmas, indices, syn_map):
    """ get 3 random synonyms with its index """
    result = [(np.random.choice(syn_map[lemmas[ndx]]), ndx) for ndx in indices]
    return result


def get_similar_directions(directions_tokenized, syn_map):
    """ get similar directions  """
    result = []
    for i in range(3):
        indices = get_3_rand_indices(directions_tokenized, syn_map)
        synonyms = get_random_synonyms(directions_tokenized, indices, syn_map)
        new_directions = copy(directions_tokenized)
        for words, index in synonyms:
            new_directions[index] = words
        result.append(lemmatize(tokenize(" ".join(new_directions))))
    return result


def get_text_array(data):
    """ get text array """
    data = data.replace("'", "")
    tokens = data.split(",")
    return tokens


def remove_duplicates(data, mera):
    """ remove duplicates """
    if len(data) >= 3 and len(mera) >= 3:
        if data[0].strip() == data[1].strip() and mera[0].strip() == mera[1].strip():
            return data[2:], mera[2:]
    return data, mera


def pad(arr, padding, max_len=MAX_LEN):
    """ pad to 400 words"""
    result = arr + ([padding] * (max_len - len(arr)))
    return result


def truncate_or_pad(arr, padding, max_len=MAX_LEN):
    """ truncate or pad array """
    if len(arr) < max_len:
        return pad(arr, padding)
    return arr[:max_len]


def recipe_to_mult_texts(recipe, syn_map, end_token):
    """ convert recipe to text """
    arr = get_text_array(replace_special_chars(recipe.directions.lower()))
    name_tokenized = tokenize(recipe.name.lower()) + [end_token]
    directions_tokenized = lemmatize(tokenize(" ".join(arr)))
    three_directions = get_similar_directions(directions_tokenized, syn_map)
    directions_tokenized = name_tokenized + directions_tokenized
    three_directions = [name_tokenized + d for d in three_directions]
    directions = [directions_tokenized] + three_directions
    ingredients = get_text_array(recipe.ingredients.lower().replace(".", ","))
    measures = get_text_array(replace_special_chars(recipe.mera.lower().replace(".", ",")))
    ingredients, measures = remove_duplicates(ingredients, measures)
    arr = [f"{i.strip()} {element.strip()}" for i, element in zip(ingredients, measures)]
    ingredients_tokenized = lemmatize(tokenize(" ".join(arr)))
    all_ingredients = [ingredients_tokenized] * 4
    all_types = [(TYPE_MAP[recipe.typed], CUISINES[recipe.cusine])] * 4
    return directions, all_ingredients, all_types


def tokenize_recipe(recipe, end_token):
    """ convert recipe to text """
    arr = get_text_array(replace_special_chars(recipe[0]["directions"].lower()))
    name_tokenized = tokenize(recipe[0]["name"].lower()) + [end_token]
    directions_tokenized = lemmatize(tokenize(" ".join(arr)))
    directions_tokenized = name_tokenized + directions_tokenized
    ingredients = get_text_array(recipe[0]["ingredients"].lower().replace(".", ","))
    measures = get_text_array(replace_special_chars(recipe[0]["mera"].lower().replace(".", ",")))
    ingredients, measures = remove_duplicates(ingredients, measures)
    arr = [f"{i.strip()} {element.strip()}" for i, element in zip(ingredients, measures)]
    ingredients_tokenized = lemmatize(tokenize(" ".join(arr)))
    return directions_tokenized, ingredients_tokenized
