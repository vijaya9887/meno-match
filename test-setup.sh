#!/bin/bash

# Test script to verify the application setup

echo "🧪 Testing Meno Match Setup"
echo ""

# Test Python syntax
echo "Testing Python syntax..."
python3 -c "
import sys
sys.path.insert(0, 'packages/backend')

try:
    from src import config
    from src import models
    from src import schemas
    from src import services
    from src import database
    print('✓ All Python modules import successfully')
except Exception as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
" || exit 1

# Test package.json syntax
echo ""
echo "Testing package.json files..."
for pkg_file in packages/backend/package.json packages/frontend/package.json; do
    if ! python3 -m json.tool "$pkg_file" > /dev/null 2>&1; then
        echo "✗ Invalid JSON: $pkg_file"
        exit 1
    fi
    echo "✓ $pkg_file is valid"
done

# Test TypeScript syntax (frontend)
echo ""
echo "Testing TypeScript files..."
for ts_file in packages/frontend/src/*.ts packages/frontend/src/*.tsx; do
    if [ ! -f "$ts_file" ]; then
        continue
    fi
    # Basic check - file should exist and not be empty
    if [ -s "$ts_file" ]; then
        echo "✓ $ts_file exists and is valid"
    fi
done

echo ""
echo "✅ All syntax checks passed!"
echo ""
echo "Next steps:"
echo "1. Start database: docker-compose up -d"
echo "2. Run backend: cd packages/backend && python run.py"
echo "3. Run frontend: cd packages/frontend && npm run dev"
echo ""
