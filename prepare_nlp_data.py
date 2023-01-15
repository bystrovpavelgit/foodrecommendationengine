"""
   Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
   utility to convert text to numerical format for classificator
"""
import csv
import pickle
import nltk
from webapp import create_app
from webapp.stat.models import Note
from webapp.utils.nlp_util import recipe_to_mult_texts, process_synsets
#nltk.download('stopwords')
#nltk.download('punkt')


def replace_special_chars(text):
    """ replace special chars """
    specials = [("¼", "четверть"), ("½", "половина"), ("⅓", "треть"), ("¾", "три четверти")]
    for tuple_ in specials:
        text = text.replace(tuple_[0], tuple_[1])
    return text


def save_row(csvfile, name, text, ingreds, dish_type, cuisine):
    """ save row """
    new_row = {"name": name,
               "text": text,
               "ingreds": ingreds,
               "dish_type": dish_type,
               "cuisine": cuisine}
    csvfile.writerow(new_row)


if __name__ == "__main__":
    # main method
    special_tokens = [" еос "]
    app = create_app()
    with app.app_context():
        syn_map = process_synsets(csvfile="data/yarn-synsets.csv")
        continuous_text = []
        with open("models/recipes_nlp_data.csv", "w", encoding="utf-8") as cf:
            fields = ["name", "text", "ingreds", "dish_type", "cuisine"]
            cc = csv.DictWriter(cf, fieldnames=fields, delimiter=",")
            cc.writeheader()
            num = 0
            for recipe in Note.query.order_by(Note.id).all():
                dirs, ingredients, y_true = recipe_to_mult_texts(recipe,
                                                                 syn_map,
                                                                 special_tokens[0])
                if num < 3500:
                    for k in range(4):
                        continuous_text = continuous_text + dirs[k] + ingredients[k]
                        save_row(cc,
                                 recipe.name,
                                 " ".join(dirs[k]),
                                 replace_special_chars(" ".join(ingredients[k])),
                                 y_true[k][0],
                                 y_true[k][1])
                else:
                    continuous_text = continuous_text + dirs[0] + ingredients[0]
                    save_row(cc,
                             recipe.name,
                             " ".join(dirs[0]),
                             replace_special_chars(" ".join(ingredients[0])),
                             y_true[0][0],
                             y_true[0][1])
        counts = nltk.FreqDist(continuous_text).most_common(22000)
        vocab = {x[0]: (n + 1) for n, x in enumerate(counts)}
        # save vocabulary
        with open("models/vocabulary.pkl", "wb", encoding="utf-8") as f:
            pickle.dump(vocab, f)
        print("dictionary len ", len(vocab))
