import os
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.makedirs('dataset', exist_ok=True)
os.makedirs('static/covers', exist_ok=True)

# 100 Curated Books: 60 Iconic Indian Books + 40 World Classics / Bestsellers
books_data = [
    # =========================================================================
    # 60 BOOKS BY INDIAN WRITERS (IDs 1 - 60)
    # =========================================================================
    {
        "bookId": 1,
        "title": "The White Tiger",
        "author": "Aravind Adiga",
        "origin": "Indian",
        "genres": "Fiction|Dark Comedy|Social Satire",
        "themes": "Social Class|Ambition|Corruption|Modern India",
        "publication_year": 2008,
        "rating": 4.2,
        "cover_url": "/static/covers/1.jpg",
        "description": "Balram Halwai narrates his rise from a poor sweet-maker's son in a dark village to an entrepreneurial chauffeur in New Delhi and Bangalore, exposing the moral compromises of modern India."
    },
    {
        "bookId": 2,
        "title": "The God of Small Things",
        "author": "Arundhati Roy",
        "origin": "Indian",
        "genres": "Literary Fiction|Drama|Family Saga",
        "themes": "Caste|Forbidden Love|Memory|Family Secrets",
        "publication_year": 1997,
        "rating": 4.1,
        "cover_url": "/static/covers/2.jpg",
        "description": "The tragic childhood memories of fraternal twins Rahel and Estha in Kerala, whose lives are shattered by the 'Love Laws' dictating who should be loved, and how, and how much."
    },
    {
        "bookId": 3,
        "title": "Midnight's Children",
        "author": "Salman Rushdie",
        "origin": "Indian",
        "genres": "Magical Realism|Historical Fiction|Literary",
        "themes": "Identity|Post-Colonial India|Telepathy|Destiny",
        "publication_year": 1981,
        "rating": 4.0,
        "cover_url": "/static/covers/3.jpg",
        "description": "Born at the exact stroke of midnight on August 15, 1947, Saleem Sinai is telepathically linked to 1,000 other children born at India's independence, mirroring the nation's tumultuous history."
    },
    {
        "bookId": 4,
        "title": "A Suitable Boy",
        "author": "Vikram Seth",
        "origin": "Indian",
        "genres": "Historical Fiction|Romance|Family Saga",
        "themes": "Marriage|Post-Independence Politics|Tradition|Religious Harmony",
        "publication_year": 1993,
        "rating": 4.1,
        "cover_url": "/static/covers/4.jpg",
        "description": "Set in early 1950s India, Mrs. Rupa Mehra embarks on an exhaustive quest to find a suitable match for her spirited younger daughter, Lata, across four interconnected families."
    },
    {
        "bookId": 5,
        "title": "The Palace of Illusions",
        "author": "Chitra Banerjee Divakaruni",
        "origin": "Indian",
        "genres": "Mythological Fiction|Fantasy|Feminist Drama",
        "themes": "Mahabharata|Panchaali|Feminism|War & Honor",
        "publication_year": 2008,
        "rating": 4.3,
        "cover_url": "/static/covers/5.jpg",
        "description": "A reimagining of the world-famous Indian epic The Mahabharata from the poignant, powerful perspective of Panchaali (Draupadi), wife of the five Pandava brothers."
    },
    {
        "bookId": 6,
        "title": "The Forest of Enchantments",
        "author": "Chitra Banerjee Divakaruni",
        "origin": "Indian",
        "genres": "Mythological Fiction|Drama|Feminist",
        "themes": "Ramayana|Sita|Duty|Unconditional Love",
        "publication_year": 2019,
        "rating": 4.2,
        "cover_url": "/static/covers/6.jpg",
        "description": "The Ramayana told through Sita's tender yet fiercely resilient voice, highlighting the inner emotional lives of the women often silenced in heroic patriarchal tales."
    },
    {
        "bookId": 7,
        "title": "Train to Pakistan",
        "author": "Khushwant Singh",
        "origin": "Indian",
        "genres": "Historical Fiction|War|Drama",
        "themes": "Partition 1947|Communal Violence|Love & Sacrifice|Mano Majra",
        "publication_year": 1956,
        "rating": 4.3,
        "cover_url": "/static/covers/7.jpg",
        "description": "In the peaceful border village of Mano Majra, Sikhs and Muslims coexist harmoniously until the tragic ghost train filled with corpses arrives during the 1947 Partition of India."
    },
    {
        "bookId": 8,
        "title": "The Immortals of Meluha",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Thriller|Fantasy|Action",
        "themes": "Shiva Trilogy|Somras|Suryavanshis|Destiny & Karma",
        "publication_year": 2010,
        "rating": 4.4,
        "cover_url": "/static/covers/8.jpg",
        "description": "Tibetan tribal warrior Shiva is invited to the near-perfect empire of Meluha, where drinking the sacred Somras turns his throat blue, fulfilling the legend of the Neelkanth savior."
    },
    {
        "bookId": 9,
        "title": "The Secret of the Nagas",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Thriller|Fantasy|Action",
        "themes": "Shiva Trilogy|Deformed Nagas|Good vs Evil|Mystery",
        "publication_year": 2011,
        "rating": 4.3,
        "cover_url": "/static/covers/9.jpg",
        "description": "Shiva's quest to avenge his friend's murder takes him across ancient India to the sinister realm of the Nagas, only to reveal heartbreaking truths about justice and family."
    },
    {
        "bookId": 10,
        "title": "The Oath of the Vayuputras",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Thriller|Fantasy|Epic War",
        "themes": "Shiva Trilogy Finale|Evil of Somras|Vayuputras|Sacrifice",
        "publication_year": 2013,
        "rating": 4.2,
        "cover_url": "/static/covers/10.jpg",
        "description": "The climactic final showdown where Shiva leads a continent-wide crusade against the evil usage of Somras, reaching out to the mysterious and powerful Vayuputra tribe."
    },
    {
        "bookId": 11,
        "title": "Ram: Scion of Ikshvaku",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Fiction|Epic|Action",
        "themes": "Ram Chandra Series|Dharma|Ayodhya|Asura Raavan",
        "publication_year": 2015,
        "rating": 4.1,
        "cover_url": "/static/covers/11.jpg",
        "description": "Prince Ram struggles as a tortured, rule-bound prince of a weakened Ayodhya, striving to restore order and righteousness under the brutal economic blockade of Lanka's demon king Raavan."
    },
    {
        "bookId": 12,
        "title": "Sita: Warrior of Mithila",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Fiction|Action|Feminist Epic",
        "themes": "Warrior Sita|Vishnu Legacy|Martial Prowess|Governance",
        "publication_year": 2017,
        "rating": 4.3,
        "cover_url": "/static/covers/12.jpg",
        "description": "An abandoned infant found in a furrow grows to become the fierce prime minister and martial protector of Mithila, chosen as the next visionary Vishnu to deliver the subcontinent from darkness."
    },
    {
        "bookId": 13,
        "title": "Raavan: Enemy of Aryavarta",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Fiction|Dark Drama|Epic",
        "themes": "Raavan's Origin|Art & Rage|Tragedy|Lanka Empire",
        "publication_year": 2019,
        "rating": 4.4,
        "cover_url": "/static/covers/13.jpg",
        "description": "A complex psychological chronicle of Raavan, a brilliant artist, fearsome warrior, and ruthless pirate king pushed into monstrous vengeance by personal grief and societal cruelty."
    },
    {
        "bookId": 14,
        "title": "War of Lanka",
        "author": "Amish Tripathi",
        "origin": "Indian",
        "genres": "Mythological Fiction|Epic War|Strategy",
        "themes": "Battle of Lanka|Vayuputras|Dharma|Honor",
        "publication_year": 2022,
        "rating": 4.2,
        "cover_url": "/static/covers/14.jpg",
        "description": "Following Sita's abduction, Ram, Lakshman, and the fierce army of Kishkindha march onto Lanka for an apocalyptic war of strategy, cosmic weapons, and supreme devotion."
    },
    {
        "bookId": 15,
        "title": "Five Point Someone",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Contemporary Fiction|Humor|Campus Life",
        "themes": "IIT Delhi|Academic Pressure|Friendship|Underdogs",
        "publication_year": 2004,
        "rating": 4.0,
        "cover_url": "/static/covers/15.jpg",
        "description": "Three engineering undergraduates at IIT Delhi struggle to survive extreme academic competition, tyrannical professors, and a low GPA (five point something) while seeking their true callings."
    },
    {
        "bookId": 16,
        "title": "2 States: The Story of My Marriage",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Romance|Humor|Contemporary",
        "themes": "Inter-Community Marriage|Punjabi vs Tamil|Family Expectations|IIM Ahmedabad",
        "publication_year": 2009,
        "rating": 3.9,
        "cover_url": "/static/covers/16.jpg",
        "description": "Krish from Punjab and Ananya from Tamil Nadu fall in love at IIM Ahmedabad, but must navigate conservative families, cultural stereotypes, and quirky parents to win mutual approval."
    },
    {
        "bookId": 17,
        "title": "The 3 Mistakes of My Life",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Drama|Cricket|Contemporary",
        "themes": "Ahmedabad|Cricket Talent|Earthquake & Riots|Ambition",
        "publication_year": 2008,
        "rating": 3.8,
        "cover_url": "/static/covers/17.jpg",
        "description": "Set in early 2000s Gujarat, three young friends open a cricket equipment shop and coach a prodigy, until religious tensions and natural disasters put their bonds to the ultimate trial."
    },
    {
        "bookId": 18,
        "title": "Half Girlfriend",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Romance|Drama|Young Adult",
        "themes": "Language Barrier|Bihari Youth|Delhi Elite|Unrequited Love",
        "publication_year": 2014,
        "rating": 3.6,
        "cover_url": "/static/covers/18.jpg",
        "description": "Madhav, a Hindi-medium boy from rural Bihar, falls in love with Riya, a wealthy Delhi socialite who agrees to be his 'half girlfriend' amidst class and language insecurities."
    },
    {
        "bookId": 19,
        "title": "One Indian Girl",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Contemporary Fiction|Romance|Feminism",
        "themes": "Modern Women|Wall Street|Gender Double Standards|Goa Wedding",
        "publication_year": 2016,
        "rating": 3.7,
        "cover_url": "/static/covers/19.jpg",
        "description": "Radhika Chetan is an ambitious Goldman Sachs banker making lots of money, but finds Indian society still judges her past relationships and independence before her Goa wedding."
    },
    {
        "bookId": 20,
        "title": "Revolution 2020",
        "author": "Chetan Bhagat",
        "origin": "Indian",
        "genres": "Drama|Crime|Youth Politics",
        "themes": "Varanasi|Engineering Coaching Scandals|Love Triangle|Corruption",
        "publication_year": 2011,
        "rating": 3.8,
        "cover_url": "/static/covers/20.jpg",
        "description": "In the ancient city of Varanasi, childhood friends Gopal, Raghav, and Aarti navigate ambition, coaching mafia corruption, political power, and a heart-wrenching love triangle."
    },
    {
        "bookId": 21,
        "title": "The Guide",
        "author": "R.K. Narayan",
        "origin": "Indian",
        "genres": "Literary Classic|Drama|Philosophical",
        "themes": "Malgudi|Spiritual Transformation|Fasting & Sacrifice|Raju",
        "publication_year": 1958,
        "rating": 4.3,
        "cover_url": "/static/covers/21.jpg",
        "description": "Raju, a corrupt and flamboyant tourist guide in Malgudi, finds himself mistakenly elevated to the status of a holy spiritual saint, forced into a fatal sacrificial fast to end a drought."
    },
    {
        "bookId": 22,
        "title": "Malgudi Days",
        "author": "R.K. Narayan",
        "origin": "Indian",
        "genres": "Short Stories|Classic|Slice of Life",
        "themes": "Malgudi Town|Everyday Human Nature|Innocence|Simplicity",
        "publication_year": 1943,
        "rating": 4.5,
        "cover_url": "/static/covers/22.jpg",
        "description": "A delightful and heartwarming collection of short stories depicting the poignant, humorous, and timeless daily lives of ordinary residents in the fictional South Indian town of Malgudi."
    },
    {
        "bookId": 23,
        "title": "Swami and Friends",
        "author": "R.K. Narayan",
        "origin": "Indian",
        "genres": "Classic|Coming of Age|Humor",
        "themes": "Childhood Adventures|School Truancy|Malgudi Cricket Club|Colonial India",
        "publication_year": 1935,
        "rating": 4.4,
        "cover_url": "/static/covers/23.jpg",
        "description": "Ten-year-old schoolboy Swaminathan and his friends navigate the joys of cricket, school misadventures, and the turbulent waves of freedom protests in British-ruled India."
    },
    {
        "bookId": 24,
        "title": "The English Teacher",
        "author": "R.K. Narayan",
        "origin": "Indian",
        "genres": "Classic|Drama|Spiritual",
        "themes": "Love & Grief|Grief Transcendence|Teaching|Inner Peace",
        "publication_year": 1945,
        "rating": 4.2,
        "cover_url": "/static/covers/24.jpg",
        "description": "A college English lecturer in Malgudi experiences the devastating grief of his beloved young wife's sudden death from typhoid, leading him to communicate with her spirit."
    },
    {
        "bookId": 25,
        "title": "The Shadow Lines",
        "author": "Amitav Ghosh",
        "origin": "Indian",
        "genres": "Literary Fiction|Historical|Post-Colonial",
        "themes": "Dhaka & Calcutta Riots|Borders & Maps|Memory|Nationalism",
        "publication_year": 1988,
        "rating": 4.1,
        "cover_url": "/static/covers/25.jpg",
        "description": "A lyrical meditation weaving memories across Calcutta, Dhaka, and WWII London, exploring how arbitrary political borders (shadow lines) fail to divide human connections and trauma."
    },
    {
        "bookId": 26,
        "title": "Sea of Poppies",
        "author": "Amitav Ghosh",
        "origin": "Indian",
        "genres": "Historical Epic|Adventure|Literary",
        "themes": "Ibis Trilogy|Opium Wars|Indentured Laborers|Ganges",
        "publication_year": 2008,
        "rating": 4.2,
        "cover_url": "/static/covers/26.jpg",
        "description": "On the eve of the 19th-century Opium Wars, a former slave ship, the Ibis, gathers an eclectic crew of bankrupt rajahs, indentured coolies, and outcasts sailing across the Indian Ocean."
    },
    {
        "bookId": 27,
        "title": "The Glass Palace",
        "author": "Amitav Ghosh",
        "origin": "Indian",
        "genres": "Historical Saga|Epic|War",
        "themes": "Burma & Malaya|Teak Trade|Colonialism|Exiled Royals",
        "publication_year": 2000,
        "rating": 4.3,
        "cover_url": "/static/covers/27.jpg",
        "description": "Spanning three generations from the British fall of the Burmese Konbaung Dynasty in Mandalay to WWII Malaya, tracing an orphan boy's empire in the lucrative teak and rubber trade."
    },
    {
        "bookId": 28,
        "title": "The Hungry Tide",
        "author": "Amitav Ghosh",
        "origin": "Indian",
        "genres": "Literary Fiction|Eco-Fiction|Mystery",
        "themes": "Sundarbans Mangroves|River Dolphins|Human vs Nature|Morichjhanpi",
        "publication_year": 2004,
        "rating": 4.2,
        "cover_url": "/static/covers/28.jpg",
        "description": "In the perilous labyrinth of tidal islands in the Sundarbans, a cetologist and an illiterate fisherman forge an unlikely bond while tracking endangered river dolphins."
    },
    {
        "bookId": 29,
        "title": "Gun Island",
        "author": "Amitav Ghosh",
        "origin": "Indian",
        "genres": "Speculative Fiction|Climate Fiction|Mystery",
        "themes": "Climate Change|Bengali Folklore|Bonduki Sadagar|Venice Migrations",
        "publication_year": 2019,
        "rating": 3.9,
        "cover_url": "/static/covers/29.jpg",
        "description": "Rare books dealer Deen Datta investigates an ancient 17th-century Bengali myth of the Gun Merchant, unraveling global climate displacement from the Sundarbans to Venice."
    },
    {
        "bookId": 30,
        "title": "The Inheritance of Loss",
        "author": "Kiran Desai",
        "origin": "Indian",
        "genres": "Literary Fiction|Drama|Post-Colonial",
        "themes": "Kalimpong|Gorkhaland Agitation|Immigration in NYC|Man Booker Winner",
        "publication_year": 2006,
        "rating": 4.0,
        "cover_url": "/static/covers/30.jpg",
        "description": "Set in a decaying mansion in the Himalayan foothills of Kalimpong during the Gorkha insurgency, juxtaposed with the harsh immigrant underground in New York City."
    },
    {
        "bookId": 31,
        "title": "Hullabaloo in the Guava Orchard",
        "author": "Kiran Desai",
        "origin": "Indian",
        "genres": "Humor|Satire|Magical Realism",
        "themes": "Tree Guru|Indian Bureaucracy|Monkeys|Eccentricity",
        "publication_year": 1998,
        "rating": 3.8,
        "cover_url": "/static/covers/31.jpg",
        "description": "Sampath Chawla escapes his nagging family and tedious post office job by climbing a high guava tree, where townspeople soon mistake his overheard gossip for divine prophecy."
    },
    {
        "bookId": 32,
        "title": "The Namesake",
        "author": "Jhumpa Lahiri",
        "origin": "Indian",
        "genres": "Literary Fiction|Drama|Immigrant Experience",
        "themes": "Gogol Ganguli|Bengali Diaspora|Identity Crisis|Boston to Calcutta",
        "publication_year": 2003,
        "rating": 4.4,
        "cover_url": "/static/covers/32.jpg",
        "description": "Gogol Ganguli struggles with the bizarre Russian author namesake chosen by his Bengali immigrant parents, striving to forge his own identity between traditional roots and modern America."
    },
    {
        "bookId": 33,
        "title": "Interpreter of Maladies",
        "author": "Jhumpa Lahiri",
        "origin": "Indian",
        "genres": "Short Stories|Literary|Drama",
        "themes": "Pulitzer Prize|Exile|Cultural Alienation|Marital Disconnect",
        "publication_year": 1999,
        "rating": 4.5,
        "cover_url": "/static/covers/33.jpg",
        "description": "Nine deeply empathetic short stories capturing the quiet longings, misunderstandings, and cultural rifts experienced by Indians and Indian Americans navigating new lands."
    },
    {
        "bookId": 34,
        "title": "The Lowland",
        "author": "Jhumpa Lahiri",
        "origin": "Indian",
        "genres": "Literary Fiction|Historical|Family Drama",
        "themes": "Naxalite Movement|Calcutta Brothers|Sacrifice|Rhode Island",
        "publication_year": 2013,
        "rating": 4.1,
        "cover_url": "/static/covers/34.jpg",
        "description": "Two inseparable Calcutta brothers take radically divergent paths in the 1960s: Subhash heads to quiet research in America while Udayan plunges into the violent Naxalite rebellion."
    },
    {
        "bookId": 35,
        "title": "Unaccustomed Earth",
        "author": "Jhumpa Lahiri",
        "origin": "Indian",
        "genres": "Short Stories|Literary|Drama",
        "themes": "Generational Shifts|Love & Loss|Bengali Heritage|Belonging",
        "publication_year": 2008,
        "rating": 4.3,
        "cover_url": "/static/covers/35.jpg",
        "description": "Luminous, emotionally rich stories exploring how subsequent generations of immigrants transform their relationships, grapple with secrets, and seek roots on unaccustomed earth."
    },
    {
        "bookId": 36,
        "title": "The Rozabal Line",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Conspiracy Thriller|Historical Mystery|Religious Fiction",
        "themes": "Jesus in Kashmir|Secret Societies|Cryptology|Kashmir Shrine",
        "publication_year": 2007,
        "rating": 4.1,
        "cover_url": "/static/covers/36.jpg",
        "description": "A heart-pounding Da Vinci Code-style thriller investigating the provocative conspiracy that Jesus survived the crucifixion and lies buried at the Rozabal shrine in Srinagar."
    },
    {
        "bookId": 37,
        "title": "Chanakya's Chant",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Historical Thriller|Political Fiction|Mystery",
        "themes": "Chanakya & Chandragupta|Modern Political Kingmaker|Chanakya Neeti",
        "publication_year": 2010,
        "rating": 4.3,
        "cover_url": "/static/covers/37.jpg",
        "description": "Two parallel narratives 2,300 years apart: ancient master strategist Chanakya uniting fractured kingdoms, and modern Brahmin Pandit Gangasagar maneuvering a slum girl into the Prime Minister's seat."
    },
    {
        "bookId": 38,
        "title": "The Krishna Key",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Mythological Thriller|Mystery|Crime",
        "themes": "Lord Krishna Artifacts|Somnath|Dwarka|Kalki Avatar Serial Killer",
        "publication_year": 2012,
        "rating": 4.2,
        "cover_url": "/static/covers/38.jpg",
        "description": "Historian Ravi Mohan Saini must decipher ancient Vedic puzzles and the submerged lost treasures of Dwarka to clear his name and stop a serial killer claiming to be Lord Krishna's final avatar."
    },
    {
        "bookId": 39,
        "title": "The Sialkot Saga",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Business Thriller|Historical Fiction|Crime",
        "themes": "Post-Partition Business|Post-1947 Mumbai & Calcutta|Ashoka Secrets",
        "publication_year": 2016,
        "rating": 4.3,
        "cover_url": "/static/covers/39.jpg",
        "description": "Two fierce business titans—one an underworld smuggler and the other a ruthless Wall Street corporate tycoon—clash over decades, unknowing that their fate is tied to Emperor Ashoka's secrets."
    },
    {
        "bookId": 40,
        "title": "Keepers of the Kalachakra",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Sci-Fi Thriller|Mythology|Quantum Physics",
        "themes": "Kalachakra Wheel|Quantum Dimension|Global Politics|Terror Plots",
        "publication_year": 2018,
        "rating": 4.1,
        "cover_url": "/static/covers/40.jpg",
        "description": "A high-octane blend of quantum physics, Tibetan Buddhist philosophy, and international geopolitics as an ex-soldier investigates assassinations driven by the mysterious wheel of time."
    },
    {
        "bookId": 41,
        "title": "The Vault of Vishnu",
        "author": "Ashwin Sanghi",
        "origin": "Indian",
        "genres": "Historical Thriller|Action|Mythology",
        "themes": "Bodhidharma|Shaolin Kung Fu|Pallava Dynasty|Indo-China Border",
        "publication_year": 2020,
        "rating": 4.2,
        "cover_url": "/static/covers/41.jpg",
        "description": "A secret investigator races along the ancient Buddhist trade routes of India, China, and Cambodia to discover how Bodhidharma's lost elixir connects to Chinese super-soldiers."
    },
    {
        "bookId": 42,
        "title": "Wise and Otherwise",
        "author": "Sudha Murty",
        "origin": "Indian",
        "genres": "Non-Fiction|Inspirational|Short Essays",
        "themes": "Human Values|Compassion|Rural India|Philanthropy",
        "publication_year": 2002,
        "rating": 4.6,
        "cover_url": "/static/covers/42.jpg",
        "description": "Fifty poignant true-life vignettes recorded by Sudha Murty during her travels across India as Infosys Foundation trustee, revealing human honesty, deceit, and selfless kindness."
    },
    {
        "bookId": 43,
        "title": "Three Thousand Stitches",
        "author": "Sudha Murty",
        "origin": "Indian",
        "genres": "Non-Fiction|Memoir|Social Work",
        "themes": "Devadasi Rehabilitation|Women Empowerment|Courage|True Stories",
        "publication_year": 2017,
        "rating": 4.6,
        "cover_url": "/static/covers/43.jpg",
        "description": "Heartening real stories recounting Murty's monumental mission to empower over 3,000 Devadasis in Karnataka, who stitched a celebratory bedspread for her as a token of gratitude."
    },
    {
        "bookId": 44,
        "title": "Mahashweta",
        "author": "Sudha Murty",
        "origin": "Indian",
        "genres": "Drama|Social Fiction|Women Empowerment",
        "themes": "Leukoderma (Vitiligo)|Stigma|Self-Respect|Second Chances",
        "publication_year": 2000,
        "rating": 4.4,
        "cover_url": "/static/covers/44.jpg",
        "description": "Anupama's fairy-tale marriage shatters when a small white patch of vitiligo appears on her skin. Abandoned by her husband, she rebuilds her life and self-worth as a Bombay lecturer."
    },
    {
        "bookId": 45,
        "title": "Dollar Bahu",
        "author": "Sudha Murty",
        "origin": "Indian",
        "genres": "Drama|Family Fiction|Contemporary",
        "themes": "Money vs Love|Mother-in-Law Expectations|NRI Dreams|Bangalore",
        "publication_year": 2003,
        "rating": 4.2,
        "cover_url": "/static/covers/45.jpg",
        "description": "Gouramma favors her US-dollar-earning daughter-in-law over her modest home-based one, until a journey to America reveals the cold superficiality of dollar-chasing materialism."
    },
    {
        "bookId": 46,
        "title": "Grandma's Bag of Stories",
        "author": "Sudha Murty",
        "origin": "Indian",
        "genres": "Children's Literature|Folk Tales|Fables",
        "themes": "Bedtime Tales|Moral Wisdom|Grandmother Love|Indian Folklore",
        "publication_year": 2015,
        "rating": 4.7,
        "cover_url": "/static/covers/46.jpg",
        "description": "Enchanting traditional fables and moral stories told by Ajji to her grandchildren visiting her village during summer vacations, filled with clever kings, loyal animals, and magical pots."
    },
    {
        "bookId": 47,
        "title": "Gitanjali",
        "author": "Rabindranath Tagore",
        "origin": "Indian",
        "genres": "Poetry|Spiritual|Classic",
        "themes": "Nobel Prize 1913|Song Offerings|Devotion|Nature & Soul",
        "publication_year": 1910,
        "rating": 4.6,
        "cover_url": "/static/covers/47.jpg",
        "description": "The immortal Nobel Prize-winning collection of devotional poems and spiritual song offerings exploring divine love, inner solitude, and the soul's union with nature."
    },
    {
        "bookId": 48,
        "title": "The Home and the World",
        "author": "Rabindranath Tagore",
        "origin": "Indian",
        "genres": "Classic|Political Fiction|Drama",
        "themes": "Swadeshi Movement|Nationalism vs Morality|Bimala|Bengal 1905",
        "publication_year": 1916,
        "rating": 4.3,
        "cover_url": "/static/covers/48.jpg",
        "description": "Set during Bengal's 1905 Partition, gentle landlord Nikhil and fiery nationalist Sandip present starkly conflicting visions of life and patriotism to Nikhil's sequestered wife, Bimala."
    },
    {
        "bookId": 49,
        "title": "Chokher Bali",
        "author": "Rabindranath Tagore",
        "origin": "Indian",
        "genres": "Classic|Psychological Drama|Romance",
        "themes": "Binodini|Widowhood Constraints|Passion & Betrayal|Bengal Aristocracy",
        "publication_year": 1903,
        "rating": 4.3,
        "cover_url": "/static/covers/49.jpg",
        "description": "Binodini, an educated and fiercely intelligent young widow, is taken into an affluent Kolkata household where repressed passion and jealousy unravel conventional family bonds."
    },
    {
        "bookId": 50,
        "title": "Godan",
        "author": "Munshi Premchand",
        "origin": "Indian",
        "genres": "Hindi Literature Classic|Social Realism|Drama",
        "themes": "Hori & Dhania|Cow as Salvation|Peasant Exploitation|Zamidari System",
        "publication_year": 1936,
        "rating": 4.7,
        "cover_url": "/static/covers/50.jpg",
        "description": "The quintessential masterpiece of modern Hindi literature depicting poor peasant Hori Mahato's lifelong dream to own a cow, battling corrupt moneylenders, landlords, and caste dogma."
    },
    {
        "bookId": 51,
        "title": "Nirmala",
        "author": "Munshi Premchand",
        "origin": "Indian",
        "genres": "Social Realism|Tragedy|Classic",
        "themes": "Dowry Evil|Mismatch Marriage|Woman's Plight|Sacrifice",
        "publication_year": 1927,
        "rating": 4.5,
        "cover_url": "/static/covers/51.jpg",
        "description": "A heart-wrenching exposé of the Indian dowry system following Nirmala, a vibrant teenage girl married off to an elderly widower, whose suspicious jealousy causes tragic ruin."
    },
    {
        "bookId": 52,
        "title": "Karmabhoomi",
        "author": "Munshi Premchand",
        "origin": "Indian",
        "genres": "Classic|Social Realism|Political",
        "themes": "Peasant Struggles|Untouchability|Gandhian Idealism|Freedom Movement",
        "publication_year": 1932,
        "rating": 4.4,
        "cover_url": "/static/covers/52.jpg",
        "description": "A powerful Gandhian social epic chronicling non-violent uprisings of oppressed farmers and Dalits against ruthless British land revenue systems and orthodoxy in 1930s Uttar Pradesh."
    },
    {
        "bookId": 53,
        "title": "Gaban",
        "author": "Munshi Premchand",
        "origin": "Indian",
        "genres": "Social Realism|Moral Fiction|Classic",
        "themes": "Embezzlement|Jewelry Obsession|Ramanath & Jalpa|Conscience",
        "publication_year": 1931,
        "rating": 4.5,
        "cover_url": "/static/covers/53.jpg",
        "description": "Young Ramanath's reckless desire to buy exquisite gold jewelry for his bride leads him into government embezzlement, deceit, police blackmail, and a long journey toward redemption."
    },
    {
        "bookId": 54,
        "title": "The Discovery of India",
        "author": "Jawaharlal Nehru",
        "origin": "Indian",
        "genres": "Non-Fiction|History|Philosophy",
        "themes": "Ahmednagar Fort|Indian Civilisation|Vedas to Independence|Unity in Diversity",
        "publication_year": 1946,
        "rating": 4.5,
        "cover_url": "/static/covers/54.jpg",
        "description": "Penned during Nehru's imprisonment in Ahmednagar Fort (1942–1946), an epic intellectual journey through 5,000 years of India's cultural, artistic, and philosophical heritage."
    },
    {
        "bookId": 55,
        "title": "Wings of Fire",
        "author": "A.P.J. Abdul Kalam",
        "origin": "Indian",
        "genres": "Autobiography|Inspirational|Science",
        "themes": "Missile Man of India|Rameswaram to ISRO|SLV-3 & Agni|Youth Dreams",
        "publication_year": 1999,
        "rating": 4.8,
        "cover_url": "/static/covers/55.jpg",
        "description": "Dr. Kalam's uplifting journey from selling newspapers in temple town Rameswaram to leading India's groundbreaking satellite and missile programs and the Pokhran-II tests."
    },
    {
        "bookId": 56,
        "title": "Ignited Minds",
        "author": "A.P.J. Abdul Kalam",
        "origin": "Indian",
        "genres": "Non-Fiction|Inspirational|Youth Vision",
        "themes": "Empowering Youth|Developed India|Scientific Temperament|National Vision",
        "publication_year": 2002,
        "rating": 4.6,
        "cover_url": "/static/covers/56.jpg",
        "description": "Dr. Kalam urges Indian students and citizens to unleash the dormant power within themselves to transform India into an economically and scientifically developed nation."
    },
    {
        "bookId": 57,
        "title": "India 2020: A Vision for the New Millennium",
        "author": "A.P.J. Abdul Kalam",
        "origin": "Indian",
        "genres": "Non-Fiction|Strategy|Development",
        "themes": "Technology Blueprint|Agriculture|Healthcare & Energy|Future India",
        "publication_year": 1998,
        "rating": 4.5,
        "cover_url": "/static/covers/57.jpg",
        "description": "A comprehensive technological and socio-economic roadmap by Dr. Kalam and Y.S. Rajan for transforming India into one of the top five economic superpowers by 2020."
    },
    {
        "bookId": 58,
        "title": "The Great Indian Novel",
        "author": "Shashi Tharoor",
        "origin": "Indian",
        "genres": "Satire|Historical Fiction|Political",
        "themes": "Mahabharata Parallel|Indian Independence|Nehru & Gandhi|Puns & Wit",
        "publication_year": 1989,
        "rating": 4.2,
        "cover_url": "/static/covers/58.jpg",
        "description": "A masterfully witty satirical work mapping major characters and events of the Mahabharata onto 20th-century Indian history, from the British Raj through the Emergency."
    },
    {
        "bookId": 59,
        "title": "An Era of Darkness: The British Empire in India",
        "author": "Shashi Tharoor",
        "origin": "Indian",
        "genres": "Non-Fiction|History|Post-Colonial",
        "themes": "Colonial Exploitation|Loot of Indian Wealth|Famines|Railways Reality",
        "publication_year": 2016,
        "rating": 4.5,
        "cover_url": "/static/covers/59.jpg",
        "description": "A scathing, meticulously researched historical indictment dismantling the myth of benevolent British rule, detailing economic decimation, deindustrialization, and induced famines."
    },
    {
        "bookId": 60,
        "title": "Why I Am a Hindu",
        "author": "Shashi Tharoor",
        "origin": "Indian",
        "genres": "Non-Fiction|Philosophy|Religion",
        "themes": "Hinduism Essence|Tolerance & Inclusivity|Swami Vivekananda|Pluralism",
        "publication_year": 2018,
        "rating": 4.2,
        "cover_url": "/static/covers/60.jpg",
        "description": "An eloquent exploration of the profound philosophical roots and pluralistic traditions of Hinduism, contrasted against intolerant and dogmatic political distortions."
    },

    # =========================================================================
    # 40 BOOKS BY INTERNATIONAL / OUTSIDER WRITERS (IDs 61 - 100)
    # =========================================================================
    {
        "bookId": 61,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "origin": "International",
        "genres": "Classic|Legal Drama|Coming of Age",
        "themes": "Racial Injustice|Atticus Finch|Scout|Empathy & Integrity",
        "publication_year": 1960,
        "rating": 4.7,
        "cover_url": "/static/covers/61.jpg",
        "description": "In 1930s Alabama, upright lawyer Atticus Finch defends Tom Robinson, a Black man falsely accused of raping a white woman, seen through his young daughter Scout's eyes."
    },
    {
        "bookId": 62,
        "title": "1984",
        "author": "George Orwell",
        "origin": "International",
        "genres": "Dystopian|Sci-Fi|Political Fiction",
        "themes": "Big Brother|Totalitarianism|Thoughtcrime|Surveillance State",
        "publication_year": 1949,
        "rating": 4.8,
        "cover_url": "/static/covers/62.jpg",
        "description": "Winston Smith lives in totalitarian Oceania under the omnipresent gaze of Big Brother, rebelling in secret against mind control, rewritten history, and doublethink."
    },
    {
        "bookId": 63,
        "title": "Animal Farm",
        "author": "George Orwell",
        "origin": "International",
        "genres": "Political Satire|Allegory|Classic",
        "themes": "Soviet Revolution|Napoleon the Pig|Corruption of Power|Tyranny",
        "publication_year": 1945,
        "rating": 4.6,
        "cover_url": "/static/covers/63.jpg",
        "description": "Oppressed farm animals overthrow their human master to establish an egalitarian society, only for the cunning pigs under Napoleon to install an even more brutal totalitarian dictatorship."
    },
    {
        "bookId": 64,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "origin": "International",
        "genres": "Classic Romance|Social Satire|Drama",
        "themes": "Elizabeth Bennet & Mr. Darcy|Social Class|First Impressions|Wit",
        "publication_year": 1813,
        "rating": 4.7,
        "cover_url": "/static/covers/64.jpg",
        "description": "The spirited Elizabeth Bennet and proud aristocratic Fitzwilliam Darcy must overcome initial misunderstandings and social differences to discover mutual affection and respect."
    },
    {
        "bookId": 65,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "origin": "International",
        "genres": "Classic|Tragedy|Literary Fiction",
        "themes": "American Dream|Jay Gatsby|Roaring Twenties|Unrequited Obsession",
        "publication_year": 1925,
        "rating": 4.4,
        "cover_url": "/static/covers/65.jpg",
        "description": "Narrated by Nick Carraway, mysterious millionaire Jay Gatsby throws lavish parties in Long Island to win back his lost aristocratic love, Daisy Buchanan, ending in tragedy."
    },
    {
        "bookId": 66,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "origin": "International",
        "genres": "Coming of Age|Classic|Psychological",
        "themes": "Holden Caulfield|Phoniness|Teen Alienation|New York City",
        "publication_year": 1951,
        "rating": 4.1,
        "cover_url": "/static/covers/66.jpg",
        "description": "Expelled from prep school, cynical teenager Holden Caulfield spends three wandering days in New York City railing against adult hypocrisy while struggling with grief and isolation."
    },
    {
        "bookId": 67,
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "author": "J.R.R. Tolkien",
        "origin": "International",
        "genres": "High Fantasy|Epic Adventure|Classic",
        "themes": "One Ring|Frodo Baggins|Middle-earth|Friendship & Courage",
        "publication_year": 1954,
        "rating": 4.8,
        "cover_url": "/static/covers/67.jpg",
        "description": "Hobbit Frodo Baggins inherits the master Ring of Power and sets out on a perilous quest with a fellowship of men, elves, dwarves, and wizards to cast it into Mount Doom."
    },
    {
        "bookId": 68,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "origin": "International",
        "genres": "Fantasy|Adventure|Classic",
        "themes": "Bilbo Baggins|Smaug the Dragon|Erebor|Mithril & Riddles",
        "publication_year": 1937,
        "rating": 4.7,
        "cover_url": "/static/covers/68.jpg",
        "description": "Home-loving hobbit Bilbo Baggins is swept into an epic adventure by the wizard Gandalf and thirteen dwarves to reclaim the Lonely Mountain and its gold from the dragon Smaug."
    },
    {
        "bookId": 69,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "origin": "International",
        "genres": "Fantasy|Magic|Young Adult",
        "themes": "Hogwarts|The Boy Who Lived|Voldemort|Friendship",
        "publication_year": 1997,
        "rating": 4.8,
        "cover_url": "/static/covers/69.jpg",
        "description": "On his eleventh birthday, orphan Harry Potter discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry, uncovering secrets of his parents and Lord Voldemort."
    },
    {
        "bookId": 70,
        "title": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "origin": "International",
        "genres": "Fantasy|Mystery|Adventure",
        "themes": "Sirius Black|Dementors|Marauder's Map|Time Turner",
        "publication_year": 1999,
        "rating": 4.8,
        "cover_url": "/static/covers/70.jpg",
        "description": "Harry's third year at Hogwarts is shadowed by escapee Sirius Black, soul-sucking Dementors guarding the castle, and deep revelations about his father's loyal circle."
    },
    {
        "bookId": 71,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "origin": "International",
        "genres": "Philosophical Fiction|Fable|Inspirational",
        "themes": "Personal Legend|Santiago the Shepherd|Egyptian Pyramids|Destiny",
        "publication_year": 1988,
        "rating": 4.7,
        "cover_url": "/static/covers/71.jpg",
        "description": "Andalusian shepherd boy Santiago journeys across the Moroccan desert to Egypt in search of worldly treasure, learning that true alchemy lies in pursuing one's Personal Legend."
    },
    {
        "bookId": 72,
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel García Márquez",
        "origin": "International",
        "genres": "Magical Realism|Literary Epic|Family Saga",
        "themes": "Buendía Family|Macondo Town|Generational Cycles|Nobel Laureate",
        "publication_year": 1967,
        "rating": 4.6,
        "cover_url": "/static/covers/72.jpg",
        "description": "The multi-generational saga of the Buendía family in the mythical Colombian town of Macondo, weaving miraculous wonders and tragic civil strife into timeless magical realism."
    },
    {
        "bookId": 73,
        "title": "Love in the Time of Cholera",
        "author": "Gabriel García Márquez",
        "origin": "International",
        "genres": "Romance|Literary Fiction|Drama",
        "themes": "Florentino Ariza & Fermina Daza|Enduring Love|Old Age|Caribbean",
        "publication_year": 1985,
        "rating": 4.4,
        "cover_url": "/static/covers/73.jpg",
        "description": "Florentino Ariza waits fifty-one years, nine months, and four days for his childhood beloved Fermina Daza, rekindling their passion in old age aboard a river steamship."
    },
    {
        "bookId": 74,
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "origin": "International",
        "genres": "Psychological Thriller|Philosophical Classic|Crime",
        "themes": "Raskolnikov|Guilt & Conscience|Pawnbroker Murder|Redemption",
        "publication_year": 1866,
        "rating": 4.7,
        "cover_url": "/static/covers/74.jpg",
        "description": "Impoverished student Raskolnikov murders an elderly pawnbroker to test his theory of extraordinary men, but is consumed by mental anguish, police suspicion, and moral torment."
    },
    {
        "bookId": 75,
        "title": "The Brothers Karamazov",
        "author": "Fyodor Dostoevsky",
        "origin": "International",
        "genres": "Philosophical Novel|Mystery|Classic",
        "themes": "Patricide|Faith vs Doubt|Grand Inquisitor|Free Will",
        "publication_year": 1880,
        "rating": 4.8,
        "cover_url": "/static/covers/75.jpg",
        "description": "A profound theological and psychological drama centered on the murder of a vulgar landowner and the distinct passions, moral crises, and courtroom trials of his three sons."
    },
    {
        "bookId": 76,
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "origin": "International",
        "genres": "Historical Epic|War Drama|Classic",
        "themes": "Napoleonic Invasion of Russia 1812|Pierre Bezukhov|Natasha Rostova|Destiny",
        "publication_year": 1869,
        "rating": 4.6,
        "cover_url": "/static/covers/76.jpg",
        "description": "A monumental panorama of Russian aristocratic society and military battles during Napoleon's 1812 invasion of Russia, tracing the personal evolution of Pierre, Andrei, and Natasha."
    },
    {
        "bookId": 77,
        "title": "Anna Karenina",
        "author": "Leo Tolstoy",
        "origin": "International",
        "genres": "Classic Romance|Tragedy|Drama",
        "themes": "Anna & Count Vronsky|Adultery|Russian High Society|Levin's Faith",
        "publication_year": 1878,
        "rating": 4.5,
        "cover_url": "/static/covers/77.jpg",
        "description": "St. Petersburg aristocrat Anna Karenina enters a scandalous extramarital romance with Count Vronsky, confronting societal hypocrisy and emotional tragedy."
    },
    {
        "bookId": 78,
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "origin": "International",
        "genres": "Mystery Thriller|Conspiracy|Action",
        "themes": "Robert Langdon|Louvre Murder|Holy Grail|Priory of Sion",
        "publication_year": 2003,
        "rating": 4.5,
        "cover_url": "/static/covers/78.jpg",
        "description": "Symbologist Robert Langdon and cryptologist Sophie Neveu unravel hidden codes in Leonardo da Vinci's artworks to expose a secret church conspiracy shielding the Holy Grail."
    },
    {
        "bookId": 79,
        "title": "Angels & Demons",
        "author": "Dan Brown",
        "origin": "International",
        "genres": "Mystery Thriller|Action|Suspense",
        "themes": "Illuminati|Antimatter Bomb|Vatican Conclave|CERN",
        "publication_year": 2000,
        "rating": 4.4,
        "cover_url": "/static/covers/79.jpg",
        "description": "Robert Langdon races through Rome's secret altars of science to foil an ancient Illuminati plot to annihilate Vatican City with a stolen canister of CERN antimatter."
    },
    {
        "bookId": 80,
        "title": "Inferno",
        "author": "Dan Brown",
        "origin": "International",
        "genres": "Mystery Thriller|Action|Sci-Fi",
        "themes": "Dante's Inferno|Overpopulation Plague|Florence|Transhumanism",
        "publication_year": 2013,
        "rating": 4.2,
        "cover_url": "/static/covers/80.jpg",
        "description": "Awakening with amnesia in a Florence hospital, Robert Langdon follows Dante's poetic verses across Venice and Istanbul to stop a brilliant geneticist's global plague."
    },
    {
        "bookId": 81,
        "title": "The Shining",
        "author": "Stephen King",
        "origin": "International",
        "genres": "Horror|Psychological Thriller|Supernatural",
        "themes": "Overlook Hotel|Jack Torrance|Isolation Madness|Danny's Shining",
        "publication_year": 1977,
        "rating": 4.6,
        "cover_url": "/static/covers/81.jpg",
        "description": "Jack Torrance takes a winter caretaking post at the snowbound Overlook Hotel with his wife and telepathic son, where sinister supernatural entities drive him into homicidal madness."
    },
    {
        "bookId": 82,
        "title": "It",
        "author": "Stephen King",
        "origin": "International",
        "genres": "Horror|Supernatural|Dark Fantasy",
        "themes": "Pennywise the Dancing Clown|Derry Maine|Losers Club|Childhood Trauma",
        "publication_year": 1986,
        "rating": 4.5,
        "cover_url": "/static/covers/82.jpg",
        "description": "Seven outcast children in Derry, Maine confront a shape-shifting ancient evil entity feeding on children's terror, reuniting twenty-seven years later to destroy it forever."
    },
    {
        "bookId": 83,
        "title": "Misery",
        "author": "Stephen King",
        "origin": "International",
        "genres": "Psychological Thriller|Horror|Suspense",
        "themes": "Paul Sheldon|Annie Wilkes|Number One Fan|Imprisonment",
        "publication_year": 1987,
        "rating": 4.5,
        "cover_url": "/static/covers/83.jpg",
        "description": "Famous romance novelist Paul Sheldon crashes his car in a blizzard and is rescued by his deranged 'number one fan' Annie Wilkes, who holds him captive to rewrite her favorite heroine's death."
    },
    {
        "bookId": 84,
        "title": "Dune",
        "author": "Frank Herbert",
        "origin": "International",
        "genres": "Sci-Fi Epic|Space Opera|Adventure",
        "themes": "Desert Planet Arrakis|Melange Spice|Paul Atreides|Sandworms & Fremen",
        "publication_year": 1965,
        "rating": 4.8,
        "cover_url": "/static/covers/84.jpg",
        "description": "Young Paul Atreides is thrust into treacherous intergalactic political warfare on the desert planet Arrakis, leading the native Fremen in a holy war to control the universe's spice."
    },
    {
        "bookId": 85,
        "title": "Foundation",
        "author": "Isaac Asimov",
        "origin": "International",
        "genres": "Sci-Fi Classic|Space Opera|Speculative",
        "themes": "Hari Seldon|Psychohistory|Galactic Empire Collapse|Preserving Science",
        "publication_year": 1951,
        "rating": 4.7,
        "cover_url": "/static/covers/85.jpg",
        "description": "Mathematician Hari Seldon invents psychohistory to forecast the imminent collapse of the Galactic Empire, establishing a Foundation of scientists on Terminus to shorten the dark age."
    },
    {
        "bookId": 86,
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "origin": "International",
        "genres": "Dystopian|Sci-Fi Classic|Philosophical",
        "themes": "Soma Drug|Genetic Engineering|Conditioning|Loss of Individuality",
        "publication_year": 1932,
        "rating": 4.5,
        "cover_url": "/static/covers/86.jpg",
        "description": "A futuristic World State achieves artificial harmony through test-tube reproduction, psychological conditioning, and the euphoria drug Soma, until a wild 'Savage' enters."
    },
    {
        "bookId": 87,
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "origin": "International",
        "genres": "Contemporary Drama|Historical Fiction|Emotional",
        "themes": "Kabul Afghanistan|Amir & Hassan|Betrayal & Guilt|Redemption",
        "publication_year": 2003,
        "rating": 4.8,
        "cover_url": "/static/covers/87.jpg",
        "description": "Amir haunts himself with the cowardice that destroyed his boyhood bond with his loyal Hazara kite runner Hassan in 1970s Kabul, returning decades later under Taliban rule for redemption."
    },
    {
        "bookId": 88,
        "title": "A Thousand Splendid Suns",
        "author": "Khaled Hosseini",
        "origin": "International",
        "genres": "Contemporary Drama|Historical Fiction|Tragedy",
        "themes": "Mariam & Laila|Afghan Women's Resilience|Kabul War|Enduring Bond",
        "publication_year": 2007,
        "rating": 4.8,
        "cover_url": "/static/covers/88.jpg",
        "description": "Two Afghan women from different generations and backgrounds are married to the same abusive shoemaker in war-torn Kabul, forming an unbreakable sisterhood of love and sacrifice."
    },
    {
        "bookId": 89,
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "origin": "International",
        "genres": "Historical Fiction|WWII Drama|Young Adult",
        "themes": "Narrated by Death|Nazi Germany|Liesel Meminger|Power of Words",
        "publication_year": 2005,
        "rating": 4.7,
        "cover_url": "/static/covers/89.jpg",
        "description": "Narrated by Death, young foster girl Liesel Meminger steals books in Nazi Germany, sharing stories with neighbors and the Jewish fist-fighter hidden in her basement."
    },
    {
        "bookId": 90,
        "title": "Atomic Habits",
        "author": "James Clear",
        "origin": "International",
        "genres": "Self-Help|Psychology|Productivity",
        "themes": "1% Better Every Day|Habit Loop|Systems over Goals|Identity Change",
        "publication_year": 2018,
        "rating": 4.8,
        "cover_url": "/static/covers/90.jpg",
        "description": "A practical framework on how tiny 1% daily behavior changes compound into remarkable life results by redesigning your environment and aligning habits with identity."
    },
    {
        "bookId": 91,
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "origin": "International",
        "genres": "Non-Fiction|Anthropology|History",
        "themes": "Cognitive Revolution|Agricultural Revolution|Fictional Stories|Homo Sapiens",
        "publication_year": 2011,
        "rating": 4.7,
        "cover_url": "/static/covers/91.jpg",
        "description": "A sweeping, provocative chronicle examining how an insignificant ape on the savanna became the master of Earth through shared fictions like money, religion, and nations."
    },
    {
        "bookId": 92,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "origin": "International",
        "genres": "Psychology|Behavioral Economics|Science",
        "themes": "System 1 & System 2|Cognitive Biases|Heuristics|Decision Making",
        "publication_year": 2011,
        "rating": 4.6,
        "cover_url": "/static/covers/92.jpg",
        "description": "Nobel laureate Daniel Kahneman explains the two minds that drive our thinking: fast, instinctive System 1, and slow, logical, deliberative System 2."
    },
    {
        "bookId": 93,
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "origin": "International",
        "genres": "Personal Finance|Psychology|Business",
        "themes": "Wealth vs Rich|Behavior over Formulas|Compounding|Financial Peace",
        "publication_year": 2020,
        "rating": 4.7,
        "cover_url": "/static/covers/93.jpg",
        "description": "Nineteen captivating short stories exploring the weird behavioral quirks and psychological biases that dictate how humans manage, invest, and think about money."
    },
    {
        "bookId": 94,
        "title": "Rich Dad Poor Dad",
        "author": "Robert T. Kiyosaki",
        "origin": "International",
        "genres": "Personal Finance|Investing|Self-Help",
        "themes": "Assets vs Liabilities|Financial Literacy|Cash Flow|Entrepreneurship",
        "publication_year": 1997,
        "rating": 4.5,
        "cover_url": "/static/covers/94.jpg",
        "description": "Contrasting life philosophies between Kiyosaki's highly educated but struggling 'poor dad' and his best friend's entrepreneurial 'rich dad' on creating financial freedom."
    },
    {
        "bookId": 95,
        "title": "Deep Work",
        "author": "Cal Newport",
        "origin": "International",
        "genres": "Productivity|Self-Help|Psychology",
        "themes": "Distraction-Free Focus|Shallow Work Trap|Elite Output|Digital Minimalism",
        "publication_year": 2016,
        "rating": 4.6,
        "cover_url": "/static/covers/95.jpg",
        "description": "Computer science professor Cal Newport argues that the superpower of the modern knowledge economy is the rare ability to concentrate without distraction on cognitively demanding tasks."
    },
    {
        "bookId": 96,
        "title": "Norwegian Wood",
        "author": "Haruki Murakami",
        "origin": "International",
        "genres": "Literary Fiction|Romance|Coming of Age",
        "themes": "Toru Watanabe|Tokyo 1960s|Grief & Loss|Naoko & Midori",
        "publication_year": 1987,
        "rating": 4.4,
        "cover_url": "/static/covers/96.jpg",
        "description": "Toru Watanabe reminisces about his 1960s college days in Tokyo, torn between the fragile, grief-stricken Naoko and the vibrant, vivacious Midori."
    },
    {
        "bookId": 97,
        "title": "Kafka on the Shore",
        "author": "Haruki Murakami",
        "origin": "International",
        "genres": "Magical Realism|Surreal Fiction|Mystery",
        "themes": "Kafka Tamura|Nakata the Cat Talker|Fish Rains|Parallel Realities",
        "publication_year": 2002,
        "rating": 4.5,
        "cover_url": "/static/covers/97.jpg",
        "description": "Fifteen-year-old runaway Kafka Tamura escapes an Oedipal curse, while an eccentric elderly man who talks to cats embarks on a surreal parallel quest across Japan."
    },
    {
        "bookId": 98,
        "title": "The Metamorphosis",
        "author": "Franz Kafka",
        "origin": "International",
        "genres": "Classic|Existential Fiction|Surrealism",
        "themes": "Gregor Samsa|Giant Insect|Alienation|Family Burdens",
        "publication_year": 1915,
        "rating": 4.3,
        "cover_url": "/static/covers/98.jpg",
        "description": "Traveling salesman Gregor Samsa wakes up one morning transformed into a monstrous verminous insect, leading his dependent family through shock, revulsion, and neglect."
    },
    {
        "bookId": 99,
        "title": "The Little Prince",
        "author": "Antoine de Saint-Exupéry",
        "origin": "International",
        "genres": "Children's Classic|Philosophical Fable|Fantasy",
        "themes": "Asteroid B-612|The Tamed Fox|Grown-up Foolishness|Seeing with Heart",
        "publication_year": 1943,
        "rating": 4.8,
        "cover_url": "/static/covers/99.jpg",
        "description": "An aviator stranded in the Sahara desert encounters a golden-haired boy from Asteroid B-612, learning that 'one sees clearly only with the heart; anything essential is invisible to the eyes.'"
    },
    {
        "bookId": 100,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "origin": "International",
        "genres": "Sci-Fi Comedy|Satire|Adventure",
        "themes": "Answer 42|Arthur Dent & Ford Prefect|Don't Panic|Towels",
        "publication_year": 1979,
        "rating": 4.6,
        "cover_url": "/static/covers/100.jpg",
        "description": "Seconds before Earth is demolished by a bureaucratic Vogon constructor fleet to make way for a hyperspace bypass, ordinary Englishman Arthur Dent is whisked across the galaxy."
    }
]

# Save books.csv
df_books = pd.DataFrame(books_data)
df_books.to_csv("dataset/books.csv", index=False)
print(f"Generated dataset/books.csv with {len(df_books)} books:")
print(f"  - Indian Authors: {len(df_books[df_books['origin'] == 'Indian'])}")
print(f"  - International Authors: {len(df_books[df_books['origin'] == 'International'])}")

# Generate Reader Ratings for 10 distinct Taste Personas
ratings = []

def add_book_ratings(user_id, high_books, mid_books, low_books):
    for b in high_books:
        ratings.append({"userId": user_id, "bookId": b, "rating": float(np.random.choice([4.5, 5.0])), "timestamp": 1600000000})
    for b in mid_books:
        ratings.append({"userId": user_id, "bookId": b, "rating": float(np.random.choice([3.5, 4.0])), "timestamp": 1600000000})
    for b in low_books:
        ratings.append({"userId": user_id, "bookId": b, "rating": float(np.random.choice([1.5, 2.0, 2.5])), "timestamp": 1600000000})

# User 1: Mythological Fiction & Indian Epics Enthusiast
add_book_ratings(1, [5, 6, 8, 9, 10, 11, 12, 13, 14, 38, 41, 58], [7, 36, 37, 39, 47], [15, 18, 90, 93])

# User 2: Thrillers, Suspense & Conspiracies Buff
add_book_ratings(2, [36, 37, 38, 39, 40, 78, 79, 80, 81, 82, 83], [1, 20, 74, 86], [22, 46, 64, 99])

# User 3: Dystopian, Sci-Fi & Speculative Fiction Lover
add_book_ratings(3, [62, 63, 84, 85, 86, 97, 100, 40, 29], [3, 67, 68, 71], [16, 18, 45, 51])

# User 4: Classic World Literature & High Drama Connoisseur
add_book_ratings(4, [61, 64, 65, 74, 75, 76, 77, 98, 47, 48, 50], [2, 4, 21, 66, 89], [15, 18, 20, 94])

# User 5: Contemporary Indian Fiction & Campus Drama Fan
add_book_ratings(5, [15, 16, 17, 18, 19, 20, 1, 32], [8, 11, 44, 45], [74, 76, 85, 92])

# User 6: Heartwarming, Life Wisdom & Uplifting Non-Fiction (Sudha Murty & Kalam Buff)
add_book_ratings(6, [42, 43, 44, 45, 46, 55, 56, 57, 71, 99], [22, 23, 90, 93], [62, 81, 82, 83])

# User 7: Post-Colonial History & Serious Non-Fiction Enthusiast
add_book_ratings(7, [3, 7, 25, 26, 27, 54, 58, 59, 60, 91], [2, 4, 30, 87, 88], [15, 18, 69, 100])

# User 8: Self-Improvement, Psychology & Productivity Reader
add_book_ratings(8, [90, 91, 92, 93, 94, 95, 55, 56, 71], [42, 57, 61, 62], [5, 6, 8, 81, 82])

# User 9: Fantasy, Magical Realism & Epic Adventures
add_book_ratings(9, [67, 68, 69, 70, 71, 72, 73, 96, 97, 5, 8, 9], [3, 12, 13, 84, 99], [50, 51, 92, 94])

# User 10: Casual / Light Reader (Cold-Start Persona)
add_book_ratings(10, [15, 69, 71, 90, 99, 46], [1, 22, 61], [75, 76])

df_ratings = pd.DataFrame(ratings)
df_ratings.to_csv("dataset/book_ratings.csv", index=False)
print(f"Generated dataset/book_ratings.csv with {len(df_ratings)} ratings across {df_ratings['userId'].nunique()} users.")

# Generate Aesthetic 400x600 Book Covers
def create_book_cover(book, out_path):
    width, height = 400, 600
    
    # Palette depending on origin
    is_indian = book['origin'] == 'Indian'
    
    # Sophisticated background palettes
    if is_indian:
        bg_color = (12, 22, 18)       # Deep forest obsidian
        border_color = (0, 230, 118)   # Vivid emerald
        accent_color = (251, 191, 36)  # Warm gold
        badge_bg = (16, 185, 129, 60)
        badge_text = "🇮🇳 INDIAN AUTHOR"
    else:
        bg_color = (16, 20, 28)       # Deep midnight sapphire
        border_color = (56, 189, 248)  # Bright sky cyan
        accent_color = (244, 114, 182) # Rose accent
        badge_bg = (14, 165, 233, 60)
        badge_text = "🌐 WORLD CLASSIC"

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Outer decorative frame
    draw.rectangle([12, 12, width - 13, height - 13], outline=border_color, width=2)
    draw.rectangle([18, 18, width - 19, height - 19], outline=(40, 50, 60), width=1)

    # Top Origin Tag Banner
    draw.rectangle([30, 28, width - 30, 54], fill=(24, 32, 40), outline=border_color, width=1)
    draw.text((width // 2, 41), badge_text, fill=accent_color, anchor="mm")

    # Book Spine accent strip on left
    draw.line([(24, 60), (24, height - 60)], fill=border_color, width=3)

    # Book Title (multi-line wrapping)
    title = book['title']
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 18:
            lines.append(" ".join(current_line))
            current_line = []
    if current_line:
        lines.append(" ".join(current_line))

    # Draw Title Lines
    title_start_y = 120
    for i, line in enumerate(lines[:3]):
        draw.text((width // 2, title_start_y + (i * 38)), line, fill=(255, 255, 255), anchor="mm")

    # Author Ribbon
    author_y = title_start_y + (len(lines[:3]) * 38) + 25
    draw.line([(60, author_y - 12), (width - 60, author_y - 12)], fill=(60, 75, 70), width=1)
    draw.text((width // 2, author_y + 8), f"by {book['author']}", fill=border_color, anchor="mm")
    draw.line([(60, author_y + 26), (width - 60, author_y + 26)], fill=(60, 75, 70), width=1)

    # Decorative Center Emblem / Icon
    center_y = (author_y + height - 150) // 2
    emblem_radius = 45
    draw.ellipse([width//2 - emblem_radius, center_y - emblem_radius, width//2 + emblem_radius, center_y + emblem_radius],
                 outline=accent_color, width=2)
    draw.text((width // 2, center_y), "📖", anchor="mm")

    # Genres tag
    genres_preview = book['genres'].replace("|", " • ")
    if len(genres_preview) > 36:
        genres_preview = genres_preview[:34] + "..."
    draw.text((width // 2, height - 130), genres_preview, fill=(160, 174, 192), anchor="mm")

    # Rating & Year Banner at bottom
    draw.rectangle([35, height - 95, width - 35, height - 45], fill=(20, 28, 25), outline=border_color, width=1)
    rating_str = f"⭐ {book['rating']} / 5.0  •  {book['publication_year']}"
    draw.text((width // 2, height - 70), rating_str, fill=accent_color, anchor="mm")

    img.save(out_path, "JPEG", quality=90)

print("Generating 100 aesthetic book cover cards...")
for book in books_data:
    out_file = f"static/covers/{book['bookId']}.jpg"
    create_book_cover(book, out_file)

print("Done! 100 book covers created in static/covers/")
