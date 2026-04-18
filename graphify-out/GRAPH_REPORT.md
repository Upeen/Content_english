# Graph Report - C:\Users\upens\OneDrive\Desktop\Vs code\Content  (2026-04-18)

## Corpus Check
- 8 files · ~7,838 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 77 nodes · 94 edges · 16 communities detected
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]

## God Nodes (most connected - your core abstractions)
1. `NewsAnalyzer` - 15 edges
2. `run_full_analysis()` - 10 edges
3. `extract_article_data()` - 6 edges
4. `fetch_competitor_articles()` - 5 edges
5. `ensure_data_dir()` - 4 edges
6. `combine_article_text()` - 4 edges
7. `parse_news_sitemap()` - 4 edges
8. `save_articles()` - 3 edges
9. `save_analysis()` - 3 edges
10. `clean_text()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Breaking News Finder - Streamlit Dashboard Zee Gujarati Competitor Analysis Tool` --uses--> `NewsAnalyzer`  [INFERRED]
  C:\Users\upens\OneDrive\Desktop\Vs code\Content\app.py → C:\Users\upens\OneDrive\Desktop\Vs code\Content\nlp_engine.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (13): ensure_data_dir(), get_data_freshness(), load_analysis(), load_articles(), Optimized JSON Data Store for Breaking News Finder Handles saving/loading of ne, Create data directory if it doesn't exist., Save articles to JSON file with metadata.     Overwrites previous data (each ru, Load articles from JSON file. (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (1): Breaking News Finder - Streamlit Dashboard Zee Gujarati Competitor Analysis Tool

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (4): NewsAnalyzer, Cluster articles into topics using DBSCAN on TF-IDF features., Extract keywords from a subset of texts., Core NLP analysis engine with optimized large-dataset handling.

### Community 3 - "Community 3"
Cohesion: 0.4
Nodes (5): clean_text(), combine_article_text(), NLP & ML Engine for Breaking News Finder - TF-IDF vectorization for text simila, Clean and normalize text for NLP processing., Combine title and keywords into a single text representation.

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (4): Generate overall analysis summary., Run the complete NLP analysis pipeline.     Returns a comprehensive analysis di, Prepare text data and build TF-IDF matrix., run_full_analysis()

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (3): Extract top keywords/n-grams using TF-IDF scores., Compare top keywords across all competitors., Analyze content gaps: which topics are covered by some competitors         but

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (3): Compute pairwise cosine similarity with chunked processing for large datasets., Find pairs of similar articles across different competitors.         Returns li, For similar article pairs, determine who published first.         Returns analy

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (6): extract_article_data(), extract_text(), parse_datetime(), Extract article data from a single URL element., Parse various datetime formats into timezone-aware datetime., Safely extract text from an XML element using xpath.

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (6): fetch_competitor_articles(), fetch_url(), If the XML is a sitemap index, extract all child sitemap URLs.     Returns list, Fetch and parse articles for a single competitor., Fetch URL content with retry logic and exponential backoff., resolve_sitemap_index()

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (3): fetch_all_competitors(), Optimized Sitemap Parser - Extracts news articles from XML sitemaps Handles mul, Fetch articles from all competitors in parallel.     Returns combined list of a

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Configuration for Breaking News Finder - Competitor Sitemap Sources

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (2): parse_news_sitemap(), Parse a news sitemap XML and extract articles from the last 24 hours.     Handl

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (2): extract_title_from_url(), Extract a readable title from a URL path.

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **33 isolated node(s):** `Configuration for Breaking News Finder - Competitor Sitemap Sources`, `Optimized JSON Data Store for Breaking News Finder Handles saving/loading of ne`, `Create data directory if it doesn't exist.`, `Save articles to JSON file with metadata.     Overwrites previous data (each ru`, `Load articles from JSON file.` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `config.py`, `Configuration for Breaking News Finder - Competitor Sitemap Sources`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `parse_news_sitemap()`, `Parse a news sitemap XML and extract articles from the last 24 hours.     Handl`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `extract_title_from_url()`, `Extract a readable title from a URL path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `fetch_data.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `start.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `test_date.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `NewsAnalyzer` connect `Community 2` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `Breaking News Finder - Streamlit Dashboard Zee Gujarati Competitor Analysis Tool` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `run_full_analysis()` connect `Community 4` to `Community 2`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **What connects `Configuration for Breaking News Finder - Competitor Sitemap Sources`, `Optimized JSON Data Store for Breaking News Finder Handles saving/loading of ne`, `Create data directory if it doesn't exist.` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._