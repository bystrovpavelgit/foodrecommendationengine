""" nlp tests """
import json
from webapp.utils.nlp_util import replace_special_chars, remove_stopwords, get_text_array,\
    lemmatize, tokenize, process_synsets, get_similar_directions


def test_get_text_array():
    """ nlp tests """
    txt = get_text_array("[aa]")
    assert len(txt) == 1
    assert txt[0] == "aa"


def test_remove_stopwords():
    """ nlp tests """
    txt = remove_stopwords("1 и 2")
    assert txt == '1     2'


def test_replace_special_chars():
    """ nlp tests """
    txt = replace_special_chars("¼ ½ ⅓ ¾")
    assert txt == "четверть половина треть три четверти"


def test_lemmatization():
    """ nlp tests """
    arr = "[Марокканский суп с нутом и имбирем еос Морковь, лук, чеснок нарезать, " + \
          "имбирь натереть на мелкой терке. Обжарить овощи на растительном масле до мягкости.]"
    arr = get_text_array(replace_special_chars(arr.lower()))
    tokenized = lemmatize(tokenize(" ".join(arr)))
    assert len(tokenized) == 25
    assert tokenized[0] == "марокканский"
    assert tokenized[24] == "еос"


def test_get_similar_directions():
    """ nlp tests """
    arr = "[Марокканский суп с нутом и имбирем еос Морковь, лук, чеснок нарезать, " + \
          "имбирь натереть на мелкой терке. Обжарить овощи на растительном масле до мягкости.]"
    arr = get_text_array(replace_special_chars(arr.lower()))
    tokenized = lemmatize(tokenize(" ".join(arr)))
    syn_map = process_synsets(csvfile="data/yarn-synsets.csv")
    five_directions = get_similar_directions(tokenized, syn_map)
    assert len(five_directions) == 5
    for directions in five_directions:
        assert len(directions) > 24
