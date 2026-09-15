// CineMatch AI - Clean Green & Black Movie Recommender Logic

let allMovies = [];
let selectedMovie = null;

// DOM Elements
const movieSearchInput = document.getElementById('movieSearchInput');
const searchResultsDropdown = document.getElementById('searchResultsDropdown');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const searchBtn = document.getElementById('searchBtn');
const selectedMovieSection = document.getElementById('selectedMovieSection');
const recommendationsSection = document.getElementById('recommendationsSection');
const recommendationsTitle = document.getElementById('recommendationsTitle');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const browseGrid = document.getElementById('browseGrid');
const toastNotification = document.getElementById('toastNotification');

document.addEventListener('DOMContentLoaded', async () => {
    await loadMovies();
    setupEventListeners();
    // Keep sections hidden until the user performs a search
    selectedMovieSection.style.display = 'none';
    recommendationsSection.style.display = 'none';
});

async function loadMovies() {
    try {
        const res = await fetch('/api/movies');
        const data = await res.json();
        allMovies = data.movies || [];
    } catch (err) {
        showToast('Error loading movies: ' + err.message);
    }
}

function createMovieCard(movie, isRec = false) {
    const card = document.createElement('div');
    card.className = 'movie-card';

    const simBadge = isRec && movie.similarity_score !== undefined
        ? `<div class="card-sim-badge">${Math.round(movie.similarity_score * 100)}% Match</div>`
        : '';

    const ratingBadge = movie.imdb_rating
        ? `<div class="card-rating-badge">⭐ ${Number(movie.imdb_rating).toFixed(1)}</div>`
        : '';

    const genresList = (movie.genres || '').replace(/\|/g, ', ');

    card.innerHTML = `
        <div class="card-poster-wrapper">
            <img class="card-poster" src="${movie.poster_url}" alt="${movie.title}" onerror="this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60'">
            ${simBadge}
            ${ratingBadge}
        </div>
        <div class="card-content">
            <h4 class="card-title">${movie.title} <span style="font-weight: 400; color: #6b7280; font-size: 0.8rem;">(${movie.release_year || ''})</span></h4>
            <div class="card-genres">${genresList}</div>
            <div class="card-director">Dir: <strong>${movie.director || 'N/A'}</strong></div>
        </div>
    `;
    return card;
}

async function selectMovie(movieId) {
    hideDropdown();
    try {
        const res = await fetch(`/api/movie/${movieId}`);
        if (!res.ok) throw new Error('Movie not found');
        const data = await res.json();

        selectedMovie = data.movie;
        const similarMovies = data.similar_movies || [];

        renderSelectedMovie(selectedMovie);
        renderRecommendations(similarMovies, selectedMovie.title);

    } catch (err) {
        showToast('Error selecting movie: ' + err.message);
    }
}

function renderSelectedMovie(movie) {
    const genresArr = (movie.genres || '').split('|');
    const genreTags = genresArr.map(g => `<span class="genre-tag">${g}</span>`).join('');

    selectedMovieSection.style.display = 'block';
    selectedMovieSection.innerHTML = `
        <div class="selected-movie-container">
            <img class="selected-poster" src="${movie.poster_url}" alt="${movie.title}" onerror="this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60'">
            <div class="selected-details">
                <div class="selected-header-row">
                    <div>
                        <h2 class="selected-title">${movie.title} <span class="selected-year">(${movie.release_year})</span></h2>
                        <div class="genres-row" style="margin-top: 0.4rem;">${genreTags}</div>
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

function renderRecommendations(recommendations, currentTitle) {
    recommendationsSection.style.display = 'block';
    recommendationsTitle.innerHTML = `Machine Learning Recommendations Based on <span class="green-text">"${currentTitle}"</span>`;

    recommendationsGrid.innerHTML = '';
    if (recommendations.length === 0) {
        recommendationsGrid.innerHTML = '<p style="color: #9ca3af;">No similar recommendations found.</p>';
        return;
    }

    recommendations.forEach(rec => {
        const card = createMovieCard(rec, true);
        card.addEventListener('click', () => {
            selectMovie(rec.movieId);
            movieSearchInput.value = rec.title;
            if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
            window.scrollTo({ top: 120, behavior: 'smooth' });
        });
        recommendationsGrid.appendChild(card);
    });
}

function setupEventListeners() {
    // Search input typing
    movieSearchInput.addEventListener('input', handleSearchInput);

    // Clear search button click
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            movieSearchInput.value = '';
            clearSearchBtn.classList.add('hidden');
            hideDropdown();
            selectedMovieSection.style.display = 'none';
            recommendationsSection.style.display = 'none';
            movieSearchInput.focus();
        });
    }

    // Search button click
    searchBtn.addEventListener('click', () => {
        hideDropdown();
        performSearch();
    });

    // Enter key or Escape key press in search
    movieSearchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            hideDropdown();
            performSearch();
        } else if (e.key === 'Escape') {
            hideDropdown();
        }
    });

    // Close dropdown on click outside the input
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-input-box')) {
            hideDropdown();
        }
    });
}

function hideDropdown() {
    searchResultsDropdown.classList.add('hidden');
    searchResultsDropdown.innerHTML = '';
}

function handleSearchInput(e) {
    const val = e.target.value.trim().toLowerCase();
    
    if (clearSearchBtn) {
        if (val.length > 0) {
            clearSearchBtn.classList.remove('hidden');
        } else {
            clearSearchBtn.classList.add('hidden');
        }
    }

    if (val.length === 0) {
        hideDropdown();
        return;
    }

    const ALIASES = {
        'ddlj': 'Dilwale Dulhania Le Jayenge',
        'k3g': 'Kabhi Khushi Kabhie Gham',
        'yjhd': 'Yeh Jawaani Hai Deewani',
        'gow': 'Gangs of Wasseypur',
        'znmd': 'Zindagi Na Milegi Dobara',
        'ms dhoni': 'MS Dhoni: The Untold Story',
        'dhoni': 'MS Dhoni: The Untold Story',
        'kgf': 'Krrish'
    };

    const targetVal = ALIASES[val] ? ALIASES[val].toLowerCase() : val;
    const clean = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
    const cleanVal = clean(targetVal);

    const matches = allMovies.filter(m => {
        const titleLower = m.title.toLowerCase();
        return titleLower.includes(targetVal) || clean(titleLower).includes(cleanVal);
    }).slice(0, 6);

    if (matches.length === 0) {
        hideDropdown();
        return;
    }

    searchResultsDropdown.innerHTML = '';
    matches.forEach(m => {
        const item = document.createElement('div');
        item.className = 'search-dropdown-item';
        item.innerHTML = `
            <span><strong>${m.title}</strong> (${m.release_year})</span>
            <span class="item-genres">⭐ ${m.imdb_rating} • ${m.genres.replace(/\|/g, ', ')}</span>
        `;
        item.addEventListener('click', (ev) => {
            ev.stopPropagation();
            movieSearchInput.value = m.title;
            hideDropdown();
            selectMovie(m.movieId);
            window.scrollTo({ top: 120, behavior: 'smooth' });
        });
        searchResultsDropdown.appendChild(item);
    });

    searchResultsDropdown.classList.remove('hidden');
}

function performSearch() {
    hideDropdown();
    const query = movieSearchInput.value.trim().toLowerCase();
    if (!query) {
        showToast('Please type a movie name to search');
        return;
    }

    const ALIASES = {
        'ddlj': 'Dilwale Dulhania Le Jayenge',
        'k3g': 'Kabhi Khushi Kabhie Gham',
        'yjhd': 'Yeh Jawaani Hai Deewani',
        'gow': 'Gangs of Wasseypur',
        'znmd': 'Zindagi Na Milegi Dobara',
        'ms dhoni': 'MS Dhoni: The Untold Story',
        'dhoni': 'MS Dhoni: The Untold Story'
    };

    const targetQuery = ALIASES[query] ? ALIASES[query].toLowerCase() : query;
    const clean = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
    const cleanQuery = clean(targetQuery);

    let found = allMovies.find(m => m.title.toLowerCase().includes(targetQuery));
    if (!found) {
        found = allMovies.find(m => clean(m.title).includes(cleanQuery) || cleanQuery.includes(clean(m.title)));
    }

    if (found) {
        movieSearchInput.value = found.title;
        if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
        selectMovie(found.movieId);
        window.scrollTo({ top: 120, behavior: 'smooth' });
    } else {
        showToast(`No movie found matching "${query}"`);
    }
}

function showToast(message) {
    toastNotification.textContent = message;
    toastNotification.classList.remove('hidden');
    setTimeout(() => {
        toastNotification.classList.add('hidden');
    }, 3200);
}

