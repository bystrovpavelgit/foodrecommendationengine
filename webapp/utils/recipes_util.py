"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    recipes utility
"""
from webapp.business_logic import get_recipe_names_by_cuisine, \
    get_recipe_names_by_type
from webapp.utils.nlp_util import str_to_list
from webapp.dl import RECOMMEND, prepare_embeddings_and_get_top_items


def reorder_ids_by_index(index: list, messages: list, ids: list) -> tuple:
    """ reorder ids by index """
    ids_map = {el: ndx for ndx, el in enumerate(ids)}
    result = [(messages[ids_map[i]], i) for i in index if i in ids_map.keys()]
    msgs = [el[0] for el in result]
    reordered_ids = [el[1] for el in result]
    return msgs, reordered_ids


def find_enough_recommended_recipes(id_, cuisine, dish):
    """ find enough recommended recipes """
    lst = prepare_embeddings_and_get_top_items(id_)
    ids_ = [el[0] for el in lst]
    if dish is None:
        msg, ids = get_recipe_names_by_cuisine(ids_, cuisine)
    else:
        msg, ids = get_recipe_names_by_type(ids_, dish)
    messages, ids = reorder_ids_by_index(
        ids_, msg, ids)
    return messages, ids


def calculate_embeddings():
    """ method to calculate embeddings """
    RECOMMEND.train_model_and_get_embeddings()


def to_list(text: str) -> list:
    """ convert to list """
    return str_to_list(text)
