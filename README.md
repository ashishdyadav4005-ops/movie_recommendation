# 🎬 CineMatch: Personalized Movie Recommendation System

> **A Personalized Movie Recommendation System using Machine Learning combining Content-Based (TF-IDF & Cosine Similarity) and Collaborative Filtering (SVD Matrix Factorization). It analyzes genres, cast, and user ratings to deliver tailored recommendations and rating predictions across 100 Hollywood & Bollywood films through an interactive web UI.**

---

## 🌟 Key Features

- **Hybrid Machine Learning Engine**: Blends Content-Based item similarity with Collaborative user interaction patterns.
- **Content-Based Filtering**: TF-IDF Vectorizer & Cosine Similarity across genres, director, cast, and plot overviews.
- **Collaborative Filtering**: Matrix Factorization using Truncated Singular Value Decomposition (SVD) with RMSE & MAE evaluation.
- **100 Curated Movies**: Balanced catalog of 40 iconic Hollywood and 60 classic/modern Bollywood movies with high-res local posters.
- **Modern Green & Black Web UI**: Clean, responsive interface (FastAPI + Vanilla JS) with instant search, rating comparisons, and real-time recommendations.
- **Cold-Start Problem Mitigation**: Dynamic linear weighting shifting gracefully to content matching for new users or movies.

---

## 📁 Project Structure

```
Movie Recommendation System/
│
├── dataset/
│   ├── movies.csv          # 100 movies with metadata and local poster paths
│   └── ratings.csv         # 246 user ratings across 10 taste personas
│
├── src/
│   ├── data_loader.py      # Ingestion, matrix creation & history extraction
│   ├── content_based.py    # TF-IDF & Cosine Similarity recommender
│   ├── collaborative.py    # Truncated SVD matrix factorization & evaluation
│   └── hybrid.py           # Hybrid blending engine with cold-start handler
│
├── static/
│   ├── css/style.css       # Green & Black sleek UI styling
│   ├── js/app.js           # Interactive search & recommendations logic
│   └── posters/            # 100 local, high-res verified movie posters
│
├── templates/
│   └── index.html          # Clean HTML5 web dashboard
│
├── app.py                  # FastAPI web server
├── run_pipeline.py         # Terminal ML evaluation pipeline
├── test_api.py             # Automated test suite
├── movie_recommender.ipynb # Academic Jupyter Notebook for submission
├── PROJECT_REPORT.md       # Full academic project documentation & Viva Q&A
└── requirements.txt        # Python package dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git
cd "Movie Recommendation System"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:8000`**

### 4. Run the Terminal Machine Learning Pipeline
```bash
python run_pipeline.py
```

---

## 📊 Evaluation Metrics

- **Total Movies**: 100 (40 Hollywood + 60 Bollywood)
- **Total User Ratings**: 246
- **Latent Factors ($k$)**: 5
- **Root Mean Squared Error (RMSE)**: ~1.10
- **Mean Absolute Error (MAE)**: ~0.87
