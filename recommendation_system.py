import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings('ignore')

class MovieRecommendationSystem:
    def __init__(self, movies_path='data/movies.csv', ratings_path='data/ratings.csv'):
        """
        Initialize the Movie Recommendation System
        
        Args:
            movies_path (str): Path to movies CSV file
            ratings_path (str): Path to ratings CSV file
        """
        self.movies_df = pd.read_csv(movies_path)
        self.ratings_df = pd.read_csv(ratings_path)
        
        # Create user-movie rating matrix
        self.user_movie_matrix = self.ratings_df.pivot(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        
        # Initialize content-based filtering
        self._setup_content_based_filtering()
        
        # Initialize collaborative filtering
        self._setup_collaborative_filtering()
    
    def _setup_content_based_filtering(self):
        """Setup content-based filtering using TF-IDF and cosine similarity"""
        # Create TF-IDF vectorizer for genres
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # Create genre matrix
        genre_matrix = self.tfidf.fit_transform(self.movies_df['genres'].fillna(''))
        
        # Calculate cosine similarity between movies
        self.movie_similarity = cosine_similarity(genre_matrix, genre_matrix)
        
        # Create movie index mapping
        self.movie_idx = {movie_id: idx for idx, movie_id in enumerate(self.movies_df['movieId'])}
        self.idx_movie = {idx: movie_id for movie_id, idx in self.movie_idx.items()}
    
    def _setup_collaborative_filtering(self):
        """Setup collaborative filtering using Non-negative Matrix Factorization"""
        # Convert to sparse matrix
        self.sparse_matrix = csr_matrix(self.user_movie_matrix.values)
        
        # Apply NMF (Non-negative Matrix Factorization)
        self.nmf = NMF(n_components=20, random_state=42, max_iter=200)
        self.user_features = self.nmf.fit_transform(self.sparse_matrix)
        self.movie_features = self.nmf.components_
    
    def get_movie_by_id(self, movie_id):
        """Get movie information by ID"""
        return self.movies_df[self.movies_df['movieId'] == movie_id].iloc[0]
    
    def get_movie_by_title(self, title):
        """Get movie information by title"""
        return self.movies_df[self.movies_df['title'].str.contains(title, case=False, na=False)]
    
    def content_based_recommendations(self, movie_id, n_recommendations=5):
        """
        Get content-based recommendations based on movie genres
        
        Args:
            movie_id (int): Movie ID to find similar movies for
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of recommended movie IDs with similarity scores
        """
        if movie_id not in self.movie_idx:
            return []
        
        movie_idx = self.movie_idx[movie_id]
        movie_scores = list(enumerate(self.movie_similarity[movie_idx]))
        movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)
        movie_scores = movie_scores[1:n_recommendations+1]  # Exclude the movie itself
        
        recommendations = []
        for idx, score in movie_scores:
            movie_id_rec = self.idx_movie[idx]
            movie_info = self.get_movie_by_id(movie_id_rec)
            recommendations.append({
                'movieId': movie_id_rec,
                'title': movie_info['title'],
                'genres': movie_info['genres'],
                'similarity_score': round(score, 3)
            })
        
        return recommendations
    
    def collaborative_filtering_recommendations(self, user_id, n_recommendations=5):
        """
        Get collaborative filtering recommendations based on user similarities
        
        Args:
            user_id (int): User ID to get recommendations for
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of recommended movie IDs with predicted ratings
        """
        if user_id not in self.user_movie_matrix.index:
            return []
        
        # Get user index
        user_idx = self.user_movie_matrix.index.get_loc(user_id)
        
        # Predict ratings for all movies
        predicted_ratings = np.dot(self.user_features[user_idx], self.movie_features)
        
        # Get movies the user hasn't rated
        user_ratings = self.user_movie_matrix.iloc[user_idx]
        unwatched_movies = user_ratings[user_ratings == 0].index
        
        # Get predicted ratings for unwatched movies
        movie_scores = []
        for movie_id in unwatched_movies:
            if movie_id in self.user_movie_matrix.columns:
                movie_col_idx = self.user_movie_matrix.columns.get_loc(movie_id)
                predicted_rating = predicted_ratings[movie_col_idx]
                movie_scores.append((movie_id, predicted_rating))
        
        # Sort by predicted rating
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top recommendations
        recommendations = []
        for movie_id, predicted_rating in movie_scores[:n_recommendations]:
            movie_info = self.get_movie_by_id(movie_id)
            recommendations.append({
                'movieId': movie_id,
                'title': movie_info['title'],
                'genres': movie_info['genres'],
                'predicted_rating': round(predicted_rating, 2)
            })
        
        return recommendations
    
    def hybrid_recommendations(self, user_id, movie_id=None, n_recommendations=5):
        """
        Get hybrid recommendations combining content-based and collaborative filtering
        
        Args:
            user_id (int): User ID to get recommendations for
            movie_id (int): Optional movie ID for content-based filtering
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of recommended movies with combined scores
        """
        # Get collaborative filtering recommendations
        cf_recommendations = self.collaborative_filtering_recommendations(user_id, n_recommendations * 2)
        
        # If movie_id is provided, get content-based recommendations
        if movie_id:
            cb_recommendations = self.content_based_recommendations(movie_id, n_recommendations * 2)
            
            # Combine recommendations
            hybrid_scores = {}
            
            # Add collaborative filtering scores
            for rec in cf_recommendations:
                movie_id_rec = rec['movieId']
                hybrid_scores[movie_id_rec] = {
                    'movieId': movie_id_rec,
                    'title': rec['title'],
                    'genres': rec['genres'],
                    'cf_score': rec['predicted_rating'],
                    'cb_score': 0,
                    'hybrid_score': rec['predicted_rating'] * 0.6  # Weight for CF
                }
            
            # Add content-based scores
            for rec in cb_recommendations:
                movie_id_rec = rec['movieId']
                if movie_id_rec in hybrid_scores:
                    hybrid_scores[movie_id_rec]['cb_score'] = rec['similarity_score']
                    hybrid_scores[movie_id_rec]['hybrid_score'] += rec['similarity_score'] * 0.4  # Weight for CB
                else:
                    hybrid_scores[movie_id_rec] = {
                        'movieId': movie_id_rec,
                        'title': rec['title'],
                        'genres': rec['genres'],
                        'cf_score': 0,
                        'cb_score': rec['similarity_score'],
                        'hybrid_score': rec['similarity_score'] * 0.4
                    }
            
            # Sort by hybrid score
            recommendations = sorted(hybrid_scores.values(), key=lambda x: x['hybrid_score'], reverse=True)
            return recommendations[:n_recommendations]
        
        else:
            # Return only collaborative filtering recommendations
            return cf_recommendations[:n_recommendations]
    
    def get_popular_movies(self, n_movies=10):
        """
        Get most popular movies based on number of ratings
        
        Args:
            n_movies (int): Number of popular movies to return
            
        Returns:
            list: List of popular movies
        """
        # Count ratings for each movie
        movie_ratings_count = self.ratings_df.groupby('movieId').agg({
            'rating': ['count', 'mean']
        }).round(2)
        
        movie_ratings_count.columns = ['rating_count', 'rating_mean']
        movie_ratings_count = movie_ratings_count.sort_values('rating_count', ascending=False)
        
        # Get top movies
        popular_movies = []
        for movie_id in movie_ratings_count.head(n_movies).index:
            movie_info = self.get_movie_by_id(movie_id)
            popular_movies.append({
                'movieId': movie_id,
                'title': movie_info['title'],
                'genres': movie_info['genres'],
                'rating_count': int(movie_ratings_count.loc[movie_id, 'rating_count']),
                'rating_mean': movie_ratings_count.loc[movie_id, 'rating_mean']
            })
        
        return popular_movies
    
    def search_movies(self, query, n_results=10):
        """
        Search movies by title or genre
        
        Args:
            query (str): Search query
            n_results (int): Number of results to return
            
        Returns:
            list: List of matching movies
        """
        # Search in title
        title_matches = self.movies_df[
            self.movies_df['title'].str.contains(query, case=False, na=False)
        ]
        
        # Search in genres
        genre_matches = self.movies_df[
            self.movies_df['genres'].str.contains(query, case=False, na=False)
        ]
        
        # Combine and remove duplicates
        all_matches = pd.concat([title_matches, genre_matches]).drop_duplicates()
        
        # Convert to list of dictionaries
        results = []
        for _, movie in all_matches.head(n_results).iterrows():
            results.append({
                'movieId': movie['movieId'],
                'title': movie['title'],
                'genres': movie['genres'],
                'year': movie['year']
            })
        
        return results 