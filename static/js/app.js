// CineBook - Personalized Movie & Book Recommendation System Logic

let currentMode = 'movies'; // 'movies' | 'books'
let currentBookFilter = 'all'; // 'all' | 'indian' | 'international'

let allMovies = [];
let allBooks = [];
let selectedItem = null;

// DOM Elements
const tabMovies = document.getElementById('tabMovies');
const tabBooks = document.getElementById('tabBooks');
const bookFilterRow = document.getElementById('bookFilterRow');
const filterPills = document.querySelectorAll('.filter-pill');

const searchTitle = document.getElementById('searchTitle');
const searchDesc = document.getElementById('searchDesc');
const searchInput = document.getElementById('searchInput') || document.getElementById('movieSearchInput');
const searchBoxIcon = document.getElementById('searchBoxIcon');
const searchResultsDropdown = document.getElementById('searchResultsDropdown');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const searchBtn = document.getElementById('searchBtn');
const quickPicksRow = document.getElementById('quickPicksRow');

const selectedItemSection = document.getElementById('selectedItemSection');
const recommendationsSection = document.getElementById('recommendationsSection');
const recommendationsTitle = document.getElementById('recommendationsTitle');
const recommendationsGrid = document.getElementById('recommendationsGrid');

const exploreSection = document.getElementById('exploreSection');
const exploreTitle = document.getElementById('exploreTitle');
const exploreSubtitle = document.getElementById('exploreSubtitle');
const exploreGrid = document.getElementById('exploreGrid');
const shuffleBtn = document.getElementById('shuffleBtn');

const toastNotification = document.getElementById('toastNotification');

const IMG_CACHE_BUST = '?v=20260924_art2';

const MOVIE_QUICK_PICKS = [
    'Inception', '3 Idiots', 'Interstellar', 'Sholay', 'The Dark Knight', 'Dangal', 'DDLJ', 'Gangs of Wasseypur'
];

const BOOK_QUICK_PICKS = [
    'The Palace of Illusions', 'The Immortals of Meluha', '1984', 'The Alchemist', 'Sacred Games', 'Atomic Habits', 'The White Tiger', 'The Blue Umbrella'
];

const MOVIE_ALIASES = {
    'ddlj': 'Dilwale Dulhania Le Jayenge',
    'k3g': 'Kabhi Khushi Kabhie Gham',
    'yjhd': 'Yeh Jawaani Hai Deewani',
    'gow': 'Gangs of Wasseypur',
    'znmd': 'Zindagi Na Milegi Dobara',
    'ms dhoni': 'MS Dhoni: The Untold Story',
    'dhoni': 'MS Dhoni: The Untold Story',
    'kgf': 'Krrish',
    'wall-e': 'WALL-E',
    'walle': 'WALL-E',
    'kabir': 'Kabir Singh',
    'raazi': 'Raazi',
    'gully boy': 'Gully Boy'
};

const BOOK_ALIASES = {
    'meluha': 'The Immortals of Meluha',
    'palace': 'The Palace of Illusions',
    'habits': 'Atomic Habits',
    'white tiger': 'The White Tiger',
    'god of small things': 'The God of Small Things',
    'mockingbird': 'To Kill a Mockingbird',
    'alchemist': 'The Alchemist',
    'sacred games': 'Sacred Games',
    'blue umbrella': 'The Blue Umbrella',
    'love story': 'I Too Had a Love Story',
    'kalam': 'Wings of Fire',
    'wings of fire': 'Wings of Fire',
    'potter': "Harry Potter and the Sorcerer's Stone",
    'lotr': 'The Lord of the Rings: The Fellowship of the Ring',
    'da vinci': 'The Da Vinci Code',
    'orwell': '1984',
    'dune': 'Dune',
    'malgudi': 'Malgudi Days',
    'sudha murty': 'Wise and Otherwise'
};

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();

    if (selectedItemSection) selectedItemSection.style.display = 'none';
    if (recommendationsSection) recommendationsSection.style.display = 'none';

    renderQuickPicks();

    try {
        await Promise.all([loadMovies(), loadBooks()]);
        renderRandomExplore();
    } catch (err) {
        console.error('Initialization error:', err);
    }
});

// Data Loaders
async function loadMovies() {
    try {
        const res = await fetch('/api/movies');
        const data = await res.json();
        allMovies = data.movies || [];
    } catch (err) {
        showToast('Error loading movies: ' + err.message);
    }
}

async function loadBooks() {
    try {
        const res = await fetch('/api/books');
        const data = await res.json();
        allBooks = data.books || [];
    } catch (err) {
        showToast('Error loading books: ' + err.message);
    }
}

// Switch Mode (Movies vs Books)
function switchMode(newMode) {
    if (currentMode === newMode) return;
    currentMode = newMode;

    if (searchInput) searchInput.value = '';
    if (clearSearchBtn) clearSearchBtn.classList.add('hidden');
    hideDropdown();

    if (selectedItemSection) selectedItemSection.style.display = 'none';
    if (recommendationsSection) recommendationsSection.style.display = 'none';

    if (currentMode === 'movies') {
        if (tabMovies) tabMovies.classList.add('active');
        if (tabBooks) tabBooks.classList.remove('active');
        if (bookFilterRow) bookFilterRow.classList.add('hidden');

        if (searchTitle) searchTitle.innerHTML = `Find Any Movie & Its <span class="green-text">Rating</span>`;
        if (searchDesc) searchDesc.textContent = `Type any movie name to check its details, IMDb rating, and get instant recommendations.`;
        if (searchInput) searchInput.placeholder = `Search a movie (e.g. 3 Idiots, Sholay, Dangal, DDLJ, Inception, Interstellar)...`;
        if (searchBoxIcon) searchBoxIcon.textContent = `🔍`;
    } else {
        if (tabBooks) tabBooks.classList.add('active');
        if (tabMovies) tabMovies.classList.remove('active');
        if (bookFilterRow) bookFilterRow.classList.remove('hidden');

        if (searchTitle) searchTitle.innerHTML = `Find Any Book & Its <span class="green-text">Reader Rating</span>`;
        if (searchDesc) searchDesc.textContent = `Explore 100 curated books (60 Indian Writers + 40 International Writers) with instant recommendations.`;
        if (searchInput) searchInput.placeholder = `Search a book or author (e.g. The Palace of Illusions, 1984, The Alchemist, Amish, Premchand)...`;
        if (searchBoxIcon) searchBoxIcon.textContent = `📚`;
    }

    renderQuickPicks();
    renderRandomExplore();
    if (searchInput) searchInput.focus();
}

function renderQuickPicks() {
    if (!quickPicksRow) return;
    const list = currentMode === 'movies' ? MOVIE_QUICK_PICKS : BOOK_QUICK_PICKS;
    quickPicksRow.innerHTML = '';
    list.forEach(title => {
        const chip = document.createElement('span');
        chip.className = 'quick-chip';
        chip.textContent = title;
        chip.addEventListener('click', () => {
            if (searchInput) {
                searchInput.value = title;
                if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
                performSearch();
            }
        });
        quickPicksRow.appendChild(chip);
    });
}

// Render Random / Explore Items Grid
function renderRandomExplore() {
    if (!exploreGrid) return;
    exploreGrid.innerHTML = '';

    if (currentMode === 'movies') {
        if (exploreTitle) exploreTitle.textContent = 'Discover Movies';
        if (exploreSubtitle) exploreSubtitle.textContent = 'Click any movie below to view details and recommendations';

        if (allMovies.length === 0) return;
        const shuffled = [...allMovies].sort(() => 0.5 - Math.random()).slice(0, 12);
        shuffled.forEach(m => {
            const card = createCard(m, false);
            card.addEventListener('click', () => {
                selectMovie(m.movieId);
                if (searchInput) searchInput.value = m.title;
                if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
                window.scrollTo({ top: 120, behavior: 'smooth' });
            });
            exploreGrid.appendChild(card);
        });

    } else {
        let pool = [...allBooks];
        if (currentBookFilter === 'indian') {
            pool = pool.filter(b => b.origin === 'Indian');
            if (exploreTitle) exploreTitle.textContent = 'Discover Books by Indian Writers (60)';
            if (exploreSubtitle) exploreSubtitle.textContent = 'Featuring mythology, historical fiction, contemporary realism & classics';
        } else if (currentBookFilter === 'international') {
            pool = pool.filter(b => b.origin === 'International');
            if (exploreTitle) exploreTitle.textContent = 'Discover Books by International Writers (40)';
            if (exploreSubtitle) exploreSubtitle.textContent = 'Featuring world classics, dystopian epics, fantasy & psychology';
        } else {
            if (exploreTitle) exploreTitle.textContent = 'Discover Books (100)';
            if (exploreSubtitle) exploreSubtitle.textContent = 'Click any book below to view details and recommendations';
        }

        if (pool.length === 0) return;
        const shuffled = pool.sort(() => 0.5 - Math.random()).slice(0, 12);
        shuffled.forEach(b => {
            const card = createCard(b, false);
            card.addEventListener('click', () => {
                selectBook(b.bookId);
                if (searchInput) searchInput.value = b.title;
                if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
                window.scrollTo({ top: 120, behavior: 'smooth' });
            });
            exploreGrid.appendChild(card);
        });
    }
}

// Cards Creation
function createCard(item, isRec = false) {
    const card = document.createElement('div');
    card.className = 'item-card';

    const isBook = currentMode === 'books';

    // Similarity score badge (only for recommended items)
    const simScore = item.similarity_score !== undefined
        ? Math.round(item.similarity_score * 100)
        : (item.match_pct || (item.hybrid_score ? Math.round(item.hybrid_score * 100) : null));

    const simBadge = isRec && simScore !== null
        ? `<div class="card-sim-badge">${simScore}% Match</div>`
        : '';

    // Rating Badge
    let ratingVal = isBook ? item.rating : item.imdb_rating;
    let ratingLabel = '⭐ ' + Number(ratingVal || 0).toFixed(1);
    const ratingBadge = ratingVal
        ? `<div class="card-rating-badge">${ratingLabel}</div>`
        : '';

    // Origin Tag for Books
    let originTag = '';
    if (isBook && item.origin) {
        const flag = item.origin === 'Indian' ? '🇮🇳' : '🌐';
        originTag = `<div class="card-origin-tag ${item.origin === 'Indian' ? 'badge-origin-indian' : 'badge-origin-intl'}">${flag} ${item.origin}</div>`;
    }

    const rawCoverUrl = isBook ? item.cover_url : item.poster_url;
    const coverUrl = rawCoverUrl ? `${rawCoverUrl}${IMG_CACHE_BUST}` : '';
    const title = item.title;
    const year = isBook ? item.publication_year : item.release_year;
    const genresList = (item.genres || '').replace(/\|/g, ', ');
    const creatorLabel = isBook ? 'Author' : 'Dir';
    const creatorName = isBook ? item.author : item.director;

    card.innerHTML = `
        <div class="card-media-wrapper">
            <img class="card-media-img" src="${coverUrl}" alt="${title}" loading="lazy" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60'">
            ${simBadge}
            ${ratingBadge}
            ${originTag}
        </div>
        <div class="card-content">
            <h4 class="card-title">${title} <span style="font-weight: 400; color: #6b7280; font-size: 0.8rem;">(${year || ''})</span></h4>
            <div class="card-genres">${genresList}</div>
            <div class="card-creator">${creatorLabel}: <strong>${creatorName || 'N/A'}</strong></div>
        </div>
    `;
    return card;
}

// Selection & Recommendations
async function selectMovie(movieId) {
    hideDropdown();
    try {
        const res = await fetch(`/api/movie/${movieId}`);
        if (!res.ok) throw new Error('Movie not found');
        const data = await res.json();

        selectedItem = data.movie;
        const similarMovies = data.similar_movies || [];

        renderSelectedMovie(selectedItem);
        renderRecommendations(similarMovies, selectedItem.title, 'movie');
    } catch (err) {
        showToast('Error selecting movie: ' + err.message);
    }
}

async function selectBook(bookId) {
    hideDropdown();
    try {
        const res = await fetch(`/api/book/${bookId}`);
        if (!res.ok) throw new Error('Book not found');
        const data = await res.json();

        selectedItem = data.book;
        const similarBooks = data.similar_books || [];

        renderSelectedBook(selectedItem);
        renderRecommendations(similarBooks, selectedItem.title, 'book');
    } catch (err) {
        showToast('Error selecting book: ' + err.message);
    }
}

function renderSelectedMovie(movie) {
    if (!selectedItemSection) return;
    const genresArr = (movie.genres || '').split('|');
    const genreTags = genresArr.map(g => `<span class="genre-tag">${g}</span>`).join('');

    selectedItemSection.style.display = 'block';
    selectedItemSection.innerHTML = `
        <div class="selected-item-container">
            <img class="selected-media-cover" src="${movie.poster_url}${IMG_CACHE_BUST}" alt="${movie.title}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60'">
            <div class="selected-details">
                <div class="selected-header-row">
                    <div>
                        <h2 class="selected-title">${movie.title} <span class="selected-year">(${movie.release_year})</span></h2>
                        <div class="tags-row" style="margin-top: 0.4rem;">${genreTags}</div>
                    </div>
                    <div class="rating-badge-large">
                        ⭐ ${movie.imdb_rating} / 10 IMDb
                    </div>
                </div>

                <div class="selected-overview">
                    <p>${movie.overview || 'No synopsis available.'}</p>
                </div>

                <div class="selected-meta-grid">
                    <div>🎬 Director: <strong>${movie.director || 'N/A'}</strong></div>
                    <div>👥 Cast: <strong>${movie.cast || 'N/A'}</strong></div>
                </div>
            </div>
        </div>
    `;
}

function renderSelectedBook(book) {
    if (!selectedItemSection) return;
    const genresArr = (book.genres || '').split('|');
    const genreTags = genresArr.map(g => `<span class="genre-tag">${g}</span>`).join('');

    const themesArr = (book.themes || '').split('|');
    const themeTags = themesArr.map(t => `<span class="theme-tag">#${t}</span>`).join('');

    const isIndian = book.origin === 'Indian';
    const originBadge = isIndian
        ? `<span class="badge-origin badge-origin-indian">🇮🇳 Indian Writer</span>`
        : `<span class="badge-origin badge-origin-intl">🌐 International Writer</span>`;

    selectedItemSection.style.display = 'block';
    selectedItemSection.innerHTML = `
        <div class="selected-item-container">
            <img class="selected-media-cover" src="${book.cover_url}${IMG_CACHE_BUST}" alt="${book.title}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60'">
            <div class="selected-details">
                <div class="selected-header-row">
                    <div>
                        <h2 class="selected-title">${book.title} <span class="selected-year">(${book.publication_year})</span></h2>
                        <div class="tags-row" style="margin-top: 0.4rem;">
                            ${originBadge}
                            ${genreTags}
                        </div>
                    </div>
                    <div class="rating-badge-large">
                        ⭐ ${book.rating} / 5.0 Rating
                    </div>
                </div>

                <div class="selected-overview">
                    <p>${book.description || 'No synopsis available.'}</p>
                </div>

                <div class="tags-row" style="margin-top: -0.2rem;">
                    ${themeTags}
                </div>

                <div class="selected-meta-grid">
                    <div>✍️ Author: <strong>${book.author || 'N/A'}</strong></div>
                    <div>🌍 Origin: <strong>${book.origin} Literature</strong></div>
                </div>
            </div>
        </div>
    `;
}

function renderRecommendations(recommendations, currentTitle, mediaType) {
    if (!recommendationsSection || !recommendationsGrid) return;
    recommendationsSection.style.display = 'block';
    const label = mediaType === 'book' ? 'Books' : 'Movies';
    if (recommendationsTitle) {
        recommendationsTitle.innerHTML = `Recommended ${label} Based on <span class="green-text">"${currentTitle}"</span>`;
    }

    recommendationsGrid.innerHTML = '';
    if (recommendations.length === 0) {
        recommendationsGrid.innerHTML = `<p style="color: #9ca3af;">No similar ${label.toLowerCase()} found.</p>`;
        return;
    }

    recommendations.forEach(rec => {
        const card = createCard(rec, true);
        card.addEventListener('click', () => {
            if (mediaType === 'book') {
                selectBook(rec.bookId);
                if (searchInput) searchInput.value = rec.title;
            } else {
                selectMovie(rec.movieId);
                if (searchInput) searchInput.value = rec.title;
            }
            if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
            window.scrollTo({ top: 120, behavior: 'smooth' });
        });
        recommendationsGrid.appendChild(card);
    });
}

// Event Listeners
function setupEventListeners() {
    if (tabMovies) tabMovies.addEventListener('click', () => switchMode('movies'));
    if (tabBooks) tabBooks.addEventListener('click', () => switchMode('books'));

    if (shuffleBtn) {
        shuffleBtn.addEventListener('click', () => {
            renderRandomExplore();
            showToast(`Shuffled 12 random ${currentMode === 'movies' ? 'movies' : 'books'}!`);
        });
    }

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentBookFilter = pill.getAttribute('data-filter');
            renderRandomExplore();

            if (searchInput && searchInput.value.trim().length > 0) {
                handleSearchInput({ target: searchInput });
            }
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', handleSearchInput);
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                hideDropdown();
                performSearch();
            } else if (e.key === 'Escape') {
                hideDropdown();
            }
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            clearSearchBtn.classList.add('hidden');
            hideDropdown();
            if (selectedItemSection) selectedItemSection.style.display = 'none';
            if (recommendationsSection) recommendationsSection.style.display = 'none';
            if (searchInput) searchInput.focus();
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            hideDropdown();
            performSearch();
        });
    }

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-input-box')) {
            hideDropdown();
        }
    });
}

function hideDropdown() {
    if (searchResultsDropdown) {
        searchResultsDropdown.classList.add('hidden');
        searchResultsDropdown.innerHTML = '';
    }
}

function handleSearchInput(e) {
    const val = e.target.value.trim().toLowerCase();

    if (clearSearchBtn) {
        if (val.length > 0) clearSearchBtn.classList.remove('hidden');
        else clearSearchBtn.classList.add('hidden');
    }

    if (val.length === 0) {
        hideDropdown();
        return;
    }

    const aliases = currentMode === 'movies' ? MOVIE_ALIASES : BOOK_ALIASES;
    const targetVal = aliases[val] ? aliases[val].toLowerCase() : val;
    const clean = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const cleanVal = clean(targetVal);

    let candidates = currentMode === 'movies' ? allMovies : allBooks;

    if (currentMode === 'books' && currentBookFilter !== 'all') {
        candidates = candidates.filter(b => b.origin.toLowerCase() === currentBookFilter.toLowerCase());
    }

    const matches = candidates.filter(item => {
        const titleLower = item.title.toLowerCase();
        const authorOrDir = (currentMode === 'books' ? (item.author || '') : (item.director || '')).toLowerCase();
        return (
            titleLower.includes(targetVal) ||
            clean(titleLower).includes(cleanVal) ||
            authorOrDir.includes(targetVal) ||
            clean(authorOrDir).includes(cleanVal)
        );
    }).slice(0, 6);

    if (matches.length === 0) {
        hideDropdown();
        return;
    }

    if (searchResultsDropdown) {
        searchResultsDropdown.innerHTML = '';
        matches.forEach(item => {
            const div = document.createElement('div');
            div.className = 'search-dropdown-item';

            if (currentMode === 'books') {
                const flag = item.origin === 'Indian' ? '🇮🇳' : '🌐';
                div.innerHTML = `
                    <span><strong>${item.title}</strong> (${item.publication_year}) — <em>${item.author}</em></span>
                    <span class="item-meta">${flag} ⭐ ${item.rating} • ${item.genres.replace(/\|/g, ', ')}</span>
                `;
                div.addEventListener('click', (ev) => {
                    ev.stopPropagation();
                    if (searchInput) searchInput.value = item.title;
                    hideDropdown();
                    selectBook(item.bookId);
                    window.scrollTo({ top: 120, behavior: 'smooth' });
                });
            } else {
                div.innerHTML = `
                    <span><strong>${item.title}</strong> (${item.release_year})</span>
                    <span class="item-meta">⭐ ${item.imdb_rating} • ${item.genres.replace(/\|/g, ', ')}</span>
                `;
                div.addEventListener('click', (ev) => {
                    ev.stopPropagation();
                    if (searchInput) searchInput.value = item.title;
                    hideDropdown();
                    selectMovie(item.movieId);
                    window.scrollTo({ top: 120, behavior: 'smooth' });
                });
            }

            searchResultsDropdown.appendChild(div);
        });

        searchResultsDropdown.classList.remove('hidden');
    }
}

function performSearch() {
    hideDropdown();
    if (!searchInput) return;
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
        showToast(`Please type a ${currentMode === 'movies' ? 'movie' : 'book'} name to search`);
        return;
    }

    const aliases = currentMode === 'movies' ? MOVIE_ALIASES : BOOK_ALIASES;
    const targetQuery = aliases[query] ? aliases[query].toLowerCase() : query;
    const clean = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const cleanQuery = clean(targetQuery);

    let list = currentMode === 'movies' ? allMovies : allBooks;

    let found = list.find(m => m.title.toLowerCase().includes(targetQuery));
    if (!found) {
        found = list.find(m => {
            const authorOrDir = currentMode === 'books' ? m.author : m.director;
            return clean(m.title).includes(cleanQuery) ||
                   cleanQuery.includes(clean(m.title)) ||
                   (authorOrDir && clean(authorOrDir).includes(cleanQuery));
        });
    }

    if (found) {
        searchInput.value = found.title;
        if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
        if (currentMode === 'books') {
            selectBook(found.bookId);
        } else {
            selectMovie(found.movieId);
        }
        window.scrollTo({ top: 120, behavior: 'smooth' });
    } else {
        showToast(`No ${currentMode === 'movies' ? 'movie' : 'book'} found matching "${query}"`);
    }
}

function showToast(message) {
    if (!toastNotification) return;
    toastNotification.textContent = message;
    toastNotification.classList.remove('hidden');
    setTimeout(() => {
        toastNotification.classList.add('hidden');
    }, 3200);
}
