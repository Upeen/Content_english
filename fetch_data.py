import sys, os
sys.path.insert(0, os.getcwd())
try:
    from sitemap_parser import fetch_all_competitors
    from nlp_engine import run_full_analysis
    from data_store import save_articles, save_analysis
    from config import DEFAULT_LOOKBACK_DAYS

    print(f"Fetching data for last {DEFAULT_LOOKBACK_DAYS} days...")
    all_articles = fetch_all_competitors(hours=DEFAULT_LOOKBACK_DAYS * 24)
    if all_articles:
        save_articles(all_articles)
        analysis = run_full_analysis(all_articles)
        save_analysis(analysis)
        print(f"Fetch completed successfully. {len(all_articles)} articles saved.")
    else:
        print("No articles found!")
except Exception as e:
    print(f"Error: {e}")
