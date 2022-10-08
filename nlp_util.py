""" import fasttext
"""
import csv
import pickle
import nltk
import numpy as np
from webapp import create_app
from webapp.stat.models import Note
from copy import copy
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem
# nltk.download('stopwords')
# nltk.download('punkt')

my_stopwords = stopwords.words('russian')
m = Mystem()
MAX_LEN = 400


def replace_special_chars(text):
    """ replace special chars """
    specials = [("¼", "четверть"), ("½", "половина"), ("⅓", "треть"), ("¾", "три четверти")]
    for sp in specials:
        text = text.replace(sp[0], sp[1])
    return text


def tokenize(text):
    """  """
    txt = text.replace(".", " ЕОС ") \
        .replace(";", " ЕОС ") \
        .replace("!", " ЕОС ") \
        .replace("?", " ЕОС ")\
        .replace('\n', "")
    tokenizer = RegexpTokenizer(r'[0-9A-Fa-fА-Яа-я\-\`\,]+')
    txt = tokenizer.tokenize(txt)
    return txt


def remove_stopwords(words, the_stopwords=my_stopwords):
    """  """
    res = " ".join([token for token in words
                    if token not in the_stopwords]).strip()
    return res


def lemmatize(text, mystem=Mystem()):
    """  """
    text = " ".join(text)
    return [w for w in mystem.lemmatize(text) if w != " " and w != "\n"]


def process_synsets(csvfile="./data/yarn-synsets.csv"):
    """ process YARN synonyms """
    syn_map = {"": []}
    with open(csvfile, "r") as f:
        fields = ['id', 'words', 'grammar', 'domain']
        data = csv.DictReader(f, fields, delimiter=',')
        for row in data:
            if row["words"] is None:
                continue
            words = row["words"].split(";")
            if len(words) > 1:
                for w in words:
                    tmp = copy(words)
                    tmp.remove(w)
                    syn_map[w] = tmp
    print(f"map len = {len(syn_map)}")
    return syn_map


def get_rand_lemma(lemmas, syn_map):
    """  """
    ndx = np.random.randint(len(lemmas))
    if lemmas[ndx] in syn_map:
        return lemmas[ndx]
    else:
        ndx = np.random.randint(len(lemmas))
        if lemmas[ndx] in syn_map:
            return lemmas[ndx]
    return False


def get_lemma(lemmas, syn_map):
    """  """
    result = get_rand_lemma(lemmas, syn_map)
    if not result:
        for lemma in lemmas:
            if lemma in syn_map:
                result = lemma
                break
        if not result:
            return False
    return result


def find_3_synonyms(lemmas, syn_map):
    """ insert synonyms """
    lemma1 = get_lemma(lemmas, syn_map)
    if not lemma1:
        return "", "", ""
    lemma2 = get_lemma(lemmas, syn_map)
    if not lemma2:
        return lemma1, "", ""
    lemma3 = get_lemma(lemmas, syn_map)
    if not lemma3:
        return lemma1, lemma2, ""
    return lemma1, lemma2, lemma3


def get_rand_synonym(lst):
    """ get random synonym """
    if not lst:
        index = np.random.randint(len(lst))
        return lst[index]
    return False


def get_similar_directions(directions_tokenized, syn_map):
    """ get similar directions  """
    result = []
    for i in range(5):
        lemmas = find_3_synonyms(directions_tokenized, syn_map)
        synonyms = [get_rand_synonym(syn_map[lemmas[i]]) for i in range(3)]
        new_tokens = directions_tokenized
        for k in range(3):
            if synonyms[k]:
                new_tokens = [e if e != lemmas[k] else synonyms[k] for e in new_tokens]
        result.append(new_tokens)
    return result


def get_text_array(data):
    """ get text array """
    data = data[1:-1].replace("'", "")
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
    result = arr + [padding for i in range(max_len - len(arr))]
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
    five_directions = get_similar_directions(directions_tokenized, syn_map)
    directions_tokenized = name_tokenized + directions_tokenized
    five_directions = [name_tokenized + d for d in five_directions]
    directions = [directions_tokenized] + five_directions
    ingredients = get_text_array(recipe.ingredients.lower().replace(".", ","))
    measures = get_text_array(replace_special_chars(recipe.mera.lower().replace(".", ",")))
    ingredients, measures = remove_duplicates(ingredients, measures)
    arr = [f"{i.strip()} {m.strip()}" for i, m in zip(ingredients, measures)]
    ingredients_tokenized = lemmatize(tokenize(" ".join(arr)))
    all_ingredients = [ingredients_tokenized for i in range(6)]
    return directions, all_ingredients


special_tokens = [" еос "]

app = create_app()
BASE_DIR = "./webapp/templates/img/"
with app.app_context():
    syn_map = process_synsets(csvfile="./data/yarn-synsets.csv")
    texts = []
    cnt = 0
    txts = []
    for recipe in Note.query.limit(2000):
        cnt += 1
        dirs, all = recipe_to_mult_texts(recipe, syn_map, special_tokens[0])
        for k in range(6):
            texts = texts + dirs[k] + all[k]
            txts.append((dirs[k], all[k]))
    counts = nltk.FreqDist(texts).most_common(20000)
    ldict = {x[0]: (n + 1) for n, x in enumerate(counts)}
    print("dictionary len ", len(ldict))
    num_texts = []
    #
    for phrase in txts:
        dirs = [ldict.get(w) if ldict.get(w) else 0 for w in phrase[0]]
        ingredients = [ldict.get(w) if ldict.get(w) else 0 for w in phrase[1]]
        num_texts.append((truncate_or_pad(dirs, ldict["еос"]), truncate_or_pad(ingredients, ldict["еос"])))
    #
    with open("num_texts.pkl", "wb") as f:
        pickle.dump(num_texts, f)
