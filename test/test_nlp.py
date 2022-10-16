""" nlp tests """
from webapp.utils.nlp_util import replace_special_chars, remove_stopwords, get_text_array


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

