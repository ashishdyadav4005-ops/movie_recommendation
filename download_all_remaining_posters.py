import os
import urllib.request
import urllib.parse
import json
import pandas as pd

HEADERS = {
    'User-Agent': 'MoviePosterFetcher/2.0 (student.project@gmail.com) Mozilla/5.0'
}

df = pd.read_csv('dataset/movies.csv')

def get_real_poster_url(title, year):
    clean_title = title.split(':')[0].strip()
    
    candidates = [
        f"{title.replace(' ', '_')}_(film)",
        f"{title.replace(' ', '_')}_({year}_film)",
        title.replace(' ', '_'),
        f"{clean_title.replace(' ', '_')}_(film)",
        f"{clean_title.replace(' ', '_')}_({year}_film)",
        clean_title.replace(' ', '_'),
        f"{clean_title.replace(' ', '_')}_(Hindi_film)",
        f"{title.replace(' ', '_')}_(Hindi_film)"
    ]
    
    # Specific overrides for tricky titles
    custom_map = {
        'Toy Story': 'Toy_Story',
        'Spirited Away': 'Spirited_Away',
        'Coco': 'Coco_(2017_film)',
        'Up': 'Up_(2009_film)',
        'Memento': 'Memento_(film)',
        'Lagaan: Once Upon a Time in India': 'Lagaan',
        'Chak De! India': 'Chak_De!_India',
        'Kabhi Khushi Kabhie Gham': 'Kabhi_Khushi_Kabhie_Gham...',
        'Dil To Pagal Hai': 'Dil_To_Pagal_Hai',
        'Kuch Kuch Hota Hai': 'Kuch_Kuch_Hota_Hai',
        'Kal Ho Naa Ho': 'Kal_Ho_Naa_Ho',
        'Veer-Zaara': 'Veer-Zaara',
        'Swades': 'Swades',
        'Omkara': 'Omkara_(2006_film)',
        'Talaash: The Answer Lies Within': 'Talaash:_The_Answer_Lies_Within',
        'Kahaani': 'Kahaani',
        'Badlapur': 'Badlapur_(film)',
        'Queen': 'Queen_(2014_film)',
        'Piku': 'Piku',
        'Bajrangi Bhaijaan': 'Bajrangi_Bhaijaan',
        'Raazi': 'Raazi',
        'Bareilly Ki Barfi': 'Bareilly_Ki_Barfi',
        'Jab We Met': 'Jab_We_Met',
        'Zindagi Na Milegi Dobara': 'Zindagi_Na_Milegi_Dobara',
        'Dil Chahta Hai': 'Dil_Chahta_Hai',
        'Haider': 'Haider_(film)',
        'Dev.D': 'Dev.D',
        'Udta Punjab': 'Udta_Punjab',
        'Barfi!': 'Barfi!',
        'Sacred Games': 'Sacred_Games_(TV_series)',
        'Mirzapur': 'Mirzapur_(TV_series)',
        'Paatal Lok': 'Paatal_Lok',
        'Chhichhore': 'Chhichhore',
        'Stree': 'Stree_(2018_film)',
        'Uri: The Surgical Strike': 'Uri:_The_Surgical_Strike',
        'Drishyam': 'Drishyam_(2015_film)',
        'Article 15': 'Article_15_(film)',
        'Krrish 3': 'Krrish_3',
        'Koi... Mil Gaya': 'Koi..._Mil_Gaya'
    }

    if title in custom_map:
        candidates.insert(0, custom_map[title])
    if clean_title in custom_map:
        candidates.insert(0, custom_map[clean_title])

    for page in candidates:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page)}"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                thumb = data.get('thumbnail', {}).get('source')
                if thumb and any(ext in thumb.lower() for ext in ['jpg', 'jpeg', 'png']):
                    if 'svg' not in thumb.lower():
                        return thumb
        except Exception:
            continue
    return None

print("Checking and downloading all missing official movie posters...")
updated = 0
for idx, row in df.iterrows():
    mid = int(row['movieId'])
    title = str(row['title'])
    year = int(row['release_year'])
    out_file = f"static/posters/{mid}.jpg"
    
    # Check if placeholder (< 23000 bytes)
    if os.path.exists(out_file) and os.path.getsize(out_file) < 23000:
        thumb_url = get_real_poster_url(title, year)
        if thumb_url:
            try:
                req = urllib.request.Request(thumb_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    if len(data) > 6000:
                        with open(out_file, 'wb') as f:
                            f.write(data)
                        updated += 1
                        print(f"[SUCCESS] #{mid} {title} -> {len(data)} bytes ({thumb_url[:60]}...)")
            except Exception as e:
                print(f"[FAIL] #{mid} {title}: {e}")
        else:
            print(f"[NOT FOUND] #{mid} {title}")

print(f"\nCompleted! Updated {updated} movie posters with authentic theatrical artwork.")
