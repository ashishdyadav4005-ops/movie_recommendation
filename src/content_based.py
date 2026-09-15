import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    """
    Content-Based Filtering Recommender using TF-IDF and Cosine Similarity.
    Builds item representations from genres, director, cast, and overview.
    """
    def __init__(self, movies_df):
        self.movies_df = movies_df.copy().reset_index(drop=True)
        self.tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self._fit()

    def _create_metadata_soup(self, row):
        # Clean director and cast names to prevent partial token overlap
        director = str(row['director']).replace(" ", "_") if pd.notna(row['director']) else ""
        cast_list = [c.strip().replace(" ", "_") for c in str(row['cast']).split(",")[:3]] if pd.notna(row['cast']) else []
        cast_str = " ".join(cast_list)
        
        genres_str = str(row['genres']).replace("|", " ")
        # Double weight genres and director by repeating
        genres_weighted = f"{genres_str} {genres_str}"
        director_weighted = f"{director} {director}"
        overview = str(row['overview']) if pd.notna(row['overview']) else ""
        
        return f"{genres_weighted} {director_weighted} {cast_str} {overview}"

    def _fit(self):
        self.movies_df['soup'] = self.movies_df.apply(self._create_metadata_soup, axis=1)
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['soup'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_by_movie(self, movie_identifier, top_n=5):
        """
        Recommends top_n similar movies given a movieId or movie title.
        """
        if isinstance(movie_identifier, str):
            matches = self.movies_df[self.movies_df['title'].str.lower() == movie_identifier.lower().strip()]
            if matches.empty:
                # Try substring search
                matches = self.movies_df[self.movies_df['title'].str.lower().str.contains(movie_identifier.lower().strip())]
                if matches.empty:
                    raise ValueError(f"Movie '{movie_identifier}' not found in dataset.")
            idx = matches.index[0]
        else:
            matches = self.movies_df[self.movies_df['movieId'] == movie_identifier]
            if matches.empty:
                raise ValueError(f"Movie ID {movie_identifier} not found.")
            idx = matches.index[0]

        target_movie = self.movies_df.iloc[idx]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        
        # Sort by similarity score descending (excluding the movie itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [item for item in sim_scores if item[0] != idx][:top_n]
        
        movie_indices = [i[0] for i in sim_scores]
        scores = [round(float(i[1]), 4) for i in sim_scores]
        
        recommendations = self.movies_df.iloc[movie_indices].copy()
        recommendations['similarity_score'] = scores
        recommendations['recommendation_reason'] = recommendations.apply(
            lambda r: f"Matches genre '{r['genres']}' and director/themes of '{target_movie['title']}'", axis=1
        )
        return recommendations[['movieId', 'title', 'genres', 'director', 'imdb_rating', 'similarity_score', 'poster_url', 'overview', 'recommendation_reason']]

    def recommend_for_user_profile(self, liked_movie_ids, exclude_movie_ids=None, top_n=5):
        """
        Constructs a User Taste Vector by aggregating TF-IDF representations
        of movies the user liked, and computes cosine similarity with unrated movies.
        """
        if exclude_movie_ids is None:
            exclude_movie_ids = set(liked_movie_ids)
        else:
            exclude_movie_ids = set(exclude_movie_ids)
            
        liked_indices = self.movies_df[self.movies_df['movieId'].isin(liked_movie_ids)].index.tolist()
        if not liked_indices:
            # Fallback to top IMDb rated
            return self.movies_df.sort_values(by='imdb_rating', ascending=False).head(top_n)
            
        # User profile vector = centroid (mean) of TF-IDF vectors of liked movies
        user_vector = np.asarray(self.tfidf_matrix[liked_indices].mean(axis=0))
        
        # Compute cosine similarity between user vector and all movies
        scores = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Rank movies
        ranked_indices = np.argsort(scores)[::-1]
        
        results = []
        for idx in ranked_indices:
            mid = self.movies_df.iloc[idx]['movieId']
            if mid not in exclude_movie_ids:
                row = self.movies_df.iloc[idx].to_dict()
                row['similarity_score'] = round(float(scores[idx]), 4)
                row['recommendation_reason'] = f"High content alignment ({int(scores[idx]*100)}%) with movies you enjoyed"
                results.append(row)
                if len(results) >= top_n:
                    break
                    
        return pd.DataFrame(results)
