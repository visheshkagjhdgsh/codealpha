import pickle
import streamlit as st
import requests

# Function to fetch poster image
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to fetch movie details (e.g., description, rating)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    description = data.get('overview', 'No description available')
    rating = data.get('vote_average', 'No rating available')
    return description, rating

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    recommended_movie_ratings = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        description, rating = fetch_movie_details(movie_id)
        recommended_movie_descriptions.append(description)
        recommended_movie_ratings.append(rating)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions, recommended_movie_ratings


# Set up Streamlit UI
st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for selecting a movie
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# When the user clicks "Show Recommendations"
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions, recommended_movie_ratings = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display recommended movies in columns
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.text(f"Rating: {recommended_movie_ratings[0]}")
        st.text(f"Description: {recommended_movie_descriptions[0]}")

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.text(f"Rating: {recommended_movie_ratings[1]}")
        st.text(f"Description: {recommended_movie_descriptions[1]}")

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.text(f"Rating: {recommended_movie_ratings[2]}")
        st.text(f"Description: {recommended_movie_descriptions[2]}")

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.text(f"Rating: {recommended_movie_ratings[3]}")
        st.text(f"Description: {recommended_movie_descriptions[3]}")

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.text(f"Rating: {recommended_movie_ratings[4]}")
        st.text(f"Description: {recommended_movie_descriptions[4]}")

# Add empty space to push the button to the bottom
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# Add custom styles for the "Developed by Shivay Mehra" button
st.markdown(
    """
    <style>
    .dev-text {
        font-size: 16px;
        color: white;
    }
    .dev-button {
        background-color: black;
        color: white;
        padding: 0.5em 1em; /* Adjust the padding to fit the text */
        border: 2px solid grey;
        border-radius: 0.25em;
        text-align: center;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: color 0.3s ease;
        margin-top: 2em;
        white-space: nowrap;  /* Prevent text wrapping */
    }
    .dev-button:hover {
        color: red; /* Text turns red on hover */
    }
    .feedback {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background-color: #212121;
        padding: 1em;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .feedback input {
        width: 150px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display text "Developed by" and a clickable button for "Shivay Mehra"
st.markdown('<div class="dev-text" style="text-align: center;">Developed by <a href="https://www.linkedin.com/in/shivay-mehra-8a66ba251/" class="dev-button" target="_blank">Shivay Mehra</a></div>', unsafe_allow_html=True)

# Feedback form positioned in the bottom-right corner
st.markdown("""
<div class="feedback">
    <h4>Your Feedback</h4>
    <form>
        <label>How would you rate the recommendations?</label><br>
        <input type="radio" id="excellent" name="feedback" value="Excellent">
        <label for="excellent">Excellent</label><br>
        <input type="radio" id="good" name="feedback" value="Good">
        <label for="good">Good</label><br>
        <input type="radio" id="average" name="feedback" value="Average">
        <label for="average">Average</label><br>
        <input type="radio" id="poor" name="feedback" value="Poor">
        <label for="poor">Poor</label><br>
        <input type="submit" value="Submit">
    </form>
</div>
""", unsafe_allow_html=True)

# Add a "Favorites" feature (storing user preferences in session state)
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if st.button("Add to Favorites"):
    st.session_state.favorites.append(selected_movie)
    st.write(f"Added {selected_movie} to your favorites!")
    
# Display the favorites list
if len(st.session_state.favorites) > 0:
    st.subheader("Your Favorite Movies")
    for movie in st.session_state.favorites:
        st.write(movie)



