#!/bin/bash

# ===========================================
# Breaking News Finder - Startup Script
# Zee Gujarati Competitor Analysis Tool
# ===========================================

echo "📰 Breaking News Finder"
echo "========================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -f ".packages_installed" ]; then
    echo "📥 Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch .packages_installed
        echo "✅ Dependencies installed successfully."
    else
        echo "❌ Failed to install dependencies."
        exit 1
    fi
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data
fi

# Start Streamlit
echo "🚀 Starting Streamlit server..."
if [ -n "$PORT" ]; then
    echo "🌐 Running in cloud environment on port $PORT"
    python -m streamlit run app.py --server.port "$PORT" --server.address 0.0.0.0 --server.headless true
else
    echo "🌐 Running locally on port 8501"
    python -m streamlit run app.py --server.headless false --browser.gatherUsageStats false
fi
