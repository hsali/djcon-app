# https://nicschrading.com/project/Intro-to-NLP-with-spaCy/
# Set up spaCy
import json
import time
import sys

sys.path.append('/home/shehbaz/Documents/spacy/.env/lib/python2.7/site-packages/')
from spacy.en import English

t1 = time.time()
parser = English()

from numpy import dot
from numpy.linalg import norm


def related_words(word):
    """
    related words
    :param word:
    :return:
    """
    # word = unicode(word, encoding="UTF-8")
    search_word = parser.vocab[word]
    # cosine similarity
    cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))

    # gather all known words, take only the lowercased versions
    all_words = list({w for w in parser.vocab if w.has_vector and w.orth_.islower() and w.lower_ != "nasa"})

    # sort by similarity to NASA
    all_words.sort(key=lambda w: cosine(w.vector, search_word.vector))
    all_words.reverse()
    # words = (word.orth_ for word in all_words[:10])
    word_list = []
    for word in all_words[:10]:
        word_list.append(word.orth_)
        # print(word.orth_)
        # print(type(word.orth_))
        print(word.orth_)
    print(word_list)
    json_list = json.dumps(word_list)
    print(json_list)
    return json_list

j= related_words(u"NASA");
print(len(j))
print(j)