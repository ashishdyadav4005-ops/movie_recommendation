import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class HybridRecommender:
    """
    Hybrid Recommendation Engine combining:
    1. Content-Based Filtering (TF-IDF & Cosine Similarity on metadata)
    2. Collaborative Filtering (Latent Factor Matrix Factorization via SVD)
    
    Formula:
    Score = alpha * Normalized_Collab_Rating + (1 - alpha) * Content_Similarity_Score
    """
    def __init__(self, content_model, collab_model, movies_df, ratings_df):
        self.content_model = content_model
        self.collab_model = collab_model
        self.movies_df = movies_df.copy()
        self.ratings_df = ratings_df.copy()

    def recommend(self, user_id, top_n=5, alpha=0.5):
        """
        Generates personalized hybrid recommendations for a given user_id.
        alpha: weight for Collaborative Filtering (0.0 = pure Content, 1.0 = pure Collab).
        """
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
        rated_movie_ids = set(user_ratings['movieId'].tolist())
        
        # Identify candidate unrated movies
        all_movie_ids = set(self.movies_df['movieId'].tolist())
        candidate_ids = list(all_movie_ids - rated_movie_ids)
        
        if not candidate_ids:
            return pd.DataFrame()

        # Handle Cold-Start scenario
        if len(user_ratings) < 2:
            # Shift weight almost entirely to content / popularity
            effective_alpha = 0.1
        else:
            effective_alpha = alpha

        # 1. Content Component: Build user profile vector from movies rated >= 3.5
        liked_movies = user_ratings[user_ratings['rating'] >= 3.5]['movieId'].tolist()
        if not liked_movies:
            liked_movies = user_ratings['movieId'].tolist()
            
        if liked_movies:
            liked_indices = self.content_model.movies_df[
                self.content_model.movies_df['movieId'].isin(liked_movies)
            ].index.tolist()
            user_taste_vec = np.asarray(self.content_model.tfidf_matrix[liked_indices].mean(axis=0))
            all_content_sims = cosine_similarity(user_taste_vec, self.content_model.tfidf_matrix).flatten()
            content_sim_dict = {
                self.content_model.movies_df.iloc[i]['movieId']: float(all_content_sims[i])
                for i in range(len(all_content_sims))
            }
        else:
            # Fallback uniform
            content_sim_dict = {mid: 0.5 for mid in candidate_ids}

        # 2. Collaborative Component & Hybrid Combination
        results = []
        for mid in candidate_ids:
            collab_pred = self.collab_model.predict_rating(user_id, mid)
            # Normalize collaborative rating [1.0, 5.0] to [0.0, 1.0]
            norm_collab = (collab_pred - 1.0) / 4.0
            
            content_sim = content_sim_dict.get(mid, 0.0)
            # Normalize content similarity to [0, 1]
            content_sim = max(0.0, min(1.0, content_sim))
            
            # Hybrid combined score
            hybrid_score = (effective_alpha * norm_collab) + ((1.0 - effective_alpha) * content_sim)
            
            movie_row = self.movies_df[self.movies_df['movieId'] == mid].iloc[0].to_dict()
            movie_row['hybrid_score'] = round(float(hybrid_score), 4)
            movie_row['predicted_rating'] = collab_pred
            movie_row['content_similarity'] = round(float(content_sim * 100), 1)
            movie_row['recommendation_reason'] = (
                f"Hybrid Match: {int(hybrid_score * 100)}% | "
                f"SVD Est. Rating: {collab_pred}★ | "
                f"Content Match: {int(content_sim * 100)}%"
            )
            results.append(movie_row)

        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values(by='hybrid_score', ascending=False).head(top_n)
        return df_results
