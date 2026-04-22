import os

# =========================
# CONFIG: Fetch & Lookback
# =========================
DEFAULT_LOOKBACK_DAYS = int(os.getenv("DEFAULT_DAYS_BACK", 1))
DATA_DIRECTORY = os.getenv("DATA_DIR", "data")

NEWS_SOURCES = {
    "india_today": {
        "sitemap_url": "https://www.indiatoday.in/news-it-sitemap.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "times_of_india": {
        "sitemap_url": "https://timesofindia.indiatimes.com/sitemap/today",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "news18": {
        "sitemap_url": "https://www.news18.com/commonfeeds/v1/eng/sitemap/google-news.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "india_tv": {
        "sitemap_url": "https://www.indiatvnews.com/news-sitemap.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "hindustan_times": {
        "sitemap_url": "https://www.hindustantimes.com/sitemap-news.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "zee_news": {
        "sitemap_url": "https://zeenews.india.com/sitemap.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "dainik_jagran": {
        "sitemap_url": "https://www.thedailyjagran.com/news-sitemap.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "the_hindu_businessline": {
        "sitemap_url": "https://www.thehindubusinessline.com/sitemap/googlenews/all/all.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "indian_express": {
        "sitemap_url": "https://indianexpress.com/sitemap/today.xml",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    },
    "ndtv": {
        "sitemap_url": "https://www.ndtv.com/sitemap/google-news-sitemap",
        "fetch_method": "direct",
        "lookback_days": DEFAULT_LOOKBACK_DAYS
    }
}

# =========================
# STORAGE CONFIG
# =========================
NEWS_DATA_FILE = os.path.join(DATA_DIRECTORY, "news_data.json")
ANALYSIS_RESULTS_FILE = os.path.join(DATA_DIRECTORY, "analysis_results.json")

# =========================
# NETWORK / PARSING CONFIG
# =========================
HTTP_REQUEST_TIMEOUT = 30
MAX_REQUEST_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2
PROCESSING_CHUNK_SIZE = 1000

# =========================
# NLP CONFIG
# =========================
SIMILARITY_THRESHOLD_MIN = 0.35
SIMILARITY_THRESHOLD_HIGH = 0.65
KEYWORD_TOP_N = 20
KEYWORD_NGRAM_RANGE = (1, 3)
