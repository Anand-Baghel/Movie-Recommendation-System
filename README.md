# 🎬 Movie Recommendation System

A comprehensive movie recommendation system that implements multiple recommendation algorithms including content-based filtering, collaborative filtering, and hybrid approaches. Built with Python, Flask, and modern web technologies.

## ✨ Features

### 🧠 Recommendation Algorithms
- **Content-Based Filtering**: Recommends movies based on genre similarity using TF-IDF and cosine similarity
- **Collaborative Filtering**: Uses Non-negative Matrix Factorization (NMF) to find similar users and predict ratings
- **Hybrid Approach**: Combines both methods for more accurate recommendations

### 🌐 Web Interface
- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **Interactive Search**: Search movies by title or genre
- **Real-time Recommendations**: Get instant recommendations with detailed scores
- **API Endpoints**: RESTful API for programmatic access

### 📊 Data Management
- **Sample Dataset**: Includes 50 popular movies with ratings
- **Extensible**: Easy to add more movies and ratings
- **Popular Movies**: Shows most-rated movies with statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Movie_Recommendation_System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the demo script** (optional)
   ```bash
   python demo.py
   ```

4. **Start the web application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage

### Web Interface

1. **Homepage**: View popular movies and system overview
2. **Search**: Find movies by title or genre
3. **Recommendations**: Get personalized recommendations using different algorithms

### API Endpoints

#### Search Movies
```bash
GET /api/movies/search?q=action
```

#### Content-Based Recommendations
```bash
GET /api/recommendations/content-based?movie_id=1
```

#### Collaborative Filtering
```bash
GET /api/recommendations/collaborative?user_id=1
```

#### Hybrid Recommendations
```bash
GET /api/recommendations/hybrid?user_id=1&movie_id=1
```

#### Popular Movies
```bash
GET /api/movies/popular?n=10
```

#### Get Movie by ID
```bash
GET /api/movies/1
```

### Python API

```python
from recommendation_system import MovieRecommendationSystem

# Initialize the system
recommender = MovieRecommendationSystem()

# Get content-based recommendations
similar_movies = recommender.content_based_recommendations(movie_id=1, n_recommendations=5)

# Get collaborative filtering recommendations
user_recommendations = recommender.collaborative_filtering_recommendations(user_id=1, n_recommendations=5)

# Get hybrid recommendations
hybrid_recs = recommender.hybrid_recommendations(user_id=1, movie_id=1, n_recommendations=5)

# Search movies
search_results = recommender.search_movies("action", n_results=10)

# Get popular movies
popular = recommender.get_popular_movies(n_movies=10)
```

## 🏗️ System Architecture

### Core Components

1. **MovieRecommendationSystem Class** (`recommendation_system.py`)
   - Main recommendation engine
   - Implements all algorithms
   - Handles data loading and preprocessing

2. **Flask Web Application** (`app.py`)
   - RESTful API endpoints
   - Web interface routing
   - Error handling

3. **HTML Templates** (`templates/`)
   - Responsive web interface
   - Interactive JavaScript functionality
   - Modern Bootstrap styling

4. **Sample Data** (`data/`)
   - `movies.csv`: Movie information (ID, title, genres, year)
   - `ratings.csv`: User ratings (user ID, movie ID, rating, timestamp)

### Algorithm Details

#### Content-Based Filtering
- Uses TF-IDF vectorization on movie genres
- Calculates cosine similarity between movies
- Recommends movies with similar genre profiles

#### Collaborative Filtering
- Implements Non-negative Matrix Factorization (NMF)
- Decomposes user-movie rating matrix into user and movie feature matrices
- Predicts missing ratings based on learned features

#### Hybrid Approach
- Combines content-based and collaborative filtering scores
- Weights: 60% collaborative, 40% content-based
- Provides more robust recommendations

## 📁 Project Structure

```
Movie_Recommendation_System/
├── app.py                      # Flask web application
├── recommendation_system.py    # Core recommendation engine
├── demo.py                     # Demo script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/                       # Data files
│   ├── movies.csv             # Movie information
│   └── ratings.csv            # User ratings
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── index.html             # Homepage
    ├── search.html            # Search page
    └── recommendations.html   # Recommendations page
```

## 🔧 Configuration

### Adding More Data

1. **Add Movies**: Edit `data/movies.csv` with new movie entries
2. **Add Ratings**: Edit `data/ratings.csv` with new user ratings
3. **Format**: Follow the existing CSV structure

### Customizing Algorithms

- **Content-Based**: Modify TF-IDF parameters in `_setup_content_based_filtering()`
- **Collaborative**: Adjust NMF components in `_setup_collaborative_filtering()`
- **Hybrid**: Change weights in `hybrid_recommendations()`

## 🧪 Testing

### Run Demo
```bash
python demo.py
```

### Test API Endpoints
```bash
# Test search
curl "http://localhost:5000/api/movies/search?q=action"

# Test content-based recommendations
curl "http://localhost:5000/api/recommendations/content-based?movie_id=1"

# Test collaborative filtering
curl "http://localhost:5000/api/recommendations/collaborative?user_id=1"
```

## 🎯 Example Use Cases

1. **Movie Discovery**: Find new movies similar to ones you love
2. **User Personalization**: Get recommendations based on your rating history
3. **Genre Exploration**: Discover movies in specific genres
4. **Popular Content**: See what's trending among users

## 🔍 Sample Data

The system includes 50 popular movies ranging from classics to modern films:

- **Classics**: The Godfather, The Shawshank Redemption, Pulp Fiction
- **Modern**: The Dark Knight, Inception, Interstellar
- **Genres**: Action, Comedy, Drama, Sci-Fi, Thriller, and more

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Flask, Bootstrap, and scikit-learn
- Inspired by modern recommendation systems
- Designed for educational and practical use

---

**Happy Movie Watching! 🍿** 