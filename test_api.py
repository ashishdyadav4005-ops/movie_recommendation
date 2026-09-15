import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import get_users, get_movies, get_history, recommend_user, recommend_similar, rate_movie, RatingSubmission

async def test_system():
    print("Testing API Route Functions directly...")

    # Test Users
    users_res = await get_users()
    users = users_res.get("users", [])
    assert len(users) >= 10, "Expected at least 10 users"
    print(f"[+] get_users(): 200 OK ({len(users)} users found)")

    # Test Movies
    movies_res = await get_movies()
    movies = movies_res.get("movies", [])
    assert len(movies) >= 40, "Expected at least 40 movies"
    print(f"[+] get_movies(): 200 OK ({len(movies)} movies found)")

    # Test User History
    history_res = await get_history(user_id=1)
    history = history_res.get("history", [])
    assert len(history) > 0
    print(f"[+] get_history(user_id=1): 200 OK ({len(history)} rated movies)")

    # Test Hybrid Recommendations
    recs_res = await recommend_user(user_id=1, mode="hybrid", alpha=0.5, top_n=5)
    recs = recs_res.get("recommendations", [])
    assert len(recs) == 5
    print(f"[+] recommend_user(mode='hybrid'): 200 OK (returned {len(recs)} recs)")

    # Test Collaborative Recommendations
    collab_res = await recommend_user(user_id=2, mode="collab", top_n=5)
    collab_recs = collab_res.get("recommendations", [])
    assert len(collab_recs) == 5
    print(f"[+] recommend_user(mode='collab'): 200 OK (returned {len(collab_recs)} recs)")

    # Test Content Recommendations
    content_res = await recommend_user(user_id=4, mode="content", top_n=5)
    content_recs = content_res.get("recommendations", [])
    assert len(content_recs) == 5
    print(f"[+] recommend_user(mode='content'): 200 OK (returned {len(content_recs)} recs)")

    # Test Similar Movies (Content-Based)
    similar_res = await recommend_similar(movie_id=1, top_n=4)
    similar = similar_res.get("recommendations", [])
    assert len(similar) == 4
    print(f"[+] recommend_similar(movie_id=1): 200 OK (returned {len(similar)} similar movies)")

    # Test Rate Movie
    rate_res = await rate_movie(RatingSubmission(userId=1, movieId=20, rating=4.5))
    assert rate_res.get("status") == "success"
    print(f"[+] rate_movie(): 200 OK ({rate_res.get('message')})")

    print("\n[SUCCESS] ALL API AND MODEL FUNCTIONS PASSED VERIFICATION!")

if __name__ == "__main__":
    asyncio.run(test_system())
