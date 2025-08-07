#!/usr/bin/env python3
"""
Demo script for the Movie Recommendation System
This script demonstrates the different recommendation algorithms
"""

from recommendation_system import MovieRecommendationSystem
import json

def print_separator(title):
    """Print a formatted separator with title"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_movie_list(movies, title="Movies"):
    """Print a list of movies in a formatted way"""
    print(f"\n{title}:")
    print("-" * 40)
    for i, movie in enumerate(movies, 1):
        print(f"{i}. {movie['title']}")
        print(f"   Genres: {movie['genres']}")
        if 'similarity_score' in movie:
            print(f"   Similarity Score: {movie['similarity_score']}")
        if 'predicted_rating' in movie:
            print(f"   Predicted Rating: {movie['predicted_rating']}")
        if 'hybrid_score' in movie:
            print(f"   Hybrid Score: {movie['hybrid_score']}")
        print()

def main():
    """Main demo function"""
    print("🎬 Movie Recommendation System Demo")
    print("=" * 50)
    
    try:
        # Initialize the recommendation system
        print("Initializing recommendation system...")
        recommender = MovieRecommendationSystem()
        print("✅ System initialized successfully!")
        
        # Demo 1: Popular Movies
        print_separator("POPULAR MOVIES")
        popular_movies = recommender.get_popular_movies(5)
        print_movie_list(popular_movies, "Top 5 Popular Movies")
        
        # Demo 2: Content-Based Recommendations
        print_separator("CONTENT-BASED RECOMMENDATIONS")
        print("Finding movies similar to 'Toy Story (1995)' (Movie ID: 1)")
        cb_recommendations = recommender.content_based_recommendations(1, 5)
        print_movie_list(cb_recommendations, "Content-Based Recommendations")
        
        # Demo 3: Collaborative Filtering
        print_separator("COLLABORATIVE FILTERING")
        print("Getting recommendations for User ID: 1")
        cf_recommendations = recommender.collaborative_filtering_recommendations(1, 5)
        print_movie_list(cf_recommendations, "Collaborative Filtering Recommendations")
        
        # Demo 4: Hybrid Recommendations
        print_separator("HYBRID RECOMMENDATIONS")
        print("Combining content-based and collaborative filtering for User ID: 1, Movie ID: 1")
        hybrid_recommendations = recommender.hybrid_recommendations(1, 1, 5)
        print_movie_list(hybrid_recommendations, "Hybrid Recommendations")
        
        # Demo 5: Movie Search
        print_separator("MOVIE SEARCH")
        search_queries = ["Action", "Comedy", "The Matrix"]
        for query in search_queries:
            print(f"\nSearching for: '{query}'")
            search_results = recommender.search_movies(query, 3)
            print_movie_list(search_results, f"Search Results for '{query}'")
        
        # Demo 6: Different Users
        print_separator("USER COMPARISON")
        user_ids = [1, 11, 15]  # Different users with different preferences
        for user_id in user_ids:
            print(f"\nRecommendations for User {user_id}:")
            user_recommendations = recommender.collaborative_filtering_recommendations(user_id, 3)
            print_movie_list(user_recommendations, f"User {user_id} Recommendations")
        
        print_separator("DEMO COMPLETED")
        print("🎉 All demos completed successfully!")
        print("\nTo run the web interface, execute: python app.py")
        print("Then visit: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Make sure the data files exist in the data/ directory")

if __name__ == "__main__":
    main() 