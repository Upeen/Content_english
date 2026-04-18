# 🚀 Step-by-Step Render Deployment Process

Follow these exact steps to host your **Breaking News Finder** on Render.

---

### Phase 1: Preparation

1. **GitHub**: Ensure your code is pushed to your GitHub repository.
2. **Files Check**: Confirm these files exist in your root directory:
    * `render.yaml`
    * `Procfile`
    * `requirements.txt`
    * `runtime.txt`

---

### Phase 2: Render Dashboard Setup

1. **Login**: Go to [dashboard.render.com](https://dashboard.render.com).
2. **Create Service**: Click the blue **"New +"** button and select **Web Service**.
3. **Connect Repo**: Select your `Breaking News Finder` repository.
4. **Configure Settings**: Fill in the fields as follows:

| Field | Value |
| :--- | :--- |
| **Name** | `breaking-news-finder` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |

---

### Phase 3: Environment Variables (Optional)

If you want to customize the behavior of the app, add these under the **Environment** tab:

| Key | Description | Default |
| :--- | :--- | :--- |
| `DEFAULT_DAYS_BACK` | Number of days to look back for news | `3` |
| `DATA_DIR` | Directory to store JSON results | `data` |

---

### Phase 4: Data Persistence (Recommended)

Since Render has an ephemeral filesystem, your fetched news will be lost whenever the app restarts.

1. Go to the **Disk** tab.
2. Click **Add Disk**.
3. **Name**: `news-data`
4. **Mount Path**: `/opt/render/project/src/data` (matches your `DATA_DIR`)
5. **Size**: `1 GB` (Free tier is enough)

---

### Phase 5: Monitoring

1. Watch the logs. You should see `Collecting dependencies`, `Building`, and finally `Live`.
2. Click the URL provided at the top (e.g., `https://breaking-news-finder.onrender.com`).

---

### ✅ Success Checklist

* [ ] Does the "Coverage Race" dashboard load?
* [ ] Does clicking "Fetch & Analyze" successfully pull news?
* [ ] (If using Disk) Does the data stay there after you restart the service?

---

### 🛠 Troubleshooting

* **"Port Busy" or "Connection Timeout"**: Verify the **Start Command** has `--server.port $PORT`.
* **"Read-only File System"**: Ensure the `data/` folder is either part of a Disk or that the app has write permissions (default is usually fine).
* **NLTK/Sklearn errors**: These are handled by `requirements.txt`. If a specific model is missing, it will download on the first run.
