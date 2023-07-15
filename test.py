from function.summ.preprocess import clean_scraped
import pandas as pd
from function.summ.kl_topic_modeling import pipeline
from function.summ.textrank import batch_prepared
from function.summ.summary import summarise
import warnings
from function.summ.topic_bert import get_bert

warnings.filterwarnings('ignore')

print("Reading File...")
# Test for kl topic modeling
df = pd.read_csv('static/data/news.csv')
df = df[df['hashtag'] == '#บอสอยู่วิทยา']

# Clean
print("Cleaning Data...")
clean = clean_scraped(df)

print("Getting BERTopic cluster...")
# Topic Modeling
cluster = eval(get_bert(clean)['response'])
print(cluster)
print(len(cluster))

# Test cluster preproces
batches = batch_prepared(cluster, batch_size=1, method='tfidf', separator='<\s>')
print(batches)
print(len(batches))

# Summarise
summaries = ''
for b in batches:
    s = eval(summarise(b)['response'])
    # Join to be string
    s = '\n'.join(['-'+sm for sm in s])+ '\n'
    print(s)
    summaries += s
summaries = summaries.strip()

print(summaries)