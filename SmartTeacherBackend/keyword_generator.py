import logging
import boto3
from botocore.exceptions import ClientError
import json
import utilities
import math

"""Generates KeyPhrases for a given text
"""
__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

client = boto3.client('comprehend')

def generate(text_list, language_code):
    """
    Generates Keywords
    """
    keyword_list = []
    try:
        result_list = get_key_phrases(text_list, language_code)

        for cur_item in result_list:
            if len(cur_item['KeyPhrases']) <= 0:
                keyword_list.append('')
                continue

            target_phrase = cur_item['KeyPhrases'][0]

            for current_phrase in cur_item['KeyPhrases']:
                # if current_phrase['Score'] >= target_phrase['Score'] and word_count(current_phrase['Text']) < word_count(target_phrase['Text']):
                if current_phrase['Score'] >= target_phrase['Score']:
                    target_phrase = current_phrase

            keyword_list.append(target_phrase['Text'].strip())

        keyword_list = utilities.filter_nouns(keyword_list, 'en')


        # for cur_index, text_line in enumerate(text_list):
        #     text_list[cur_index] = text_line.replace(keyword_list[cur_index], "______________")

    except ClientError as e:
        logging.error(e)
        return None
    return keyword_list

def get_key_phrases(text_list, language_code):
    length = math.ceil(len(text_list)/25)

    i = 0
    result_list = []
    while i < length:
        response = client.batch_detect_key_phrases(
        TextList= text_list[(i*25):((i+1)*25)],
        LanguageCode= language_code
        )
        i += 1
        result_list += response['ResultList']

    if(not response['ResponseMetadata']['HTTPStatusCode']):
        raise RuntimeError(response['ResponseMetadata']['HTTPStatusCode'])

    return result_list


# res = generate(["A coronary artery, bypass, graft or cabbage is performed to improve circulation to the heart muscle in people with severe coronary artery disease.", "In this procedure, a healthy artery or vein from another part of the body is connected or grafted to the blocked, coronary artery.", "The grafted, artery or vein bypasses the blocked portion of the coronary artery, carrying oxygen-rich blood to the heart muscle, one or more coronary arteries may be bypassed during a single operation before the surgery, an intravenous line will be started and you may be given a medication to Help you relax." ],'en')
# print(res)