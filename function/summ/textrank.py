# Dummy function for preprocessing
import pandas as pd
import numpy as np
from pythainlp.word_vector import WordVector
from pythainlp.tokenize import word_tokenize, THAI2FIT_TOKENIZER
from pythainlp.corpus.common import thai_words
from pythainlp.util import Trie
from pythainlp.corpus.common import thai_stopwords
from pythainlp.tag import pos_tag

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

wv = WordVector()
wv_model = wv.get_model()

# Function for calculating TF-IDF weighted average of words
def word_average_tfidf(model, vocab, tweet, transformed):
    result = np.zeros(300)
    tf = 0
    # Loop for each word
    for word in tweet:
        # If word is in
        if (word in model) and (word in vocab.keys()):
            # Get the value
            w2v = model.get_vector(word)
            tfidf = transformed.getrow(0).getcol(vocab[word]).toarray()[0][0]
            tf += tfidf
            result += tfidf*w2v

    # If there is no words
    if np.all(result==0):
        return np.zeros(300)

    else:
        return result/tf

# Pagerank in each cluster and feed to our model
def preprocess(tokenized, separator='<\s>', method='tfidf'):
    thai_sw = list(thai_stopwords())
    # Join tokenized sentences
    tweets = [''.join(t) for t in tokenized]
    augmented_tweets = [THAI2FIT_TOKENIZER.word_tokenize(t) for t in tweets]
    # print("\nInput Tweets")
    # for sen in sentences[:10]:
    #     print(sen)
    # print("Fitting TFIDF...")
    if method=='tfidf':
        # Fit the TFIDF vectorizer
        vectorizer = TfidfVectorizer(tokenizer=THAI2FIT_TOKENIZER.word_tokenize, stop_words=None)
        X = vectorizer.fit_transform(tweets)
        word2id = vectorizer.vocabulary_
        # Then, apply sent_vectorize
        vectorized_tweets = np.vstack([word_average_tfidf(model=wv_model, vocab=word2id, tweet=tweet, transformed=X[i]) \
                                    for i,tweet in enumerate(augmented_tweets)])

    elif method=='normal':
        vectorized_tweets = np.vstack([wv.sentence_vectorizer(tweet) for tweet in tweets])
    # Apply textrank
    sims = cosine_similarity(vectorized_tweets)

    for i in range(sims.shape[0]):
        sims[i][i] = 0.0

    g = nx.from_numpy_array(sims)

    result = nx.pagerank(g)

    # print(result)

    # Sort by final weight
    tweets = [tweets[x[0]] for x in sorted(result.items(), key=lambda x: x[1], reverse=True)]
    # debug
    # print("\nRanked Tweets")
    # for sen in sentences[:10]:
    #     print(sen)
    tweets = separator.join(tweets)
    return tweets

# Prepare to batch inputs
def batch_prepared(cluster, batch_size=1, method='tfidf', separator='<\s>'):

    # Get row with same hashtag
    all_batch = []

    keys = list(cluster.keys())
    iterations = len(keys)//batch_size
    if len(keys) % batch_size != 0:
        iterations += 1

    for i in range(iterations):
        prepared = []
        for k in keys[batch_size*i: min(batch_size*(i+1), len(keys))]:
            s = preprocess(cluster[k], method=method, separator=separator)
            # s = '<\s>'.join([''.join(c) for c in cluster[k]])[:4096]
            prepared.append(s)

        all_batch.append(prepared)

    return all_batch