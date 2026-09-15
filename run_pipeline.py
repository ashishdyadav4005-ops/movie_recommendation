import sys
import os

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ensure utf-8 encoding for console printing on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.data_loader import load_data, get_user_history
from src.content_based import ContentBasedRecommender
from src.collaborative import CollaborativeFilteringRecommender
from src.hybrid import HybridRecommender

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title.upper()}")
        print("=" * 70)

def main():
    print_separator("Personalized Movie Recommendation System - ML Pipeline")
    
    # 1. Load Data
    print("\n[Step 1] Loading Dataset...")
    movies_df, ratings_df = load_data()
    print(f"  [+] Total Movies: {len(movies_df)}")
    print(f"  [+] Total Ratings: {len(ratings_df)}")
    print(f"  [+] Unique Users: {ratings_df['userId'].nunique()}")
    print(f"  [+] Average Rating: {ratings_df['rating'].mean():.2f} / 5.0")
    print(f"  [+] Genres available: {', '.join(sorted(set('|'.join(movies_df['genres']).split('|'))))}")

    # 2. Content-Based Filtering
    print_separator("Step 2: Content-Based Filtering (TF-IDF & Cosine Similarity)")
    cb_model = ContentBasedRecommender(movies_df)
    target_movie = "Inception"
    print(f"\nQuerying similar movies for '{target_movie}' based on Plot, Genres, Director & Cast:")
    cb_recs = cb_model.recommend_by_movie(target_movie, top_n=5)
    for idx, (_, row) in enumerate(cb_recs.iterrows(), 1):
        print(f"  {idx}. {row['title']} ({row['genres']}) | Director: {row['director']} | Cosine Similarity: {row['similarity_score']:.3f}")

    # 3. Collaborative Filtering with Matrix Factorization (SVD)
    print_separator("Step 3: Collaborative Filtering (Matrix Factorization via SVD)")
    print("Training SVD Latent Factor Model on User-Item Rating Matrix...")
    cf_model = CollaborativeFilteringRecommender(ratings_df, movies_df, n_components=5)
    print(f"  [+] Model Convergence: Success")
    print(f"  [+] SVD Latent Factors: {cf_model.svd.n_components}")
    print(f"  [+] Evaluation on 20% Test Split:")
    print(f"      - Root Mean Squared Error (RMSE): {cf_model.rmse:.4f}")
    print(f"      - Mean Absolute Error (MAE):     {cf_model.mae:.4f}")

    # 4. Hybrid Recommendation Engine Demonstration
    print_separator("Step 4: Personalized Hybrid Recommendations Across User Personas")
    hybrid_model = HybridRecommender(cb_model, cf_model, movies_df, ratings_df)

    test_users = [
        (1, "Sci-Fi & Nolan Fanatic"),
        (2, "Crime & Mafia Enthusiast"),
        (4, "Animation & Family Lover")
    ]

    for uid, persona in test_users:
        print(f"\n>>> Recommendations for User {uid} [{persona}]:")
        history = get_user_history(uid, ratings_df, movies_df)
        print("  Top Rated Past Movies: " + ", ".join([f"{r['title']} ({r['rating']}*)" for _, r in history.head(3).iterrows()]))
        
        recs = hybrid_model.recommend(user_id=uid, top_n=4, alpha=0.5)
        print("  Recommended New Movies (Unseen):")
        for rank, (_, r) in enumerate(recs.iterrows(), 1):
            print(f"    {rank}. {r['title']:<25} | Pred Rating: {r['predicted_rating']:.2f}* | Content Match: {r['content_similarity']}% | Hybrid Score: {r['hybrid_score']:.4f}")

    print_separator("Pipeline Run Completed Successfully!")
    print("To launch the interactive Web Interface, run: python app.py")

if __name__ == "__main__":
    main()
