import urllib.request
import pickle
import requests
tvshows = pickle.load(urllib.request.urlopen("https://www.jiocloud.com/l/?u=SIA5Sze3ZN4NjvdVySCpemS-QV_IkeVr-jVQJaPYiH4=hIb"))

print(tvshows.iloc[0])
api_key = '1cd00a14'

def fetch_poster(id):
    # id = mediadf[mediadf['title'] == name]['imdb_id']
    # search_keyword = tvshows_list.iloc[tv_id].title.replace(' ', '-')
    # release_year = 
    response = requests.get('http://www.omdbapi.com/?i={}&apikey={}'.format(id, api_key))
    data = response.json()
    # if data['Response'] == 'True' and 'Poster' in data :
    #     return data['Poster']
    # else:
    #     return ''
    return data['Poster']


print(fetch_poster('tt0850645'))