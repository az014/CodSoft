# Import necessary libraries
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

# Step 1: Sample data - Movies and User ratings
movies = pd.DataFrame({
    'MovieID': [1, 2, 3, 4, 5],
    'Title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
    'Genre': ['Action', 'Comedy', 'Romance', 'Action', 'Thriller']
})

ratings = pd.DataFrame({
    'UserID': [1, 1, 1, 2, 2, 3, 3],
    'MovieID': [1, 2, 3, 1, 4, 2, 5],
    'Rating': [5, 3, 4, 4, 5, 2, 3]
})

# Function for Collaborative Filtering - Based on User Ratings
def collaborative_filtering(user_id, ratings, movies):
    # Pivot the ratings dataframe to create a user-movie matrix
    user_ratings = ratings.pivot(index='UserID', columns='MovieID', values='Rating').fillna(0)
    
    # Calculate cosine similarity between users
    user_similarity = cosine_similarity(user_ratings)
    
    # Get the similarity scores for the selected user
    similar_users = list(enumerate(user_similarity[user_id - 1]))
    
    # Sort users based on similarity score (highest to lowest)
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    
    # Get the most similar user (excluding the current user)
    similar_user_id = similar_users[1][0] + 1
    similar_user_ratings = ratings[ratings['UserID'] == similar_user_id]
    
    # Get the movies the similar user liked that the current user hasn't watched
    recommended_movie_ids = similar_user_ratings[~similar_user_ratings['MovieID'].isin(ratings[ratings['UserID'] == user_id]['MovieID'])]['MovieID']
    
    # Return the movie titles for the recommended movies
    return movies[movies['MovieID'].isin(recommended_movie_ids)]

# Function for Content-Based Filtering - Based on Movie Genre
def content_based_filtering(movie_title, movies):
    # Use TF-IDF to convert genres into vectors
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['Genre'])
    
    # Get the index of the movie selected by the user
    movie_index = movies[movies['Title'] == movie_title].index[0]
    
    # Calculate cosine similarity between the selected movie and all others
    cosine_sim = cosine_similarity(tfidf_matrix[movie_index], tfidf_matrix).flatten()
    
    # Get a list of movies with similarity scores and sort them
    similar_movies = list(enumerate(cosine_sim))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:4]  # Exclude the selected movie itself
    
    # Return the movie titles for the recommended movies
    recommended_movie_ids = [i[0] for i in similar_movies]
    return movies.iloc[recommended_movie_ids]

# Interactive part: Ask the user what type of recommendation they want
def recommend_movies():
    print("Welcome to the Movie Recommendation System!")
    print("Please choose the recommendation type:")
    print("1. Collaborative Filtering (Based on user preferences)")
    print("2. Content-Based Filtering (Based on movie genre similarity)")
    
    choice = int(input("Enter 1 or 2: "))
    
    if choice == 1:
        # Collaborative Filtering based on user preferences
        user_id = int(input("Enter your User ID (1, 2, or 3): "))
        print(f"\nCollaborative Filtering Recommendations for User {user_id}:")
        recommendations = collaborative_filtering(user_id, ratings, movies)
        if recommendations.empty:
            print("No recommendations found for this user.")
        else:
            print(recommendations[['Title', 'Genre']])
    
    elif choice == 2:
        # Content-Based Filtering based on movie similarity
        print("\nHere is the list of movies available:")
        print(movies[['Title', 'Genre']])
        movie_title = input("\nEnter the title of a movie you like (exactly as listed): ")
        
        if movie_title not in movies['Title'].values:
            print("Movie not found in the list. Please check your input.")
        else:
            print(f"\nContent-Based Filtering Recommendations for '{movie_title}':")
            recommendations = content_based_filtering(movie_title, movies)
            print(recommendations[['Title', 'Genre']])
    else:
        print("Invalid choice. Please enter 1 or 2.")

# Call the interactive recommendation function
recommend_movies()
