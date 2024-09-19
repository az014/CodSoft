import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample data - Movies and User ratings
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
def collaborative_filtering(user_id):
    user_ratings = ratings.pivot(index='UserID', columns='MovieID', values='Rating').fillna(0)
    user_similarity = cosine_similarity(user_ratings)
    
    similar_users = list(enumerate(user_similarity[user_id - 1]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    
    similar_user_id = similar_users[1][0] + 1
    similar_user_ratings = ratings[ratings['UserID'] == similar_user_id]
    
    recommended_movie_ids = similar_user_ratings[~similar_user_ratings['MovieID'].isin(ratings[ratings['UserID'] == user_id]['MovieID'])]['MovieID']
    
    return movies[movies['MovieID'].isin(recommended_movie_ids)]

# Function for Content-Based Filtering - Based on Movie Genre
def content_based_filtering(movie_title):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['Genre'])
    
    movie_index = movies[movies['Title'] == movie_title].index[0]
    cosine_sim = cosine_similarity(tfidf_matrix[movie_index], tfidf_matrix).flatten()
    
    similar_movies = list(enumerate(cosine_sim))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:4]
    
    recommended_movie_ids = [i[0] for i in similar_movies]
    return movies.iloc[recommended_movie_ids]

# GUI implementation
def run_gui():
    root = tk.Tk()
    root.title("Movie Recommendation System")

    def handle_collaborative():
        user_id = int(user_id_entry.get())
        if user_id not in ratings['UserID'].values:
            messagebox.showerror("Error", "Invalid User ID!")
        else:
            recommendations = collaborative_filtering(user_id)
            if recommendations.empty:
                messagebox.showinfo("No Recommendations", "No recommendations found for this user.")
            else:
                result = '\n'.join(recommendations['Title'].tolist())
                messagebox.showinfo("Recommendations", f"Recommended Movies:\n{result}")

    def handle_content_based():
        movie_title = movie_title_entry.get()
        if movie_title not in movies['Title'].values:
            messagebox.showerror("Error", "Movie not found in the list!")
        else:
            recommendations = content_based_filtering(movie_title)
            result = '\n'.join(recommendations['Title'].tolist())
            messagebox.showinfo("Recommendations", f"Recommended Movies:\n{result}")
    
    # Creating Labels and Entries
    user_id_label = tk.Label(root, text="Enter User ID:")
    user_id_label.pack(pady=5)
    user_id_entry = tk.Entry(root)
    user_id_entry.pack(pady=5)

    collaborative_button = tk.Button(root, text="Collaborative Filtering", command=handle_collaborative)
    collaborative_button.pack(pady=10)

    movie_title_label = tk.Label(root, text="Enter Movie Title:")
    movie_title_label.pack(pady=5)
    movie_title_entry = tk.Entry(root)
    movie_title_entry.pack(pady=5)

    content_based_button = tk.Button(root, text="Content-Based Filtering", command=handle_content_based)
    content_based_button.pack(pady=10)

    root.mainloop()

# Call the function to run the GUI
run_gui()
