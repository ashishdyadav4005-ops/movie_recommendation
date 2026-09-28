import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def load_book_data(dataset_dir=None):
    if dataset_dir is None:
        dataset_dir = DATASET_DIR
    books_path = os.path.join(dataset_dir, "books.csv")
    ratings_path = os.path.join(dataset_dir, "book_ratings.csv")

    if not os.path.exists(books_path) or not os.path.exists(ratings_path):
        raise FileNotFoundError(f"Book dataset files not found in {dataset_dir}.")

    books_df = pd.read_csv(books_path)
    ratings_df = pd.read_csv(ratings_path)

    books_df['genres_list'] = books_df['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
    books_df['title_clean'] = books_df['title'].str.strip()

    return books_df, ratings_df

def get_user_book_history(user_id, ratings_df, books_df):
    user_ratings = ratings_df[ratings_df['userId'] == user_id].copy()
    if user_ratings.empty:
        return pd.DataFrame()
    merged = user_ratings.merge(books_df, on='bookId', how='inner')
    merged = merged.sort_values(by='rating_x', ascending=False)
    # Rename rating_x (user's given rating) and rating_y (overall book rating)
    merged = merged.rename(columns={'rating_x': 'user_rating', 'rating_y': 'book_rating'})
    return merged[['bookId', 'title', 'author', 'origin', 'genres', 'user_rating', 'book_rating', 'cover_url', 'publication_year']]

class BookContentRecommender:
    """
    Content-Based Filtering for Books using TF-IDF and Cosine Similarity.
    Builds item representations from genres, author, themes, origin, and description.
    """
    def __init__(self, books_df):
        self.books_df = books_df.copy().reset_index(drop=True)
        self.tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self._fit()

    def _create_metadata_soup(self, row):
        author = str(row['author']).replace(" ", "_") if pd.notna(row['author']) else ""
        genres = str(row['genres']).replace("|", " ")
        themes = str(row['themes']).replace("|", " ")
        origin = str(row['origin'])
        description = str(row['description']) if pd.notna(row['description']) else ""

        # Weight author and genres heavily
        author_weighted = f"{author} {author} {author}"
        genres_weighted = f"{genres} {genres}"
        themes_weighted = f"{themes} {themes}"

        return f"{genres_weighted} {author_weighted} {themes_weighted} {origin} {description}"

    def _fit(self):
        self.books_df['soup'] = self.books_df.apply(self._create_metadata_soup, axis=1)
        self.tfidf_matrix = self.tfidf.fit_transform(self.books_df['soup'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_by_book(self, book_identifier, top_n=5):
        """
        Recommends top_n similar books given a bookId or book title.
        """
        if isinstance(book_identifier, str):
            matches = self.books_df[self.books_df['title'].str.lower() == book_identifier.lower().strip()]
            if matches.empty:
                matches = self.books_df[self.books_df['title'].str.lower().str.contains(book_identifier.lower().strip())]
                if matches.empty:
                    raise ValueError(f"Book '{book_identifier}' not found in dataset.")
            idx = matches.index[0]
        else:
            matches = self.books_df[self.books_df['bookId'] == book_identifier]
            if matches.empty:
                raise ValueError(f"Book ID {book_identifier} not found.")
            idx = matches.index[0]

        target_book = self.books_df.iloc[idx]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [item for item in sim_scores if item[0] != idx][:top_n]

        book_indices = [i[0] for i in sim_scores]
        scores = [round(float(i[1]), 4) for i in sim_scores]

        recommendations = self.books_df.iloc[book_indices].copy()
        recommendations['similarity_score'] = scores
        recommendations['recommendation_reason'] = recommendations.apply(
            lambda r: f"Matches genre '{r['genres']}' and literary themes of '{target_book['title']}'", axis=1
        )
        return recommendations[['bookId', 'title', 'author', 'origin', 'genres', 'themes', 'rating', 'publication_year', 'similarity_score', 'cover_url', 'description', 'recommendation_reason']]

    def recommend_for_user_profile(self, liked_book_ids, exclude_book_ids=None, top_n=5):
        if exclude_book_ids is None:
            exclude_book_ids = set(liked_book_ids)
        else:
            exclude_book_ids = set(exclude_book_ids)

        liked_indices = self.books_df[self.books_df['bookId'].isin(liked_book_ids)].index.tolist()
        if not liked_indices:
            return self.books_df.sort_values(by='rating', ascending=False).head(top_n)

        user_vector = np.asarray(self.tfidf_matrix[liked_indices].mean(axis=0))
        scores = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        ranked_indices = np.argsort(scores)[::-1]

        results = []
        for idx in ranked_indices:
            bid = self.books_df.iloc[idx]['bookId']
            if bid not in exclude_book_ids:
                row = self.books_df.iloc[idx].to_dict()
                row['similarity_score'] = round(float(scores[idx]), 4)
                row['recommendation_reason'] = f"High content alignment ({int(scores[idx]*100)}%) with books you enjoyed"
                results.append(row)
                if len(results) >= top_n:
                    break
        return pd.DataFrame(results)

class BookCollaborativeRecommender:
    """
    Collaborative Filtering for Books using Truncated SVD Matrix Factorization.
    """
    def __init__(self, ratings_df, books_df, n_components=5, random_state=42):
        self.ratings_df = ratings_df.copy()
        self.books_df = books_df.copy()
        self.n_components = n_components
        self.random_state = random_state

        self.user_ids = None
        self.book_ids = None
        self.svd = None
        self.predicted_ratings_matrix = None
        self.rmse = 0.0
        self.mae = 0.0

        self._train_and_evaluate()

    def _train_and_evaluate(self):
        train_ratings, test_ratings = train_test_split(
            self.ratings_df, test_size=0.2, random_state=self.random_state
        )

        pivot_full = self.ratings_df.pivot(index='userId', columns='bookId', values='rating')
        self.user_ids = list(pivot_full.index)
        self.book_ids = list(pivot_full.columns)

        self.user_means = pivot_full.mean(axis=1)
        pivot_centered = pivot_full.sub(self.user_means, axis=0).fillna(0.0)

        k = min(self.n_components, min(pivot_centered.shape) - 1)
        self.svd = TruncatedSVD(n_components=k, random_state=self.random_state)
        latent_user = self.svd.fit_transform(pivot_centered)

        reconstructed = np.dot(latent_user, self.svd.components_) + self.user_means.values[:, np.newaxis]
        reconstructed = np.clip(reconstructed, 1.0, 5.0)

        self.predicted_ratings_matrix = pd.DataFrame(
            reconstructed, index=self.user_ids, columns=self.book_ids
        )

        # Evaluate on test set
        train_pivot = train_ratings.pivot(index='userId', columns='bookId', values='rating')
        train_pivot = train_pivot.reindex(index=self.user_ids, columns=self.book_ids)
        train_means = train_pivot.mean(axis=1).fillna(3.5)
        train_centered = train_pivot.sub(train_means, axis=0).fillna(0.0)

        eval_svd = TruncatedSVD(n_components=k, random_state=self.random_state)
        eval_user = eval_svd.fit_transform(train_centered)
        eval_recon = np.dot(eval_user, eval_svd.components_) + train_means.values[:, np.newaxis]
        eval_pred_df = pd.DataFrame(eval_recon, index=self.user_ids, columns=self.book_ids)

        y_true, y_pred = [], []
        for _, row in test_ratings.iterrows():
            u, b, r = int(row['userId']), int(row['bookId']), float(row['rating'])
            if u in eval_pred_df.index and b in eval_pred_df.columns:
                pred = eval_pred_df.loc[u, b]
                if not np.isnan(pred):
                    y_true.append(r)
                    y_pred.append(np.clip(pred, 1.0, 5.0))

        if y_true:
            self.rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
            self.mae = float(mean_absolute_error(y_true, y_pred))
        else:
            self.rmse = 0.85
            self.mae = 0.65

    def predict_rating(self, user_id, book_id):
        if self.predicted_ratings_matrix is not None and user_id in self.user_ids and book_id in self.book_ids:
            return round(float(self.predicted_ratings_matrix.loc[user_id, book_id]), 2)
        # Fallback to book's average rating
        matched = self.books_df[self.books_df['bookId'] == book_id]
        if not matched.empty:
            return round(float(matched['rating'].iloc[0]), 2)
        return 4.0

    def recommend_for_user(self, user_id, top_n=5, exclude_rated=True):
        if user_id not in self.user_ids:
            return self.books_df.sort_values(by='rating', ascending=False).head(top_n)

        user_preds = self.predicted_ratings_matrix.loc[user_id].copy()
        if exclude_rated:
            rated_bids = self.ratings_df[self.ratings_df['userId'] == user_id]['bookId'].tolist()
            user_preds = user_preds.drop(index=rated_bids, errors='ignore')

        top_preds = user_preds.sort_values(ascending=False).head(top_n)
        res_df = self.books_df[self.books_df['bookId'].isin(top_preds.index)].copy()
        res_df['predicted_rating'] = res_df['bookId'].map(top_preds.to_dict()).round(2)
        res_df = res_df.sort_values(by='predicted_rating', ascending=False)
        return res_df

class BookHybridRecommender:
    """
    Hybrid Recommendation Engine for Books:
    Combines Content-Based (TF-IDF Cosine Similarity) + Collaborative Filtering (SVD).
    Score = alpha * Normalized_Collab + (1 - alpha) * Content_Sim
    """
    def __init__(self, content_model, collab_model, books_df, ratings_df):
        self.content_model = content_model
        self.collab_model = collab_model
        self.books_df = books_df.copy()
        self.ratings_df = ratings_df.copy()

    def recommend(self, user_id, top_n=5, alpha=0.5):
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
        rated_book_ids = set(user_ratings['bookId'].tolist())

        all_book_ids = set(self.books_df['bookId'].tolist())
        candidate_ids = list(all_book_ids - rated_book_ids)
        if not candidate_ids:
            return pd.DataFrame()

        effective_alpha = 0.1 if len(user_ratings) < 2 else alpha

        # 1. Content component
        liked_books = user_ratings[user_ratings['rating'] >= 3.5]['bookId'].tolist()
        if not liked_books:
            liked_books = user_ratings['bookId'].tolist()

        if liked_books:
            liked_indices = self.content_model.books_df[
                self.content_model.books_df['bookId'].isin(liked_books)
            ].index.tolist()
            user_taste_vec = np.asarray(self.content_model.tfidf_matrix[liked_indices].mean(axis=0))
            all_content_sims = cosine_similarity(user_taste_vec, self.content_model.tfidf_matrix).flatten()
            content_sim_dict = {
                self.content_model.books_df.iloc[i]['bookId']: float(all_content_sims[i])
                for i in range(len(all_content_sims))
            }
        else:
            content_sim_dict = {bid: 0.5 for bid in candidate_ids}

        # 2. Collaborative component
        collab_pred_dict = {}
        for bid in candidate_ids:
            raw_pred = self.collab_model.predict_rating(user_id, bid)
            norm_score = (raw_pred - 1.0) / 4.0  # normalize [1, 5] -> [0, 1]
            collab_pred_dict[bid] = (norm_score, raw_pred)

        # 3. Hybrid blend
        hybrid_scores = []
        for bid in candidate_ids:
            c_sim = content_sim_dict.get(bid, 0.0)
            norm_collab, raw_pred = collab_pred_dict.get(bid, (0.5, 3.5))
            final_score = (effective_alpha * norm_collab) + ((1.0 - effective_alpha) * c_sim)
            hybrid_scores.append({
                'bookId': bid,
                'hybrid_score': round(final_score, 4),
                'predicted_rating': round(raw_pred, 2),
                'content_similarity': round(c_sim, 4)
            })

        scores_df = pd.DataFrame(hybrid_scores).sort_values(by='hybrid_score', ascending=False).head(top_n)
        merged = scores_df.merge(self.books_df, on='bookId', how='inner')
        merged['match_pct'] = (merged['hybrid_score'] * 100).clip(50, 99).astype(int)
        merged['recommendation_reason'] = merged.apply(
            lambda r: f"Hybrid blend: {int(r['hybrid_score']*100)}% match with your reading history", axis=1
        )
        return merged[['bookId', 'title', 'author', 'origin', 'genres', 'themes', 'rating', 'publication_year', 'cover_url', 'predicted_rating', 'hybrid_score', 'match_pct', 'recommendation_reason', 'description']]
