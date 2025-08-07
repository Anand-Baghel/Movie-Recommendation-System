from flask import Flask, render_template, request, jsonify
from recommendation_system import MovieRecommendationSystem
import json

app = Flask(__name__)

# Initialize the recommendation system
try:
    recommender = MovieRecommendationSystem()
    print("✅ Recommendation system initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing recommendation system: {e}")
    recommender = None

@app.route('/')
def index():
    """Main page with web interface"""
    if recommender is None:
        return "Error: Recommendation system not initialized", 500
    
    # Get popular movies for the homepage
    popular_movies = recommender.get_popular_movies(10)
    return render_template('index.html', popular_movies=popular_movies)

@app.route('/api/movies/search')
def search_movies():
    """API endpoint to search movies"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    results = recommender.search_movies(query, 10)
    return jsonify({"results": results})

@app.route('/api/recommendations/content-based')
def content_based_recommendations():
    """API endpoint for content-based recommendations"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    movie_id = request.args.get('movie_id')
    if not movie_id:
        return jsonify({"error": "movie_id parameter is required"}), 400
    
    try:
        movie_id = int(movie_id)
        recommendations = recommender.content_based_recommendations(movie_id, 5)
        return jsonify({"recommendations": recommendations})
    except ValueError:
        return jsonify({"error": "movie_id must be an integer"}), 400

@app.route('/api/recommendations/collaborative')
def collaborative_recommendations():
    """API endpoint for collaborative filtering recommendations"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400
    
    try:
        user_id = int(user_id)
        recommendations = recommender.collaborative_filtering_recommendations(user_id, 5)
        return jsonify({"recommendations": recommendations})
    except ValueError:
        return jsonify({"error": "user_id must be an integer"}), 400

@app.route('/api/recommendations/hybrid')
def hybrid_recommendations():
    """API endpoint for hybrid recommendations"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    user_id = request.args.get('user_id')
    movie_id = request.args.get('movie_id')
    
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400
    
    try:
        user_id = int(user_id)
        movie_id = int(movie_id) if movie_id else None
        recommendations = recommender.hybrid_recommendations(user_id, movie_id, 5)
        return jsonify({"recommendations": recommendations})
    except ValueError:
        return jsonify({"error": "user_id and movie_id must be integers"}), 400

@app.route('/api/movies/popular')
def popular_movies():
    """API endpoint to get popular movies"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    n_movies = request.args.get('n', 10)
    try:
        n_movies = int(n_movies)
        movies = recommender.get_popular_movies(n_movies)
        return jsonify({"movies": movies})
    except ValueError:
        return jsonify({"error": "n parameter must be an integer"}), 400

@app.route('/api/movies/<int:movie_id>')
def get_movie(movie_id):
    """API endpoint to get movie information by ID"""
    if recommender is None:
        return jsonify({"error": "Recommendation system not initialized"}), 500
    
    try:
        movie = recommender.get_movie_by_id(movie_id)
        return jsonify({
            "movieId": movie['movieId'],
            "title": movie['title'],
            "genres": movie['genres'],
            "year": movie['year']
        })
    except IndexError:
        return jsonify({"error": "Movie not found"}), 404

@app.route('/recommendations')
def recommendations_page():
    """Page for getting recommendations"""
    if recommender is None:
        return "Error: Recommendation system not initialized", 500
    
    return render_template('recommendations.html')

@app.route('/search')
def search_page():
    """Page for searching movies"""
    if recommender is None:
        return "Error: Recommendation system not initialized", 500
    
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 