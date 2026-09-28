import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("Running Full System End-to-End Verification on http://127.0.0.1:8000...")

    # 1. Stats
    with urllib.request.urlopen(f"{BASE_URL}/api/stats") as resp:
        stats = json.loads(resp.read().decode())
        assert stats["movies"]["total"] == 100
        assert stats["books"]["total"] == 100
        assert stats["books"]["indian_count"] == 60
        assert stats["books"]["international_count"] == 40
        print(f"[OK] /api/stats: {stats}")

    # 2. Books query origin=indian
    with urllib.request.urlopen(f"{BASE_URL}/api/books?origin=indian") as resp:
        res = json.loads(resp.read().decode())
        books = res["books"]
        assert len(books) == 60
        print(f"[OK] /api/books?origin=indian: returned {len(books)} books")

    # 3. Books query origin=international
    with urllib.request.urlopen(f"{BASE_URL}/api/books?origin=international") as resp:
        res = json.loads(resp.read().decode())
        books = res["books"]
        assert len(books) == 40
        print(f"[OK] /api/books?origin=international: returned {len(books)} books")

    # 4. Book search query
    with urllib.request.urlopen(f"{BASE_URL}/api/books?query=palace") as resp:
        res = json.loads(resp.read().decode())
        books = res["books"]
        assert len(books) >= 1
        print(f"[OK] /api/books?query=palace: found '{books[0]['title']}' by {books[0]['author']}")

    # 5. Similar Books recommendations
    with urllib.request.urlopen(f"{BASE_URL}/api/recommend/book/similar?book_id=62&top_n=4") as resp:
        res = json.loads(resp.read().decode())
        recs = res["recommendations"]
        assert len(recs) == 4
        print(f"[OK] /api/recommend/book/similar for 1984: {[r['title'] for r in recs]}")

    # 6. User Personalized Recommendations (Hybrid)
    with urllib.request.urlopen(f"{BASE_URL}/api/recommend/book/user?user_id=1&mode=hybrid&top_n=5") as resp:
        res = json.loads(resp.read().decode())
        recs = res["recommendations"]
        assert len(recs) == 5
        print(f"[OK] /api/recommend/book/user (Hybrid) for User 1: {[r['title'] for r in recs]}")

    # 7. Rate a book
    rate_payload = json.dumps({"userId": 1, "bookId": 90, "rating": 5.0}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/rate/book", data=rate_payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        rate_res = json.loads(resp.read().decode())
        assert rate_res["status"] == "success"
        print(f"[OK] /api/rate/book: {rate_res['message']}")

    # 8. Check Movie endpoints still 100% functional
    with urllib.request.urlopen(f"{BASE_URL}/api/movies") as resp:
        res = json.loads(resp.read().decode())
        assert len(res["movies"]) == 100
        print(f"[OK] /api/movies: verified 100 movies")

    with urllib.request.urlopen(f"{BASE_URL}/api/movie/1") as resp:
        res = json.loads(resp.read().decode())
        assert res["movie"]["title"] == "Inception"
        print(f"[OK] /api/movie/1: verified Inception with {len(res['similar_movies'])} recommendations")

    print("\n>>> ALL SYSTEM ENDPOINTS VERIFIED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_endpoints()
