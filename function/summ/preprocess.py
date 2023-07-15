# Module to preprocess the csv file
# Import necessary packages to preprocess the data
# Clean Text like Earth's method
import re
import numpy as np
import pandas as pd
import gensim

import pythainlp
from pythainlp.corpus.common import thai_stopwords
from pythainlp.word_vector import WordVector
from pythainlp.tokenize import word_tokenize, THAI2FIT_TOKENIZER
from pythainlp.corpus.common import thai_words
from pythainlp.util import Trie
from pythainlp.tag import pos_tag

from function.summ.simple_thai_sentence_segmentation import ThaiSentenceSegmentor

def clean_text(text):

  # remove @ mention
  text = re.sub(r'@[A-Za-z0-9\u0E00-\u0E7F_\-]+', '', text, flags=re.I)

  # remove link url
  text = re.sub(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', '', text, flags=re.I)

  # remove hashtag that are end of content (not between the sentence)
  text = text.strip()
  text = re.sub(r'( +#)', '#', text, flags=re.I)
  text = re.sub(r'(#[A-Za-z0-9\u0E00-\u0E7F_\-]+)+$', '', text, flags=re.I)

  # replace apostrophe http://www.unicode.org/charts/PDF/U2000.pdf
  text = re.sub(r'[\u0022\u021C\u021D”“]', '"', text, flags=re.I)
  text = re.sub(r'[\u0027\u0060\u00B4\u0018\u0019’‘]', "'", text, flags=re.I)

  # remove non-thai character, non-english character, punctuatioin exept ' " , . <spacebar> \n
  text = re.sub(r'[^\u0E00-\u0E7Fa-zA-Z0-9\'\"\., \n]', '', text).strip()

  #clear multiple dot
  text = re.sub('\.+', '.', text)

  #clear multiple !
  text = re.sub('!+', '!', text)

  #clear multiple ?
  text = re.sub(r'\?+', '?', text)

  #clear multiple 5
  text = re.sub(r'[456]+', '', text)

  #clear multiple space
  text = re.sub(' +', ' ', text)

  #clear multiple space and dot
  text = re.sub(r'( \.)+', '', text)

  # replace newline char with special sentinel <sep>
  text = re.sub(r'(\n+ *)+', '<sep>', text)



  return text

# Remove tweets that are all in English
def is_all_non_thai(text):
#   Regex unicode for Thai language
  regex = r"[(\u0E00-\u0E7F)]+"
    
  match = re.search(regex, text)
  return match is None

# Method for splitting sentences
def split_sentences(s, segmentor):
  sentences = [i.strip().lower() for i in segmentor.split_into_sentences(s)]
  sentences = '<sep>'.join(sentences)
  # print(sentences)
  sentences = re.sub(r' *<sep> *', '<sep>', sentences)
  sentences = re.sub(r'<sep>.{0,3}<sep>', '<sep>', sentences, flags=re.I)
  sentences = re.sub(r'(<sep>)+', '<sep>', sentences)
  return sentences

# filter by these rules

# 1.   remove repetive tokens <br>
# eg. <br>
# ถถถถถ -> empty string <br>
# จังงงง -> จัง <br>
# เย่ๆๆๆๆๆ -> เย่ <br>
# 2.   have less tokens than 5 tokens
# 3.   is not setence; do not have NOUN and VERB 
def filter_sentence(tokenized):
    tweets = tokenized.split('|<sep_tweet>|')
    filtered_tweet = []
    for tweet in tweets:

        s = tweet.split('|<sep>|')
        # print(s)
        s = [sen.split('|') for sen in s]
        pos_list = [pos_tag(sen, corpus='orchid_ud') for sen in s]
        # print(pos_list)
        filtered_s = []
        for sen in pos_list:

            # check repetitive token
            new_tok_list = []
            for pos in sen:
              # new_tok = re.sub(r'(.)\1{1,}', '', pos[0])
              if re.match(r'(.)\1{1,}', pos[0]):
                  # ignore repetitive token
                  continue

              new_tok_list.append((pos[0], pos[1]))
            sen = new_tok_list
            # print(sen)

            # check token length
            if len(sen) < 5:
              # print('remove short sentence: {}'.format(sen))
              continue

            # check pos; is_sentence = has_verb & has_noun
            has_verb = False
            has_noun = False
            is_sentence = False
            for pos in sen:
                if pos[1] == 'VERB':
                    has_verb = True
                elif pos[1] == 'NOUN':
                    has_noun = True
                if has_verb and has_noun:
                    is_sentence = True
                    break
            if is_sentence:
                filtered_s.append('|'.join([pos[0] for pos in sen]))
            else:
                # print('remove not sentence: {}'.format(sen))
                continue

        filtered_tweet.append('|<sep>|'.join(filtered_s))
    return '|<sep_tweet>|'.join(filtered_tweet)


def clean_scraped(df):
    # Function to translate and remove URLs
    MIN_CHAR = 20
    # Custom dict for tokenizing words
    custom_dict = set(thai_words())
    custom_dict.add('<sep>')
    custom_dict.add('<sep_tweet>')

    trie = Trie(words=custom_dict)
    # Segmentor used in Thaisum preparation for BERTSum training
    segmentor = ThaiSentenceSegmentor()
    # If it is empty, return None
    if df.shape[0] == 0:
        return None
    # Remove URLs
    url_pattern = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
    df['content'] = df['content'].apply(lambda x: re.sub(url_pattern, '', x))
    df['content'] = df['content'].apply(lambda x: clean_text(x))
    df = df[~df['content'].apply(is_all_non_thai)]
    df = df[df['content'].apply(lambda x: len(x)>MIN_CHAR)]
    df['content'] = df['content'].apply(split_sentences, segmentor=segmentor)
    all_tweets = '<sep_tweet>'.join(df['content'].tolist())
    tok_list = word_tokenize(all_tweets, engine='newmm', keep_whitespace=False, custom_dict=trie)
    tok = '|'.join(tok_list)
    cleaned_contents = filter_sentence(tok)



    return cleaned_contents


