#!/bin/bash

# Meno Match - Frontend Start Script

cd "$(dirname "$0")"

echo "🚀 Starting Meno Match Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Dependencies not found. Installing..."
    npm install
fi

echo "Starting dev server on http://localhost:3000"
echo "Backend API: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev
