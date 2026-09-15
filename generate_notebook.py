import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Personalized Movie Recommendation System using Machine Learning\n",
    "\n",
    "**Course / Subject**: Machine Learning Project  \n",
    "**Project Type**: Hybrid Recommendation Engine (Content-Based + Collaborative Filtering)  \n",
    "\n",
    "---\n",
    "\n",
    "## 1. Project Overview & Objectives\n",
    "Recommendation systems are a fundamental application of Machine Learning in the entertainment industry (Netflix, Amazon Prime, YouTube). This notebook implements an end-to-end personalized movie recommender combining:\n",
    "1. **Content-Based Filtering**: Uses **TF-IDF Vectorization** and **Cosine Similarity** on metadata (genres, director, cast, and plot overviews).\n",
    "2. **Collaborative Filtering**: Uses **Matrix Factorization (Truncated SVD)** to learn latent user-item interaction vectors and predict user ratings.\n",
    "3. **Hybrid Engine**: Dynamically weights and combines both models, overcoming the **Cold-Start Problem** while maximizing personalization."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Imports and Environment Setup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.metrics.pairwise import cosine_similarity\n",
    "from sklearn.decomposition import TruncatedSVD\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error\n",
    "from sklearn.model_selection import train_test_split\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "print(\"Libraries successfully imported!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Data Ingestion & Exploratory Data Analysis (EDA)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load datasets\n",
    "movies_df = pd.read_csv('dataset/movies.csv')\n",
    "ratings_df = pd.read_csv('dataset/ratings.csv')\n",
    "\n",
    "print(f\"Movies shape: {movies_df.shape}\")\n",
    "print(f\"Ratings shape: {ratings_df.shape}\")\n",
    "print(f\"Unique Users: {ratings_df['userId'].nunique()}\")\n",
    "print(f\"Rating Distribution:\\n{ratings_df['rating'].describe()}\")\n",
    "\n",
    "movies_df.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Content-Based Filtering (TF-IDF + Cosine Similarity)\n",
    "\n",
    "### Mathematical Formulation:\n",
    "$$\\text{TF-IDF}(t, d, D) = \\text{TF}(t, d) \\times \\log\\left(\\frac{|D|}{1 + |\\{d \\in D : t \\in d\\}|}\\right)$$\n",
    "\n",
    "$$\\text{Cosine Similarity}(A, B) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|} = \\frac{\\sum_{i=1}^{n} A_i B_i}{\\sqrt{\\sum_{i=1}^{n} A_i^2} \\sqrt{\\sum_{i=1}^{n} B_i^2}}$$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create metadata soup combining genres, director, cast, and overview\n",
    "def create_soup(row):\n",
    "    director = str(row['director']).replace(' ', '_')\n",
    "    cast_top = ' '.join([c.strip().replace(' ', '_') for c in str(row['cast']).split(',')[:3]])\n",
    "    genres = str(row['genres']).replace('|', ' ')\n",
    "    return f\"{genres} {genres} {director} {director} {cast_top} {str(row['overview'])}\"\n",
    "\n",
    "movies_df['soup'] = movies_df.apply(create_soup, axis=1)\n",
    "\n",
    "# Compute TF-IDF Matrix\n",
    "tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))\n",
    "tfidf_matrix = tfidf.fit_transform(movies_df['soup'])\n",
    "print(f\"TF-IDF Matrix Shape: {tfidf_matrix.shape}\")\n",
    "\n",
    "# Compute Pairwise Cosine Similarity\n",
    "cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)\n",
    "\n",
    "def get_content_recommendations(title, top_n=5):\n",
    "    idx = movies_df[movies_df['title'].str.lower() == title.lower()].index[0]\n",
    "    sim_scores = list(enumerate(cosine_sim[idx]))\n",
    "    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)\n",
    "    sim_scores = [item for item in sim_scores if item[0] != idx][:top_n]\n",
    "    \n",
    "    indices = [i[0] for i in sim_scores]\n",
    "    recs = movies_df.iloc[indices][['movieId', 'title', 'genres', 'director']].copy()\n",
    "    recs['similarity_score'] = [round(i[1], 4) for i in sim_scores]\n",
    "    return recs\n",
    "\n",
    "get_content_recommendations('Inception', top_n=5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Collaborative Filtering (Matrix Factorization via SVD)\n",
    "\n",
    "### Mathematical Formulation:\n",
    "Matrix Factorization decomposes the centered user-item interaction matrix $R \\approx U \\cdot \\Sigma \\cdot V^T$ where $U$ represents user latent factors and $V$ represents item latent factors.\n",
    "\n",
    "$$\\hat{r}_{u,i} = \\mu_u + p_u \\cdot q_i^T$$\n",
    "\n",
    "Evaluation metrics:\n",
    "$$\\text{RMSE} = \\sqrt{\\frac{1}{N}\\sum_{u,i}(r_{u,i} - \\hat{r}_{u,i})^2}$$\n",
    "$$\\text{MAE} = \\frac{1}{N}\\sum_{u,i}|r_{u,i} - \\hat{r}_{u,i}|$$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Split ratings into train and test sets (80% / 20%)\n",
    "train_df, test_df = train_test_split(ratings_df, test_size=0.2, random_state=42)\n",
    "\n",
    "# Pivot tables\n",
    "user_ids = sorted(ratings_df['userId'].unique())\n",
    "movie_ids = sorted(ratings_df['movieId'].unique())\n",
    "\n",
    "train_pivot = train_df.pivot(index='userId', columns='movieId', values='rating').reindex(index=user_ids, columns=movie_ids)\n",
    "user_means = train_pivot.mean(axis=1).fillna(3.0)\n",
    "centered_train = train_pivot.sub(user_means, axis=0).fillna(0.0)\n",
    "\n",
    "# Fit Truncated SVD\n",
    "k = min(5, min(centered_train.shape) - 1)\n",
    "svd = TruncatedSVD(n_components=k, random_state=42)\n",
    "user_factors = svd.fit_transform(centered_train)\n",
    "\n",
    "# Reconstruct rating predictions\n",
    "recon_centered = np.dot(user_factors, svd.components_)\n",
    "pred_matrix = recon_centered + user_means.values[:, np.newaxis]\n",
    "pred_matrix = np.clip(pred_matrix, 1.0, 5.0)\n",
    "pred_df = pd.DataFrame(pred_matrix, index=user_ids, columns=movie_ids)\n",
    "\n",
    "# Evaluate on Test Set\n",
    "y_true, y_pred = [], []\n",
    "for _, row in test_df.iterrows():\n",
    "    u, m, r = int(row['userId']), int(row['movieId']), float(row['rating'])\n",
    "    if u in pred_df.index and m in pred_df.columns:\n",
    "        y_true.append(r)\n",
    "        y_pred.append(pred_df.loc[u, m])\n",
    "\n",
    "rmse = np.sqrt(mean_squared_error(y_true, y_pred))\n",
    "mae = mean_absolute_error(y_true, y_pred)\n",
    "\n",
    "print(f\"Collaborative Filtering Evaluation:\")\n",
    "print(f\"  - Latent Factors (k): {k}\")\n",
    "print(f\"  - Root Mean Squared Error (RMSE): {rmse:.4f}\")\n",
    "print(f\"  - Mean Absolute Error (MAE):     {mae:.4f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Hybrid Recommendation Engine\n",
    "\n",
    "Blends collaborative predicted ratings with content similarity to provide a balanced, highly personalized recommendation score:\n",
    "$$\\text{Score}_{hybrid} = \\alpha \\cdot \\text{Normalized}(\\hat{r}_{u,i}) + (1 - \\alpha) \\cdot \\text{Sim}_{content}(u, i)$$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_hybrid_recommendations(user_id, top_n=5, alpha=0.5):\n",
    "    user_ratings = ratings_df[ratings_df['userId'] == user_id]\n",
    "    rated_mids = set(user_ratings['movieId'].tolist())\n",
    "    candidate_mids = [m for m in movie_ids if m not in rated_mids]\n",
    "    \n",
    "    # Content component: centroid of liked movies\n",
    "    liked = user_ratings[user_ratings['rating'] >= 3.5]['movieId'].tolist()\n",
    "    if not liked: liked = list(rated_mids)\n",
    "    liked_indices = movies_df[movies_df['movieId'].isin(liked)].index\n",
    "    user_vec = np.asarray(tfidf_matrix[liked_indices].mean(axis=0))\n",
    "    content_sims = cosine_similarity(user_vec, tfidf_matrix).flatten()\n",
    "    \n",
    "    results = []\n",
    "    for mid in candidate_mids:\n",
    "        m_idx = movies_df[movies_df['movieId'] == mid].index[0]\n",
    "        c_sim = content_sims[m_idx]\n",
    "        collab_pred = pred_df.loc[user_id, mid]\n",
    "        norm_collab = (collab_pred - 1.0) / 4.0\n",
    "        \n",
    "        hybrid_score = (alpha * norm_collab) + ((1 - alpha) * c_sim)\n",
    "        m_info = movies_df.iloc[m_idx]\n",
    "        results.append({\n",
    "            'movieId': mid,\n",
    "            'title': m_info['title'],\n",
    "            'genres': m_info['genres'],\n",
    "            'pred_rating': round(collab_pred, 2),\n",
    "            'content_match': f\"{round(c_sim*100, 1)}%\",\n",
    "            'hybrid_score': round(hybrid_score, 4)\n",
    "        })\n",
    "        \n",
    "    df_res = pd.DataFrame(results).sort_values(by='hybrid_score', ascending=False).head(top_n)\n",
    "    return df_res\n",
    "\n",
    "print(\"Top Hybrid Recommendations for User 1 (Sci-Fi Fan):\")\n",
    "get_hybrid_recommendations(user_id=1, top_n=5, alpha=0.5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Conclusion & Key Findings\n",
    "- **Content-Based Filtering** succeeds at recommending movies with related thematic tokens, genres, and directors without needing other users' data.\n",
    "- **Collaborative Filtering (SVD)** captures latent community tastes and serendipitous connections between movies that don't necessarily share the exact same words.\n",
    "- **The Hybrid Engine** achieves the best of both worlds: resolves the Cold-Start problem and adapts to custom weighting $\\alpha$."
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("movie_recommender.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)

print("Created movie_recommender.ipynb successfully!")
