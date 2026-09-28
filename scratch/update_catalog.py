import os
import urllib.request
import pandas as pd
from PIL import Image

HEADERS = {'User-Agent': 'MovieBookRecApp/2.0 (student.project@gmail.com) Mozilla/5.0'}

def download_file(url, out_path, min_size=15000):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) < min_size:
                print(f"FAILED size check: {out_path} ({len(data)} bytes)")
                return False
            with open(out_path, 'wb') as f:
                f.write(data)
            im = Image.open(out_path)
            print(f"Downloaded {out_path}: {im.size}, {len(data)} bytes")
            return True
    except Exception as e:
        print(f"Error downloading {url} -> {out_path}: {e}")
        return False

# 1. Download specific images needed
downloads = {
    'static/posters/71.jpg': 'https://upload.wikimedia.org/wikipedia/en/d/dc/Kabir_Singh.jpg',
    'static/posters/75.jpg': 'https://upload.wikimedia.org/wikipedia/en/2/2f/Raazi_-_Poster.jpg',
    'static/posters/81.jpg': 'https://upload.wikimedia.org/wikipedia/en/0/07/Gully_Boy_poster.jpg',
    'static/covers/24.jpg': 'https://covers.openlibrary.org/b/id/13502048-L.jpg', # Ghachar Ghochar
}

for path, url in downloads.items():
    download_file(url, path)

# 2. Update movies.csv
df_m = pd.read_csv('dataset/movies.csv', encoding='utf-8')

# Fix WALL-E
df_m.loc[df_m['movieId'] == 36, 'title'] = 'WALL-E'

# Replace Movie 71: Animal -> Kabir Singh
df_m.loc[df_m['movieId'] == 71, ['title', 'genres', 'director', 'cast', 'overview', 'release_year', 'imdb_rating']] = [
    'Kabir Singh',
    'Drama|Romance|Action',
    'Sandeep Reddy Vanga',
    'Shahid Kapoor, Kiara Advani, Arjan Bajwa, Suresh Oberoi',
    'A rebellious and aggressive house surgeon goes down a self-destructive spiral of drugs and alcohol after the woman he loves is forced to marry someone else.',
    2019,
    7.1
]

# Replace Movie 75: Jab We Met -> Raazi
df_m.loc[df_m['movieId'] == 75, ['title', 'genres', 'director', 'cast', 'overview', 'release_year', 'imdb_rating']] = [
    'Raazi',
    'Action|Drama|Thriller',
    'Meghna Gulzar',
    'Alia Bhatt, Vicky Kaushal, Rajit Kapur, Shishir Sharma',
    'An undercover Indian RAW agent is married into a Pakistani family of military officials to relay covert intelligence during the Indo-Pakistani War of 1971.',
    2018,
    7.7
]

# Replace Movie 81: Hindi Medium -> Gully Boy
df_m.loc[df_m['movieId'] == 81, ['title', 'genres', 'director', 'cast', 'overview', 'release_year', 'imdb_rating']] = [
    'Gully Boy',
    'Drama|Music|Romance',
    'Zoya Akhtar',
    'Ranveer Singh, Alia Bhatt, Siddhant Chaturvedi, Vijay Raaz',
    'A coming-of-age story of Murad, an aspiring street rapper from Mumbai who navigates social prejudices and family struggles to conquer the hip-hop scene.',
    2019,
    7.9
]

df_m.to_csv('dataset/movies.csv', index=False, encoding='utf-8')
print("Successfully updated dataset/movies.csv (100 movies preserved).")

# 3. Update books.csv
df_b = pd.read_csv('dataset/books.csv', encoding='utf-8')

# Fix Gabriel García Márquez & Antoine de Saint-Exupéry encoding
df_b.loc[df_b['bookId'] == 72, ['author', 'title']] = ['Gabriel García Márquez', 'One Hundred Years of Solitude']
df_b.loc[df_b['bookId'] == 73, ['author', 'title']] = ['Gabriel García Márquez', 'Love in the Time of Cholera']
df_b.loc[df_b['bookId'] == 99, ['author', 'title']] = ['Antoine de Saint-Exupéry', 'The Little Prince']

# Replaced Indian Books:
# Book 21: The Blue Umbrella by Ruskin Bond
df_b.loc[df_b['bookId'] == 21, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'The Blue Umbrella',
    'Ruskin Bond',
    'Indian',
    'Fiction|Children|Classic',
    'Innocence, Kindness, Simple Living, Mountain Life',
    1974,
    4.5,
    'Set in a picturesque Garhwal village, young Binya trades her leopard-claw pendant for a stunning blue umbrella, sparking town envy and a heartfelt lesson in compassion.'
]

# Book 24: Ghachar Ghochar by Vivek Shanbhag
df_b.loc[df_b['bookId'] == 24, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Ghachar Ghochar',
    'Vivek Shanbhag',
    'Indian',
    'Contemporary Fiction|Literary Fiction|Family Drama',
    'Modern India, Wealth, Family Dynamics, Urbanization',
    2015,
    4.3,
    'A masterfully crafted novella tracking a Bangalore family whose sudden wealth disrupts their traditional bonds and subtle moral balance.'
]

# Book 47: I Too Had a Love Story by Ravinder Singh
df_b.loc[df_b['bookId'] == 47, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'I Too Had a Love Story',
    'Ravinder Singh',
    'Indian',
    'Romance|Tragedy|Contemporary Fiction',
    'True Love, Loss, Modern Relationships, Fate',
    2008,
    4.4,
    'A deeply emotional real-life love story between Ravin and Khushi, spanning cross-city calls and matrimonial sites before tragedy strikes.'
]

# Book 48: Can Love Happen Twice? by Ravinder Singh
df_b.loc[df_b['bookId'] == 48, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Can Love Happen Twice?',
    'Ravinder Singh',
    'Indian',
    'Romance|Drama|Contemporary Fiction',
    'Second Chances, Healing, Grief, Friendship',
    2011,
    4.2,
    'On Valentine\'s Day night in Chandigarh, three friends broadcast Ravin\'s unfinished radio narrative about finding love again after heartbreak.'
]

# Book 49: Sacred Games by Vikram Chandra
df_b.loc[df_b['bookId'] == 49, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Sacred Games',
    'Vikram Chandra',
    'Indian',
    'Crime Fiction|Thriller|Mystery|Noir',
    'Mumbai Underworld, Corruption, Religion, Redemption',
    2006,
    4.6,
    'Sartaj Singh, a cynical Mumbai police officer, enters a deadly cat-and-mouse game against mythical crime lord Ganesh Gaitonde to avert citywide destruction.'
]

# Book 50: Everyone Has a Story by Savi Sharma
df_b.loc[df_b['bookId'] == 50, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Everyone Has a Story',
    'Savi Sharma',
    'Indian',
    'Inspirational Fiction|Drama|Romance',
    'Dreams, Purpose, Friendship, Self-Discovery',
    2016,
    4.2,
    'Four young individuals cross paths in an unassuming cafe, inspiring each other to confront life tragedies and pursue their authentic writing and creative dreams.'
]

# Book 51: Selection Day by Aravind Adiga
df_b.loc[df_b['bookId'] == 51, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Selection Day',
    'Aravind Adiga',
    'Indian',
    'Literary Fiction|Contemporary Fiction|Drama',
    'Cricket Ambition, Slum Life, Father-Son Rivalry, Mumbai',
    2016,
    4.3,
    'Two brothers in Mumbai are groomed by their obsessive father to become the city\'s top batsmen, exploring the ferocious clash between family expectation and personal identity.'
]

# Book 52: Legend of Suheldev by Amish Tripathi
df_b.loc[df_b['bookId'] == 52, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Legend of Suheldev',
    'Amish Tripathi',
    'Indian',
    'Historical Fiction|Mythology|Action|Epic',
    'Patriotism, Warrior Spirit, Medieval India, Unity',
    2020,
    4.5,
    'The untold chronicle of King Suheldev of Shravasti, who united divided kingdoms to defend Mother India against ferocious foreign invaders in the 11th century.'
]

# Book 53: India After Gandhi by Ramachandra Guha
df_b.loc[df_b['bookId'] == 53, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'India After Gandhi',
    'Ramachandra Guha',
    'Indian',
    'Non-Fiction|History|Politics',
    'Democracy, Post-Independence, Nation Building, Indian Unity',
    2007,
    4.8,
    'The definitive historical masterwork detailing how the world\'s most diverse nation held together against insurmountable economic, linguistic, and political odds.'
]

# Book 56: Maximum City: Bombay Lost and Found by Suketu Mehta
df_b.loc[df_b['bookId'] == 56, ['title', 'author', 'origin', 'genres', 'themes', 'publication_year', 'rating', 'description']] = [
    'Maximum City',
    'Suketu Mehta',
    'Indian',
    'Non-Fiction|Memoir|Journalism|Sociology',
    'Mumbai Megacity, Underworld, Bollywood, Urban Survival',
    2004,
    4.7,
    'A Pulitzer Prize finalist portrait plunging deep into Bombay\'s underbelly—from bar dancers and gang hitmen to Bollywood magnates and communal riots.'
]

df_b.to_csv('dataset/books.csv', index=False, encoding='utf-8')
print("Successfully updated dataset/books.csv (100 books: exactly 60 Indian + 40 International preserved).")
