import flask
import question_generator 
import summarizer 
import utilities 
import os
from os import path
import re
from flask import request
import vtt_to_txt
from flask_cors import CORS
from keyword_generator import get_key_phrases
import json
import time
from nltk.corpus import wordnet

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

text_folder_path = 'Text_Files/'
vtt_folder_path = 'VTT_Files/'
json_folder_path = 'JSON_Files/'

@app.route('/', methods=['GET'])
def home():
    video_id = request.args.get('v')
    if not video_id:
        return {"Issue":"Please pass video ID v in query params"}

    url = 'https://www.youtube.com/watch?v=' + video_id
    #get audio 
    # video_id = utilities.get_audio_file(url)
    text_file_path = text_folder_path+video_id+'.txt'
    json_file_path = json_folder_path+video_id+'.json'


    if not utilities.check_if_video_exists(video_id):
        utilities.get_vtt_file(url)
        vtt_to_txt.convert_to_text(video_id)

    # get summary
    summary = summarizer.get_summary(open(text_file_path,'r').read())

    # Add space after full stop
    rx = r"\.(?=\S)"
    summary = re.sub(rx, ". ", summary)
    re.sub(".", ". ",summary)

    # get questions and return
    json_sentences = json.loads(open(json_file_path,'r').read())

    questions = question_generator.generate_trivia(summary)
    prevJumpToTime = 0
    for question in questions:
        correct_index = question['correctIndex']
        correct_answer = question['answers'][correct_index]
        for json_sentence in json_sentences:
            json_sentence_time = utilities.get_sec(json_sentence['time'])
            if json_sentence_time >= prevJumpToTime and json_sentence['line'].find(correct_answer) >= 0:
                question['jumpToTime'] = json_sentence_time
                prevJumpToTime = json_sentence_time
                break

    # print(questions)
    return json.dumps(questions)

@app.route('/notes', methods=['GET'])
def notes():
    video_id = request.args.get('v')
    if not video_id:
        return {"Issue":"Please pass video ID v in query params"}

    text_file_path = text_folder_path+video_id+'.txt'
    json_file_path = json_folder_path+video_id+'.json'

    url = 'https://www.youtube.com/watch?v=' + video_id

    if not utilities.check_if_video_exists(video_id):
        utilities.get_vtt_file(url)
        vtt_to_txt.convert_to_text(video_id)

    notes = summarizer.get_summary_with_ratio(open(text_file_path,'r').read(),0.5)

    result_list = get_key_phrases(notes, 'en')
    global_keywords = []

    prevJumpToTime = 0
    for out_index, cur_item in enumerate(result_list):
        keyword_list = []
        for current_phrase in cur_item['KeyPhrases']:
            # if current_phrase['Score'] >= target_phrase['Score'] and word_count(current_phrase['Text']) < word_count(target_phrase['Text']):
            if utilities.isGoodScore(current_phrase):
                keyword_list.append(current_phrase['Text'].strip())

        if len(keyword_list) > 0:
            keyword_list = utilities.filter_nouns(keyword_list, 'en')

            # remove similar words
            for keyword in keyword_list:
                if keyword not in global_keywords:
                    global_keywords.append(keyword.strip())
                else:
                    keyword_list.remove(keyword)
        
        keyword_list = [x for x in keyword_list if x in keyword_list]

        for keyword in keyword_list:
            syns = wordnet.synsets(keyword)

            if len(syns) > 0:
                keyword_obj = {}
                keyword_obj['keyword'] = keyword
                keyword_obj['definition'] = syns[0].definition()
                keyword_obj['examples'] = syns[0].examples()
                keyword_list[keyword_list.index(keyword)] = keyword_obj

        keyword_list = [x for x in keyword_list if type(x) is not str]

        json_sentences = json.loads(open(json_file_path,'r').read())

        sentence = str(notes[out_index])
        note = {}
        note['sentence'] = sentence
        note['keywords'] = keyword_list
        print(keyword_list)
        # need to improve
        if len(keyword_list) > 0:
            keyword = keyword_list[0]['keyword']
            for json_sentence in json_sentences:
                json_sentence_time = utilities.get_sec(json_sentence['time'])
                if json_sentence_time >= prevJumpToTime and json_sentence['line'].find(keyword) >= 0:
                    note['jumpToTime'] = json_sentence_time
                    prevJumpToTime = json_sentence_time
                    break
        else:
            note['jumpToTime'] = prevJumpToTime
        
        notes[out_index] = note

    summary = summarizer.get_short_summary(video_id)
    response = {"notes": notes,"summary": summary}
    return json.dumps(response)

app.run()

# print(notes())
# print(home())