import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.models.ldamodel import LdaModel
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from scipy import stats
from pythainlp.util import Trie
from pythainlp.corpus.common import thai_stopwords

class Topic_kl:

    def __init__(self, tokenized):
        self.row = tokenized
        self.epsilon = 1e-8

    def tokenize_tweet(self):
        text = self.row
        text = text.split('|<sep_tweet>|')
        text = [[tmp for tmp in tweet.split("|") if tmp not in ['<sep>']] for tweet in text]
        self.tweets = text

    def get_vocabs(self, min_count=3, n_gram='bigram'):
        tweets = self.tweets
        # Join vocab that occurs
        bigram = gensim.models.Phrases(tweets, min_count=min_count, threshold=100)
        trigram = gensim.models.Phrases(bigram[tweets], threshold=100)

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        if n_gram=='bigram':
            corpus = [bigram_mod[c] for c in tweets]
        elif n_gram=='trigram':
            corpus = [trigram_mod[c] for c in tweets]

        corpus = [[w if len(w.split('_'))==0 else ''.join(w.split('_')) for w in t ] for t in corpus]
        corpus = [[w for w in t if len(w) > 1] for t in corpus]

        # remove stopwords
        thai_sw = list(thai_stopwords())
        cleaned_corpus = [[word for word in tweet if word not in thai_sw] for tweet in corpus]

        # Get the vocab dictionary
        id2word = corpora.Dictionary(cleaned_corpus)
        # Convert to BOW
        bow = [id2word.doc2bow(c) for c in cleaned_corpus]

        self.bow, self.id2word, self.corpus, self.cleaned_corpus = bow, id2word, corpus, cleaned_corpus

        # self.real_corpus = [id2word.doc2bow(text) for text in cleaned_corpus]

    def load_lda(self, k=15):
        self.lda_model = LdaModel(corpus=self.bow, id2word=self.id2word, num_topics=k, random_state=42,
                update_every=1, chunksize=100, passes=100, alpha='auto', per_word_topics=True)

    def convert_to_df(self):
        d = {}
        for i, doc in enumerate(self.lda_model.get_document_topics(self.bow, minimum_probability=0)):
            d[i] = [prob[1] for prob in doc]
        self.doc_topic_df = pd.DataFrame.from_dict(d)

        d2 = {}
        for i in range(len(self.lda_model.get_topics())):
            sorted_topic_terms = sorted(self.lda_model.get_topic_terms(i, topn=len(self.id2word)), key=lambda x: x[0])
            word_prob = [x[1] for x in sorted_topic_terms]
            d2[i] = word_prob
        self.topic_word_df = pd.DataFrame.from_dict(d2)

    def z_normalize_list(self, score_dict):
        score_list = [value for value in score_dict.values()]

        percentile_95 = np.percentile(score_list, 95)
        percentile_5 = np.percentile(score_list, 5)

        mean = np.mean(score_list)
        std = np.std(score_list)

        z_score_95th = (percentile_95 - mean) / std
        z_score_5th = (percentile_5 - mean) / std

        scaled_dict = {k: (v - mean) / std for k, v in score_dict.items()}
        # capping z-score of all values to be between 5th and 95th percentile, and adding 95th percentile to shift the scale
        z_scores_capped = {k: min(z_score_95th, max(z_score_5th, v)) + z_score_95th for k, v in scaled_dict.items()}

        z_scores_capped_max = max([v for v in z_scores_capped.values()])
        z_scores_capped = {k: v / z_scores_capped_max for k, v in z_scores_capped.items()}

        return z_scores_capped

    def kl_df(self, col, df):
        arr = col.to_numpy()
        result = np.log((arr.reshape(-1, 1) + self.epsilon) / (df + self.epsilon)) * arr.reshape(-1, 1)
        return result.sum(axis=1)

    # def diver_df(self, df):
    #     tqdm.pandas()
    #     return df.progress_apply(lambda x: self.kl_df(x, df), axis=0)

    def get_diver_df(self):
        kl_word = self.topic_word_df.apply(lambda x: self.kl_df(x, self.topic_word_df), axis=0)
        kl_topic = self.doc_topic_df.apply(lambda x: self.kl_df(x, self.doc_topic_df), axis=0)
        self.kl_word = kl_word
        self.kl_topic = kl_topic

        kl_topic['sum'] = kl_topic.sum(axis=1)/kl_topic.shape[1]
        kl_word.loc['sum'] = kl_word.sum(axis=0)/kl_word.shape[0]

        word_div = kl_word.loc['sum'].to_numpy()
        topic_div = kl_topic.loc[:, 'sum'].to_numpy()

        self.word_div_norm = word_div / word_div.max()
        self.topic_div_norm = topic_div / topic_div.max()

    def rank_topic(self, kl_ctrl, social_ctrl, percentile):
        rank = {}
        for i in range(self.word_div_norm.shape[0]):
            rank[i] = kl_ctrl * self.word_div_norm[i] + (1 - kl_ctrl) * self.topic_div_norm[i]

        dict_sorted = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        rank_list = [(k ,v) for k, v in dict_sorted.items()]
        score_list = [topic[1] for topic in rank_list]
        mean = sum(score_list) / len(rank_list)
        p_value = None
        if percentile is not None:
            p_value = np.percentile(score_list, percentile)
        return rank_list, mean, p_value

    def get_topic_rank(self, hashtag=None, k=15, kl_ctrl=0.5, mean_fil=True, social_ctrl=0.5, percentile=None):
        self.tokenize_tweet()
        self.get_vocabs()
        self.load_lda(k)
        self.convert_to_df()
        self.get_diver_df()
        rank_list, mean, p_value = self.rank_topic(kl_ctrl, social_ctrl, percentile)
        # print('rank list before filter', rank_list)
        if p_value is not None:
            rank_list = [topic for topic in rank_list if topic[1] >= p_value]
        if mean_fil:
            rank_list = [topic for topic in rank_list if topic[1] >= mean]
        self.rank_list = rank_list
        return self.rank_list

    def get_topic_words(self):
        result = []
        for topic, words in self.lda_model.show_topics(formatted=False):
            topics_words = list()
            if topic in [t[0] for t in self.rank_list]:
                topics_words.append(str(topic))
                for w in words[:10]:
                    topics_words.append(w[0])
                topics_words = "_".join(topics_words)
                result.append(topics_words)
        self.topic_words = result

    def get_cluster(self):
        filtered_topics = [topic[0] for topic in self.rank_list]
        dic = defaultdict(list)
        for doc_bow, doc_text in zip(self.bow, self.corpus):
            doc_topics = self.lda_model.get_document_topics(doc_bow)
            doc_topics = [tp for tp in doc_topics if tp[0] in filtered_topics]
            top_topic = max(doc_topics, key=lambda x: x[1])[0]
            dic[top_topic].append(doc_text)

        self.cluster = dict(dic)
        # return self.cluster

# Function for inputting clean scraped and get dict of cluster
def pipeline(clean):
    tmp = Topic_kl(clean)
    tmp.get_topic_rank(k=15, percentile=75)
    tmp.get_topic_words()
    tmp.get_cluster()

    return tmp.cluster
