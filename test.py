from function.summ.preprocess import clean_scraped
import pandas as pd
from function.summ.kl_topic_modeling import pipeline
from function.summ.textrank import batch_prepared
from function.summ.summary import summarise
import warnings

warnings.filterwarnings('ignore')


# Test for kl topic modeling
df = pd.read_csv('static/data/news.csv')
df = df[df['hashtag'] == '#บอสอยู่วิทยา']

# Clean
clean = clean_scraped(df)

# Topic Modeling
cluster = pipeline(clean)
print(len(cluster))

# Test cluster preproces
batches = batch_prepared(cluster, batch_size=1, method='tfidf', separator='<\s>')
print(batches)
print(len(batches))

# Summarise
summaries = ''
for b in batches:
    s = summarise(b)['response']
    print(s)
    # Join to be string
    s = ' '.join(s)+ ' '
    summaries += s
summaries = summaries.strip()

print(summaries)