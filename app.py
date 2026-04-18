"""
Breaking News Finder - Streamlit Dashboard
Zee Gujarati Competitor Analysis Tool
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import COMPETITORS, DEFAULT_DAYS_BACK
from sitemap_parser import fetch_all_competitors
from nlp_engine import NewsAnalyzer, run_full_analysis
from data_store import save_articles, load_articles, save_analysis, load_analysis, get_data_freshness

st.set_page_config(
    page_title="Breaking News Finder | Zee Gujarati",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGE_LATEST = "⏱ Latest Articles"
PAGE_COVERAGE = "🏁 Coverage Race"
PAGE_DUPLICATES = "🔁 Duplicate Content"
PAGE_DATE_WISE = "📅 Volume Intelligence"

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --primary: #2BD2FF;
        --secondary: #7000FF;
        --accent: #FF3D71;
        --bg-dark: #0A0A0F;
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-main: #E2E2E6;
        --text-dim: #9494B8;
        --glass-bg: rgba(15, 15, 25, 0.7);
    }

    html, body {
        font-size: 18px !important;
    }

    [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: var(--text-main);
        font-size: 1.1rem !important;
    }

    .stApp {
        background: #05050A;
        background-attachment: fixed;
    }

    /* Professional Glassmorphism */
    .stat-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 24px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        text-align: center;
        margin-bottom: 16px;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        border-color: rgba(43, 210, 255, 0.3);
        background: rgba(43, 210, 255, 0.05);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 15px rgba(43, 210, 255, 0.1);
    }

    .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.6rem;
        font-weight: 800;
        color: var(--primary);
        letter-spacing: -1.5px;
        filter: drop-shadow(0 0 12px rgba(43, 210, 255, 0.4));
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-top: 8px;
    }

    .section-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }

    .section-subtitle {
        color: var(--text-dim);
        font-size: 1.15rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    [data-testid="stSidebar"] {
        background: #05050A !important;
        backdrop-filter: blur(25px);
        border-right: 1px solid var(--card-border);
    }

    [data-testid="stSidebar"] {
        background: #05050A !important;
        backdrop-filter: blur(25px);
        border-right: 1px solid var(--card-border);
    }

    [data-testid="stSidebar"] section::-webkit-scrollbar {
        display: none;
    }

    [data-testid="stSidebar"] .stMarkdown h1 {
        background: linear-gradient(135deg, #2BD2FF, #BAFF29);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--secondary) 0%, #4D00B0 100%);
        color: white;
        border: none;
        padding: 0.85rem 1.6rem;
        border-radius: 14px;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 1rem;
        width: 100%;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, #0089FF 100%);
        color: #05050A;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(112, 0, 255, 0.4);
        opacity: 0.9;
    }

    .gradient-text-warm {
        background: linear-gradient(135deg, #2BD2FF, #BAFF29);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Hide standard Streamlit elements for a cleaner look */
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 6px 12px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
        margin-top: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent !important;
        border-radius: 30px !important;
        border: none !important;
        color: var(--text-dim) !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 0 24px !important;
        margin-right: 4px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: var(--text-main) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF2B5E 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4) !important;
    }

    .stTabs [aria-selected="true"] p {
        color: white !important;
        font-weight: 800 !important;
    }

    /* Remove the default underline */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Custom Tables Styling */
    .stDataFrame {
        border: 1px solid var(--card-border);
        border-radius: 12px;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 10px !important;
        color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def format_time_gap(seconds):
    if seconds == 0:
        return "🚀 First!"
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hrs > 0:
        return f"+{hrs}h {mins}m {secs}s"
    elif mins > 0:
        return f"+{mins}m {secs}s"
    else:
        return f"+{secs}s"


def parse_ts(pub_str):
    try:
        ts = pd.to_datetime(pub_str)
        if pd.isna(ts):
            return None
        return ts
    except Exception:
        return None


def render_frontend_table(df, key, column_config=None, filename="data.csv", hide_controls=False):
    import base64
    
    # ---- SESSION STATE ----
    search_key = f"{key}_search"
    view_key = f"{key}_view"
    
    if search_key not in st.session_state:
        st.session_state[search_key] = ""
    if view_key not in st.session_state:
        st.session_state[view_key] = "table"

    # ---- SEARCH FILTER ----
    filtered_df = df.copy()
    if st.session_state[search_key]:
        query = st.session_state[search_key].lower()
        filtered_df = df[df.astype(str).apply(lambda row: row.str.lower().str.contains(query).any(), axis=1)]

    # ---- DOWNLOAD CSV ----
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()

    # ---- UI HEADER ----
    pass

    # ---- SEARCH INPUT REMOVED ----
    pass

    # ---- VIEW TOGGLE ----
    # Account for custom CSS 18px font size when calculating height
    dynamic_height = (len(filtered_df) + 1) * 45 + 50
    if dynamic_height < 200: dynamic_height = 200 # Minimum height for header and a couple rows

    if st.session_state[view_key] == "table":
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            key=key,
            height=dynamic_height,
        )
    else:
        st.data_editor(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            key=f"{key}_editor",
            height=dynamic_height,
        )


def get_filters(key_prefix, include_hours=False):
    import datetime
    with st.expander("🔍 Filters & Tools", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            today = datetime.date.today()
            date_range = st.date_input("Date Range", value=(today - datetime.timedelta(days=DEFAULT_DAYS_BACK), today), key=f"{key_prefix}_date")
        with col2:
            all_sources = ["All"] + list(COMPETITORS.keys())
            source = st.selectbox("Source", all_sources, key=f"{key_prefix}_source")
        with col3:
            if include_hours:
                lookback = st.number_input("Last - Hours", min_value=1, max_value=168, value=4, key=f"{key_prefix}_hours")
                return date_range, source, lookback
    return date_range, source


with st.sidebar:
    st.markdown("# 📰 News Finder")
    st.caption("Competitor Analysis")
    
    freshness = get_data_freshness()
    if not freshness:
        st.warning("⚠️ No data loaded yet.")
    else:
        try:
            import pandas as pd
            dt_utc = pd.to_datetime(freshness, utc=True)
            now_utc = pd.Timestamp.now(tz="UTC")
            diff = now_utc - dt_utc
            seconds = int(diff.total_seconds())
            if seconds < 60: time_str = "Just now"
            elif seconds < 3600: time_str = f"{seconds // 60} mins ago"
            elif seconds < 86400: time_str = f"{seconds // 3600} hrs ago"
            else: time_str = f"{seconds // 86400} days ago"
            
            st.markdown(f'<div style="font-size: 0.75rem; color: #2BD2FF; background: rgba(43, 210, 255, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(43, 210, 255, 0.2); font-weight: 600;">💾 Updated {time_str}</div>', unsafe_allow_html=True)
            
            _arts = st.session_state.get("articles", [])
            if not _arts:
                _arts = load_articles()
            if _arts:
                _dates = [pd.to_datetime(a.get("published_at"), utc=True, errors="coerce") for a in _arts]
                _dates = [d for d in _dates if pd.notna(d)]
                if _dates:
                    min_dt = min(_dates).strftime("%d %b %H:%M")
                    max_dt = max(_dates).strftime("%d %b %H:%M")
                    st.markdown(f'<div style="font-size: 0.75rem; color: #BAFF29; background: rgba(186, 255, 41, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(186, 255, 41, 0.2); font-weight: 600; margin-top: 8px; text-align: center;">⏳ {min_dt} - {max_dt}</div>', unsafe_allow_html=True)
        except Exception:
            st.caption(f"💾 Freshness: {freshness}")
    
    st.divider()
    page = st.radio(
        "Navigate",
        [PAGE_COVERAGE, PAGE_DUPLICATES, PAGE_DATE_WISE, PAGE_LATEST],
        label_visibility="collapsed",
    )
    st.divider()
    
    fetch_btn = st.button("🚀 Fetch & Analyze", use_container_width=True, type="primary")
    load_btn = st.button("📂 Load Cached Data", use_container_width=True)


if fetch_btn:
    with st.status("🚀 Processing Competitor Scans...", expanded=True) as status:
        all_articles = fetch_all_competitors(hours=DEFAULT_DAYS_BACK * 24)
        if all_articles:
            save_articles(all_articles)
            analysis = run_full_analysis(all_articles)
            save_analysis(analysis)
            st.session_state.articles = all_articles
            st.session_state.analysis = analysis
            status.update(label=f"✅ Analysis Complete ({len(all_articles)} items)", state="complete")
        else:
            status.update(label="⚠️ No news found", state="error")

if load_btn or ("articles" not in st.session_state):
    arts = load_articles()
    if arts:
        st.session_state.articles = arts
        st.session_state.analysis = load_analysis()
        if load_btn: st.success(f"Loaded {len(arts)} entries")

articles = st.session_state.get("articles", [])
analysis = st.session_state.get("analysis", {})

if not articles:
    st.markdown('<div style="text-align:center; padding:150px 20px;"><div style="font-size:6rem; margin-bottom:32px;">📡</div><h3>Initialize Dataset</h3><p>Click Fetch or Load to begin.</p></div>', unsafe_allow_html=True)
    st.stop()


if page == PAGE_COVERAGE:
    st.markdown('<div class="section-title">🏁 Coverage Race</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Real-time delta analysis between competitor publications.</div>', unsafe_allow_html=True)

    local_date_range, local_source = get_filters("coverage")

    st.markdown("---")

    topic_query = st.text_input(
        "🔎 Search (Title, URL, Keywords)",
        placeholder="Type keyword to search across titles, URLs, or metadata...",
        key="coverage_query",
    )

    cov_start, cov_end = local_date_range if (local_date_range and len(local_date_range) == 2) else (None, None)

    if not topic_query:
        st.markdown(
            """<div style="text-align:center;padding:60px 20px;color:#5e5e78;">
            <div style="font-size:3rem;margin-bottom:12px;">🏁</div>
            <p>Enter a topic keyword above to see which competitors covered it first</p>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        query_tokens = set(re.sub(r"[^\w\s]", " ", topic_query.lower()).split())

        matched = []
        for a in articles:
            pub_str = a.get("published_at", "")
            if not pub_str:
                continue
            try:
                pub_date = pd.to_datetime(pub_str).date()
            except Exception:
                continue
            if cov_start and cov_end and not (cov_start <= pub_date <= cov_end):
                continue

            if local_source != "All" and a.get("source") != local_source:
                continue

            title_text = a.get("title", "").lower()
            keywords_text = a.get("keywords", "").lower()
            url_text = a.get("url", "").lower()
            
            # Accurate Word Matching
            matches_all = True
            for tok in query_tokens:
                if tok.isalnum():
                    pattern = rf"\b{re.escape(tok)}\b"
                    if not (re.search(pattern, title_text) or re.search(pattern, keywords_text) or re.search(pattern, url_text)):
                        matches_all = False
                        break
                else:
                    if tok not in title_text and tok not in keywords_text and tok not in url_text:
                        matches_all = False
                        break
            
            if matches_all:
                matched.append(a)

        if not matched:
            st.warning(f'No articles found for **"{topic_query}"** in the selected date range.')
        else:
            matched.sort(key=lambda x: x.get("published_at", ""))

            first_ts = parse_ts(matched[0].get("published_at", ""))
            first_source = matched[0].get("source", "Unknown")

            st.success(f'Found **{len(matched)}** articles covering **"{topic_query}"** — '
                       f'First reported by **{first_source}** at `{first_ts.strftime("%Y-%m-%d %H:%M") if first_ts else "N/A"}`')

            st.markdown("---")

            st.markdown("### 🥇 Competitor Speed Podium")
            channel_first = {}
            channel_story_count = {}
            for a in matched:
                ch = a.get("source", "Unknown")
                channel_story_count[ch] = channel_story_count.get(ch, 0) + 1
                if ch not in channel_first:
                    channel_first[ch] = a

            podium_list = sorted(channel_first.items(), key=lambda x: x[1].get("published_at", ""))

            medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
            medal_icons = ["🥇", "🥈", "🥉"]

            cols_per_row = 4
            num_channels = len(podium_list)
            
            for i in range(0, num_channels, cols_per_row):
                row_channels = podium_list[i:i + cols_per_row]
                row_cols = st.columns(cols_per_row)
                
                for idx, (ch, a) in enumerate(row_channels):
                    total_idx = i + idx
                    ts = parse_ts(a.get("published_at", ""))
                    delay_seconds = (ts - first_ts).total_seconds() if ts and first_ts else 0
                    
                    medal_color = medal_colors[total_idx] if total_idx < 3 else "#2d2d3d"
                    medal_icon = medal_icons[total_idx] if total_idx < 3 else "📺"
                    
                    with row_cols[idx]:
                        story_count = channel_story_count.get(ch, 0)
                        st.markdown(
                            f"""<div class="stat-card" style="border-color:{medal_color};border-width:2px; height:100%;">
                            <div class="stat-value" style="font-size:2.2rem;">{medal_icon}</div>
                            <div class="stat-value gradient-text-warm" style="font-size:1rem;margin-top:6px;">{ch}</div>
                            <div class="stat-label" style="margin-top:6px;">{ts.strftime('%H:%M, %d %b') if ts else 'N/A'}</div>
                            <div class="stat-label">{format_time_gap(delay_seconds)}</div>
                            <div class="stat-label">📰 {story_count} {'story' if story_count == 1 else 'stories'}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )

            st.markdown("---")

            st.markdown("### ⏱ Full Coverage Timeline")

            timeline_rows = []
            for rank, (ch, a) in enumerate(podium_list, start=1):
                ts = parse_ts(a.get("published_at", ""))
                delay_seconds = (ts - first_ts).total_seconds() if ts and first_ts else 0
                delay_str = format_time_gap(delay_seconds)

                timeline_rows.append({
                    "Rank": rank,
                    "Competitor": ch,
                    "Published At": ts.strftime("%Y-%m-%d %H:%M") if ts else "N/A",
                    "Time Gap": delay_str,
                    "Stories": channel_story_count.get(ch, 0),
                    "Title": a.get("title", "")[:80],
                    "URL": a.get("url", ""),
                })

            timeline_df = pd.DataFrame(timeline_rows)
            render_frontend_table(
                timeline_df,
                "coverage_timeline_table",
                filename="coverage_timeline.csv",
                column_config={
                    "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                }
            )

            st.markdown("---")

            st.markdown("### 📺 Chronological Feed")

            feed_data = []
            for a in matched:
                ts = parse_ts(a.get("published_at", ""))
                delay_seconds = (ts - first_ts).total_seconds() if ts and first_ts else 0
                delay_label = format_time_gap(delay_seconds)

                feed_data.append({
                    "Time Gap": delay_label,
                    "Competitor": a.get("source", ""),
                    "Published At": ts.strftime("%Y-%m-%d %H:%M") if ts else "",
                    "Title": a.get("title", ""),
                    "URL": a.get("url", ""),
                    "Keywords": a.get("keywords", ""),
                })

            feed_df = pd.DataFrame(feed_data)
            render_frontend_table(
                feed_df,
                "chronological_feed_table",
                filename="chronological_feed.csv",
                column_config={
                    "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                }
            )

elif page == PAGE_DUPLICATES:
    st.markdown('<div class="section-title">🔁 Duplicate Content</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">All duplicate content across competitors — who published first and the time gap</div>', unsafe_allow_html=True)

    import datetime as dt
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        today = dt.date.today()
        local_date_range = st.date_input("Date Range", value=(today - dt.timedelta(days=DEFAULT_DAYS_BACK), today), key="dup_date")
    with filter_col2:
        all_sources = ["All"] + list(COMPETITORS.keys())
        local_source = st.selectbox("Source", all_sources, key="dup_source")

    st.markdown("---")

    similar = analysis.get("similar_articles", []) if analysis else []

    cov_start, cov_end = local_date_range if (local_date_range and len(local_date_range) == 2) else (None, None)

    if local_source != "All":
        source_pairs = [
            p for p in similar
            if p["article_1"].get("source") == local_source or p["article_2"].get("source") == local_source
        ]
    else:
        source_pairs = similar

    filtered_pairs = []
    for pair in source_pairs:
        a1 = pair["article_1"]
        a2 = pair["article_2"]
        ts1 = parse_ts(a1.get("published_at", ""))
        ts2 = parse_ts(a2.get("published_at", ""))

        if cov_start and cov_end and ts1 and ts2:
            date1 = ts1.date()
            date2 = ts2.date()
            if not ((cov_start <= date1 <= cov_end) or (cov_start <= date2 <= cov_end)):
                continue

        filtered_pairs.append(pair)

    filtered_pairs.sort(key=lambda p: p.get("similarity_score", 0), reverse=True)

    topic_groups = {}
    for pair in filtered_pairs:
        a1 = pair["article_1"]
        a2 = pair["article_2"]

        ts1 = parse_ts(a1.get("published_at", ""))
        ts2 = parse_ts(a2.get("published_at", ""))

        key1 = a1.get("title", "")[:50]
        key2 = a2.get("title", "")[:50]
        topic_key = min(key1, key2)

        if topic_key not in topic_groups:
            topic_groups[topic_key] = []

        if ts1 and ts2:
            if ts1 < ts2:
                time_gap = (ts2 - ts1).total_seconds()
            else:
                time_gap = (ts1 - ts2).total_seconds()
        else:
            time_gap = 0

        topic_groups[topic_key].append({
            "article": a1,
            "ts": ts1,
            "time_gap": time_gap,
            "similarity": pair["similarity_score"],
        })
        topic_groups[topic_key].append({
            "article": a2,
            "ts": ts2,
            "time_gap": time_gap,
            "similarity": pair["similarity_score"],
        })

    grouped_results = []
    for topic, items in topic_groups.items():
        unique_articles = {}
        for item in items:
            art = item["article"]
            source = art.get("source", "")
            if source not in unique_articles:
                unique_articles[source] = item

        sorted_articles = sorted(
            [(source, data) for source, data in unique_articles.items() if data["ts"]],
            key=lambda x: x[1]["ts"]
        )

        if len(sorted_articles) > 1:
            first_ts = sorted_articles[0][1]["ts"]
            story_score = max(d["similarity"] for _, d in sorted_articles)
            grouped_results.append({
                "topic": topic,
                "publishers": sorted_articles,
                "first_ts": first_ts,
                "count": len(sorted_articles),
                "story_score": story_score,
            })

    grouped_results.sort(key=lambda x: x["story_score"], reverse=True)

    if not grouped_results:
        st.info("No duplicate content found in the current filters.")
    else:
        st.markdown("---")
        st.markdown("### Ranked Duplicates by Story")

        medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#2d2d3d", "#3d3d4d", "#4d4d5d", "#5d5d6d"]
        medal_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

        for g_idx, group in enumerate(grouped_results, start=1):
            all_sims = [data["similarity"] for _, data in group["publishers"]]
            max_sim = max(all_sims) if all_sims else 0

            st.markdown(
                f"""
                <div class="stat-card" style="text-align: left; padding: 20px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <span style="background: linear-gradient(135deg, var(--secondary), var(--accent)); color: white; font-weight: 800; font-size: 1.2rem; padding: 10px 16px; border-radius: 12px; min-width: 60px; text-align: center; box-shadow: 0 4px 15px rgba(112, 0, 255, 0.3);">
                                #{g_idx}
                            </span>
                            <div>
                                <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-main); margin-bottom: 4px;">{group['topic']}</div>
                                <div style="font-size: 0.9rem; color: var(--text-dim);">📡 Intelligence gathered from {group['count']} competitor sources</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div style="background: rgba(0, 242, 255, 0.1); border: 1px solid var(--primary); padding: 8px 16px; border-radius: 30px;">
                                <span style="color: var(--primary); font-weight: 800; font-size: 0.9rem;">
                                    ANALYSIS SCORE: {max_sim:.1%}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            cols_per_row = min(group["count"], 7)
            row_cols = st.columns(cols_per_row)

            for p_idx, (source, data) in enumerate(group["publishers"]):
                ts = data["ts"]
                delay_seconds = (ts - group["first_ts"]).total_seconds() if ts and group["first_ts"] else 0

                medal_color = medal_colors[p_idx] if p_idx < len(medal_colors) else "#2d2d3d"
                medal_icon = medal_icons[p_idx] if p_idx < len(medal_icons) else f"{p_idx+1}️⃣"

                with row_cols[p_idx]:
                    st.markdown(
                        f"""<div class="stat-card" style="border-color:{medal_color}; border-width:2px; padding:16px;">
                        <div class="stat-value" style="font-size:1.8rem;">{medal_icon}</div>
                        <div class="stat-label" style="color:var(--primary); font-size:0.8rem; margin-top:8px;">{source}</div>
                        <div style="font-size:0.75rem; color:var(--text-dim); margin-top:4px;">{ts.strftime('%H:%M, %d %b') if ts else 'N/A'}</div>
                        <div style="font-size:0.85rem; font-weight:600; color:var(--text-main); margin-top:4px;">{format_time_gap(delay_seconds)}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

            publishers_data = []
            for rank, (source, data) in enumerate(group["publishers"], start=1):
                art = data["article"]
                ts = data["ts"]
                delay_seconds = (ts - group["first_ts"]).total_seconds() if ts and group["first_ts"] else 0
                publishers_data.append({
                    "Rank": rank,
                    "Publisher": source,
                    "Published At": ts.strftime("%Y-%m-%d %H:%M") if ts else "N/A",
                    "Time Gap": format_time_gap(delay_seconds),
                    "Duplicate Score": f"{data['similarity']:.1%}",
                    "Title": art.get("title", "")[:60],
                    "URL": art.get("url", ""),
                })

            publisher_df = pd.DataFrame(publishers_data)
            render_frontend_table(
                publisher_df,
                f"duplicate_story_{g_idx}_table",
                filename=f"duplicate_story_{g_idx:03}.csv",
                column_config={
                    "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                },
                hide_controls=True,
            )

            st.markdown("---")

        st.markdown("### 📊 Summary Table")

        all_export_data = []
        for g_idx, group in enumerate(grouped_results):
            story_no = 101 + g_idx
            dup_sr_no = f"DUP{str(story_no)}"
            for rank, (source, data) in enumerate(group["publishers"], start=1):
                art = data["article"]
                ts = data["ts"]
                delay_seconds = (ts - group["first_ts"]).total_seconds() if ts and group["first_ts"] else 0
                all_export_data.append({
                    "Duplicate_Sr_no.": dup_sr_no,
                    "Rank": rank,
                    "Publisher": source,
                    "Published At": ts.strftime("%Y-%m-%d %H:%M") if ts else "N/A",
                    "Time Gap": format_time_gap(delay_seconds),
                    "Duplicate %": round(data["similarity"] * 100, 1),
                    "Title": art.get("title", ""),
                    "URL": art.get("url", ""),
                })

        export_df = pd.DataFrame(all_export_data)
        if not export_df.empty:
            export_df = export_df.sort_values("Duplicate %", ascending=False).reset_index(drop=True)

        render_frontend_table(
            export_df,
            "duplicate_summary_table",
            filename="duplicate_summary.csv",
            column_config={
                "Duplicate %": st.column_config.NumberColumn("Duplicate %", format="%.1f%%"),
                "URL": st.column_config.LinkColumn("Link", display_text="Open"),
            },
            hide_controls=True,
        )

elif page == PAGE_DATE_WISE:
    st.markdown('<div class="section-title">📅 Date-wise Story Count</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Chronological distribution of content volume across all monitored channels.</div>', unsafe_allow_html=True)

    import datetime as dt
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        today = dt.date.today()
        local_date_range = st.date_input("Date Range", value=(today - dt.timedelta(days=DEFAULT_DAYS_BACK), today), key="date_wise_date")
    with filter_col2:
        all_sources = ["All"] + list(COMPETITORS.keys())
        local_source = st.selectbox("Source", all_sources, key="date_wise_source")

    # ---- Scoreboard Logic ----
    cov_start, cov_end = local_date_range if (local_date_range and len(local_date_range) == 2) else (None, None)
    
    from collections import defaultdict
    sb_counts = defaultdict(int)
    total_count = 0
    
    for a in articles:
        ts = parse_ts(a.get("published_at", ""))
        if not ts: continue
        if cov_start and cov_end and not (cov_start <= ts.date() <= cov_end):
            continue
        sb_counts[a.get("source", "Unknown")] += 1
        total_count += 1
        
    sb_cards_html = f'''
    <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 20px; margin-bottom: 20px;">
        <div style="flex: 1 1 120px; background: linear-gradient(135deg, rgba(10,10,15,0.95), rgba(15,15,22,0.95)); border: 1px solid rgba(43,210,255,0.3); border-radius: 12px; padding: 15px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8rem; font-weight: 800; color: #2BD2FF; line-height: 1;">{total_count}</div>
            <div style="font-size: 0.70rem; color: #9898b0; font-weight: 700; text-transform: uppercase; margin-top: 6px;">All Channels</div>
        </div>
    '''
    for comp in sorted(COMPETITORS.keys()):
        val = sb_counts.get(comp, 0)
        sb_cards_html += f'''
        <div style="flex: 1 1 120px; background: linear-gradient(135deg, rgba(10,10,15,0.95), rgba(15,15,22,0.95)); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8rem; font-weight: 800; color: #f0f0f5; line-height: 1;">{val}</div>
            <div style="font-size: 0.70rem; color: #9898b0; font-weight: 700; text-transform: uppercase; margin-top: 6px;">{comp.replace(" Gujarati", "")}</div>
        </div>
        '''
    sb_cards_html += '</div>'
    st.markdown(sb_cards_html, unsafe_allow_html=True)

    filtered_articles = []
    for a in articles:
        ts = parse_ts(a.get("published_at", ""))
        if not ts:
            continue
        
        if local_source != "All" and a.get("source") != local_source:
            continue
        
        article_date = ts.date()
        
        if local_date_range and len(local_date_range) == 2:
            cov_start, cov_end = local_date_range
            if not (cov_start <= article_date <= cov_end):
                continue
        
        filtered_articles.append(a)

    if not filtered_articles:
        st.info("No articles found in the selected date range.")
    else:
        date_source_counts = {}
        for a in filtered_articles:
            ts = parse_ts(a.get("published_at", ""))
            if ts:
                date_key = ts.strftime("%Y-%m-%d")
                source = a.get("source", "Unknown")
                if date_key not in date_source_counts:
                    date_source_counts[date_key] = {}
                date_source_counts[date_key][source] = date_source_counts[date_key].get(source, 0) + 1

        all_dates = sorted(date_source_counts.keys(), reverse=True)
        all_sources_in_data = sorted(set(s for d in date_source_counts for s in date_source_counts[d].keys()))

        pivot_rows = []
        for source in all_sources_in_data:
            row = {"Channel": source}
            row_total = 0
            for date_key in all_dates:
                count = date_source_counts[date_key].get(source, 0)
                row[date_key] = count
                row_total += count
            row["Total"] = row_total
            pivot_rows.append(row)

        total_row = {"Channel": "**Day Total**"}
        grand_total = 0
        for date_key in all_dates:
            day_total = sum(date_source_counts[date_key].get(source, 0) for source in all_sources_in_data)
            total_row[date_key] = day_total
            grand_total += day_total
        total_row["Total"] = grand_total
        pivot_rows.append(total_row)

        pivot_df = pd.DataFrame(pivot_rows)
        pivot_df = pivot_df.set_index("Channel")
        pivot_df.index.name = None

        def styler_func(s, pivot_df=pivot_df):
            is_total_row = pivot_df.index[pivot_df.index.get_indexer([s.index[0]])[0]] == "**Day Total**"
            if is_total_row:
                return ['min-width: 120px; text-align: center; font-weight: bold; background: rgba(255,61,113,0.1);' for _ in s]
            return ['min-width: 120px; text-align: center;' for _ in s]

        styler = pivot_df.style.apply(styler_func).set_properties(**{
            'text-align': 'center',
            'border': '1px solid rgba(255,255,255,0.05)',
        }).set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center'), ('padding', '8px'), ('background', 'rgba(10,10,15,0.95)')]},
            {'selector': 'td', 'props': [('padding', '8px')]},
        ])

        pivot_height = (len(pivot_df) + 1) * 45 + 50

        st.dataframe(
            styler,
            use_container_width=True,
            height=pivot_height,
        )


elif page == PAGE_LATEST:
    st.markdown('<div class="section-title">⏱ Latest Articles</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Real-time feed of the most recently published content across all platforms.</div>', unsafe_allow_html=True)
    
    local_date_range, local_source, lookback_hours = get_filters("latest_tab", include_hours=True)
    
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    hour_threshold = now - timedelta(hours=lookback_hours)
    
    latest_articles = []
    start_date, end_date = local_date_range if (local_date_range and len(local_date_range) == 2) else (None, None)

    for a in articles:
        if local_source != "All" and a.get("source") != local_source:
            continue
            
        ts = pd.to_datetime(a.get("published_at"))
        if pd.isna(ts):
            continue
            
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
            
        if start_date and end_date:
            try:
                article_date = ts.date()
                if not (start_date <= article_date <= end_date):
                    continue
            except:
                continue
        
        if not start_date or start_date == now.date():
             if ts < hour_threshold:
                 continue
        
        latest_articles.append({
            "Published": ts.strftime("%Y-%m-%d"),
            "Time": ts.strftime("%I:%M %p"),
            "Channel": a.get("source"),
            "Title": a.get("title"),
            "URL": a.get("url"),
        })
            
    if not latest_articles:
        st.info("No articles found matching the current criteria.")
    else:
        latest_df = pd.DataFrame(latest_articles)
        latest_df = latest_df.sort_values(["Published", "Time"], ascending=False)
        
        st.success(f"Found **{len(latest_articles)}** articles.")
        
        sources = sorted(latest_df["Channel"].unique())
        
        if local_source != "All":
            st.markdown(f"### {local_source}")
            render_frontend_table(
                latest_df,
                f"latest_{local_source}_single_table",
                filename=f"latest_{local_source}.csv",
                column_config={
                    "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                    "Title": st.column_config.TextColumn("Title", width="large"),
                }
            )
        elif sources:
            all_count = len(latest_df)
            tab_names = [f"All Sources ({all_count})"]
            for s in sources:
                count = len(latest_df[latest_df["Channel"] == s])
                tab_names.append(f"{s} ({count})")
            
            tabs = st.tabs(tab_names)
            
            with tabs[0]:
                render_frontend_table(
                    latest_df,
                    "latest_all_combined_table",
                    filename="latest_all_sources.csv",
                    column_config={
                        "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                        "Title": st.column_config.TextColumn("Title", width="large"),
                    }
                )
            
            for i, source in enumerate(sources):
                with tabs[i+1]:
                    src_df = latest_df[latest_df["Channel"] == source]
                    render_frontend_table(
                        src_df,
                        f"latest_{source}_tab_table",
                        filename=f"latest_{source}.csv",
                        column_config={
                            "URL": st.column_config.LinkColumn("Link", display_text="Open"),
                            "Title": st.column_config.TextColumn("Title", width="large"),
                        }
                    )
        else:
            st.warning("No articles categorized by source found.")
