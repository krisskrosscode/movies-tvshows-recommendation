import streamlit as st
import pickle
import requests 
import pandas as pd
from preparation import similarity as similarity_ndarray
api_key = '1cd00a14'


tvshows_list = pickle.load(open('tvshows.pkl', 'rb'))
# similarity = pickle.load(open('similarity2.pkl', 'rb'))
similarity = similarity_ndarray
st.title('Movies/TV Shows recommendation')

selected_tvshow = st.selectbox(
    "Select a Movie/TV Show you like",
    tvshows_list
)

mediadf = pickle.load(open('imdbid.pkl', 'rb'))

def fetch_poster(name):
    id = mediadf[mediadf['title'] == name].iloc[0]['imdb_id']
    response = requests.get('http://www.omdbapi.com/?i={}&apikey={}'.format(id, api_key))
    data = response.json()
    # print(data)
    if 'Poster' in data :
        return data['Poster']
    
    return 'https://t3.ftcdn.net/jpg/04/62/93/66/360_F_462936689_BpEEcxfgMuYPfTaIAOC1tCDurmsno7Sp.jpg'

def fetch_info(name):
    id = mediadf[mediadf['title'] == name].iloc[0]['imdb_id']
    response = requests.get('http://www.omdbapi.com/?i={}&apikey={}'.format(id, api_key))
    data = response.json()
    if data['Response'] == 'True':
        res = dict((i, data[i]) for i in ['Title', 'Genre' , 'Type', 'Released','Director', 'Actors', 'Plot','Language', 'Country', 'imdbRating'] if i in data)
        return res
    return {"Reponse" : "False"}

def recommend(tvshow):
    index = tvshows_list[tvshows_list['title'] == tvshow].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommended_shows = []
    recommended_shows_posters = []
    for i in distances[1:6]:
        recommended_shows.append(tvshows_list.iloc[i[0]].title)
        poster = fetch_poster(tvshows_list.iloc[i[0]].title)
        recommended_shows_posters.append(poster)


    return recommended_shows, recommended_shows_posters



if st.button('Recommend'):
    # st.write(recommend(selected_tvshow))
    st.subheader('Selected Movie/TV Show')
    col1, col2 = st.columns(2)
    with col1 :
        st.image(fetch_poster(selected_tvshow))
    with col2 :
        st.json(fetch_info(selected_tvshow))

    st.subheader('Movies/TV Shows you might like')
    names, posters  = recommend(selected_tvshow)
    for i in range(5):
        with st.container():
            with st.expander(names[i]):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(posters[i])
                with col2 :
                    st.json(fetch_info(names[i]))

    

