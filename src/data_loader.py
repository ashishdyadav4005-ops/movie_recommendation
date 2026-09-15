import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def load_data(dataset_dir=None):
    """
    Loads movies and ratings dataframes.
    """
    if dataset_dir is None:
        dataset_dir = DATASET_DIR
    
    movies_path = os.path.join(dataset_dir, "movies.csv")
    ratings_path = os.path.join(dataset_dir, "ratings.csv")
    
    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        raise FileNotFoundError(f"Dataset files not found in {dataset_dir}. Please run generate_dataset.py first.")
        
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    # Data cleaning / standardizing
    movies_df['genres_list'] = movies_df['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
    movies_df['title_clean'] = movies_df['title'].str.strip()
    
    return movies_df, ratings_df

def get_user_item_matrix(ratings_df, fill_value=0.0):
    """
    Converts ratings DataFrame into a 2D User-Item Pivot Matrix.
    Rows: Users, Columns: Movies
    """
    pivot_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(fill_value)
    return pivot_matrix

def get_user_history(user_id, ratings_df, movies_df):
    """
    Returns the list of movies already rated by a user, ordered by rating desc.
    """
    user_ratings = ratings_df[ratings_df['userId'] == user_id].copy()
    if user_ratings.empty:
        return pd.DataFrame()
        
    merged = user_ratings.merge(movies_df, on='movieId', how='inner')
    merged = merged.sort_values(by='rating', ascending=False)
    return merged[['movieId', 'title', 'genres', 'director', 'rating', 'poster_url', 'release_year']]
