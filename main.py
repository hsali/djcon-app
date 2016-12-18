import flask
from flask import render_template

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
