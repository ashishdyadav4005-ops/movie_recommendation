import os
import re
import json
import urllib.request
import urllib.parse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

HEADERS = {
    'User-Agent': 'MovieBookRecApp/2.0 (student.project@gmail.com) Mozilla/5.0'
}

FONT_TITLE = None
FONT_AUTHOR = None
FONT_SUB = None

for font_path in [
    'C:/Windows/Fonts/segoeuib.ttf',
    'C:/Windows/Fonts/arialbd.ttf',
    'C:/Windows/Fonts/calibrib.ttf'
]:
    if os.path.exists(font_path):
        try:
            FONT_TITLE = ImageFont.truetype(font_path, 32)
            FONT_AUTHOR = ImageFont.truetype(font_path, 22)
            FONT_SUB = ImageFont.truetype(font_path, 16)
            break
        except Exception:
            pass

if FONT_TITLE is None:
    FONT_TITLE = ImageFont.load_default()
    FONT_AUTHOR = ImageFont.load_default()
    FONT_SUB = ImageFont.load_default()

def create_gorgeous_book_cover(book, out_path):
    width, height = 400, 600
    is_indian = book.get('origin') == 'Indian'
    
    # Sophisticated cover colors
    if is_indian:
        bg_top = (18, 55, 42)     # Deep emerald
        bg_bottom = (8, 20, 15)
        border_col = (0, 230, 118) # Vivid green
        gold_col = (251, 191, 36)
        tag_text = "INDIAN LITERATURE"
    else:
        bg_top = (20, 35, 60)     # Midnight sapphire
        bg_bottom = (9, 14, 25)
        border_col = (56, 189, 248) # Sky blue
        gold_col = (244, 114, 182) # Rose
        tag_text = "WORLD CLASSIC"

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(height):
        t = y / height
        r = int(bg_top[0] * (1 - t) + bg_bottom[0] * t)
        g = int(bg_top[1] * (1 - t) + bg_bottom[1] * t)
        b = int(bg_top[2] * (1 - t) + bg_bottom[2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Decorative borders
    draw.rectangle([10, 10, width - 11, height - 11], outline=border_col, width=2)
    draw.rectangle([16, 16, width - 17, height - 17], outline=(80, 100, 110), width=1)

    # Top Tag
    draw.rectangle([35, 30, width - 35, 58], fill=(12, 18, 24), outline=border_col, width=1)
    draw.text((width // 2, 44), tag_text, fill=gold_col, font=FONT_SUB, anchor="mm")

    # Title with wrapping
    title = str(book['title'])
    words = title.split()
    lines = []
    curr = []
    for w in words:
        if len(" ".join(curr + [w])) > 15:
            lines.append(" ".join(curr))
            curr = [w]
        else:
            curr.append(w)
    if curr:
        lines.append(" ".join(curr))

    y_title = 160
    for line in lines[:3]:
        draw.text((width // 2, y_title), line, fill=(255, 255, 255), font=FONT_TITLE, anchor="mm")
        y_title += 44

    # Author
    author = str(book.get('author', ''))
    draw.line([(60, y_title + 15), (width - 60, y_title + 15)], fill=border_col, width=1)
    draw.text((width // 2, y_title + 38), f"by {author}", fill=gold_col, font=FONT_AUTHOR, anchor="mm")
    draw.line([(60, y_title + 60), (width - 60, y_title + 60)], fill=border_col, width=1)

    # Genre preview at bottom
    genres = str(book.get('genres', '')).replace('|', ' • ')
    if len(genres) > 34:
        genres = genres[:32] + '...'
    draw.text((width // 2, height - 90), genres, fill=(200, 210, 220), font=FONT_SUB, anchor="mm")

    # Rating badge
    draw.rectangle([60, height - 60, width - 60, height - 28], fill=(12, 20, 16), outline=border_col, width=1)
    draw.text((width // 2, height - 44), f"RATING: {book.get('rating', '4.5')} / 5.0", fill=(255, 255, 255), font=FONT_SUB, anchor="mm")

    img.save(out_path, 'JPEG', quality=92)

def fetch_openlibrary_cover(title, author):
    try:
        q = urllib.parse.quote(f"{title} {author}")
        url = f"https://openlibrary.org/search.json?q={q}&limit=1"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            docs = data.get('docs', [])
            if docs and 'cover_i' in docs[0]:
                cid = docs[0]['cover_i']
                cover_url = f"https://covers.openlibrary.org/b/id/{cid}-L.jpg"
                c_req = urllib.request.Request(cover_url, headers=HEADERS)
                with urllib.request.urlopen(c_req, timeout=5) as c_resp:
                    img_data = c_resp.read()
                    if len(img_data) > 8000:
                        return img_data
    except Exception:
        pass
    return None

def fetch_wiki_book_cover(title, author):
    candidates = [
        f"{title.replace(' ', '_')}_(novel)",
        f"{title.replace(' ', '_')}_(book)",
        title.replace(' ', '_')
    ]
    for page in candidates:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page)}"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                thumb = data.get('thumbnail', {}).get('source')
                if thumb and any(ext in thumb.lower() for ext in ['jpg', 'jpeg', 'png']):
                    # Check if thumb is an actual image
                    t_req = urllib.request.Request(thumb, headers=HEADERS)
                    with urllib.request.urlopen(t_req, timeout=4) as t_resp:
                        t_data = t_resp.read()
                        if len(t_data) > 6000:
                            return t_data
        except Exception:
            continue
    return None

def process_books():
    books_df = pd.read_csv("dataset/books.csv")
    print(f"Downloading/Updating authentic covers for {len(books_df)} books...")
    
    os.makedirs("static/covers", exist_ok=True)
    real_count = 0
    fallback_count = 0

    for idx, row in books_df.iterrows():
        bid = int(row['bookId'])
        title = str(row['title'])
        author = str(row['author'])
        out_file = f"static/covers/{bid}.jpg"
        
        # Try fetching real cover from OpenLibrary
        cover_bytes = fetch_openlibrary_cover(title, author)
        
        # If not, try Wikipedia
        if not cover_bytes:
            cover_bytes = fetch_wiki_book_cover(title, author)
            
        if cover_bytes:
            with open(out_file, 'wb') as f:
                f.write(cover_bytes)
            real_count += 1
            print(f"[REAL COVER] #{bid} {title}")
        else:
            # Generate high-res TrueType typography cover
            create_gorgeous_book_cover(row.to_dict(), out_file)
            fallback_count += 1
            print(f"[STYLED COVER] #{bid} {title}")

    print(f"\nDone Books: {real_count} real published covers downloaded, {fallback_count} styled TrueType covers generated.")

def fetch_wiki_movie_poster(title, year):
    candidates = [
        f"{title.replace(' ', '_')}_(film)",
        f"{title.replace(' ', '_')}_({year}_film)",
        title.replace(' ', '_'),
        f"{title.replace(' ', '_')}_(Hindi_film)"
    ]
    for page in candidates:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page)}"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                thumb = data.get('thumbnail', {}).get('source')
                if thumb and any(ext in thumb.lower() for ext in ['jpg', 'jpeg', 'png']):
                    # Don't take SVG or tiny icons
                    if 'svg' in thumb.lower() or 'icon' in thumb.lower():
                        continue
                    t_req = urllib.request.Request(thumb, headers=HEADERS)
                    with urllib.request.urlopen(t_req, timeout=5) as t_resp:
                        t_data = t_resp.read()
                        if len(t_data) > 6000:
                            return t_data
        except Exception:
            continue
    return None

def process_movies():
    movies_df = pd.read_csv("dataset/movies.csv")
    print(f"\nChecking movie posters for {len(movies_df)} movies...")
    
    os.makedirs("static/posters", exist_ok=True)
    updated_movies = 0

    for idx, row in movies_df.iterrows():
        mid = int(row['movieId'])
        title = str(row['title'])
        year = int(row['release_year'])
        out_file = f"static/posters/{mid}.jpg"

        # Check if existing poster is a placeholder/fallback (< 25000 bytes)
        is_fallback = not os.path.exists(out_file) or os.path.getsize(out_file) < 25000
        
        if is_fallback:
            print(f"Fetching authentic poster for Movie #{mid}: {title} ({year})...")
            poster_data = fetch_wiki_movie_poster(title, year)
            if poster_data:
                with open(out_file, 'wb') as f:
                    f.write(poster_data)
                updated_movies += 1
                print(f"[UPDATED POSTER] #{mid} {title} ({len(poster_data)} bytes)")
            else:
                print(f"[RETAINED] #{mid} {title}")

    print(f"Done Movies: {updated_movies} movie posters updated with authentic artwork!")

if __name__ == "__main__":
    process_books()
    process_movies()
