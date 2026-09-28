import os
import sys
import time
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Movie Modules
from src.data_loader import load_data, get_user_history
from src.content_based import ContentBasedRecommender
from src.collaborative import CollaborativeFilteringRecommender
from src.hybrid import HybridRecommender

# Book Modules
from src.book_recommender import (
    load_book_data,
    get_user_book_history,
    BookContentRecommender,
    BookCollaborativeRecommender,
    BookHybridRecommender
)

app = FastAPI(title="Personalized Movie & Book Recommendation System", version="2.0.0")

# Mount static and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# =============================================================================
# Global State & Models: Movies (100 Movies: 40 Hollywood + 60 Bollywood)
# =============================================================================
movies_df, ratings_df = load_data()
cb_recommender = ContentBasedRecommender(movies_df)
cf_recommender = CollaborativeFilteringRecommender(ratings_df, movies_df, n_components=5)
hybrid_recommender = HybridRecommender(cb_recommender, cf_recommender, movies_df, ratings_df)
print(f"[MOVIES LOADED] Loaded {len(movies_df)} movies with 100% verified local posters.")

# =============================================================================
# Global State & Models: Books (100 Books: 60 Indian + 40 International)
# =============================================================================
books_df, book_ratings_df = load_book_data()
book_cb_recommender = BookContentRecommender(books_df)
book_cf_recommender = BookCollaborativeRecommender(book_ratings_df, books_df, n_components=5)
book_hybrid_recommender = BookHybridRecommender(book_cb_recommender, book_cf_recommender, books_df, book_ratings_df)
print(f"[BOOKS LOADED] Loaded {len(books_df)} books (60 Indian + 40 International) with verified covers.")

USER_PERSONAS = {
    1: {"name": "User 1", "persona": "Sci-Fi & Nolan / Indian Epics Fan", "icon": "🚀"},
    2: {"name": "User 2", "persona": "Crime, Gangs & Conspiracy Thrillers", "icon": "🕵️"},
    3: {"name": "User 3", "persona": "Action, Superheroes & Dystopian Sci-Fi", "icon": "⚡"},
    4: {"name": "User 4", "persona": "Animation & Classic World Literature", "icon": "🎨"},
    5: {"name": "User 5", "persona": "Psychological Mystery & Campus Drama", "icon": "🧩"},
    6: {"name": "User 6", "persona": "Romance & Life Wisdom (Sudha Murty)", "icon": "🎻"},
    7: {"name": "User 7", "persona": "Stylized Realism & Post-Colonial History", "icon": "🤠"},
    8: {"name": "User 8", "persona": "Cosmic Philosophy & Self-Improvement", "icon": "🪐"},
    9: {"name": "User 9", "persona": "All-Rounder Cinephile & Epic Fantasy Buff", "icon": "🎬"},
    10: {"name": "User 10", "persona": "Casual Reader & Viewer (Cold-Start)", "icon": "🍿"}
}

class RatingSubmission(BaseModel):
    userId: int
    movieId: int
    rating: float

class BookRatingSubmission(BaseModel):
    userId: int
    bookId: int
    rating: float

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "cache_bust": int(time.time()),
            "total_movies": len(movies_df),
            "total_books": len(books_df),
            "indian_books": len(books_df[books_df['origin'] == 'Indian']),
            "international_books": len(books_df[books_df['origin'] == 'International']),
            "total_ratings": len(ratings_df) + len(book_ratings_df),
            "total_users": ratings_df['userId'].nunique(),
            "movie_rmse": round(cf_recommender.rmse, 3),
            "movie_mae": round(cf_recommender.mae, 3),
            "book_rmse": round(book_cf_recommender.rmse, 3),
            "book_mae": round(book_cf_recommender.mae, 3)
        }
    )

@app.get("/api/stats")
async def get_system_stats():
    return {
        "movies": {
            "total": len(movies_df),
            "ratings_count": len(ratings_df),
            "rmse": round(cf_recommender.rmse, 3),
            "mae": round(cf_recommender.mae, 3)
        },
        "books": {
            "total": len(books_df),
            "indian_count": len(books_df[books_df['origin'] == 'Indian']),
            "international_count": len(books_df[books_df['origin'] == 'International']),
            "ratings_count": len(book_ratings_df),
            "rmse": round(book_cf_recommender.rmse, 3),
            "mae": round(book_cf_recommender.mae, 3)
        }
    }

# =============================================================================
# MOVIE ROUTES
# =============================================================================

@app.get("/api/users")
async def get_users():
    users = []
    for uid in sorted(ratings_df['userId'].unique()):
        u_info = USER_PERSONAS.get(uid, {"name": f"User {uid}", "persona": "Standard User", "icon": "👤"})
        count = int(ratings_df[ratings_df['userId'] == uid].shape[0])
        users.append({
            "userId": int(uid),
            "name": u_info["name"],
            "persona": u_info["persona"],
            "icon": u_info["icon"],
            "rating_count": count
        })
    return {"users": users}

@app.get("/api/movies")
async def get_movies(query: Optional[str] = None):
    df = movies_df.copy()
    if query:
        df = df[df['title'].str.lower().str.contains(query.lower().strip())]
    return {"movies": df[['movieId', 'title', 'genres', 'director', 'release_year', 'imdb_rating', 'poster_url']].to_dict(orient="records")}

@app.get("/api/user/{user_id}/history")
async def get_history(user_id: int):
    history_df = get_user_history(user_id, ratings_df, movies_df)
    return {"history": history_df.to_dict(orient="records")}

@app.get("/api/movie/{movie_id}")
async def get_movie_details(movie_id: int, user_id: Optional[int] = 1):
    matches = movies_df[movies_df['movieId'] == movie_id]
    if matches.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie_info = matches.iloc[0].to_dict()

    user_rating_row = ratings_df[(ratings_df['userId'] == user_id) & (ratings_df['movieId'] == movie_id)]
    actual_rating = float(user_rating_row['rating'].iloc[0]) if not user_rating_row.empty else None
    predicted_rating = cf_recommender.predict_rating(user_id, movie_id)
    similar = cb_recommender.recommend_by_movie(movie_id, top_n=4).to_dict(orient="records")

    return {
        "movie": movie_info,
        "actual_rating": actual_rating,
        "predicted_rating": predicted_rating,
        "similar_movies": similar
    }

@app.get("/api/recommend/user")
async def recommend_user(user_id: int, mode: str = "hybrid", alpha: float = 0.5, top_n: int = 6):
    if mode == "content":
        liked = ratings_df[(ratings_df['userId'] == user_id) & (ratings_df['rating'] >= 3.0)]['movieId'].tolist()
        rated_all = ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist()
        recs = cb_recommender.recommend_for_user_profile(liked, exclude_movie_ids=rated_all, top_n=top_n)
        return {"mode": "content", "recommendations": recs.to_dict(orient="records")}
    elif mode == "collab":
        recs = cf_recommender.recommend_for_user(user_id=user_id, top_n=top_n, exclude_rated=True)
        return {"mode": "collaborative", "recommendations": recs.to_dict(orient="records")}
    else:
        recs = hybrid_recommender.recommend(user_id=user_id, top_n=top_n, alpha=alpha)
        return {"mode": "hybrid", "recommendations": recs.to_dict(orient="records")}

@app.get("/api/recommend/similar")
async def recommend_similar(movie_id: int, top_n: int = 5):
    try:
        recs = cb_recommender.recommend_by_movie(movie_id, top_n=top_n)
        return {"recommendations": recs.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/rate")
async def rate_movie(payload: RatingSubmission):
    global ratings_df, cf_recommender, hybrid_recommender

    if payload.movieId not in movies_df['movieId'].values:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing_idx = ratings_df[(ratings_df['userId'] == payload.userId) & (ratings_df['movieId'] == payload.movieId)].index
    if not existing_idx.empty:
        ratings_df.loc[existing_idx, 'rating'] = payload.rating
    else:
        new_row = pd.DataFrame([{
            "userId": payload.userId,
            "movieId": payload.movieId,
            "rating": payload.rating,
            "timestamp": 1600000000
        }])
        ratings_df = pd.concat([ratings_df, new_row], ignore_index=True)

    cf_recommender = CollaborativeFilteringRecommender(ratings_df, movies_df, n_components=5)
    hybrid_recommender = HybridRecommender(cb_recommender, cf_recommender, movies_df, ratings_df)

    return {
        "status": "success",
        "message": f"Rating {payload.rating} recorded for Movie ID {payload.movieId}",
        "new_history_count": int(ratings_df[ratings_df['userId'] == payload.userId].shape[0])
    }

# =============================================================================
# BOOK ROUTES
# =============================================================================

@app.get("/api/books")
async def get_books(query: Optional[str] = None, origin: Optional[str] = None):
    df = books_df.copy()
    if origin and origin.lower() in ["indian", "international"]:
        df = df[df['origin'].str.lower() == origin.lower()]
    if query:
        q = query.lower().strip()
        df = df[df['title'].str.lower().str.contains(q) | df['author'].str.lower().str.contains(q)]
    return {"books": df[['bookId', 'title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'cover_url']].to_dict(orient="records")}

@app.get("/api/book/{book_id}")
async def get_book_details(book_id: int, user_id: Optional[int] = 1):
    matches = books_df[books_df['bookId'] == book_id]
    if matches.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    book_info = matches.iloc[0].to_dict()

    user_rating_row = book_ratings_df[(book_ratings_df['userId'] == user_id) & (book_ratings_df['bookId'] == book_id)]
    actual_rating = float(user_rating_row['rating'].iloc[0]) if not user_rating_row.empty else None
    predicted_rating = book_cf_recommender.predict_rating(user_id, book_id)
    similar = book_cb_recommender.recommend_by_book(book_id, top_n=4).to_dict(orient="records")

    return {
        "book": book_info,
        "actual_rating": actual_rating,
        "predicted_rating": predicted_rating,
        "similar_books": similar
    }

@app.get("/api/user/{user_id}/book_history")
async def get_book_history(user_id: int):
    history_df = get_user_book_history(user_id, book_ratings_df, books_df)
    return {"history": history_df.to_dict(orient="records")}

@app.get("/api/recommend/book/similar")
async def recommend_similar_books(book_id: int, top_n: int = 5):
    try:
        recs = book_cb_recommender.recommend_by_book(book_id, top_n=top_n)
        return {"recommendations": recs.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/recommend/book/user")
async def recommend_book_user(user_id: int, mode: str = "hybrid", alpha: float = 0.5, top_n: int = 6):
    if mode == "content":
        liked = book_ratings_df[(book_ratings_df['userId'] == user_id) & (book_ratings_df['rating'] >= 3.5)]['bookId'].tolist()
        rated_all = book_ratings_df[book_ratings_df['userId'] == user_id]['bookId'].tolist()
        recs = book_cb_recommender.recommend_for_user_profile(liked, exclude_book_ids=rated_all, top_n=top_n)
        return {"mode": "content", "recommendations": recs.to_dict(orient="records")}
    elif mode == "collab":
        recs = book_cf_recommender.recommend_for_user(user_id=user_id, top_n=top_n, exclude_rated=True)
        return {"mode": "collaborative", "recommendations": recs.to_dict(orient="records")}
    else:
        recs = book_hybrid_recommender.recommend(user_id=user_id, top_n=top_n, alpha=alpha)
        return {"mode": "hybrid", "recommendations": recs.to_dict(orient="records")}

@app.post("/api/rate/book")
async def rate_book(payload: BookRatingSubmission):
    global book_ratings_df, book_cf_recommender, book_hybrid_recommender

    if payload.bookId not in books_df['bookId'].values:
        raise HTTPException(status_code=404, detail="Book not found")

    existing_idx = book_ratings_df[(book_ratings_df['userId'] == payload.userId) & (book_ratings_df['bookId'] == payload.bookId)].index
    if not existing_idx.empty:
        book_ratings_df.loc[existing_idx, 'rating'] = payload.rating
    else:
        new_row = pd.DataFrame([{
            "userId": payload.userId,
            "bookId": payload.bookId,
            "rating": payload.rating,
            "timestamp": 1600000000
        }])
        book_ratings_df = pd.concat([book_ratings_df, new_row], ignore_index=True)

    book_cf_recommender = BookCollaborativeRecommender(book_ratings_df, books_df, n_components=5)
    book_hybrid_recommender = BookHybridRecommender(book_cb_recommender, book_cf_recommender, books_df, book_ratings_df)

    return {
        "status": "success",
        "message": f"Rating {payload.rating} recorded for Book ID {payload.bookId}",
        "new_history_count": int(book_ratings_df[book_ratings_df['userId'] == payload.userId].shape[0])
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Movie & Book Recommendation Web App on http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
