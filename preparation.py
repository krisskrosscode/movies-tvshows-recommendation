import pandas as pd
import numpy as np
import warnings 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer


warnings.filterwarnings('ignore')
import ast

amazon = pd.read_csv('./amazon/titles.csv')
netflix = pd.read_csv('./netflix/titles.csv')

df = pd.concat([amazon, netflix], axis = 0)

df.title.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df['description'].fillna('', inplace = True)
df['description'] = df['description'].apply(lambda x : x.split()) 
df['genres'] = df['genres'].apply(lambda x : ast.literal_eval(x))
df['tags'] = df['title'].str.split() + df['description'] + df['genres']
df_new = df[['title', 'tags']]
df_new['tags'] = df_new['tags'].apply(lambda x : str(x).split() if type(x) != list else x)
df_new['tags'] = df_new['tags'].apply(lambda x : ' '.join(x))

cv = CountVectorizer(max_features=2000,stop_words='english')
vector = cv.fit_transform(df_new['tags']).toarray()

similarity  = cosine_similarity(vector)


