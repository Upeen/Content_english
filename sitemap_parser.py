"""
Optimized Sitemap Parser - Extracts news articles from XML sitemaps
Handles multiple sitemap formats (index sitemaps, news sitemaps, standard sitemaps)
with chunked processing for large datasets.
"""

import requests
import time
import logging
from datetime import datetime, timedelta, timezone
from lxml import etree
from dateutil import parser as dateparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from config import COMPETITORS, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Common XML namespaces used across news sitemaps
NAMESPACES = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "news": "http://www.google.com/schemas/sitemap-news/0.9",
    "image": "http://www.google.com/schemas/sitemap-image/1.1",
    "video": "http://www.google.com/schemas/sitemap-video/1.1",
}


def fetch_url(url: str, retries: int = MAX_RETRIES) -> Optional[bytes]:
    """Fetch URL content with retry logic, exponential backoff, and WAF bypass using curl_cffi."""
    try:
        from curl_cffi import requests as cffi_requests
        has_cffi = True
    except ImportError:
        has_cffi = False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=0.9,gu;q=0.8",
    }
    for attempt in range(retries):
        try:
            # Use curl_cffi to transparently bypass Akamai/Cloudflare for known strict sites or retries
            if has_cffi and ("zeenews" in url or attempt > 0):
                response = cffi_requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, impersonate="chrome110")
            else:
                response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{retries} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    logger.error(f"All {retries} attempts failed for {url}")
    return None


def parse_datetime(date_str: str) -> Optional[datetime]:
    """Parse various datetime formats into timezone-aware datetime."""
    if not date_str or not date_str.strip():
        return None
    try:
        dt = dateparser.parse(date_str.strip())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def extract_text(element, xpath: str, namespaces: dict) -> str:
    """Safely extract text from an XML element using xpath."""
    found = element.xpath(xpath, namespaces=namespaces)
    if found and found[0].text:
        return found[0].text.strip()
    return ""


def parse_news_sitemap(xml_content: bytes, source_name: str, cutoff_time: datetime) -> List[Dict]:
    """
    Parse a news sitemap XML and extract articles from the last 24 hours.
    Handles both standard sitemaps and Google News sitemaps.
    """
    articles = []
    try:
        root = etree.fromstring(xml_content)
    except etree.XMLSyntaxError as e:
        logger.error(f"XML parse error for {source_name}: {e}")
        return articles

    # Auto-detect namespaces from the root element
    ns = {}
    for prefix, uri in root.nsmap.items():
        if prefix is None:
            ns["sm"] = uri
        else:
            ns[prefix] = uri

    # Ensure we have the sitemap namespace
    if "sm" not in ns:
        ns["sm"] = NAMESPACES["sm"]
    if "news" not in ns:
        ns["news"] = NAMESPACES.get("news", "")
    if "image" not in ns:
        ns["image"] = NAMESPACES.get("image", "")

    # Find all URL entries
    url_elements = root.xpath("//sm:url", namespaces=ns)
    if not url_elements:
        # Try without namespace (some sitemaps don't use namespaces)
        url_elements = root.xpath("//url")

    for url_elem in url_elements:
        article = extract_article_data(url_elem, ns, source_name, cutoff_time)
        if article:
            articles.append(article)

    logger.info(f"[{source_name}] Extracted {len(articles)} articles from last 24h")
    return articles


def extract_article_data(url_elem, ns: dict, source_name: str, cutoff_time: datetime) -> Optional[Dict]:
    """Extract article data from a single URL element."""
    # Get the URL
    loc = extract_text(url_elem, "sm:loc", ns)
    if not loc:
        loc_elems = url_elem.xpath("loc")
        loc = loc_elems[0].text.strip() if loc_elems and loc_elems[0].text else ""
    if not loc:
        return None

    # Get last modification date
    lastmod = extract_text(url_elem, "sm:lastmod", ns)
    if not lastmod:
        lastmod_elems = url_elem.xpath("lastmod")
        lastmod = lastmod_elems[0].text.strip() if lastmod_elems and lastmod_elems[0].text else ""

    # Get news-specific data
    title = ""
    pub_date_str = ""
    keywords = ""
    news_name = ""

    # Try Google News sitemap format
    news_elems = url_elem.xpath("news:news", namespaces=ns) if "news" in ns and ns["news"] else []
    if not news_elems:
        news_elems = url_elem.xpath("n:news", namespaces={"n": NAMESPACES["news"]})

    if news_elems:
        news_elem = news_elems[0]
        # Title
        title_elems = news_elem.xpath("news:title", namespaces=ns)
        if not title_elems:
            title_elems = news_elem.xpath("n:title", namespaces={"n": NAMESPACES["news"]})
        if title_elems and title_elems[0].text:
            title = title_elems[0].text.strip()

        # Publication date extraction with multiple fallbacks
        pub_elems = news_elem.xpath("news:publication_date", namespaces=ns)
        if not pub_elems:
            pub_elems = news_elem.xpath("n:publication_date", namespaces={"n": NAMESPACES["news"]})
        if not pub_elems:
            pub_elems = news_elem.xpath(".//*[local-name()='publication_date']")
            
        if pub_elems and pub_elems[0].text:
            pub_date_str = pub_elems[0].text.strip()

        # Keywords
        kw_elems = news_elem.xpath("news:keywords", namespaces=ns)
        if not kw_elems:
            kw_elems = news_elem.xpath("n:keywords", namespaces={"n": NAMESPACES["news"]})
        if not kw_elems:
            kw_elems = news_elem.xpath(".//*[local-name()='keywords']")
        if kw_elems and kw_elems[0].text:
            keywords = kw_elems[0].text.strip()

        # Publication name
        pub_name_elems = news_elem.xpath("news:publication/news:name", namespaces=ns)
        if not pub_name_elems:
            pub_name_elems = news_elem.xpath("n:publication/n:name", namespaces={"n": NAMESPACES["news"]})
        if not pub_name_elems:
            pub_name_elems = news_elem.xpath(".//*[local-name()='name']")
        if pub_name_elems and pub_name_elems[0].text:
            news_name = pub_name_elems[0].text.strip()

    # Determine the best date to use
    best_date_str = pub_date_str or lastmod
    article_dt = parse_datetime(best_date_str) if best_date_str else None

    # If parsing failed, try once more with the raw string directly
    if not article_dt and best_date_str:
        try:
            # Aggressive parsing fallback
            import dateutil.parser as du_parser
            article_dt = du_parser.parse(best_date_str, fuzzy=True)
            if article_dt and article_dt.tzinfo is None:
                article_dt = article_dt.replace(tzinfo=timezone.utc)
        except Exception:
            article_dt = None

    # Filter by cutoff time (last 24 hours)
    if article_dt and article_dt < cutoff_time:
        return None

    # If no title, try to extract from URL
    if not title:
        title = extract_title_from_url(loc)

    # Get image URL if available
    image_url = ""
    if "image" in ns and ns["image"]:
        img_elems = url_elem.xpath("image:image/image:loc", namespaces=ns)
        if img_elems and img_elems[0].text:
            image_url = img_elems[0].text.strip()

    return {
        "source": source_name,
        "title": title,
        "url": loc,
        "published_at": article_dt.isoformat() if article_dt else "",
        "keywords": keywords,
        "publication_name": news_name or source_name,
        "image_url": image_url,
        "lastmod": lastmod,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def extract_title_from_url(url: str) -> str:
    """Extract a readable title from a URL path."""
    try:
        path = url.rstrip("/").split("/")[-1]
        # Remove file extensions
        path = path.rsplit(".", 1)[0] if "." in path else path
        # Replace hyphens/underscores with spaces
        title = path.replace("-", " ").replace("_", " ")
        return title.strip().title() if title else ""
    except Exception:
        return ""


def resolve_sitemap_index(xml_content: bytes, source_name: str) -> List[str]:
    """
    If the XML is a sitemap index, extract all child sitemap URLs.
    Returns list of sitemap URLs, or empty list if not an index.
    """
    try:
        root = etree.fromstring(xml_content)
    except etree.XMLSyntaxError:
        return []

    ns = {}
    for prefix, uri in root.nsmap.items():
        if prefix is None:
            ns["sm"] = uri
        else:
            ns[prefix] = uri
    if "sm" not in ns:
        ns["sm"] = NAMESPACES["sm"]

    # Check if this is a sitemap index
    sitemap_elems = root.xpath("//sm:sitemap/sm:loc", namespaces=ns)
    if not sitemap_elems:
        sitemap_elems = root.xpath("//sitemap/loc")

    urls = []
    for elem in sitemap_elems:
        if elem.text:
            urls.append(elem.text.strip())

    if urls:
        logger.info(f"[{source_name}] Found sitemap index with {len(urls)} child sitemaps")
    return urls


def fetch_competitor_articles(name: str, config: dict, cutoff_time: datetime) -> List[Dict]:
    """Fetch and parse articles for a single competitor."""
    logger.info(f"[{name}] Fetching sitemap: {config['sitemap']}")
    xml_content = fetch_url(config["sitemap"])
    if not xml_content:
        return []

    # Check if it's a sitemap index (contains links to other sitemaps)
    child_sitemaps = resolve_sitemap_index(xml_content, name)

    if child_sitemaps:
        # Fetch child sitemaps (limit to recent ones to ensure we cover the 3-day cutoff)
        all_articles = []
        for child_url in child_sitemaps[:10]:  # Limit to 10 most recent child sitemaps ensuring we hit 3+ days
            logger.info(f"[{name}] Fetching child sitemap: {child_url}")
            child_xml = fetch_url(child_url)
            if child_xml:
                articles = parse_news_sitemap(child_xml, name, cutoff_time)
                all_articles.extend(articles)
                
                # If we successfully pulled articles before, but this sitemap yields 0 valid articles 
                # based on our cutoff_time, it means we've scrolled too far back into the past.
                if len(all_articles) > 0 and len(articles) == 0:
                    break
        return all_articles
    else:
        # Direct news sitemap
        return parse_news_sitemap(xml_content, name, cutoff_time)


def fetch_all_competitors(hours: int = 24) -> List[Dict]:
    """
    Fetch articles from all competitors in parallel.
    Returns combined list of all articles from the last `hours` hours.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    all_articles = []

    # Use ThreadPoolExecutor for parallel fetching
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_name = {
            executor.submit(fetch_competitor_articles, name, config, cutoff_time): name
            for name, config in COMPETITORS.items()
        }

        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                articles = future.result()
                all_articles.extend(articles)
                logger.info(f"[{name}] Total articles collected: {len(articles)}")
            except Exception as e:
                logger.error(f"[{name}] Error during fetch: {e}")

    logger.info(f"Total articles from all competitors: {len(all_articles)}")
    return all_articles


if __name__ == "__main__":
    articles = fetch_all_competitors(hours=24)
    for a in articles[:5]:
        print(f"[{a['source']}] {a['title']} | {a['published_at']}")
    print(f"\nTotal: {len(articles)} articles")
