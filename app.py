import streamlit as st
import pickle
import pandas as pd
import requests
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Mood Based Content Recommendation System",
    layout="wide"
)

# -------------------- CONSTANTS --------------------
TMDB_API_KEY = "a84be0503a6805142e7dce9d569710e9"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"

# -------------------- FUNCTIONS --------------------

def fetch_poster(movie_id):
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


def recommend(movie, mood):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[movie_index]))

    # Base sorting
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    # Mood-based behavior
    if mood == "Happy":
        candidates = distances[1:15]        # stronger similarity
    elif mood == "Sad":
        candidates = distances[5:25]        # deeper emotional neighbors
    else:  # Neutral
        candidates = distances[1:20]

    random.shuffle(candidates)

    recommended_movies = []
    recommended_posters = []

    for i in candidates[:5]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


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
    names, posters = recommend(selected_movie, mood)

    st.subheader(f"🎯 Recommendations for mood: **{mood}**")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i], width="stretch")
            else:
                st.warning("Poster not available")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("© 2026 Mood Based Content Recommendation System")
