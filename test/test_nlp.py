""" nlp tests """
import json
from webapp.utils.nlp_util import replace_special_chars, remove_stopwords, get_text_array,\
    lemmatize, tokenize, str_to_list


def test_get_text_array():
    """ testing test_get_text_array function """
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
    """ testing lemmatize function """
    arr = "Марокканский суп с нутом и имбирем еос Морковь, лук, чеснок нарезать, " + \
          "имбирь натереть на мелкой терке. Обжарить овощи на растительном масле до мягкости."

    text = get_text_array(replace_special_chars(arr.lower()))
    tokenized = lemmatize(tokenize(" ".join(text)))

    assert len(tokenized) == 25
    assert tokenized[0] == "марокканский"
    assert tokenized[24] == "еос"


def test_str_to_list():
    """ testing str_to_list function """
    txt = str_to_list("cc,dd")

    assert len(txt) == 2
    assert txt[0] == "cc"
    assert txt[1] == "dd"


def test_tokenize():
    """ testing tokenize function """
    txt = tokenize("cc , dd")

    assert len(txt) == 3
    assert txt[0] == "cc"
    assert txt[2] == "dd"

def test_truncate_or_pad():
    """ testing truncate or pad """
    txt = tokenize("cc , dd")

    assert len(txt) == 3
    assert txt[0] == "cc"
    assert txt[2] == "dd"