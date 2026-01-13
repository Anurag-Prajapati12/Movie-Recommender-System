import streamlit as st
import pickle
import requests
import concurrent.futures
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
import os

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
            #global response
            session=requests.Session()
            retry=Retry(connect=1,backoff_factor=0.5)
            adapter=HTTPAdapter(max_retries=retry)
            session.mount('http://',adapter)
            session.mount('https://',adapter)
            load_dotenv()
            API_KEY = os.getenv("TMDB_API_KEY")

            try:
                response=session.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US',timeout=3)
                response.raise_for_status()
                data=response.json()
                return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
            except Exception as e:
                print('Error:',e)
                return "https://via.placeholder.com/500x750?text=No+Image"

        #st.write(f"Poster URL: https://image.tmdb.org/t/p/w500{data.get('poster_path')}")


def recommend(movie):
    index = data[data['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        recommended_movies.append(data.iloc[i[0]].title)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            recommended_movies_poster.append(fetch_poster(data.iloc[i[0]].movie_id))
        #time.sleep(0.3)#adding delay
    return recommended_movies, recommended_movies_poster

data=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies_list=data['title'].values


st.title('Movie Recommender System')

option=st.selectbox('type movie name',movies_list)


if st.button('Recommend'):
    names, poster=recommend(option)
    #st.write(poster[0])

    col1, col2, col3, col4, col5, =st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
