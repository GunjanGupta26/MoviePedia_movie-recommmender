
import streamlit as st
import pickle
import pandas as pd
import requests

# importing the required font from google fonts
st.markdown(""" <style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather&family=Montserrat&family=Roboto:wght@400;700&family=Sacramento&display=swap');
</style> """, True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

# function made to fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0108dc86ebfe744113ad8b08e230d9cb&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


st.title('MoviePedia')
st.markdown("""<hr></hr>""",True)
st.header('Movie Recommender')
st.markdown(""" ##### _Find movies similar to the one you loved!_ :popcorn: """)
st.write('')

 
model = pickle.load(open('model.pkl','rb'))
model1 = pickle.load(open('model1.pkl','rb'))
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# selectbox to select a movie from the list of movies
selected_movie_name = st.selectbox(' Type or Select a movie from the dropdown below', movies['original_title'].values)

# function made to take a movie and return the 5 movies that are returned from the ML model after applying the sorting algorithm 
def recommend_overview_genre(selected_movie_name,s =model1):
    index = movies[movies['original_title'] == selected_movie_name ].index.values[0]
    sig_scores = sorted(list(enumerate(s[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_poster = []

    for i in sig_scores[1:6]:

        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].original_title)
        # fetch poster from API
        try:
            recommended_movie_poster.append(fetch_poster(movie_id))
        except:
            print("Poster Unavailable")

    return recommended_movie_names,recommended_movie_poster

# button
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend_overview_genre(selected_movie_name)

# five columns to display five movies' name and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        try:
            st.image(recommended_movie_posters[0])
        except:
            print("Poster Unavailable")
    with col2:
        st.text(recommended_movie_names[1])
        try:
            st.image(recommended_movie_posters[1])
        except:
            print("Poster Unavailable")
    with col3:
        st.text(recommended_movie_names[2])
        try:
            st.image(recommended_movie_posters[2])
        except:
            print("Poster Unavailable")
    with col4:
        st.text(recommended_movie_names[3])
        try:
            st.image(recommended_movie_posters[3])
        except:
            print("Poster Unavailable")
    with col5:
        st.text(recommended_movie_names[4])
        try:
            st.image(recommended_movie_posters[4])
        except:
            print("Poster Unavailable")


