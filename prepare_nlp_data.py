"""
   utility to convert text to numerical format for classificator
"""
import pickle
import nltk
from webapp import create_app
from webapp.stat.models import Note
from webapp.utils.nlp_util import recipe_to_mult_texts, process_synsets, truncate_or_pad
nltk.download('stopwords')
nltk.download('punkt')

if __name__ == "__main__":
    # main method
    special_tokens = [" еос "]
    app = create_app()
    with app.app_context():
        syn_map = process_synsets(csvfile="./data/yarn-synsets.csv")
        continuous_text = []
        texts = []
        results = []
        results2 = []
        for recipe in Note.query.order_by(Note.id).limit(3300):
            dirs, ingredients, y_true = recipe_to_mult_texts(recipe,
                                                             syn_map,
                                                             special_tokens[0])
            for k in range(6):
                results.append(y_true[k][0])
                results2.append(y_true[k][1])
                continuous_text = continuous_text + dirs[k] + ingredients[k]
                texts.append((dirs[k], ingredients[k]))
        counts = nltk.FreqDist(continuous_text).most_common(20000)
        vocab = {x[0]: (n + 1) for n, x in enumerate(counts)}
        print("dictionary len ", len(vocab))
        num_texts = []
        # convert words to numbers using vocab
        for part in texts:
            dirs = [vocab.get(w) if vocab.get(w) else 0 for w in part[0]]
            ingredients = [vocab.get(w) if vocab.get(w) else 0 for w in part[1]]
            num_texts.append((truncate_or_pad(dirs, vocab["еос"]),
                              truncate_or_pad(ingredients, vocab["еос"])))
        # save numerical data and vocabulary to num_texts.pkl and vocabulary.pkl
        with open("num_texts.pkl", "wb") as f:
            pickle.dump(num_texts, f)
        with open("vocabulary.pkl", "wb") as f:
            pickle.dump(vocab, f)
        with open("y_gt1.pkl", "wb") as f:
            pickle.dump(results, f)
        with open("y_gt2.pkl", "wb") as f:
            pickle.dump(results2, f)
