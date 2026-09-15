import os
import re
import urllib.request
import urllib.parse
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

os.makedirs('static/posters', exist_ok=True)
df = pd.read_csv('dataset/movies.csv')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_wiki_poster(title, year):
    # Try direct page names
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
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                thumb = data.get('thumbnail', {}).get('source')
                if thumb and ('poster' in thumb.lower() or 'cover' in thumb.lower() or 'jpg' in thumb.lower() or 'png' in thumb.lower()):
                    return thumb
        except Exception:
            continue

    # Try HTML og:image on wiki search
    try:
        search_query = f"{title} {year} film"
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(search_query)}&limit=1&format=json"
        req = urllib.request.Request(search_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if len(data) > 3 and len(data[3]) > 0:
                wiki_page_url = data[3][0]
                page_req = urllib.request.Request(wiki_page_url, headers=HEADERS)
                with urllib.request.urlopen(page_req, timeout=3) as page_resp:
                    html = page_resp.read().decode('utf-8', errors='ignore')
                    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                    if m and not m.group(1).endswith('.svg.png') and 'wikipedia.org' in m.group(1):
                        return m.group(1)
    except Exception:
        pass

    return None

def generate_fallback_poster(movie_id, title, year, genres, imdb_rating, out_path):
    # Generates a sleek, cinematic movie poster card in green/black
    width, height = 400, 600
    img = Image.new('RGB', (width, height), color=(14, 18, 16))
    draw = ImageDraw.Draw(img)

    # Gradient/stripes
    for y in range(height):
        ratio = y / height
        r = int(14 * (1 - ratio) + 8 * ratio)
        g = int(24 * (1 - ratio) + 12 * ratio)
        b = int(18 * (1 - ratio) + 10 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Border
    draw.rectangle([(8, 8), (width - 8, height - 8)], outline=(0, 230, 118), width=2)
    draw.rectangle([(14, 14), (width - 14, height - 14)], outline=(28, 43, 32), width=1)

    # Accent bar
    draw.rectangle([(30, 45), (width - 30, 48)], fill=(0, 230, 118))

    # Title & Year
    # Split title if too long
    words = title.split()
    lines = []
    curr = []
    for w in words:
        if len(' '.join(curr + [w])) > 16:
            lines.append(' '.join(curr))
            curr = [w]
        else:
            curr.append(w)
    if curr:
        lines.append(' '.join(curr))

    y_pos = 180
    for line in lines:
        draw.text((width // 2, y_pos), line, fill=(255, 255, 255), anchor="mm")
        y_pos += 36

    y_pos += 15
    draw.text((width // 2, y_pos), f"({year})", fill=(156, 163, 175), anchor="mm")

    y_pos += 50
    # Rating star badge
    draw.rectangle([(width // 2 - 80, y_pos - 18), (width // 2 + 80, y_pos + 18)], fill=(20, 30, 24), outline=(251, 191, 36), width=2)
    draw.text((width // 2, y_pos), f"⭐ {imdb_rating} / 10 IMDb", fill=(251, 191, 36), anchor="mm")

    # Genres at bottom
    g_str = genres.replace('|', ' • ')
    draw.text((width // 2, height - 60), g_str, fill=(0, 230, 118), anchor="mm")

    img.save(out_path, 'JPEG', quality=90)

print(f"Checking & downloading posters for all {len(df)} movies...")

for idx, row in df.iterrows():
    mid = int(row['movieId'])
    title = str(row['title'])
    year = int(row['release_year'])
    genres = str(row['genres'])
    rating = float(row['imdb_rating'])
    
    out_file = f"static/posters/{mid}.jpg"
    
    # If already downloaded and valid (>10KB), skip
    if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
        continue
        
    downloaded = False
    
    # 1. Try existing poster_url if it's already a working image
    existing_url = str(row.get('poster_url', ''))
    if existing_url.startswith('http'):
        try:
            req = urllib.request.Request(existing_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    data = resp.read()
                    if len(data) > 5000:
                        with open(out_file, 'wb') as f:
                            f.write(data)
                        downloaded = True
        except Exception:
            pass

    # 2. Try Wikipedia / Wikimedia official film poster
    if not downloaded:
        wiki_url = get_wiki_poster(title, year)
        if wiki_url:
            try:
                req = urllib.request.Request(wiki_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=4) as resp:
                    if resp.status == 200:
                        data = resp.read()
                        if len(data) > 5000:
                            with open(out_file, 'wb') as f:
                                f.write(data)
                            downloaded = True
                            print(f"[OK] Downloaded official poster for #{mid} {title}")
            except Exception:
                pass

    # 3. If still not downloaded, generate sleek poster
    if not downloaded:
        generate_fallback_poster(mid, title, year, genres, rating, out_file)
        print(f"[GENERATED] Created poster card for #{mid} {title}")

# Update dataset/movies.csv to use local /static/posters/{mid}.jpg
df['poster_url'] = df['movieId'].apply(lambda x: f"/static/posters/{x}.jpg")
df.to_csv("dataset/movies.csv", index=False)
print("Updated dataset/movies.csv with local static poster paths!")
