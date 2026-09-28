import urllib.request, urllib.parse, json

HEADERS = {'User-Agent': 'MovieBookRecApp/2.0 (student.project@gmail.com) Mozilla/5.0'}

def get_cover(title, author):
    q = urllib.parse.quote(f'{title} {author}')
    url = f'https://openlibrary.org/search.json?q={q}&limit=1'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            docs = data.get('docs', [])
            if docs and 'cover_i' in docs[0]:
                cid = docs[0]['cover_i']
                return f'https://covers.openlibrary.org/b/id/{cid}-L.jpg'
    except Exception as e:
        pass
    return None

test_books = [
    ('The Blue Umbrella', 'Ruskin Bond'),
    ('The Room on the Roof', 'Ruskin Bond'),
    ('Sacred Games', 'Vikram Chandra'),
    ('I Too Had a Love Story', 'Ravinder Singh'),
    ('Can Love Happen Twice', 'Ravinder Singh'),
    ('Everyone Has a Story', 'Savi Sharma'),
    ('Selection Day', 'Aravind Adiga'),
    ('Legend of Suheldev', 'Amish Tripathi'),
    ('India After Gandhi', 'Ramachandra Guha'),
    ('Maximum City', 'Suketu Mehta'),
    ('Tomb of Sand', 'Geetanjali Shree'),
    ('Ladies Coupe', 'Anita Nair'),
    ('Ghachar Ghochar', 'Vivek Shanbhag'),
    ('A Flight of Pigeons', 'Ruskin Bond')
]

for title, author in test_books:
    c = get_cover(title, author)
    print(f"{title} by {author} -> {c}")
