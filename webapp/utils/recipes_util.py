"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    recipes utility
"""
import logging
from webapp.business_logic import get_recipe_names_by_cuisine, \
    get_recipe_names_by_type
from webapp.utils.nlp_util import str_to_list
from webapp.dl import RECOMMEND, prepare_embeddings_and_get_top_items


def reorder_ids_by_index(index: list, messages: list, ids: list) -> tuple:
    """ reorder ids and messages by index
        index is a list with indices from ids list
    """
    msg_len = len(messages)
    good_indices = set(index).intersection(set(range(msg_len)))
    if msg_len == 0 or len(ids) == 0 or len(index) == 0:
        logging.error("один из входных списков пустой в reorder_ids_by_index")
        return [], []
    if msg_len != len(ids) or msg_len != len(index):
        logging.error("разный размер входных списков в reorder_ids_by_index")
        return [], []
    if len(good_indices) == 0:
        logging.error(
            "все индексы из списка index не соответствуют входным данным")
        return [], []
    ids_map = {el: ndx for ndx, el in enumerate(ids)}
    result = [(messages[ids_map[ind]], ind)
              for ind in index if ind in ids_map.keys()]
    msgs = [obj[0] for obj in result]
    reordered_ids = [obj[1] for obj in result]
    return msgs, reordered_ids


def find_enough_recommended_recipes(id_, cuisine, dish):
    """ find enough recommended recipes """
    # load item ids according to popularity
    if cuisine is None and dish is None:
        logging.error("параметры cuisine и dish пустые")
        return [], []
    lst = prepare_embeddings_and_get_top_items(id_)
    ids_ = [el[0] for el in lst]
    if dish is None:
        # get names in database insertion order for cuisine
        msg, ids = get_recipe_names_by_cuisine(ids_, cuisine)
    else:
        # get recipes in database insertion order for dist type
        msg, ids = get_recipe_names_by_type(ids_, dish)
    messages, ids = reorder_ids_by_index(ids_, msg, ids)
    return messages, ids


def calculate_embeddings():
    """ method to calculate embeddings """
    RECOMMEND.train_model_and_get_embeddings()


def to_list(text: str) -> list:
    """ convert to list """
    return str_to_list(text)
