import numpy as np
import pandas as pd
import ast
import nltk
import streamlit as st
st.title("Movie Recommendation System")
movies = pd.read_csv('C:\\Users\\manoj\\OneDrive\\Desktop\\MRC\\tmdb_5000_movies.csv')
credits = pd.read_csv('C:\\Users\\manoj\\OneDrive\\Desktop\\MRC\\tmdb_5000_credits.csv')
movies = movies.merge(credits,on="title")
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace = True)
# import ast
def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
def convert_first3(obj):
    l=[]
    count = 1
    for i in ast.literal_eval(obj):
        if count > 3:
            break
        l.append(i['name'])
        count+=1
    return l
movies['cast'] = movies['cast'].apply(convert_first3)
#movies['crew'][0]
def get_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
    return l
movies['crew'] = movies['crew'].apply(get_director)
#movies['overview'][0]
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies_df = movies[['movie_id','title','tags']]
movies_df['tags'] = movies_df['tags'].apply(lambda x: " ".join(x))
#movies_df['tags'][0]
movies_df['tags'] = movies_df['tags'].apply(lambda x: x.lower())
# import nltk
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=5000, stop_words='english')
features = vectorizer.fit_transform(movies_df['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(features)
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        st.markdown(movies_df.iloc[i[0]].title)
text=st.text_input('Enter')
recommend(text)
