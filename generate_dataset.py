import os
import pandas as pd
import numpy as np

os.makedirs('dataset', exist_ok=True)

# 100 Movies: 40 Hollywood Classics + 60 Iconic Bollywood Films
movies_data = [
    # --- 40 Hollywood Movies (1-40) ---
    {
        "movieId": 1, "title": "Inception", "genres": "Action|Sci-Fi|Thriller", "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "release_year": 2010, "imdb_rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg"
    },
    {
        "movieId": 2, "title": "Interstellar", "genres": "Adventure|Drama|Sci-Fi", "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine",
        "overview": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft to find a new planet for humans.",
        "release_year": 2014, "imdb_rating": 8.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
    },
    {
        "movieId": 3, "title": "The Dark Knight", "genres": "Action|Crime|Drama", "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
        "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
        "release_year": 2008, "imdb_rating": 9.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg"
    },
    {
        "movieId": 4, "title": "The Matrix", "genres": "Action|Sci-Fi", "director": "Lana Wachowski, Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
        "overview": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is an elaborate deception.",
        "release_year": 1999, "imdb_rating": 8.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 5, "title": "The Matrix Reloaded", "genres": "Action|Sci-Fi", "director": "Lana Wachowski, Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
        "overview": "Neo and his newfound allies race to prevent an army of machines from destroying the last human refuge, Zion.",
        "release_year": 2003, "imdb_rating": 7.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODEzODEzMzIzOV5BMl5BanBnXkFtZTYwOTQ1MDI3._V1_.jpg"
    },
    {
        "movieId": 6, "title": "The Godfather", "genres": "Crime|Drama", "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan, Robert Duvall",
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "release_year": 1972, "imdb_rating": 9.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzEt._V1_.jpg"
    },
    {
        "movieId": 7, "title": "The Godfather Part II", "genres": "Crime|Drama", "director": "Francis Ford Coppola",
        "cast": "Al Pacino, Robert De Niro, Robert Duvall, Diane Keaton",
        "overview": "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the syndicate.",
        "release_year": 1974, "imdb_rating": 9.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDAtNDk2ZDQ4NDI0M2Q3XkEyXkFqcGdeQXVyNzkwMjQ5NzEt._V1_.jpg"
    },
    {
        "movieId": 8, "title": "Pulp Fiction", "genres": "Crime|Drama", "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson, Bruce Willis",
        "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "release_year": 1994, "imdb_rating": 8.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzEt._V1_.jpg"
    },
    {
        "movieId": 9, "title": "Goodfellas", "genres": "Biography|Crime|Drama", "director": "Martin Scorsese",
        "cast": "Robert De Niro, Ray Liotta, Joe Pesci, Lorraine Bracco",
        "overview": "The story of Henry Hill and his life in the mob, covering his relationship with his mob partners Jimmy Conway and Tommy DeVito.",
        "release_year": 1990, "imdb_rating": 8.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI5MzktMjY4ZjdkNjExN2IzXkEyXkFqcGdeQXVyNzkwMjQ5NzEt._V1_.jpg"
    },
    {
        "movieId": 10, "title": "The Shawshank Redemption", "genres": "Drama", "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
        "overview": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        "release_year": 1994, "imdb_rating": 9.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxNzMtYjBkNy00NmNmLWJiN2UtNmEoMWY3NWVkODcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 11, "title": "Fight Club", "genres": "Drama", "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter, Meat Loaf",
        "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "release_year": 1999, "imdb_rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODQ0OWJiMzktYjNlYi00OThlLWI0OGEtNmAwNWI5ZGYNTlmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg"
    },
    {
        "movieId": 12, "title": "Seven", "genres": "Crime|Drama|Mystery", "director": "David Fincher",
        "cast": "Morgan Freeman, Brad Pitt, Kevin Spacey, Gwyneth Paltrow",
        "overview": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
        "release_year": 1995, "imdb_rating": 8.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 13, "title": "Avengers: Endgame", "genres": "Action|Adventure|Sci-Fi", "director": "Anthony Russo, Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
        "overview": "After the devastating events of Infinity War, the remaining Avengers assemble once more to reverse Thanos' actions.",
        "release_year": 2019, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg"
    },
    {
        "movieId": 14, "title": "Avengers: Infinity War", "genres": "Action|Adventure|Sci-Fi", "director": "Anthony Russo, Joe Russo",
        "cast": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans",
        "overview": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation.",
        "release_year": 2018, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_.jpg"
    },
    {
        "movieId": 15, "title": "Iron Man", "genres": "Action|Adventure|Sci-Fi", "director": "Jon Favreau",
        "cast": "Robert Downey Jr., Gwyneth Paltrow, Terrence Howard, Jeff Bridges",
        "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor.",
        "release_year": 2008, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_.jpg"
    },
    {
        "movieId": 16, "title": "Spider-Man: Into the Spider-Verse", "genres": "Animation|Action|Adventure", "director": "Bob Persichetti, Peter Ramsey",
        "cast": "Shameik Moore, Jake Johnson, Hailee Steinfeld, Mahershala Ali",
        "overview": "Teen Miles Morales becomes the new Spider-Man and joins other Spider-Heroes from parallel dimensions to stop a threat to all reality.",
        "release_year": 2018, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgyNV5BMl5BanBnXkFtZTgwNjkwNTM3NjM@._V1_.jpg"
    },
    {
        "movieId": 17, "title": "Toy Story", "genres": "Animation|Adventure|Comedy", "director": "John Lasseter",
        "cast": "Tom Hanks, Tim Allen, Don Rickles, Jim Varney",
        "overview": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
        "release_year": 1995, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2MTMzODA@._V1_.jpg"
    },
    {
        "movieId": 18, "title": "Spirited Away", "genres": "Animation|Adventure|Family", "director": "Hayao Miyazaki",
        "cast": "Daveigh Chase, Suzanne Pleshette, Miyu Irino, Rumi Hiiragi",
        "overview": "During her family's move to the suburbs, a 10-year-old girl wanders into a world ruled by gods, witches, and spirits.",
        "release_year": 2001, "imdb_rating": 8.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjlmAmZjYzUtZjc2Ni00YzAwLWE4M2QtYTVmMz03ZDUxNTA1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
    },
    {
        "movieId": 19, "title": "Coco", "genres": "Animation|Adventure|Drama", "director": "Lee Unkrich, Adrian Molina",
        "cast": "Anthony Gonzalez, Gael García Bernal, Benjamin Bratt, Alanna Ubach",
        "overview": "Aspiring musician Miguel enters the Land of the Dead to find his great-great-grandfather, a legendary singer.",
        "release_year": 2017, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkZTE1ODMxXkEyXkFqcGdeQXVyLAxNzQzNDgzMQ@@._V1_.jpg"
    },
    {
        "movieId": 20, "title": "Up", "genres": "Animation|Adventure|Comedy", "director": "Pete Docter, Bob Peterson",
        "cast": "Edward Asner, Jordan Nagai, John Ratzenberger, Christopher Plummer",
        "overview": "78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.",
        "release_year": 2009, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTk3NDE2NzI4NF5BMl5BanBnXkFtZTgwNzE1MzEyMTE@._V1_.jpg"
    },
    {
        "movieId": 21, "title": "Titanic", "genres": "Drama|Romance", "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates",
        "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "release_year": 1997, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg"
    },
    {
        "movieId": 22, "title": "La La Land", "genres": "Comedy|Drama|Music|Romance", "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, Rosemarie DeWitt, J.K. Simmons",
        "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations.",
        "release_year": 2016, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_.jpg"
    },
    {
        "movieId": 23, "title": "Whiplash", "genres": "Drama|Music", "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Melissa Benoist, Paul Reiser",
        "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who stops at nothing.",
        "release_year": 2014, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTA5NDZlZGUtMjAxOS00YTRkLTkwYmMtYWQ0NWEwZDZiNjEzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
    },
    {
        "movieId": 24, "title": "Parasite", "genres": "Drama|Thriller", "director": "Bong Joon Ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik",
        "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "release_year": 2019, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZS00YzU4LWEyMDEtZTBiNDYzNDJjNWYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg"
    },
    {
        "movieId": 25, "title": "The Prestige", "genres": "Drama|Mystery|Sci-Fi", "director": "Christopher Nolan",
        "cast": "Christian Bale, Hugh Jackman, Scarlett Johansson, Michael Caine",
        "overview": "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything.",
        "release_year": 2006, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA4NDI0MTIxNF5BMl5BanBnXkFtZTYwNTM0MzY2._V1_.jpg"
    },
    {
        "movieId": 26, "title": "Memento", "genres": "Mystery|Thriller", "director": "Christopher Nolan",
        "cast": "Guy Pearce, Carrie-Anne Moss, Joe Pantoliano, Mark Boone Junior",
        "overview": "A man with short-term memory loss attempts to track down his wife's murderer using an intricate system of notes and tattoos.",
        "release_year": 2000, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZTcyNjk1MjgtOWI3Mi00YTRmLWI5MTktAy02YTBkYWRhMjc1XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 27, "title": "Oppenheimer", "genres": "Biography|Drama|History", "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.",
        "overview": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
        "release_year": 2023, "imdb_rating": 8.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjctNDhhOC00NDU2LTllMTctYzdmOTExYjc3ZDlhXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg"
    },
    {
        "movieId": 28, "title": "Dune", "genres": "Action|Adventure|Sci-Fi", "director": "Denis Villeneuve",
        "cast": "Timothée Chalamet, Rebecca Ferguson, Zendaya, Oscar Isaac",
        "overview": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset on a dangerous desert planet.",
        "release_year": 2021, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtODExMTkxODlmZTM2XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg"
    },
    {
        "movieId": 29, "title": "Blade Runner 2049", "genres": "Action|Drama|Mystery|Sci-Fi", "director": "Denis Villeneuve",
        "cast": "Ryan Gosling, Harrison Ford, Ana de Armas, Sylvia Hoeks",
        "overview": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard.",
        "release_year": 2017, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_.jpg"
    },
    {
        "movieId": 30, "title": "Arrival", "genres": "Drama|Mystery|Sci-Fi", "director": "Denis Villeneuve",
        "cast": "Amy Adams, Jeremy Renner, Forest Whitaker, Michael Stuhlbarg",
        "overview": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.",
        "release_year": 2016, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_.jpg"
    },
    {
        "movieId": 31, "title": "Gladiator", "genres": "Action|Adventure|Drama", "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed",
        "overview": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "release_year": 2000, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 32, "title": "The Departed", "genres": "Crime|Drama|Thriller", "director": "Martin Scorsese",
        "cast": "Leonardo DiCaprio, Matt Damon, Jack Nicholson, Mark Wahlberg",
        "overview": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
        "release_year": 2006, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_.jpg"
    },
    {
        "movieId": 33, "title": "Shutter Island", "genres": "Mystery|Thriller", "director": "Martin Scorsese",
        "cast": "Leonardo DiCaprio, Emily Mortimer, Mark Ruffalo, Ben Kingsley",
        "overview": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.",
        "release_year": 2010, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY3gwMjVhOWMtYjVkMS00ZTM1LTlmMzgtYjMzNTE3MTY1M2FkXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg"
    },
    {
        "movieId": 34, "title": "The Wolf of Wall Street", "genres": "Biography|Comedy|Crime", "director": "Martin Scorsese",
        "cast": "Leonardo DiCaprio, Jonah Hill, Margot Robbie, Matthew McConaughey",
        "overview": "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker to his fall involving crime and corruption.",
        "release_year": 2013, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_.jpg"
    },
    {
        "movieId": 35, "title": "Forrest Gump", "genres": "Drama|Romance", "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise, Sally Field",
        "overview": "The history of the United States unfolds from the perspective of an Alabama man with an IQ of 75 who yearns to be reunited with his childhood sweetheart.",
        "release_year": 1994, "imdb_rating": 8.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg"
    },
    {
        "movieId": 36, "title": "WALL·E", "genres": "Animation|Adventure|Family|Sci-Fi", "director": "Andrew Stanton",
        "cast": "Ben Burtt, Elissa Knight, Jeff Garlin, Fred Willard",
        "overview": "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will decide the fate of mankind.",
        "release_year": 2008, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@._V1_.jpg"
    },
    {
        "movieId": 37, "title": "Inglourious Basterds", "genres": "Adventure|Drama|War", "director": "Quentin Tarantino",
        "cast": "Brad Pitt, Diane Kruger, Eli Roth, Christoph Waltz",
        "overview": "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by Jewish U.S. soldiers coincides with a theatre owner's vengeful plans.",
        "release_year": 2009, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTJiNDEzOWYtMTVjOC00ZjlmLWE0NGMtZmE1OWVmZDQ3OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzEt._V1_.jpg"
    },
    {
        "movieId": 38, "title": "Django Unchained", "genres": "Drama|Western", "director": "Quentin Tarantino",
        "cast": "Jamie Foxx, Christoph Waltz, Leonardo DiCaprio, Kerry Washington",
        "overview": "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner.",
        "release_year": 2012, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjIyNTQ5NjQ1OV5BMl5BanBnXkFtZTcwODg1MDU4OA@@._V1_.jpg"
    },
    {
        "movieId": 39, "title": "The Lion King", "genres": "Animation|Adventure|Drama", "director": "Roger Allers, Rob Minkoff",
        "cast": "Matthew Broderick, Jeremy Irons, James Earl Jones, Whoopi Goldberg",
        "overview": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
        "release_year": 1994, "imdb_rating": 8.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZCEtMjE3MS00MzNjLWFjNmYtMDk3N2ExMmM4Yzk2XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_.jpg"
    },
    {
        "movieId": 40, "title": "Jurassic Park", "genres": "Action|Adventure|Sci-Fi", "director": "Steven Spielberg",
        "cast": "Sam Neill, Laura Dern, Jeff Goldblum, Richard Attenborough",
        "overview": "A pragmatic paleontologist touring an almost complete theme park on an island is tasked with protecting kids after cloned dinosaurs run loose.",
        "release_year": 1993, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjM2MDgxMDg0Nl5BMl5BanBnXkFtZTgwNTM2OTM5NDE@._V1_.jpg"
    },

    # --- 60 Bollywood Movies (41-100) ---
    {
        "movieId": 41, "title": "3 Idiots", "genres": "Comedy|Drama", "director": "Rajkumar Hirani",
        "cast": "Aamir Khan, Madhavan, Sharman Joshi, Kareena Kapoor, Boman Irani",
        "overview": "Two friends search for their long lost companion who inspired them to think differently, while looking back on their engineering college days.",
        "release_year": 2009, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 42, "title": "Dangal", "genres": "Action|Biography|Drama|Sport", "director": "Nitesh Tiwari",
        "cast": "Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh, Sanya Malhotra",
        "overview": "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.",
        "release_year": 2016, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ4MzQzMzM2Nl5BMl5BanBnXkFtZTgwMTQ1NzU3MDI@._V1_.jpg"
    },
    {
        "movieId": 43, "title": "Sholay", "genres": "Action|Adventure|Comedy|Drama", "director": "Ramesh Sippy",
        "cast": "Dharmendra, Amitabh Bachchan, Sanjeev Kumar, Hema Malini, Amjad Khan",
        "overview": "After his family is murdered by a notorious and ruthless bandit, a former police officer enlists the services of two outlaws to capture him.",
        "release_year": 1975, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOGJiN2Q0OGItMzRhNS00YmM1LWEzYzctYWY5ZTBhNTQ5M2U4XkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg"
    },
    {
        "movieId": 44, "title": "Dilwale Dulhania Le Jayenge", "genres": "Drama|Romance", "director": "Aditya Chopra",
        "cast": "Shah Rukh Khan, Kajol, Amrish Puri, Farida Jalal",
        "overview": "When Raj and Simran meet on a trip across Europe, love blossoms. Raj follows Simran back to India to win over her traditional father.",
        "release_year": 1995, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNmJkODlhNmUtYTY4NC00ODNmLTlmNmQtMDQzNTQ0YjM1YzcxXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg"
    },
    {
        "movieId": 45, "title": "Taare Zameen Par", "genres": "Drama|Family", "director": "Aamir Khan, Amole Gupte",
        "cast": "Darsheel Safary, Aamir Khan, Tisca Chopra, Vipin Sharma",
        "overview": "An eight-year-old boy is thought to be a lazy trouble-maker, until the new art teacher has the patience and compassion to discover the real face behind his struggles.",
        "release_year": 2007, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTVmNjY3NWUtNDkxZS00NWNhLTk4ODEtYjkwNTFlOGJjNjc3XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 46, "title": "Lagaan: Once Upon a Time in India", "genres": "Adventure|Drama|Musical|Sport", "director": "Ashutosh Gowariker",
        "cast": "Aamir Khan, Gracy Singh, Rachel Shelley, Paul Blackthorne",
        "overview": "The people of a small village in Victorian India stake their future on a game of cricket against their ruthless British rulers to avoid exorbitant taxes.",
        "release_year": 2001, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDYxNWUzZmYtBhYmM1LTkxNjctOTRhODg3ODIzMmUzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 47, "title": "PK", "genres": "Comedy|Drama|Sci-Fi", "director": "Rajkumar Hirani",
        "cast": "Aamir Khan, Anushka Sharma, Sushant Singh Rajput, Boman Irani",
        "overview": "An alien on Earth loses the only device he can use to communicate with his spaceship. His innocent nature and questions force humanity to confront religious dogmas.",
        "release_year": 2014, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTYzOTE2NjkxN15BMl5BanBnXkFtZTgwMDgzMTg0MzE@._V1_.jpg"
    },
    {
        "movieId": 48, "title": "Swades", "genres": "Drama", "director": "Ashutosh Gowariker",
        "cast": "Shah Rukh Khan, Gayatri Joshi, Kishori Ballal, Rajesh Vivek",
        "overview": "A successful Indian scientist working at NASA returns to an Indian village to find his childhood nanny, only to discover his true calling.",
        "release_year": 2004, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQ2Njg0NTY1OV5BMl5BanBnXkFtZTcwMjg5MjAzMQ@@._V1_.jpg"
    },
    {
        "movieId": 49, "title": "Chak De! India", "genres": "Drama|Sport", "director": "Shimit Amin",
        "cast": "Shah Rukh Khan, Vidya Malvade, Sagarika Ghatge, Shilpa Shukla",
        "overview": "Kabir Khan, a former hockey star tainted by false betrayal allegations, takes charge of the underdog Indian women's national hockey team to lead them to world glory.",
        "release_year": 2007, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTcxODgyNDY3Ml5BMl5BanBnXkFtZTcwMDQ5Mjg3NA@@._V1_.jpg"
    },
    {
        "movieId": 50, "title": "Kal Ho Naa Ho", "genres": "Comedy|Drama|Musical|Romance", "director": "Nikkhil Advani",
        "cast": "Shah Rukh Khan, Preity Zinta, Saif Ali Khan, Jaya Bachchan",
        "overview": "A terminally ill man falls in love with an uptight MBA student in New York, but tries to set her up with her best friend before it is too late.",
        "release_year": 2003, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA0YzA4N2ItZjQ3Ny00NDQ0LWIzOGMtMmQxOGY2NGMwNTY4XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 51, "title": "Kabhi Khushi Kabhie Gham", "genres": "Drama|Musical|Romance", "director": "Karan Johar",
        "cast": "Amitabh Bachchan, Shah Rukh Khan, Kajol, Hrithik Roshan, Kareena Kapoor",
        "overview": "After marrying a poor woman, rich son Rahul is disowned by his father. Years later, his younger brother Rohan embarks on a mission to bring his family back together.",
        "release_year": 2001, "imdb_rating": 7.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTk5ODg0OTU5MV5BMl5BanBnXkFtZTgwMDQ3MDY3NjE@._V1_.jpg"
    },
    {
        "movieId": 52, "title": "Kuch Kuch Hota Hai", "genres": "Comedy|Drama|Romance", "director": "Karan Johar",
        "cast": "Shah Rukh Khan, Kajol, Rani Mukerji, Salman Khan",
        "overview": "An 8-year-old girl sets out on a journey to fulfill her late mother's dying wish: to reunite her widower father with his college best friend who was secretly in love with him.",
        "release_year": 1998, "imdb_rating": 7.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E2YmM2YjItYTI4Zi00YzBhLTkyNDUtZTZkNjMwNzg3OTMwXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 53, "title": "Zindagi Na Milegi Dobara", "genres": "Adventure|Comedy|Drama|Romance", "director": "Zoya Akhtar",
        "cast": "Hrithik Roshan, Farhan Akhtar, Abhay Deol, Katrina Kaif, Kalki Koechlin",
        "overview": "Three friends embark on a bachelor road trip across Spain, confronting their deepest fears, healing past wounds, and discovering true freedom.",
        "release_year": 2011, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZGFmMjM5OWMtZTRiNC00ODhlLThlYTItYDcyZDMyYWRlYWY1XkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg"
    },
    {
        "movieId": 54, "title": "Dil Chahta Hai", "genres": "Comedy|Drama|Romance", "director": "Farhan Akhtar",
        "cast": "Aamir Khan, Saif Ali Khan, Akshaye Khanna, Preity Zinta",
        "overview": "Three inseparable college friends navigate romance, adult responsibilities, and emotional rifts that threaten to break their bond in modern Mumbai.",
        "release_year": 2001, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODg1ZTgyN2ItZTZiYi00MWFmLWJkMWQtZjkwNTY2ZWY5OGJiXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 55, "title": "Queen", "genres": "Adventure|Comedy|Drama", "director": "Vikas Bahl",
        "cast": "Kangana Ranaut, Rajkummar Rao, Lisa Haydon, Mish Boyko",
        "overview": "A Delhi girl from a traditional family sets out on a solo honeymoon trip across Paris and Amsterdam after her fiancé calls off their wedding.",
        "release_year": 2013, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ4MzMzNzA0MF5BMl5BanBnXkFtZTgwNTU0ODAzMTE@._V1_.jpg"
    },
    {
        "movieId": 56, "title": "Barfi!", "genres": "Comedy|Drama|Romance", "director": "Anurag Basu",
        "cast": "Ranbir Kapoor, Priyanka Chopra, Ileana D'Cruz, Saurabh Shukla",
        "overview": "Set in the 1970s in Darjeeling and Kolkata, this heartfelt story follows Barfi, a mute and deaf young man, and his relationships with two extraordinary women.",
        "release_year": 2012, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ0MzI1NjYxMV5BMl5BanBnXkFtZTcwNTUwNTQ0OA@@._V1_.jpg"
    },
    {
        "movieId": 57, "title": "Gangs of Wasseypur", "genres": "Action|Comedy|Crime|Drama", "director": "Anurag Kashyap",
        "cast": "Manoj Bajpayee, Richa Chadha, Nawazuddin Siddiqui, Tigmanshu Dhulia",
        "overview": "A clash between Sultan and Shahid Khan leads to the expulsion of Khan from Wasseypur, igniting a deadly multigenerational coal mafia blood feud.",
        "release_year": 2012, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc5NjY4MjUwNF5BMl5BanBnXkFtZTgwODM3NzM5MzE@._V1_.jpg"
    },
    {
        "movieId": 58, "title": "Gangs of Wasseypur Part 2", "genres": "Action|Comedy|Crime|Drama", "director": "Anurag Kashyap",
        "cast": "Nawazuddin Siddiqui, Huma Qureshi, Tigmanshu Dhulia, Zeishan Quadri",
        "overview": "Faizal Khan avenges the brutal murders of his father and brother as ruthless bloodshed engulfs the Dhanbad coal mafia in an epic criminal showdown.",
        "release_year": 2012, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ1Mzc4MzE2OF5BMl5BanBnXkFtZTcwMTc5MjA0OA@@._V1_.jpg"
    },
    {
        "movieId": 59, "title": "Andhadhun", "genres": "Crime|Drama|Music|Mystery|Thriller", "director": "Sriram Raghavan",
        "cast": "Ayushmann Khurrana, Tabu, Radhika Apte, Anil Dhawan",
        "overview": "A series of mysterious events unfold after a visually impaired pianist unintentionally reports the murder of a former film star.",
        "release_year": 2018, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWZhMjhhZmYtOTIzOC00MGYzLWI1OGYtM2ZkN2IxNTI4ZWI3XkEyXkFqcGdeQXVyNDAzNDk0MTQ@._V1_.jpg"
    },
    {
        "movieId": 60, "title": "Drishyam", "genres": "Crime|Drama|Mystery|Thriller", "director": "Nishikant Kamat",
        "cast": "Ajay Devgn, Shriya Saran, Tabu, Rajat Kapoor",
        "overview": "Desperate measures are taken by a cable TV operator to protect his family from the dark side of the law after they commit an accidental murder.",
        "release_year": 2015, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmJhZmJlYTItZmZlNy00MGY0LTg5MmNmM2NjN2M1ODk5M2FmXkEyXkFqcGdeQXVyMTA4NDI1NTM@._V1_.jpg"
    },
    {
        "movieId": 61, "title": "Kahaani", "genres": "Mystery|Thriller", "director": "Sujoy Ghosh",
        "cast": "Vidya Balan, Parambrata Chatterjee, Nawazuddin Siddiqui, Indraneil Sengupta",
        "overview": "A pregnant woman arrives in Kolkata from London to search for her missing husband during the vibrant festival of Durga Puja.",
        "release_year": 2012, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTg0NjUxMzM2NF5BMl5BanBnXkFtZTcwMTgyMzg4Nw@@._V1_.jpg"
    },
    {
        "movieId": 62, "title": "Tumbbad", "genres": "Drama|Fantasy|Horror|Mystery|Thriller", "director": "Rahi Anil Barve, Anand Gandhi",
        "cast": "Sohum Shah, Jyoti Malshe, Anita Date, Ronjini Chakraborty",
        "overview": "A mythological horror story revolving around human greed and the forbidden worship of Hastar, the demon god of gold and grain.",
        "release_year": 2018, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmQxNmU4ZjgtZjk2NC00OWFiLWI3NjQtMDdhNGJhODJlYWE3XkEyXkFqcGdeQXVyMTA4NDI1NTM@._V1_.jpg"
    },
    {
        "movieId": 63, "title": "Stree", "genres": "Comedy|Horror", "director": "Amar Kaushik",
        "cast": "Rajkummar Rao, Shraddha Kapoor, Pankaj Tripathi, Aparshakti Khurana",
        "overview": "In the small town of Chanderi, men live in fear of an evil spirit named Stree who abducts men in the dark during the festival season.",
        "release_year": 2018, "imdb_rating": 7.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5NTg3NTU3N15BMl5BanBnXkFtZTgwNTI4MDYyNTM@._V1_.jpg"
    },
    {
        "movieId": 64, "title": "Munna Bhai M.B.B.S.", "genres": "Comedy|Drama|Musical", "director": "Rajkumar Hirani",
        "cast": "Sanjay Dutt, Arshad Warsi, Gracy Singh, Boman Irani, Sunil Dutt",
        "overview": "A lovable underworld don enrols in medical college to fulfil his father's dream of seeing him become a respected doctor, spreading warmth and laughter.",
        "release_year": 2003, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODg2ZDVlZDMtOWQ3MS00OGMwLTgyM2UtYmVjMTI4Y2M5YTgzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 65, "title": "Lage Raho Munna Bhai", "genres": "Comedy|Drama|Fantasy", "director": "Rajkumar Hirani",
        "cast": "Sanjay Dutt, Arshad Warsi, Vidya Balan, Boman Irani, Dilip Prabhavalkar",
        "overview": "Munna Bhai begins to see the spirit of Mahatma Gandhi. Through their conversations, he champions non-violence and truth, known as Gandhigiri.",
        "release_year": 2006, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTczMDc5MzU0Ml5BMl5BanBnXkFtZTcwNTg2MzAzMQ@@._V1_.jpg"
    },
    {
        "movieId": 66, "title": "Bajrangi Bhaijaan", "genres": "Action|Adventure|Comedy|Drama", "director": "Kabir Khan",
        "cast": "Salman Khan, Harshaali Malhotra, Nawazuddin Siddiqui, Kareena Kapoor",
        "overview": "A devout Indian man undertakes a heartfelt and perilous journey across the border to reunite a mute Pakistani girl with her family.",
        "release_year": 2015, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc1NzkzMzM1M15BMl5BanBnXkFtZTgwMTcxNjc4NTE@._V1_.jpg"
    },
    {
        "movieId": 67, "title": "Sultan", "genres": "Action|Drama|Sport", "director": "Ali Abbas Zafar",
        "cast": "Salman Khan, Anushka Sharma, Randeep Hooda, Amit Sadh",
        "overview": "Sultan Ali Khan, a middle-aged former wrestling champion from Haryana, attempts a heroic comeback in mixed martial arts.",
        "release_year": 2016, "imdb_rating": 7.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTU3MTU1NjkzNF5BMl5BanBnXkFtZTgwNzg4MjM3OTE@._V1_.jpg"
    },
    {
        "movieId": 68, "title": "War", "genres": "Action|Thriller", "director": "Siddharth Anand",
        "cast": "Hrithik Roshan, Tiger Shroff, Vaani Kapoor, Ashutosh Rana",
        "overview": "An Indian soldier is assigned to eliminate his former mentor and decorated rogue special agent in an international high-octane cat-and-mouse chase.",
        "release_year": 2019, "imdb_rating": 6.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA4YzM5NmQtMDc4MC00NGU1LWE2NGEtOWZhNTAzMTNhYzVlXkEyXkFqcGdeQXVyMTA5NzIyMDY5._V1_.jpg"
    },
    {
        "movieId": 69, "title": "Pathaan", "genres": "Action|Adventure|Thriller", "director": "Siddharth Anand",
        "cast": "Shah Rukh Khan, Deepika Padukone, John Abraham, Dimple Kapadia",
        "overview": "An exiled RAW field operative is called back to active duty to prevent a catastrophic biological terror strike on India planned by a rogue mercenary outfit.",
        "release_year": 2023, "imdb_rating": 5.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BM2QzM2UxNzMtN2Y5Yi00MDVmLTgwYmEtODQ2OWQ5NDUzM2RkXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg"
    },
    {
        "movieId": 70, "title": "Jawan", "genres": "Action|Thriller", "director": "Atlee",
        "cast": "Shah Rukh Khan, Nayanthara, Vijay Sethupathi, Deepika Padukone",
        "overview": "A prison warden and a high-profile vigilante commando team set out on a crusade to dismantle systemic corruption across society.",
        "release_year": 2023, "imdb_rating": 7.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODg1ZTkyYmMtZTI0Mi00ZTIxLWI3YTItMzIxYTY0ZjY5NDI1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 71, "title": "Animal", "genres": "Action|Crime|Drama", "director": "Sandeep Reddy Vanga",
        "cast": "Ranbir Kapoor, Anil Kapoor, Bobby Deol, Rashmika Mandanna",
        "overview": "A fierce father-son bond spirals into a violent obsession when a wealthy industrialist is targeted by assassins, unleashing utter devastation.",
        "release_year": 2023, "imdb_rating": 6.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNGViM2M4NmUtMmNkNy00MTU4LTgxNTAtYTlhYzgyN2FiNzk3XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 72, "title": "Brahmastra Part One: Shiva", "genres": "Action|Adventure|Fantasy|Sci-Fi", "director": "Ayan Mukerji",
        "cast": "Ranbir Kapoor, Alia Bhatt, Amitabh Bachchan, Mouni Roy, Nagarjuna",
        "overview": "A young DJ named Shiva discovers his supernatural connection to fire and embarks on an epic journey to protect the celestial weapon Brahmastra.",
        "release_year": 2022, "imdb_rating": 5.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjY5ZGE1OGYtNjlmMi00YmNmLWE1OTEtNjM5NjA0NzYwODk3XkEyXkFqcGdeQXVyMTA3MDk2NDg2._V1_.jpg"
    },
    {
        "movieId": 73, "title": "Yeh Jawaani Hai Deewani", "genres": "Comedy|Drama|Musical|Romance", "director": "Ayan Mukerji",
        "cast": "Ranbir Kapoor, Deepika Padukone, Aditya Roy Kapur, Kalki Koechlin",
        "overview": "Kabir and Naina meet during a trekking trip to the Himalayas. Years later, they reunite at a friend's lavish wedding, rediscovering love and dreams.",
        "release_year": 2013, "imdb_rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODA2MjU1NTMzMl5BMl5BanBnXkFtZTgwNTU5NTg2MDE@._V1_.jpg"
    },
    {
        "movieId": 74, "title": "Rockstar", "genres": "Drama|Music|Musical|Romance", "director": "Imtiaz Ali",
        "cast": "Ranbir Kapoor, Nargis Fakhri, Shammi Kapoor, Kumud Mishra",
        "overview": "Janardhan Jakhar seeks heartbreak to discover the true anguish needed to become a legendary music icon, ascending to fame as Jordan.",
        "release_year": 2011, "imdb_rating": 7.7,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTc3NzAxMjg4Ml5BMl5BanBnXkFtZTcwMDc2ODQwNw@@._V1_.jpg"
    },
    {
        "movieId": 75, "title": "Jab We Met", "genres": "Comedy|Drama|Romance", "director": "Imtiaz Ali",
        "cast": "Shahid Kapoor, Kareena Kapoor, Tarun Arora, Saumya Tandon",
        "overview": "A depressed wealthy businessman's life turns around when he meets a bubbly, talkative Punjabi girl on an overnight train journey.",
        "release_year": 2007, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA2Nzk5M2EtNWY4Yi00ZDY4LThkZTgtYjhhNzc4NWI3MmMwXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 76, "title": "Tamasha", "genres": "Comedy|Drama|Romance", "director": "Imtiaz Ali",
        "cast": "Ranbir Kapoor, Deepika Padukone, Piyush Mishra, Javed Sheikh",
        "overview": "Ved and Tara meet in Corsica, living an untamed fantasy. Back in Delhi, Tara helps Ved break free from robotic corporate conformity to follow his inner artist.",
        "release_year": 2015, "imdb_rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5OTUyMzQ2N15BMl5BanBnXkFtZTgwNzYwMzU2NTE@._V1_.jpg"
    },
    {
        "movieId": 77, "title": "Haider", "genres": "Action|Crime|Drama|Thriller", "director": "Vishal Bhardwaj",
        "cast": "Shahid Kapoor, Tabu, Kay Kay Menon, Shraddha Kapoor, Irrfan Khan",
        "overview": "A modern adaptation of Shakespeare's Hamlet set against the turbulent backdrop of 1990s Kashmir, where a young poet searches for his disappeared father.",
        "release_year": 2014, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzg2NDg4NjAwMl5BMl5BanBnXkFtZTgwODc0ODk0MjE@._V1_.jpg"
    },
    {
        "movieId": 78, "title": "Omkara", "genres": "Action|Crime|Drama|Thriller", "director": "Vishal Bhardwaj",
        "cast": "Ajay Devgn, Saif Ali Khan, Kareena Kapoor, Vivek Oberoi, Konkona Sen Sharma",
        "overview": "An Indian adaptation of Othello set amidst the political mafia underworld of rural Uttar Pradesh, where jealousy and betrayal breed tragedy.",
        "release_year": 2006, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDJkMDY0OTEtNzI3Ni00ZjQ1LTljNjgtNjE5Yzc5M2RhYWI3XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 79, "title": "Maqbool", "genres": "Crime|Drama", "director": "Vishal Bhardwaj",
        "cast": "Irrfan Khan, Tabu, Pankaj Kapur, Om Puri, Naseeruddin Shah",
        "overview": "A gripping Mumbai underworld adaptation of Shakespeare's Macbeth, where right-hand henchman Maqbool falls into an ambitious vortex of ambition and betrayal.",
        "release_year": 2003, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTI2NzY3NzYxNl5BMl5BanBnXkFtZTcwNzU3MjYxMQ@@._V1_.jpg"
    },
    {
        "movieId": 80, "title": "The Lunchbox", "genres": "Drama|Romance", "director": "Ritesh Batra",
        "cast": "Irrfan Khan, Nimrat Kaur, Nawazuddin Siddiqui, Denzil Smith",
        "overview": "A mistaken delivery in Mumbai's famously efficient lunchbox delivery system connects a lonely housewife to an older man nearing retirement.",
        "release_year": 2013, "imdb_rating": 7.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTUxMzg2NzA2MV5BMl5BanBnXkFtZTgwNTU0OTkwMTE@._V1_.jpg"
    },
    {
        "movieId": 81, "title": "Hindi Medium", "genres": "Comedy|Drama", "director": "Saket Chaudhary",
        "cast": "Irrfan Khan, Saba Qamar, Dishita Sehgal, Deepak Dobriyal",
        "overview": "A wealthy Delhi boutique owner and his ambitious wife go to hilarious and desperate lengths to secure admission for their daughter in an elite English school.",
        "release_year": 2017, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjY5MzA3NzkwMV5BMl5BanBnXkFtZTgwNDU1NDYyMjI@._V1_.jpg"
    },
    {
        "movieId": 82, "title": "Paan Singh Tomar", "genres": "Action|Biography|Crime|Drama", "director": "Tigmanshu Dhulia",
        "cast": "Irrfan Khan, Mahie Gill, Vipin Sharma, Imran Hasnee",
        "overview": "The true story of an Indian army soldier and seven-time national steeplechase champion who turns into a dreaded Chambal valley rebel due to land injustice.",
        "release_year": 2012, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA3NDkyMzYyMV5BMl5BanBnXkFtZTcwNjY0MjA0OA@@._V1_.jpg"
    },
    {
        "movieId": 83, "title": "Special 26", "genres": "Crime|Drama|Thriller", "director": "Neeraj Pandey",
        "cast": "Akshay Kumar, Anupam Kher, Manoj Bajpayee, Jimmy Shergill",
        "overview": "A team of daring con artists pose as CBI officers and execute audacious fake income tax raids on corrupt politicians and businessmen in 1980s India.",
        "release_year": 2013, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjI3Nzk2OTI3Ml5BMl5BanBnXkFtZTcwNTg5MDY2OA@@._V1_.jpg"
    },
    {
        "movieId": 84, "title": "A Wednesday", "genres": "Action|Crime|Drama|Mystery|Thriller", "director": "Neeraj Pandey",
        "cast": "Naseeruddin Shah, Anupam Kher, Jimmy Shergill, Aamir Bashir",
        "overview": "A retiring Mumbai police commissioner reminisces about the most mind-bending case of his career: a common man who held the entire city hostage over the phone.",
        "release_year": 2008, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDJkYzY3MzMtMGFhYi00MmQ4LWJkNTgtMDAzMmQ3MmY5N2VmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    },
    {
        "movieId": 85, "title": "Baby", "genres": "Action|Crime|Thriller", "director": "Neeraj Pandey",
        "cast": "Akshay Kumar, Danny Denzongpa, Rana Daggubati, Taapsee Pannu",
        "overview": "An elite counter-intelligence black-ops unit embarks on a covert global manhunt to neutralize a mastermind plotting major terrorist strikes on Indian soil.",
        "release_year": 2015, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQzMzE2ODAzNl5BMl5BanBnXkFtZTgwNTU5NTA3NDE@._V1_.jpg"
    },
    {
        "movieId": 86, "title": "Hera Pheri", "genres": "Action|Comedy|Crime", "director": "Priyadarshan",
        "cast": "Akshay Kumar, Suniel Shetty, Paresh Rawal, Tabu, Gulshan Grover",
        "overview": "Three broke roommates stumble into an accidental ransom phone call and hatch a comically disastrous plan to claim the ransom money for themselves.",
        "release_year": 2000, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2ZhZjk4YTQtYTVkZC00MTY2LWFmZTUtMDQzYTFjM2YyYzgxXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg"
    },
    {
        "movieId": 87, "title": "Phir Hera Pheri", "genres": "Comedy|Crime", "director": "Neeraj Vora",
        "cast": "Akshay Kumar, Suniel Shetty, Paresh Rawal, Bipasha Basu, Rimi Sen",
        "overview": "Babu Bhaiya, Raju, and Shyam fall victim to a hilarious investment scam promising to double their wealth in 21 days.",
        "release_year": 2006, "imdb_rating": 7.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZTU5ODliNjYtMmE0My00ZTdiLTlmMDItZDU4OGYxY2YwZTUxXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 88, "title": "Bhool Bhulaiyaa", "genres": "Comedy|Horror|Mystery|Psychological|Thriller", "director": "Priyadarshan",
        "cast": "Akshay Kumar, Vidya Balan, Shiney Ahuja, Ameesha Patel, Paresh Rawal",
        "overview": "An eccentric psychiatrist is summoned to an ancestral royal palace to unravel strange supernatural occurrences and the haunting presence of Manjulika.",
        "release_year": 2007, "imdb_rating": 7.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5OTg2ODE0NF5BMl5BanBnXkFtZTcwMTc5MjA0OA@@._V1_.jpg"
    },
    {
        "movieId": 89, "title": "Chhichhore", "genres": "Comedy|Drama", "director": "Nitesh Tiwari",
        "cast": "Sushant Singh Rajput, Shraddha Kapoor, Varun Sharma, Tahir Raj Bhasin",
        "overview": "Following a tragic accident, a grieving father gathers his nostalgic college hostel mates to recount their unforgettable days as proud losers.",
        "release_year": 2019, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjg2ZDI2YTYtN2E5Mi00YzM1LTg4OGUtNDViMDNjNDcxN2RhXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 90, "title": "MS Dhoni: The Untold Story", "genres": "Biography|Drama|Sport", "director": "Neeraj Pandey",
        "cast": "Sushant Singh Rajput, Kiara Advani, Disha Patani, Anupam Kher",
        "overview": "The inspiring life story of Mahendra Singh Dhoni, from a small-town railway ticket collector in Ranchi to leading India to World Cup cricket victory.",
        "release_year": 2016, "imdb_rating": 8.0,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjAzZjZiMmQtMDZmOC00NjVmLTkyNTItOGI2Mzg4NTBhZTA1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 91, "title": "Uri: The Surgical Strike", "genres": "Action|Drama|War", "director": "Aditya Dhar",
        "cast": "Vicky Kaushal, Paresh Rawal, Yami Gautam, Mohit Raina",
        "overview": "Major Vihaan Singh Shergill leads Indian special forces in a daring, covert counter-terrorist surgical strike following the Uri army base attack.",
        "release_year": 2019, "imdb_rating": 8.2,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWU4ZjNlNTQtOGE2MS00NTAyLWEyZWYtNzExNzAxNTQ1ES0yXkEyXkFqcGdeQXVyODMyODMxNDY@._V1_.jpg"
    },
    {
        "movieId": 92, "title": "Sardar Udham", "genres": "Biography|Crime|Drama|History", "director": "Shoojit Sircar",
        "cast": "Vicky Kaushal, Shaun Scott, Stephen Hogan, Amol Parashar",
        "overview": "A poignant biopic of Indian freedom fighter Udham Singh, who spent over two decades meticulously tracking down Michael O'Dwyer to avenge the Jallianwala Bagh massacre.",
        "release_year": 2021, "imdb_rating": 8.4,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjBiNzRhYzUtZjg0YS00YzQzLWEwYjMtZmFiOWVjNzM5ZDAwXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg"
    },
    {
        "movieId": 93, "title": "Piku", "genres": "Comedy|Drama", "director": "Shoojit Sircar",
        "cast": "Amitabh Bachchan, Deepika Padukone, Irrfan Khan, Moushumi Chatterjee",
        "overview": "A quirky, warm road trip across India brings an independent architect daughter, her hypochondriac aging father, and a taxi business owner together.",
        "release_year": 2015, "imdb_rating": 7.6,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5OTUyMzQ2N15BMl5BanBnXkFtZTgwNzYwMzU2NTE@._V1_.jpg"
    },
    {
        "movieId": 94, "title": "Pink", "genres": "Crime|Drama|Thriller", "director": "Aniruddha Roy Chowdhury",
        "cast": "Amitabh Bachchan, Taapsee Pannu, Kirti Kulhari, Andrea Kevichüsa",
        "overview": "When three independent young women are falsely accused of assault by influential men, a retired bipolar lawyer steps forward to champion the sanctity of female consent.",
        "release_year": 2016, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E0YmM4NGMtZTNiMC00OTk4LTk3N2EtNWIzZDk4ZjYxNTljXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 95, "title": "Badhaai Ho", "genres": "Comedy|Drama|Romance", "director": "Amit Sharma",
        "cast": "Ayushmann Khurrana, Neena Gupta, Gajraj Rao, Sanya Malhotra",
        "overview": "A 25-year-old middle-class Delhi man faces social awkwardness and familial chaos when his middle-aged mother becomes unexpectedly pregnant.",
        "release_year": 2018, "imdb_rating": 7.9,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWNmOTYyZmItNmY5MC00ZjQ1LWI4YTItODQ2ZjcxZjU4MTNkXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 96, "title": "Article 15", "genres": "Crime|Drama|Mystery|Thriller", "director": "Anubhav Sinha",
        "cast": "Ayushmann Khurrana, Nassar, Manoj Pahwa, Kumud Mishra",
        "overview": "An upright, city-bred police officer in rural Uttar Pradesh investigates the brutal rape and murder of two Dalit girls, battling deeply entrenched caste discrimination.",
        "release_year": 2019, "imdb_rating": 8.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA2Nzk5M2EtNWY4Yi00ZDY4LThkZTgtYjhhNzc4NWI3MmMwXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 97, "title": "Vicky Donor", "genres": "Comedy|Romance", "director": "Shoojit Sircar",
        "cast": "Ayushmann Khurrana, Yami Gautam, Annu Kapoor, Dolly Ahluwalia",
        "overview": "A charming, unemployed young Punjabi man is persuaded by an infertility specialist to become a secret sperm donor, testing his relationship with his Bengali lover.",
        "release_year": 2012, "imdb_rating": 7.8,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5OTUyMzQ2N15BMl5BanBnXkFtZTgwNzYwMzU2NTE@._V1_.jpg"
    },
    {
        "movieId": 98, "title": "Shershaah", "genres": "Action|Biography|Drama|War", "director": "Vishnuvardhan",
        "cast": "Sidharth Malhotra, Kiara Advani, Shiv Panditt, Nikitin Dheer",
        "overview": "The valorous journey of Captain Vikram Batra (Param Vir Chakra), whose extraordinary battlefield courage turned the tide of the 1999 Kargil War.",
        "release_year": 2021, "imdb_rating": 8.3,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzZjctZWQ4Ni00YWYwLWEwNzktNTk0NTc1ZTNjYjU4XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 99, "title": "Krrish", "genres": "Action|Adventure|Sci-Fi", "director": "Rakesh Roshan",
        "cast": "Hrithik Roshan, Priyanka Chopra, Rekha, Naseeruddin Shah",
        "overview": "Krishna inherits the superhuman powers endowed upon his father by an extraterrestrial visitor, adopting the superhero mantle of Krrish to save innocent lives.",
        "release_year": 2006, "imdb_rating": 6.5,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA2Nzk5M2EtNWY4Yi00ZDY4LThkZTgtYjhhNzc4NWI3MmMwXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    },
    {
        "movieId": 100, "title": "Koi... Mil Gaya", "genres": "Action|Drama|Fantasy|Sci-Fi", "director": "Rakesh Roshan",
        "cast": "Hrithik Roshan, Preity Zinta, Rekha, Prem Chopra",
        "overview": "A developmentally disabled young man befriends a stranded extraterrestrial alien named Jadoo, who bestows him with supernatural intellect and physical strength.",
        "release_year": 2003, "imdb_rating": 7.1,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E0YmM4NGMtZTNiMC00OTk4LTk3N2EtNWIzZDk4ZjYxNTljXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
    }
]

df_movies = pd.DataFrame(movies_data)
df_movies.to_csv("dataset/movies.csv", index=False)
print(f"Generated dataset/movies.csv with {len(df_movies)} total movies (40 Hollywood + 60 Bollywood).")

# Generate Realistic Rating Interactions for 10 users across the full 100 movie database
ratings = []

def add_ratings(user_id, high_movies, mid_movies, low_movies):
    for m in high_movies:
        ratings.append({"userId": user_id, "movieId": m, "rating": float(np.random.choice([4.5, 5.0])), "timestamp": 1600000000})
    for m in mid_movies:
        ratings.append({"userId": user_id, "movieId": m, "rating": float(np.random.choice([3.5, 4.0])), "timestamp": 1600000000})
    for m in low_movies:
        ratings.append({"userId": user_id, "movieId": m, "rating": float(np.random.choice([1.5, 2.0, 2.5])), "timestamp": 1600000000})

# User 1: Sci-Fi, Mind-Benders & Mystery
add_ratings(1, [1, 2, 3, 4, 25, 27, 28, 29, 47, 62, 99, 100], [5, 30, 40, 13, 59, 72], [17, 19, 21, 22, 51, 52])

# User 2: Crime, Gangs, Mafia & Dark Thrillers
add_ratings(2, [6, 7, 8, 9, 32, 34, 57, 58, 77, 78, 79, 82], [3, 12, 37, 38, 60, 83, 84], [18, 19, 20, 22, 44, 51])

# User 3: Action, High-Octane Thrillers & Superheroes
add_ratings(3, [3, 4, 13, 14, 15, 16, 40, 43, 68, 69, 70, 71, 91, 98], [1, 5, 31, 66, 67, 85], [6, 7, 21, 23, 80])

# User 4: Comedy, Family, Drama & Uplifting Cinema
add_ratings(4, [16, 17, 18, 19, 20, 36, 39, 41, 42, 45, 64, 65, 86, 89], [22, 35, 40, 46, 53, 55, 87, 93], [6, 8, 11, 12, 57, 71])

# User 5: Mystery, Psychological & Gripping Suspense
add_ratings(5, [11, 12, 24, 26, 33, 1, 25, 59, 60, 61, 62, 84, 88, 94], [8, 30, 29, 83, 96], [17, 20, 21, 15, 51, 87])

# User 6: Romance, Musical, Melodrama & Heartwarming
add_ratings(6, [21, 22, 23, 35, 10, 44, 50, 51, 52, 73, 74, 75, 80], [19, 24, 1, 53, 54, 76, 95], [4, 5, 12, 14, 57, 71])

# User 7: Stylized Drama, Dark Comedy & Gritty Realism
add_ratings(7, [8, 37, 38, 9, 11, 57, 58, 63, 77, 81, 95, 96, 97], [32, 3, 1, 55, 82, 93], [17, 19, 20, 21, 51, 72])

# User 8: Deep Drama, Biopics & National Classics
add_ratings(8, [2, 4, 28, 29, 30, 36, 25, 27, 46, 48, 49, 80, 90, 92], [1, 40, 56, 76, 94], [6, 21, 22, 68, 71])

# User 9: Top-Tier All-Rounder (Loves highest rated cinema across Hollywood & Bollywood)
add_ratings(9, [1, 3, 6, 8, 10, 18, 24, 27, 41, 42, 43, 44, 45, 53, 59, 60], [2, 11, 16, 23, 31, 35, 48, 49, 64, 86, 91], [5, 15, 68, 69, 72])

# User 10: Casual / Light Rater (Cold-Start candidate)
add_ratings(10, [1, 13, 35, 41, 66, 86], [17, 21, 44, 73], [6, 57])

df_ratings = pd.DataFrame(ratings)
df_ratings.to_csv("dataset/ratings.csv", index=False)
print(f"Generated dataset/ratings.csv with {len(df_ratings)} ratings across {df_ratings['userId'].nunique()} users.")
