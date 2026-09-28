import urllib.request, urllib.parse, json

HEADERS = {'User-Agent': 'MovieBookRecApp/2.0 (student.project@gmail.com) Mozilla/5.0'}

def get_covers(title, author):
    q = urllib.parse.quote(f"{title} {author}")
    url = f"https://openlibrary.org/search.json?q={q}&limit=6"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            for doc in data.get('docs', []):
                if 'cover_i' in doc:
                    cid = doc['cover_i']
                    print(f"{title} cover: https://covers.openlibrary.org/b/id/{cid}-L.jpg")
    except Exception as e:
        print('Error:', e)

get_covers('Crime and Punishment', 'Fyodor Dostoevsky')
get_covers('Anna Karenina', 'Leo Tolstoy')
get_covers('Foundation', 'Isaac Asimov')
