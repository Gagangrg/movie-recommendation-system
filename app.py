import pickle
import streamlit as st
import requests
import streamlit.components.v1 as components
from time import sleep

# ----------------------------
# TMDb poster fetch
# ----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9a822079af3bd503eb7defeeb091b314&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

# ----------------------------
# Recommend movies
# ----------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ----------------------------
# Load backend data
# ----------------------------
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown(
    """
    <style>
    /* Background cinematic gradient */
    body {
        background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .stButton button {
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stButton button:hover {
        background-color: #b00610;
        transform: scale(1.05);
        transition: 0.3s;
    }
    .stSelectbox>div>div>div {
        background-color: #1c1c1c;
        color: white;
        border-radius: 8px;
        padding: 4px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title(" Movie Recommender System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie:", movie_list)

if st.button("Show Recommendation"):
    # Lazy-loading / processing indicator
    with st.spinner("Fetching recommendations... "):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        sleep(1)  # simulate loading time

    # Generate HTML cards
    cards_html = ""
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        cards_html += f"""
        <div class="card">
            <img src="{poster}" loading="lazy" alt="{name}" />
            <p>{name}</p>
        </div>
        """

    html_code = f"""
    <style>
    .cards-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        margin-top: 20px;
    }}
    .card {{
        width: 180px;
        background: #1c1c1c;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.7);
        text-align: center;
        padding: 10px;
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    .card:hover {{
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 12px 25px rgba(255,0,0,0.6);
    }}
    .card img {{
        width: 100%;
        border-radius: 12px;
        display: block;
    }}
    .card p {{
        margin-top: 8px;
        font-weight: bold;
        font-size: 14px;
        color: #ffffAC;
    }}
    </style>

    <div class="cards-container">
        {cards_html}
    </div>
    """

    components.html(html_code, height=450, scrolling=True)
