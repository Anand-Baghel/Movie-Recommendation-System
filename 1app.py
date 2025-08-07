import streamlit as st
import pandas as pd
import numpy as np
from recommendation_system import MovieRecommendationSystem
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .movie-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 25px;
        color: white;
        padding: 0.5rem 2rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #5a6fd8, #6a4190);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommendation_system():
    """Load the recommendation system with caching"""
    try:
        recommender = MovieRecommendationSystem()
        return recommender
    except Exception as e:
        st.error(f"Error loading recommendation system: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
    
    # Load recommendation system
    recommender = load_recommendation_system()
    if recommender is None:
        st.error("Failed to load recommendation system. Please check your data files.")
        return
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "🔍 Search Movies", "⭐ Get Recommendations", "📊 Analytics", "📈 Popular Movies"]
    )
    
    if page == "🏠 Home":
        show_home_page(recommender)
    elif page == "🔍 Search Movies":
        show_search_page(recommender)
    elif page == "⭐ Get Recommendations":
        show_recommendations_page(recommender)
    elif page == "📊 Analytics":
        show_analytics_page(recommender)
    elif page == "📈 Popular Movies":
        show_popular_movies_page(recommender)

def show_home_page(recommender):
    """Display the home page with overview and quick stats"""
    st.markdown("## 🎬 Welcome to Your Movie Discovery Platform")
    st.markdown("Discover your next favorite movie using advanced AI recommendation algorithms!")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>100</h3>
            <p>Movies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>20</h3>
            <p>Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>3</h3>
            <p>Algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>53</h3>
            <p>Years</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent popular movies
    st.markdown("## 🔥 Recently Popular Movies")
    popular_movies = recommender.get_popular_movies(6)
    
    cols = st.columns(3)
    for i, movie in enumerate(popular_movies):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="movie-card">
                <h4>{movie['title']}</h4>
                <p><strong>Genres:</strong> {movie['genres']}</p>
                <p><strong>Rating:</strong> ⭐ {movie['rating_mean']:.1f} ({movie['rating_count']} ratings)</p>
            </div>
            """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("---")
    st.markdown("## 🧠 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏷️ Content-Based Filtering")
        st.markdown("Recommends movies similar to ones you've enjoyed based on genres and features.")
    
    with col2:
        st.markdown("### 👥 Collaborative Filtering")
        st.markdown("Suggests movies that similar users have rated highly.")
    
    with col3:
        st.markdown("### 🧬 Hybrid Approach")
        st.markdown("Combines both methods for the most accurate recommendations.")

def show_search_page(recommender):
    """Display the search page"""
    st.markdown("## 🔍 Search Movies")
    
    # Search input
    search_query = st.text_input("Enter movie title or genre:", placeholder="e.g., Action, Comedy, The Matrix")
    
    if search_query:
        with st.spinner("Searching for movies..."):
            results = recommender.search_movies(search_query, 10)
        
        if results:
            st.markdown(f"### Found {len(results)} movies:")
            
            for movie in results:
                with st.expander(f"🎬 {movie['title']} ({movie['year']})"):
                    st.markdown(f"**Genres:** {movie['genres']}")
                    st.markdown(f"**Movie ID:** {movie['movieId']}")
                    
                    if st.button(f"Get Similar Movies", key=f"similar_{movie['movieId']}"):
                        similar_movies = recommender.content_based_recommendations(movie['movieId'], 5)
                        st.markdown("#### Similar Movies:")
                        for similar in similar_movies:
                            st.markdown(f"- **{similar['title']}** (Similarity: {similar['similarity_score']:.3f})")
        else:
            st.warning("No movies found matching your search.")
    
    # Browse by genre
    st.markdown("---")
    st.markdown("### 🏷️ Browse by Genre")
    
    # Get all unique genres
    movies_df = recommender.movies_df
    all_genres = set()
    for genres in movies_df['genres']:
        all_genres.update(genres.split('|'))
    
    selected_genre = st.selectbox("Select a genre:", sorted(all_genres))
    
    if selected_genre:
        genre_movies = movies_df[movies_df['genres'].str.contains(selected_genre, na=False)]
        st.markdown(f"### Movies in {selected_genre}:")
        
        for _, movie in genre_movies.head(10).iterrows():
            st.markdown(f"- **{movie['title']}** ({movie['year']})")

def show_recommendations_page(recommender):
    """Display the recommendations page"""
    st.markdown("## ⭐ Get Movie Recommendations")
    
    # Tabs for different recommendation types
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Content-Based", "👥 Collaborative", "🧬 Hybrid", "📊 Compare All"])
    
    with tab1:
        st.markdown("### 🎯 Content-Based Recommendations")
        st.markdown("Find movies similar to a specific movie based on genres and features.")
        
        # Movie selection
        movies_df = recommender.movies_df
        movie_options = {f"{row['title']} ({row['year']})": row['movieId'] 
                        for _, row in movies_df.iterrows()}
        
        selected_movie = st.selectbox("Choose a movie:", list(movie_options.keys()))
        
        if st.button("Get Similar Movies", key="content_based"):
            movie_id = movie_options[selected_movie]
            with st.spinner("Finding similar movies..."):
                recommendations = recommender.content_based_recommendations(movie_id, 10)
            
            if recommendations:
                st.markdown("#### Similar Movies:")
                for i, movie in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>#{i} {movie['title']}</h4>
                        <p><strong>Genres:</strong> {movie['genres']}</p>
                        <p><strong>Similarity Score:</strong> {movie['similarity_score']:.3f}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 👥 Collaborative Filtering")
        st.markdown("Get recommendations based on what similar users have rated highly.")
        
        user_id = st.number_input("Enter User ID (1-20):", min_value=1, max_value=20, value=1)
        
        if st.button("Get Recommendations", key="collaborative"):
            with st.spinner("Finding recommendations..."):
                recommendations = recommender.collaborative_filtering_recommendations(user_id, 10)
            
            if recommendations:
                st.markdown("#### Recommended Movies:")
                for i, movie in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>#{i} {movie['title']}</h4>
                        <p><strong>Genres:</strong> {movie['genres']}</p>
                        <p><strong>Predicted Rating:</strong> {movie['predicted_rating']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🧬 Hybrid Recommendations")
        st.markdown("Combine content-based and collaborative filtering for the best results.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.number_input("Enter User ID (1-20):", min_value=1, max_value=20, value=1, key="hybrid_user")
        
        with col2:
            movie_options = {f"{row['title']} ({row['year']})": row['movieId'] 
                            for _, row in movies_df.iterrows()}
            selected_movie_hybrid = st.selectbox("Choose a movie (optional):", 
                                               ["None"] + list(movie_options.keys()), key="hybrid_movie")
        
        if st.button("Get Hybrid Recommendations", key="hybrid"):
            with st.spinner("Generating hybrid recommendations..."):
                movie_id = None
                if selected_movie_hybrid != "None":
                    movie_id = movie_options[selected_movie_hybrid]
                
                recommendations = recommender.hybrid_recommendations(user_id, movie_id, 10)
            
            if recommendations:
                st.markdown("#### Hybrid Recommendations:")
                for i, movie in enumerate(recommendations, 1):
                    cf_score = movie.get('cf_score', 0)
                    cb_score = movie.get('cb_score', 0)
                    hybrid_score = movie.get('hybrid_score', 0)
                    
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>#{i} {movie['title']}</h4>
                        <p><strong>Genres:</strong> {movie['genres']}</p>
                        <p><strong>Scores:</strong> CF: {cf_score:.2f} | CB: {cb_score:.2f} | Hybrid: {hybrid_score:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📊 Compare All Algorithms")
        st.markdown("Compare recommendations from all three algorithms.")
        
        user_id_compare = st.number_input("Enter User ID (1-20):", min_value=1, max_value=20, value=1, key="compare_user")
        movie_id_compare = st.selectbox("Choose a movie:", list(movie_options.keys()), key="compare_movie")
        
        if st.button("Compare All Algorithms", key="compare"):
            movie_id = movie_options[movie_id_compare]
            
            with st.spinner("Generating recommendations..."):
                cb_recs = recommender.content_based_recommendations(movie_id, 5)
                cf_recs = recommender.collaborative_filtering_recommendations(user_id_compare, 5)
                hybrid_recs = recommender.hybrid_recommendations(user_id_compare, movie_id, 5)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🎯 Content-Based")
                for movie in cb_recs:
                    st.markdown(f"- {movie['title']}")
            
            with col2:
                st.markdown("#### 👥 Collaborative")
                for movie in cf_recs:
                    st.markdown(f"- {movie['title']}")
            
            with col3:
                st.markdown("#### 🧬 Hybrid")
                for movie in hybrid_recs:
                    st.markdown(f"- {movie['title']}")

def show_analytics_page(recommender):
    """Display analytics and insights"""
    st.markdown("## 📊 Analytics & Insights")
    
    # Load data
    movies_df = recommender.movies_df
    ratings_df = recommender.ratings_df
    
    # Basic statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Movies", len(movies_df))
    
    with col2:
        st.metric("Total Ratings", len(ratings_df))
    
    with col3:
        st.metric("Unique Users", ratings_df['userId'].nunique())
    
    # Genre distribution
    st.markdown("### 🏷️ Genre Distribution")
    all_genres = []
    for genres in movies_df['genres']:
        all_genres.extend(genres.split('|'))
    
    genre_counts = pd.Series(all_genres).value_counts().head(10)
    
    fig = px.bar(
        x=genre_counts.values,
        y=genre_counts.index,
        orientation='h',
        title="Top 10 Movie Genres",
        labels={'x': 'Number of Movies', 'y': 'Genre'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Year distribution
    st.markdown("### 📅 Movies by Year")
    year_counts = movies_df['year'].value_counts().sort_index()
    
    fig = px.line(
        x=year_counts.index,
        y=year_counts.values,
        title="Movies Released by Year",
        labels={'x': 'Year', 'y': 'Number of Movies'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Rating distribution
    st.markdown("### ⭐ Rating Distribution")
    rating_counts = ratings_df['rating'].value_counts().sort_index()
    
    fig = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        title="Distribution of User Ratings",
        labels={'x': 'Rating', 'y': 'Number of Ratings'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Most active users
    st.markdown("### 👥 Most Active Users")
    user_activity = ratings_df['userId'].value_counts().head(10)
    
    fig = px.bar(
        x=user_activity.index,
        y=user_activity.values,
        title="Top 10 Most Active Users",
        labels={'x': 'User ID', 'y': 'Number of Ratings'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_popular_movies_page(recommender):
    """Display popular movies with detailed information"""
    st.markdown("## 📈 Popular Movies")
    
    # Number of movies to show
    n_movies = st.slider("Number of movies to display:", min_value=5, max_value=50, value=20)
    
    # Get popular movies
    popular_movies = recommender.get_popular_movies(n_movies)
    
    if popular_movies:
        # Create a DataFrame for better display
        df = pd.DataFrame(popular_movies)
        
        # Display as a table
        st.markdown("### 📊 Popular Movies Table")
        st.dataframe(
            df[['title', 'genres', 'rating_count', 'rating_mean']].rename(columns={
                'title': 'Movie Title',
                'genres': 'Genres',
                'rating_count': 'Number of Ratings',
                'rating_mean': 'Average Rating'
            }),
            use_container_width=True
        )
        
        # Rating vs Count scatter plot
        st.markdown("### 📊 Rating vs Popularity")
        fig = px.scatter(
            df,
            x='rating_count',
            y='rating_mean',
            size='rating_count',
            hover_data=['title'],
            title="Movie Popularity vs Average Rating",
            labels={'rating_count': 'Number of Ratings', 'rating_mean': 'Average Rating'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top movies by rating
        st.markdown("### 🏆 Top Rated Movies")
        top_rated = df.nlargest(10, 'rating_mean')
        
        fig = px.bar(
            top_rated,
            x='rating_mean',
            y='title',
            orientation='h',
            title="Top 10 Movies by Average Rating",
            labels={'rating_mean': 'Average Rating', 'title': 'Movie Title'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

import streamlit as st
from recommendation_system import MovieRecommendationSystem

st.title("Movie Recommendation System")

try:
    recommender = MovieRecommendationSystem()
except Exception as e:
    st.error(f"Error initializing recommendation system: {e}")
    st.stop()

st.header("Popular Movies")
popular_movies = recommender.get_popular_movies(10)
for movie in popular_movies:
    st.write(f"{movie['title']} ({movie['year']}) - {movie['genres']}")

st.header("Search Movies")
query = st.text_input("Enter movie name")
if query:
    results = recommender.search_movies(query, 10)
    for movie in results:
        st.write(f"{movie['title']} ({movie['year']}) - {movie['genres']}")

