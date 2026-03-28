#!/bin/bash
# Build and run with Docker Compose

set -e

ENVIRONMENT="${1:-development}"

echo "🐳 Building PathOs with Docker"
echo "==============================="
echo "Environment: $ENVIRONMENT"
echo ""

if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "development" ]; then
    echo "📦 Building development images..."
    docker-compose build backend-dev frontend-dev
    
    echo "🚀 Starting development servers..."
    docker-compose --profile dev up
else
    echo "📦 Building production images..."
    docker-compose build backend frontend
    
    echo "🚀 Starting production servers..."
    docker-compose up
fi
