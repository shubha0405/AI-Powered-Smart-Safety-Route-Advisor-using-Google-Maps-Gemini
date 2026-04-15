#!/bin/bash

# Smart Safe Route Advisor - Quick Start Script

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "📱 Starting Smart Safe Route Advisor UI..."
echo "✨ Opening at http://localhost:8501"
echo ""

streamlit run ui/app.py
