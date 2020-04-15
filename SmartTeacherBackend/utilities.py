from __future__ import unicode_literals
import youtube_dl
from urllib import parse 
import os
from os import path
from punctuator import Punctuator
import requests
import boto3
from nltk.tag import pos_tag
import math

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2030, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

audio_file_dir = 'Audio_Files/'
vtt_file_dir = 'VTT_Files/'
#text_file_dir = 'Text_Files/'
comprehend_client = boto3.client('comprehend')

def get_audio_file(url):
    video_id = ''.join (c for c in parse.parse_qs(parse.urlsplit(url).query)['v'])
    audio_file_path = audio_file_dir+video_id

    if  os.path.exists(audio_file_path + '.wav'):
        return video_id
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio':True,
        'audioformat':'wav',
        'noplaylist':True,
        'nocheckcertificate':True,
        'outtmpl': audio_file_path+'.%(ext)s',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
            
        }],
        'prefer_ffmpeg': True,
        'keepaudio': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return video_id

def get_vtt_file(url):
    video_id = ''.join (c for c in parse.parse_qs(parse.urlsplit(url).query)['v'])
    if check_if_video_exists(video_id):
        return video_id
    
    vtt_file_path = vtt_file_dir+video_id

    # youtube-dl --skip-download --sub-format vtt --write-auto-sub https://www.youtube.com/watch?v=5DGwOJXSx
    ydl_opts = {
    'skip_download': True,
    'subtitlesformat': 'vtt',
    'writeautomaticsub': True,
    'outtmpl': vtt_file_path+'.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return video_id

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
    
# print(get_vtt_file('https://www.youtube.com/watch?v=_VhcZTGv0CU'))
# print(get_audio_file('https://www.youtube.com/watch?v=UPBMG5EYydo'))

import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3')
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    try:
        response = s3_client.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
        print(response)

    except ClientError as e:
        logging.error(e)
        return False
    return True

def check_if_video_exists(video_id):

    vtt_file_path = vtt_file_dir+video_id

    if  os.path.exists(vtt_file_path + '.en.vtt'):
        return True

def punctuate_online(text):
    # defining the api-endpoint  
    API_ENDPOINT = "http://bark.phon.ioc.ee/punctuator"
    
    # data to be sent to api 
    data = dict(text=text)
    
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 
    
    # extracting response text  
    punctuatedText = r.text
    return punctuatedText


def word_count(phrase):
    return len(phrase.split(' '))

def filter_nouns(text_list,language_code):
    removed_elements = []
    for i, el in enumerate(text_list):
        if el == "":
            removed_elements.append(i)

    while '' in text_list:
        text_list.remove('')

    # if len(text_list) >= 25:
    #     text_list = text_list[:24]

    length = math.ceil(len(text_list)/25)

    i = 0
    result_list = []
    while i < length:
        response =     response = comprehend_client.batch_detect_syntax(
        TextList= text_list[(i*25):((i+1)*25)],
        LanguageCode= language_code
        )
        i += 1
        result_list += response['ResultList']

    for index, target in enumerate(result_list):
        for syntax_token in target['SyntaxTokens']:
            if syntax_token['PartOfSpeech']['Tag'] == 'NOUN' or syntax_token['PartOfSpeech']['Tag'] == 'PROPN':
                continue

            text_list[index] = text_list[index].replace(syntax_token['Text'], '')
            text_list[index] = text_list[index].strip()
    
    for el in removed_elements:
        text_list.insert(el,'')

    return text_list

def isGoodScore(phrase):
    return phrase['Score'] == 1

def get_proper_nouns(sentence):

    tagged_sent = pos_tag(sentence.split())
    propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
    return propernouns