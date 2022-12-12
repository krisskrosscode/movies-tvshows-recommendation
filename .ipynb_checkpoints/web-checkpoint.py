import streamlit as st
import pickle
import requests 

api_key = '1cd00a14'


tvshows_list = pickle.load(open('tvshows.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('TV Shows recommendation')

selected_tvshow = st.selectbox(
    "Select a TV Show you like",
    tvshows_list
)


def fetch_poster(tv_id):

    search_keyword = tvshows_list.iloc[tv_id].Title.replace(' ', '-')
    # release_year = 
    response = requests.get('http://www.omdbapi.com/?t={}&apikey={}'.format(search_keyword, api_key))
    data = response.json()
    if data['Response'] == True and 'Poster' in data :
        return data['Poster']
    else:
        return 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.redbubble.com%2Fshop%2Fimage%2Bloading%2Bposters&psig=AOvVaw2lrNHdtYc7Ab4G179Mty_f&ust=1670838998839000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCIilyrim8fsCFQAAAAAdAAAAABAE'
    # return data['poster_path']

def recommend(tvshow):
    index = tvshows_list[tvshows_list['Title'] == tvshow].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommended_shows = []
    recommended_shows_posters = []
    for i in distances[1:6]:
        recommended_shows.append(tvshows_list.iloc[i[0]].Title)
        poster = fetch_poster(i[0])
        recommended_shows_posters.append(poster)


    return recommended_shows, recommended_shows_posters



if st.button('Recommend'):
    st.write(recommend(selected_tvshow))
    names, posters  = recommend(selected_tvshow)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])

