import os
import pandas as pd
from PIL import Image

def audit():
    print("=== AUDITING 100 MOVIES ===")
    df_m = pd.read_csv('dataset/movies.csv')
    movie_issues = []
    for idx, r in df_m.iterrows():
        mid = int(r['movieId'])
        p = f'static/posters/{mid}.jpg'
        if not os.path.exists(p):
            movie_issues.append((mid, r['title'], "MISSING FILE"))
            continue
        sz = os.path.getsize(p)
        try:
            im = Image.open(p)
            w, h = im.size
            ratio = h / w
            if sz < 15000:
                movie_issues.append((mid, r['title'], f"Small size ({sz} bytes)"))
            elif ratio < 1.15:
                movie_issues.append((mid, r['title'], f"Square/Horizontal ({w}x{h}, r={ratio:.2f})"))
            elif w < 180 or h < 260:
                movie_issues.append((mid, r['title'], f"Low resolution ({w}x{h})"))
        except Exception as e:
            movie_issues.append((mid, r['title'], f"Corrupt image: {e}"))
    
    print(f"Total movie issues: {len(movie_issues)}")
    for item in movie_issues:
        print(" ", item)

    print("\n=== AUDITING 100 BOOKS ===")
    df_b = pd.read_csv('dataset/books.csv')
    book_issues = []
    for idx, r in df_b.iterrows():
        bid = int(r['bookId'])
        p = f'static/covers/{bid}.jpg'
        if not os.path.exists(p):
            book_issues.append((bid, r['title'], r['author'], "MISSING FILE"))
            continue
        sz = os.path.getsize(p)
        try:
            im = Image.open(p)
            w, h = im.size
            ratio = h / w
            if sz < 15000:
                book_issues.append((bid, r['title'], r['author'], f"Small size ({sz} bytes)"))
            elif ratio < 1.2:
                book_issues.append((bid, r['title'], r['author'], f"Square/Horizontal ({w}x{h}, r={ratio:.2f})"))
            elif w < 180 or h < 260:
                book_issues.append((bid, r['title'], r['author'], f"Low resolution ({w}x{h})"))
        except Exception as e:
            book_issues.append((bid, r['title'], r['author'], f"Corrupt image: {e}"))
            
    print(f"Total book issues: {len(book_issues)}")
    for item in book_issues:
        print(" ", item)

    print("\n=== CHECKING LOW CONTRAST / FLAT COVERS ===")
    import numpy as np
    for idx, r in df_b.iterrows():
        bid = int(r['bookId'])
        p = f'static/covers/{bid}.jpg'
        if os.path.exists(p):
            im = Image.open(p).convert('RGB')
            arr = np.array(im)
            mean = arr.mean()
            std = arr.std()
            if std < 30 or mean < 30 or mean > 230:
                print(f"Book #{bid}: {r['title']} -> mean={mean:.1f}, std={std:.1f}")

    print("\n=== CHECKING LOW CONTRAST / FLAT MOVIE POSTERS ===")
    for idx, r in df_m.iterrows():
        mid = int(r['movieId'])
        p = f'static/posters/{mid}.jpg'
        if os.path.exists(p):
            im = Image.open(p).convert('RGB')
            arr = np.array(im)
            mean = arr.mean()
            std = arr.std()
            if std < 30 or mean < 30 or mean > 230:
                print(f"Movie #{mid}: {r['title']} -> mean={mean:.1f}, std={std:.1f}")

if __name__ == '__main__':
    audit()

