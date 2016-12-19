import json
import time

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from numpy import dot
from numpy.linalg import norm
from pip._vendor import requests
from spacy.en import English

lt1 = time.time()
parser = English()

load_time = time.time() - lt1



def home(request):
    """
    http://domain.com/
    :param request:
    :return:
    """
    return render(request, "api/index.html", {})


def index(request):
    """
    Default index page
    :param request:
    :return:
    """
    return render(request, 'api/index.html', {})


@csrf_exempt
def api1(request):
    """
    route api/rw
    API to send the related words in JSON format.
    :param request:
    :return:
    """

    word = request.POST.get("word")
    print(type(word))
    print(word)
    t1 = time.time()
    b = related_words(word)
    print(len(b))
    t2 = time.time() - t1
    print(b)
    print("Loading time : "+ str(load_time))
    # return HttpResponse("Post Method request :" + str(b))
    return JsonResponse({"time_consumed": str(t2), "word": word, "count": len(b), "related_words": b}, safe=False)


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


@csrf_exempt
def pos_tagging(request):
    """
    API to return the part of speech tagging.
    :param request:
    :return: JSON
    """
    post_text = request.POST.get("txt")
    print(type(post_text))
    print(post_text)
    t1 = time.time()
    #start: tagging code
    parsedData = parser(post_text)
    pos = {}
    for token in parsedData:
        print(token.orth_, token.pos_)
        pos[token.orth_] = token.pos_
    print("Part speech in dictionary")
    print(pos)
    print (type(pos))
    json_pos = json.dumps(pos)
    print ("type of json_pos : " + str(type(json_pos)))
    print("json response words :" + json_pos)
    # end: tagging code

    t2 = time.time() - t1
    print("Loading time : " + str(load_time))
    return JsonResponse({"execution_time": str(t2), "loading_time": str(load_time), "text": post_text, "tagged_pos": json_pos}, safe=False)


@csrf_exempt
def label_entities(request):
    """

    :param request:
    :return: JSON
    """
    post_text = request.POST.get("txt")
    print(type(post_text))
    print(post_text)
    t1 = time.time()
    # start : entities labeling code
    parsedEx = parser(post_text)
    entities = list(parsedEx.ents)
    entity_words = {}
    for entity in entities:
        print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
        for t in entity:
            entity_words[t.orth_] = entity.label_
    print(entity_words)
    print("type " + str(entity_words))
    print("json format")
    json_entity_words = json.dumps(entity_words)
    print("json entity type : " + str(json_entity_words))
    print(json_entity_words)
    # end : entities labeling code
    t2 = time.time() - t1
    print("Loading time : " + str(load_time))
    return JsonResponse({"execution_time": str(t2), "loading_time": str(load_time), "text": post_text, "label_entities": json_entity_words}, safe=False)

@csrf_exempt
def sense_word(request):
    """
    sense 2 word is API.
    URL : https://demos.explosion.ai/sense2vec/?word=natural%20language%20processing&sense=auto
    :param request:
    :return:
    """
    if request.method == "GET":
        word = request.GET.get("word")
    elif request.method == "POST":
        word = request.POST.get("word")

    response = requests.get("https://api.explosion.ai/sense2vec/" + str(word))
    return HttpResponse(response)


@csrf_exempt
def phrase_extraction(request):
    """
    phrases extraction of the text
    Limit:
    no value for text is provided
    text exceeds 1,000 characters
    an incorrect language is specified
    URL : http://text-processing.com/docs/phrases.html
    :param request:
    :return: JSON
    """
    if request.method == "GET":
        text = request.GET.get("text")
    elif request.method == "POST":
        text = request.POST.get("text")

    response = requests.post("http://text-processing.com/api/phrases/",{"text": text})
    return HttpResponse(response)


@csrf_exempt
def polarity(request):
    """
    phrases extraction of the text
    Limits:
    no value for text is provided
    text exceeds 80,000 characters
    URL : http://text-processing.com/docs/sentiment.html
    :param request:
    :return: JSON
    """
    if request.method == "GET":
        text = request.GET.get("text")
    elif request.method == "POST":
        text = request.POST.get("text")

    response = requests.post("http://text-processing.com/api/sentiment/",{"text": text})
    return HttpResponse(response)