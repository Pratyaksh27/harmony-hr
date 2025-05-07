#!/bin/bash

echo "🔁 Starting backend..."
cd backend || exit

# Create venv if not present
if [ ! -d "venv" ]; then
  echo "🧪 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate it
source venv/bin/activate

# Install deps if needed
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
