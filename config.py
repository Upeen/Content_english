import os

# Fetching & Lookback (Unified Time Span)
DEFAULT_DAYS_BACK = int(os.getenv("DEFAULT_DAYS_BACK", 3))
DATA_DIR = os.getenv("DATA_DIR", "data")

COMPETITORS = {
    "Navbharat Times": {
        "sitemap": "https://navbharattimes.indiatimes.com/staticsitemap/nbt/news/sitemap-48hours.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "AAJTAK.IN": {
        "sitemap": "https://www.aajtak.in/rssfeeds/news-sitemap.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "JAGRAN.COM": {
        "sitemap": "https://www.jagran.com/news-sitemap.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "ABP Live Hindi": {
        "sitemap": "https://www.abplive.com/news-19-04-2026.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "NDTV.IN": {
        "sitemap": "https://ndtv.in/sitemap.xml?yyyy=2026&mm=3&sitename=ndtv-khabar&category=",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "LiveHindustan": {
        "sitemap": "https://www.livehindustan.com/news-sitemap.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "News18 Hindi": {
        "sitemap": "https://hindi.news18.com/allstory-sitemap-data.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "INDIATV.IN": {
        "sitemap": "https://www.indiatv.in/xmlsitemap/sitemap/generic-articles-2026-04-19.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "TIMESNOWHINDI.COM": {
        "sitemap": "https://www.timesnowhindi.com/feeds/tnhindi-google-news-sitemap.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "JANSATTA.COM": {
        "sitemap": "https://www.jansatta.com/sitemap.xml?yyyy=2026&mm=04&dd=19",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "TV9HINDI.COM": {
        "sitemap": "https://www.tv9hindi.com/sitemap.xml?yyyy=2026&mm=04&dd=19",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "ZeeNews Hindi": {
        "sitemap": "https://zeenews.india.com/hindi/sitemaps/news-sitemap.xml",
        "fetch_strategy": "direct",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
    "Zee Delhi NCR": {
        "sitemap": "https://zeenews.india.com/hindi/sitemaps/delhi-haryana-{yyyy}-{mmm}-sitemap.xml",
        "fetch_strategy": "date_based",
        "days_to_fetch": DEFAULT_DAYS_BACK
    },
}
# Data storage
JSON_STORE_FILE = os.path.join(DATA_DIR, "news_data.json")
ANALYSIS_STORE_FILE = os.path.join(DATA_DIR, "analysis_results.json")

# Parsing settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2
CHUNK_SIZE = 500  # Process articles in chunks for memory optimization

# NLP settings
MIN_SIMILARITY_THRESHOLD = 0.35
HIGH_SIMILARITY_THRESHOLD = 0.65
TOP_KEYWORDS_COUNT = 20
NGRAM_RANGE = (1, 3)

# Fetching & Lookback
# Controlled globally at the top of the file via DEFAULT_DAYS_BACK
