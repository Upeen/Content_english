# Streamlit Cloud Deployment Guide

## Breaking News Finder

This guide covers deploying to **Render** (Recommended for stability) and **Streamlit Cloud**.

---

## ☁️ Deploying to Render (Recommended)

Render is excellent for production because it supports **Persistent Disks** and custom environment variables.

### Configuration Files
I have already set up the following for you:
- **`render.yaml`**: Standard configuration file for Render blue/green deployments.
- **`Procfile`**: Tells Render how to run the Streamlit server.
- **`runtime.txt`**: Pins the Python version for stability.

### Deployment Instructions
1.  Push your code to GitHub.
2.  Connect the repository to **Render**.
3.  Use the `render.yaml` template or manually set the start command to:
    `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
4.  (Optional) Attach a **Disk** pointing to the `/data` folder to keep your news cache.

---

## 🎈 Deploying to Streamlit Cloud

## Prerequisites

1. **GitHub Account** - Push your code to a GitHub repository
2. **Streamlit Cloud Account** - Sign up at streamlit.io/cloud

---

## Project Structure for Deployment

```
breaking-news-finder/
├── app.py              # Main Streamlit app (REQUIRED)
├── config.py           # Configuration
├── sitemap_parser.py  # Data fetching
├── nlp_engine.py      # NLP analysis
├── data_store.py      # Data persistence
├── requirements.txt   # Dependencies (REQUIRED)
├── .streamlit/
│   └── config.toml    # Theme settings
├── .gitignore         # Git ignore file
└── README.md          # Documentation
```

---

## Deployment Steps

### 1. Push to GitHub

```bash
# Navigate to project directory
cd breaking-news-finder

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub, then
git remote add origin https://github.com/yourusername/breaking-news-finder.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to **streamlit.io/cloud**
2. Click **New app**
3. Select your GitHub repository
4. Set branch: `main`
5. Set main file path: `app.py`
6. Click **Deploy!**

---

## Configuration

### Environment Variables (Optional)

In Streamlit Cloud settings, you can configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOOKBACK_HOURS` | Default lookback window | 48 |

### Secrets (Optional)

If you need API keys or external services, add them in Streamlit Cloud **Secrets** section.

---

## Important Notes

### Data Persistence

- **Streamlit Cloud has ephemeral filesystem** - data is lost on app restart
- For production, consider:
  - External database (PostgreSQL, MongoDB)
  - Cloud storage (AWS S3, Google Cloud Storage)
  - External API for data fetching

### Current Architecture

The app uses local JSON files for caching (`data/news_data.json`, `data/analysis_results.json`). These are:
- Created on first run
- Persisted while app is running
- **Lost when app restarts on Streamlit Cloud**

### For Production Use

1. **Replace data_store.py** to use cloud storage
2. **Add periodic data refresh** using Streamlit's `st.experimental_singleton` or external schedulers
3. **Consider adding authentication** if needed

---

## Local Development

### Quick Start

```bash
cd breaking-news-finder
pip install -r requirements.txt
streamlit run app.py
```

### Or use provided scripts

```powershell
.\start.ps1
```

```bash
./start.sh
```

---

## Troubleshooting

### App not loading
- Check GitHub repository is public
- Verify requirements.txt is correct
- Check app.py for import errors

### Data not appearing
- This is expected on first deploy (no cached data)
- Click "Fetch & Analyze" button to load data

### Errors after deployment
- Check Streamlit Cloud logs
- Verify all Python modules are included
- Ensure imports in app.py match actual file names
