#!/bin/bash

# Installation script for Meno Match

set -e

echo "📦 Installing Meno Match"
echo ""

# Install backend dependencies
echo "Installing Backend Dependencies..."
cd packages/backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install packages
echo "Installing Python packages..."
pip install --upgrade pip setuptools wheel --quiet
pip install -r requirements.txt --quiet

echo "✓ Backend dependencies installed"

# Install frontend dependencies
echo ""
echo "Installing Frontend Dependencies..."
cd ../frontend

echo "Installing npm packages..."
npm install --silent

echo "✓ Frontend dependencies installed"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo ""
echo "1. Set up PostgreSQL database:"
echo "   docker-compose up -d"
echo ""
echo "2. Initialize database (in one terminal):"
echo "   cd packages/backend"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "3. Start frontend (in another terminal):"
echo "   cd packages/frontend"
echo "   npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
