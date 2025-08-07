import streamlit as st
from recommendation_system import MovieRecommendationSystem

# Modern dark theme CSS with fixed top navbar, logo left, menu centered
st.markdown(
    '''
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <style>
    body {
      font-family: 'Montserrat', sans-serif;
      background: #18181f;
      min-height: 100vh;
      color: #f3f3f3;
      margin: 0;
      padding: 0;
    }
    .main-navbar {
      width: 100vw;
      position: fixed;
      top: 0;
      left: 0;
      z-index: 1000;
      background: rgba(20, 20, 30, 0.98);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 70px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.25);
      border-bottom: 1.5px solid #23233a;
      backdrop-filter: blur(8px);
      padding: 0;
    }
    .navbar-inner {
      width: 100vw;
      max-width: 1200px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 100%;
      margin: 0 auto;
      padding: 0 2em;
    }
    .navbar-title {
      font-size: 1.7em;
      font-weight: 900;
      color: #00ffe7;
      letter-spacing: 2px;
      text-decoration: none;
      background: none;
      border: none;
      box-shadow: none;
      display: flex;
      align-items: center;
      font-family: 'Montserrat', sans-serif;
      margin: 0;
      padding: 0;
    }
    .navbar-menu {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2.5em;
      list-style: none;
      margin: 0 auto;
      padding: 0;
      flex: 1;
    }
    .navbar-menu li {
      font-size: 1.1em;
      font-weight: 600;
      letter-spacing: 1px;
      transition: color 0.2s;
    }
    .navbar-menu li a {
      color: #fff;
      text-decoration: none;
      padding: 0.2em 0.7em;
      border-radius: 4px;
      transition: background 0.2s, color 0.2s;
      cursor: pointer;
    }
    .navbar-menu li a:hover {
      background: #00ffe7;
      color: #18181f;
      box-shadow: 0 2px 8px #00ffe799;
    }
    @media (max-width: 800px) {
      .navbar-inner {
        flex-direction: column;
        align-items: flex-start;
        padding: 0 1em;
      }
      .navbar-menu {
        flex-direction: column;
        align-items: flex-start;
        gap: 1em;
        width: 100%;
        margin-top: 0.5em;
      }
    }
    .hero-section {
      margin-top: 100px;
      margin-bottom: 2.5em;
      padding: 3em 2em 3em 2em;
      border-radius: 18px;
      background: #23233a;
      color: #fff;
      box-shadow: 0 4px 32px rgba(0,255,231,0.08);
      text-align: center;
      position: relative;
      border: 1.5px solid #00ffe7;
      backdrop-filter: blur(2px);
    }
    .hero-title {
      font-size: 2.7em;
      font-weight: bold;
      margin-bottom: 0.3em;
      letter-spacing: 2px;
      color: #00ffe7;
      text-shadow: 0 2px 8px #00ffe799;
    }
    .hero-desc {
      font-size: 1.25em;
      margin-bottom: 2em;
      color: #e0e0e0;
    }
    .recommend-btn {
      display: inline-block;
      background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%);
      color: #18181f;
      font-size: 1.25em;
      font-weight: 700;
      border: none;
      border-radius: 8px;
      padding: 0.7em 2.5em;
      margin: 0 auto;
      box-shadow: 0 2px 16px #00ffe799;
      cursor: pointer;
      transition: background 0.2s, transform 0.2s;
    }
    .recommend-btn:hover {
      background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%);
      color: #fff;
      transform: scale(1.04);
    }
    .movie-card {
      background: rgba(30, 30, 40, 0.95);
      padding: 1.2em 1.5em 1.2em 1.5em;
      margin-bottom: 1.2em;
      border-radius: 14px;
      box-shadow: 0 2px 16px #00ffe71a;
      display: flex;
      align-items: center;
      gap: 1.5em;
      transition: box-shadow 0.2s, transform 0.2s;
      border: 1.5px solid #23233a;
    }
    .movie-card:hover {
      box-shadow: 0 6px 32px #00ffe799;
      transform: translateY(-2px) scale(1.01);
      border: 1.5px solid #00ffe7;
    }
    .movie-poster {
      width: 70px;
      height: 100px;
      background: #23233a url('https://img.icons8.com/ios-filled/50/00ffe7/movie-projector.png') center/40px no-repeat;
      border-radius: 8px;
      flex-shrink: 0;
      box-shadow: 0 1px 8px #00ffe733;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .movie-info {
      flex: 1;
    }
    .movie-title {
      font-weight: bold;
      font-size: 1.15em;
      color: #00ffe7;
      margin-bottom: 0.2em;
      letter-spacing: 1px;
    }
    .movie-year {
      display: inline-block;
      background: #007cf0;
      color: #fff;
      font-size: 0.85em;
      border-radius: 6px;
      padding: 0.1em 0.6em;
      margin-left: 0.5em;
      vertical-align: middle;
    }
    .movie-genres {
      margin-top: 0.2em;
    }
    .genre-badge {
      display: inline-block;
      background: #23233a;
      color: #00ffe7;
      font-size: 0.85em;
      border-radius: 6px;
      padding: 0.1em 0.6em;
      margin-right: 0.3em;
      margin-bottom: 0.2em;
      border: 1px solid #00ffe7;
    }
    .movie-actions {
      display: flex;
      flex-direction: column;
      gap: 0.5em;
      align-items: flex-end;
    }
    .action-btn {
      background: #007cf0;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 0.4em 1em;
      font-size: 0.95em;
      cursor: pointer;
      transition: background 0.2s;
      margin-bottom: 0.2em;
      font-weight: 600;
      letter-spacing: 1px;
    }
    .action-btn:hover {
      background: #00ffe7;
      color: #18181f;
    }
    .footer {
      margin-top: 2em;
      padding: 1em 0;
      text-align: center;
      color: #00ffe7;
      font-size: 1em;
      letter-spacing: 1px;
      border-top: 1.5px solid #23233a;
      background: rgba(20, 20, 30, 0.98);
    }
    </style>
    ''', unsafe_allow_html=True)

# Fixed top Navbar with logo left, menu centered
st.markdown('''
<nav class="main-navbar">
  <div class="navbar-inner">
    <div class="navbar-title">Movie Recommendation System</div>
    <ul class="navbar-menu">
      <li><a href="#Recommend">Home</a></li>
      <li><a href="#Recommend">About Us</a></li>
      <li><a href="#Recommend">Search</a></li>
      <li><a href="#Recommend">Recommend</a></li>
      <li><a href="#Recommend">Chiku</a></li>
    </ul>
  </div>
</nav>
<div style="height: 90px;"></div>
''', unsafe_allow_html=True)

# Hero Section with solid background
def hero_section():
    st.markdown(
        '''
        <div class="hero-section">
            <div class="hero-title">🎬 Movie Recommendation System</div>
            <div class="hero-desc">
                Welcome! Get movie suggestions based on popularity, content, collaborative filtering, or hybrid methods.<br>
                <b>Find your next favorite movie!</b>
            </div>
            <a href="#Recommend"><button class="recommend-btn" type="button">Recommend</button></a>
        </div>
        ''',
        unsafe_allow_html=True,
    )

hero_section()

# Helper to render movie card
def render_movie_card(title, year, genres):
    genre_list = genres.split('|') if isinstance(genres, str) else []
    genre_html = ''.join([f'<span class="genre-badge">{g}</span>' for g in genre_list])
    return f'''
    <div class="movie-card">
        <div class="movie-poster"></div>
        <div class="movie-info">
            <span class="movie-title">{title}<span class="movie-year">{year}</span></span><br>
            <div class="movie-genres">{genre_html}</div>
        </div>
        <div class="movie-actions">
            <button class="action-btn" title="Add to Favorites">❤️ Add to Favorites</button>
            <button class="action-btn" title="More Info">ℹ️ More Info</button>
        </div>
    </div>
    '''

# Initialize the recommendation system
try:
    recommender = MovieRecommendationSystem()
    st.success("Recommendation system initialized successfully!")
except Exception as e:
    st.error(f"Error initializing recommendation system: {e}")
    recommender = None

if recommender:
    tabs = st.tabs(["Popular", "Search", "Content-Based", "Collaborative", "Hybrid"])

    # Set the default active tab to "Hybrid" (Recommend)
    selected_tab = 4
    for i, tab in enumerate(tabs):
        if i == selected_tab:
            with tab:
                st.header("Hybrid Recommendations", anchor="Recommend")
                hybrid_user_id = st.number_input("User ID", min_value=1, step=1, key="hybrid_user")
                hybrid_movie_id = st.number_input("Movie ID", min_value=1, step=1, key="hybrid_movie")
                if hybrid_user_id:
                    try:
                        recommendations = recommender.hybrid_recommendations(int(hybrid_user_id), int(hybrid_movie_id), 5)
                        st.subheader("Recommended Movies")
                        for movie in recommendations:
                            title = movie.get("title", "Unknown Title")
                            year = movie.get("year", "Unknown Year")
                            genres = movie.get("genres", "Unknown Genres")
                            st.markdown(render_movie_card(title, year, genres), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            with tab:
                if i == 0:
                    st.header("Popular Movies", anchor="Popular")
                    popular_movies = recommender.get_popular_movies(10)
                    for movie in popular_movies:
                        title = movie.get("title", "Unknown Title")
                        year = movie.get("year", "Unknown Year")
                        genres = movie.get("genres", "Unknown Genres")
                        st.markdown(render_movie_card(title, year, genres), unsafe_allow_html=True)
                elif i == 1:
                    st.header("Search Movies", anchor="Search")
                    query = st.text_input("Enter movie name")
                    if query:
                        results = recommender.search_movies(query, 10)
                        st.subheader("Search Results")
                        for movie in results:
                            title = movie.get("title", "Unknown Title")
                            year = movie.get("year", "Unknown Year")
                            genres = movie.get("genres", "Unknown Genres")
                            st.markdown(render_movie_card(title, year, genres), unsafe_allow_html=True)
                elif i == 2:
                    st.header("Content-Based Recommendations", anchor="Content-Based")
                    movie_id = st.number_input("Enter Movie ID", min_value=1, step=1)
                    if movie_id:
                        try:
                            recommendations = recommender.content_based_recommendations(int(movie_id), 5)
                            st.subheader("Recommended Movies")
                            for movie in recommendations:
                                title = movie.get("title", "Unknown Title")
                                year = movie.get("year", "Unknown Year")
                                genres = movie.get("genres", "Unknown Genres")
                                st.markdown(render_movie_card(title, year, genres), unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
                elif i == 3:
                    st.header("Collaborative Recommendations", anchor="Collaborative")
                    user_id = st.number_input("Enter User ID", min_value=1, step=1)
                    if user_id:
                        try:
                            recommendations = recommender.collaborative_filtering_recommendations(int(user_id), 5)
                            st.subheader("Recommended Movies")
                            for movie in recommendations:
                                title = movie.get("title", "Unknown Title")
                                year = movie.get("year", "Unknown Year")
                                genres = movie.get("genres", "Unknown Genres")
                                st.markdown(render_movie_card(title, year, genres), unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
else:
    st.error("Recommendation system not initialized.")

# Footer
st.markdown(
    '''
    <div class="footer">
        &copy; 2024 Movie Recommendation System &mdash; Built with ❤️ using Streamlit
    </div>
    ''',
    unsafe_allow_html=True,
)