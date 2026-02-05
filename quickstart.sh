#!/bin/bash

# Meno Match - Quick Start Script

echo "🚀 Starting Meno Match Setup"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✓ Python 3 found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi
echo "✓ Node.js found"

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd packages/backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate

echo "  Installing dependencies..."
pip install -r requirements.txt --quiet

echo "✓ Backend setup complete"

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd ../frontend

echo "  Installing dependencies..."
npm install --silent

echo "✓ Frontend setup complete"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd packages/backend"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd packages/frontend"
echo "  npm run dev"
echo ""
echo "📍 Access the app at: http://localhost:3000"
echo "📚 API docs at: http://localhost:3001/docs"
