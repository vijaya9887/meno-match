#!/bin/bash

# Meno Match - Backend Start Script

cd "$(dirname "$0")"

echo "🚀 Starting Meno Match Backend..."
echo ""

# Activate venv if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Run quickstart.sh first."
    exit 1
fi

echo "Starting FastAPI server on http://localhost:3001"
echo "API Documentation: http://localhost:3001/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python run.py
