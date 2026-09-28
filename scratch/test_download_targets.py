import os
import urllib.request
from PIL import Image

HEADERS = {'User-Agent': 'MovieBookRecApp/2.0 (student.project@gmail.com) Mozilla/5.0'}

def download_and_verify(url, out_path, min_size=15000):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) < min_size:
                print(f"FAILED: {out_path} downloaded size too small ({len(data)} bytes)")
                return False
            with open(out_path, 'wb') as f:
                f.write(data)
            im = Image.open(out_path)
            print(f"SUCCESS: {out_path} -> {im.size}, {len(data)} bytes")
            return True
    except Exception as e:
        print(f"ERROR downloading {url} -> {out_path}: {e}")
        return False

# Test downloads
targets = {
    # Replaced Indian Books
    'static/covers/21.jpg': 'https://covers.openlibrary.org/b/id/10389985-L.jpg', # The Blue Umbrella
    'static/covers/24.jpg': 'https://covers.openlibrary.org/b/id/6763274-L.jpg',  # The Room on the Roof
    'static/covers/47.jpg': 'https://covers.openlibrary.org/b/id/14428236-L.jpg', # I Too Had a Love Story
    'static/covers/48.jpg': 'https://covers.openlibrary.org/b/id/13320267-L.jpg', # Can Love Happen Twice
    'static/covers/49.jpg': 'https://covers.openlibrary.org/b/id/46045-L.jpg',    # Sacred Games
    'static/covers/50.jpg': 'https://covers.openlibrary.org/b/id/10487719-L.jpg', # Everyone Has a Story
    'static/covers/51.jpg': 'https://covers.openlibrary.org/b/id/9704090-L.jpg',  # Selection Day
    'static/covers/52.jpg': 'https://covers.openlibrary.org/b/id/10532595-L.jpg', # Legend of Suheldev
    'static/covers/53.jpg': 'https://covers.openlibrary.org/b/id/6821235-L.jpg',  # India After Gandhi
    'static/covers/56.jpg': 'https://covers.openlibrary.org/b/id/225645-L.jpg',   # Maximum City
    # International covers updated
    'static/covers/74.jpg': 'https://covers.openlibrary.org/b/id/10040573-L.jpg', # Crime and Punishment
    'static/covers/77.jpg': 'https://covers.openlibrary.org/b/id/2560652-L.jpg',  # Anna Karenina
    'static/covers/85.jpg': 'https://covers.openlibrary.org/b/id/9261324-L.jpg',  # Foundation
    'static/covers/15.jpg': 'https://covers.openlibrary.org/b/id/14428236-L.jpg', # Five Point Someone / Bhagat bestseller cover
    'static/covers/33.jpg': 'https://covers.openlibrary.org/b/id/8231990-L.jpg',  # Interpreter of Maladies
    # Movie posters
    'static/posters/71.jpg': 'https://upload.wikimedia.org/wikipedia/en/d/dc/Kabir_Singh.jpg', # Kabir Singh
    'static/posters/75.jpg': 'https://upload.wikimedia.org/wikipedia/en/9/9f/Jab_We_Met_Poster.jpg', # Jab We Met
    'static/posters/81.jpg': 'https://upload.wikimedia.org/wikipedia/en/f/f4/Hindi_Medium_poster.jpg', # Hindi Medium
    'static/posters/85.jpg': 'https://upload.wikimedia.org/wikipedia/en/d/da/BABY_poster_2015.jpg', # Baby
    'static/posters/36.jpg': 'https://upload.wikimedia.org/wikipedia/en/4/4c/WALL-E_poster.jpg', # WALL-E
}

for path, url in targets.items():
    download_and_verify(url, path)
