#!/bin/bash
# Run all tests

set -e

echo "🧪 Running PathOs Tests"
echo "======================="
echo ""

# Python tests
echo "📝 Python tests..."
pytest tests/ -v --tb=short

# Frontend linting
echo ""
echo "✅ Frontend linting..."
cd pathos-ui
npm run lint
cd ..

echo ""
echo "✅ All tests passed!"
