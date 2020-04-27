import json
from urllib import parse
import os.path
import json
from nltk.corpus import wordnet as wn
import random
from keyword_generator import generate
import time
import re
from nltk.tokenize import sent_tokenize, word_tokenize

"""Generates Quiz for text
"""

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

class Article:
    def __init__(self, article):
        self.sentences = sent_tokenize(article)

    def generate_trivia_sentences(self):
        sentences = self.sentences
        sentences.pop()
        
        trivia_sentences = []

        keyword_list = generate(sentences,'en')

        for cur_index, sentence in enumerate(sentences):
            if not keyword_list[cur_index]:
                continue

            trivia = {
                "sentence": str(sentence), 
            }
            trivia["question"] = sentence.replace(keyword_list[cur_index], " ______________ ")

            trivia["answers"] = []
            correct_answer = keyword_list[cur_index].strip().lower()

            trivia['answers'].append(correct_answer)

            similar_words = self.get_similar_words(correct_answer)
            if len(similar_words) < 3:
                continue

            trivia['answers'].extend(random.sample(similar_words,3))

            random.shuffle(trivia['answers'])
            if len(trivia['answers']) < 3:
                continue

            if len(trivia['answers'])==3:
                trivia['answers'].append('None of the Above')
            
            if len(trivia['answers'])>1:
                trivia['correctIndex'] = trivia['answers'].index(correct_answer)
                trivia['jumpToTime'] = 0

            trivia_sentences.append(trivia)

        return trivia_sentences

    def get_similar_words(self, word):
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos='n')

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]

        # Get the hypernym for this synset (again, take the first)
        hypernyms = synset.hypernyms()
        if len(hypernyms) <= 0:
            return []
        
        hypernym = hypernyms[0]
        
        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()

        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
            
            if similar_word != word:
                similar_words.append(similar_word)

            if len(similar_words) == 8:
                break
        similar_words = [x for x in similar_words if x not in word]

        return similar_words

def generate_trivia(article):

    questions = []
    
    article = Article(article)
    generated_sentence = article.generate_trivia_sentences()
    if(generated_sentence):
        questions = questions + generated_sentence
    '''f=open("questions.json","a")
    print('Questions ' + json.dumps(questions))
    f.write(json.dumps(questions))
    f.close()'''
    return questions

