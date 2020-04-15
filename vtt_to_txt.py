"""
Convert YouTube subtitles(vtt) to human readable text.

Download only subtitles from YouTube with youtube-dl:
youtube-dl  --skip-download --convert-subs vtt <video_url>

Note that default subtitle format provided by YouTube is ass, which is hard
to process with simple regex. Luckily youtube-dl can convert ass to vtt, which
is easier to process.

"""

import sys
import re
import json
import requests
import os
import utilities

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

text_folder_path = 'Text_Files/'
vtt_folder_path = 'VTT_Files/'
json_folder_path = 'JSON_Files/'

def remove_tags(text):
    """
    Remove vtt markup tags
    """
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',

    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    # extract timestamp, only kep HH:MM:SS
    text = re.sub(
        r'(\d{2}:\d{2}:\d{2})\.\d{3} --> .* align:start position:0%',
        r'\g<1>',
        text
    )

    text = re.sub(
        r'(\d{2}:\d{2}:\d{2})\.\d{3} --> .*',
        r'\g<1>',
        text
    )

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text

def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in ('##', 'Language: en',):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match(r'^\d{2}:\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match(r'^\d{2}:\d{2}:\d{2}$', line):
            yield '' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer

def duplicate_punctuation(text):
    # pattern_regex = r'[\.,?\(\)\{\}\[\]\!\&/\"\'\:\;]+'
    # regex_req = re.sub(pattern_regex, '', text)
    # print(regex_req)
    text = re.sub(r'[\.]+','.',text)
    return text

def convert_to_text(video_id):
    text_file_path = text_folder_path + video_id + '.txt'
    json_file_path = json_folder_path + video_id + '.json'

    if  os.path.exists(text_file_path):
        return
    vtt_file_path = vtt_folder_path+video_id+'.en.vtt'
    with open(vtt_file_path) as f:
        text = f.read()
    text = remove_tags(text)
    lines = text.splitlines()
    lines = remove_header(lines)
    lines = merge_duplicates(lines)
    lines = list(lines)
    lines = merge_short_lines(lines)
    lines = list(lines)
    # generate JSON with timestamp and line
    flag = False
    jsonList = []
    counter = 0
    for line in lines:
        if(re.match(r'^\d{2}:\d{2}:\d{2}$', line) and not flag):
            flag = True
            jsonList.insert(counter,{'time' : line})
        elif not re.match(r'^\d{2}:\d{2}:\d{2}$', line):
            flag = False
            if counter < len(jsonList):
                jsonList[counter]['line'] = line
                counter += 1
            else:
                jsonList[counter-1]['line'] += ' ' + line


    unPunctuatedText = ''
    for jsonObj in jsonList:
        unPunctuatedText += jsonObj['line'] + ' '


    # offline punctuation
    # p = Punctuator('model.pcl')
    # punctuatedText = p.punctuate(unPunctuatedText)
    # print(unPunctuatedText)
    # spell_checked_text = spell_check(unPunctuatedText)

    # online punctuation
    punctuatedText = utilities.punctuate_online(unPunctuatedText)

    # remove duplicate punctuations
    punctuatedText = duplicate_punctuation(punctuatedText)


    with open(json_file_path, 'w+') as f:
        f.write(json.dumps(jsonList))
    with open(text_file_path, 'w+') as f:
        f.write(punctuatedText)
