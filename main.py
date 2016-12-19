import json
import sys
import time

sys.path.append('/home/shehbaz/Documents/spacy/.env/lib/python2.7/site-packages')

from flask import request
from numpy import dot
from numpy.linalg import norm

import flask
from flask import render_template

from flask import Flask

from spacy.en import English

lt1 = time.time()
parser = English()

load_time = time.time() - lt1

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/rw')
def api_rw():
    if request.method == 'POST':
        word = request.form['word']
        myDict = {'a': 2, 'b': 3, "user": word}
    else:
        word = request.args.get('word')
        myDict = {'a': 2, 'b': 3, "user": word}
    # print(type(word))
    # print(word)
    # t1 = time.time()
    # b = related_words(u'NASA')
    # print(len(b))
    # t2 = time.time() - t1
    # print(b)
    # print("Loading time : " + str(load_time))
    # return flask.jsonify({"time_consumed": str(t2), "word": word, "count": len(b), "related_words": b})
    # return flask.jsonify({"time_consumed": "2", "word": "NASA", "count": "23", "related_words": "GOOGLE, YAHOO"})
    return "word : " + word


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


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        myDict = {'a': 2, 'b': 3, "user": user}
        return flask.jsonify(myDict)
    else:
        user = request.args.get('nm')
        myDict = {'a': 2, 'b': 3, "user": user}
        return flask.jsonify(myDict)


@app.route('/json')
def hello_json():
    myDict = {'a': 2, 'b': 3}
    return flask.jsonify(myDict)


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name


@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number %d' % postID


@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number %f' % revNo


@app.route('/flask')
def hello_flask():
    return 'Hello <h2>Flask</h2>'


@app.route('/python/')
def hello_python():
    """
    canonical url. /python and /python/ are same.
    :return:
    """
    return 'Hello <h2>Python</h2>'


if __name__ == '__main__':
    app.run()
