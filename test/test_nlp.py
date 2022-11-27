""" nlp tests """
import json
from webapp.utils.nlp_util import replace_special_chars, remove_stopwords, get_text_array,\
    lemmatize, tokenize


def test_get_text_array():
    """ nlp tests """
    txt = get_text_array("aa,bb")

    assert len(txt) == 2
    assert txt[0] == "aa"
    assert txt[1] == "bb"


def test_remove_stopwords():
    """ testing remove_stopwords function """
    txt = remove_stopwords(["1", "и", "2"])

    assert txt == "1 2"


def test_replace_special_chars():
    """ testing replace_special_chars function """
    txt = replace_special_chars("¼ ½ ⅓ ¾")

    assert txt == "четверть половина треть три четверти"


def test_lemmatization():
    """ testing lemmatize """
    arr = "Марокканский суп с нутом и имбирем еос Морковь, лук, чеснок нарезать, " + \
          "имбирь натереть на мелкой терке. Обжарить овощи на растительном масле до мягкости."

    text = get_text_array(replace_special_chars(arr.lower()))
    tokenized = lemmatize(tokenize(" ".join(text)))

    assert len(tokenized) == 25
    assert tokenized[0] == "марокканский"
    assert tokenized[24] == "еос"
