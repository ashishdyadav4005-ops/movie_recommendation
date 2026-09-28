import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.book_recommender import (
    load_book_data,
    BookContentRecommender,
    BookCollaborativeRecommender,
    BookHybridRecommender
)

def test_book_engine():
    print("Testing Book Recommendation Models...")
    books_df, ratings_df = load_book_data()
    
    assert len(books_df) == 100, f"Expected 100 books, got {len(books_df)}"
    indian_count = len(books_df[books_df['origin'] == 'Indian'])
    intl_count = len(books_df[books_df['origin'] == 'International'])
    assert indian_count == 60, f"Expected 60 Indian books, got {indian_count}"
    assert intl_count == 40, f"Expected 40 International books, got {intl_count}"
    print(f"[+] Loaded {len(books_df)} books: {indian_count} Indian authors, {intl_count} International authors.")

    # Content-based test
    cb = BookContentRecommender(books_df)
    # Test similar by bookId 5 (The Palace of Illusions)
    recs_by_id = cb.recommend_by_book(5, top_n=4)
    assert len(recs_by_id) == 4
    print(f"[+] Content-Based: top 4 for 'The Palace of Illusions': {recs_by_id['title'].tolist()}")

    # Test similar by title query
    recs_by_title = cb.recommend_by_book("1984", top_n=4)
    assert len(recs_by_title) == 4
    print(f"[+] Content-Based: top 4 for '1984': {recs_by_title['title'].tolist()}")

    # Collaborative Filtering test
    cf = BookCollaborativeRecommender(ratings_df, books_df, n_components=5)
    assert cf.rmse > 0, "RMSE should be computed"
    print(f"[+] Collaborative Filtering: RMSE={round(cf.rmse, 3)}, MAE={round(cf.mae, 3)}")
    pred_rating = cf.predict_rating(user_id=1, book_id=8)
    print(f"[+] SVD Predicted rating for User 1, Book 8 (The Immortals of Meluha): {pred_rating}")

    # Hybrid test
    hybrid = BookHybridRecommender(cb, cf, books_df, ratings_df)
    hybrid_recs = hybrid.recommend(user_id=1, top_n=5)
    assert len(hybrid_recs) == 5
    print(f"[+] Hybrid Recommendations for User 1: {hybrid_recs['title'].tolist()}")

    print("\n[SUCCESS] ALL BOOK RECOMMENDATION ENGINE TESTS PASSED!")

if __name__ == "__main__":
    test_book_engine()
