import streamlit as st
import pickle
import pandas as pd
import requests
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Movie&Mood Based Content Recommendation System",
    layout="wide"
)

# -------------------- CONSTANTS --------------------
TMDB_API_KEY = "a84be0503a6805142e7dce9d569710e9"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"

# -------------------- FUNCTIONS --------------------

def fetch_poster(movie_id):
    """Fetch movie poster safely from TMDB"""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=5
        )
        data = response.json()
        if data.get("poster_path"):
            return POSTER_BASE_URL + data["poster_path"]
        return None
    except:
        return None


def recommend_by_movie(movie):
    """Recommendation based ONLY on selected movie"""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[movie_index]))

    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    names, posters = [], []
    for i in distances:
        movie_id = movies.iloc[i[0]]['movie_id']
        names.append(movies.iloc[i[0]]['title'])
        posters.append(fetch_poster(movie_id))

    return names, posters


def recommend_by_mood(mood):
    """Recommendation based ONLY on mood (independent of selected movie)"""
    total_movies = len(movies)
    indices = list(range(total_movies))

    if mood == "Happy":
        sampled = random.sample(indices, 20)
    elif mood == "Sad":
        sampled = random.sample(indices, 20)
    else:  # Neutral
        sampled = random.sample(indices, 20)

    names, posters = [], []
    for idx in sampled[:5]:
        movie_id = movies.iloc[idx]['movie_id']
        names.append(movies.iloc[idx]['title'])
        posters.append(fetch_poster(movie_id))

    return names, posters


# -------------------- LOAD DATA --------------------

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# -------------------- UI --------------------

st.title("🎬 Mood Based Content Recommendation System")

col_search, col_mood = st.columns([3, 1])

with col_search:
    selected_movie = st.selectbox(
        "Search Movie",
        movies['title'].values
    )

with col_mood:
    mood = st.radio(
        "Mood ❤️",
        ["Happy 😊", "Sad 😢", "Neutral 😐"],
        horizontal=True
    )
    mood = mood.split()[0]

# -------------------- ACTION --------------------

if st.button("Recommend"):

    # -------- Selected Movie Based --------
    st.subheader(f"🎯 Because you selected: **{selected_movie}**")
    movie_names, movie_posters = recommend_by_movie(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(movie_names[i])
            if movie_posters[i]:
                st.image(movie_posters[i], width="stretch")
            else:
                st.warning("Poster not available")

    st.markdown("---")

    # -------- Mood Based --------
    st.subheader(f"❤️ Because you feel: **{mood}**")
    mood_names, mood_posters = recommend_by_mood(mood)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(mood_names[i])
            if mood_posters[i]:
                st.image(mood_posters[i], width="stretch")
            else:
                st.warning("Poster not available")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("© 2026 Mood Based Content Recommendation System")
