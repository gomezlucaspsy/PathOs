#!/bin/bash
# Development setup script

set -e

echo "🚀 PathOs Development Setup"
echo "=============================="
echo ""

# Python setup
echo "📦 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate || . venv/Scripts/activate

echo "📚 Installing Python dependencies..."
pip install -e ".[dev]"

# Environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
fi

# Frontend setup
echo ""
echo "🎨 Setting up frontend..."
cd pathos-ui
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  Terminal 1 (Backend):"
echo "    source venv/bin/activate  # or: venv\\Scripts\\activate on Windows"
echo "    python run_dev.py"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd pathos-ui"
echo "    npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
