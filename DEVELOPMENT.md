# Development Guide

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 20+
- Git

### Setup

1. **Backend Setup**

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# or: source venv/bin/activate  # Unix

# Install dependencies
pip install -e ".[dev]"

# Setup environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

2. **Frontend Setup**

```bash
cd pathos-ui
npm install
```

3. **Run Development Servers**

```bash
# Terminal 1 - Backend API
python -m pathos.api

# Terminal 2 - Frontend
cd pathos-ui
npm run dev
```

Visit http://localhost:3000

## File Structure Overview

```
PathOs/
├── pathos/                    # Python backend
│   ├── core/                  # Domain logic
│   │   ├── graph.py          # Topology graph
│   │   ├── parser.py         # Code parsing
│   │   └── contradiction.py  # Contradiction detection
│   ├── ai/                    # AI integration
│   │   └── claude.py         # Claude synthesis
│   ├── infrastructure/        # Cross-cutting concerns
│   │   ├── config/           # Configuration management
│   │   ├── logging/          # Logging setup
│   │   └── plugins/          # Plugin system
│   ├── services/              # Orchestration layer
│   │   └── analysis_service.py
│   ├── api/                   # REST API
│   │   ├── __init__.py       # App factory
│   │   └── v1/               # API v1
│   │       ├── analysis.py
│   │       └── visualization.py
│   ├── cli.py                # CLI commands
│   └── __init__.py
│
├── pathos-ui/                 # Next.js frontend
│   ├── types/                # TypeScript types
│   ├── context/              # React context
│   ├── hooks/                # Custom hooks
│   ├── lib/                  # Utilities
│   ├── components/           # React components
│   ├── app/                  # Next.js routes
│   │   ├── api/             # API routes
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.ts
│
├── tests/                     # Test suite
│   ├── conftest.py           # Fixtures
│   ├── test_analysis_service.py
│   ├── test_config.py
│   └── sample_contradictions.py
│
├── Docker files
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── .env.example              # Environment template
├── .env                      # Local (git-ignored)
├── pyproject.toml           # Python project config
├── README.md                # Project overview
└── ARCHITECTURE.md          # This architecture doc
```

## Commands

### Backend

```bash
# Run API server
python -m pathos.api

# Run as module
python -m pathos.api --host 0.0.0.0 --port 5000

# CLI: Analyze code
pathos check <file_or_directory>
pathos check . --interpret
pathos check . --all-interpret

# Tests
pytest tests/
pytest tests/test_analysis_service.py -v
pytest tests/ -k "test_analyze" --collect-only
```

### Frontend

```bash
cd pathos-ui

# Development
npm run dev          # http://localhost:3000
npm run build        # Production build
npm start            # Run production build
npm run lint         # Lint code
```

### Docker

```bash
# Build all
docker-compose build

# Run production
docker-compose up

# Run development
docker-compose --profile dev up

# Logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Shell access
docker-compose exec backend bash
docker-compose exec frontend bash
```

## Development Workflow

### Adding a Feature

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Backend changes**
   - Keep domain logic in `core/`
   - Add services to `services/`
   - Add API routes to `api/v1/`
   - Add tests in `tests/`
   - Update `ARCHITECTURE.md`

3. **Frontend changes**
   - Add types to `types/index.ts`
   - Add hooks to `hooks/`
   - Add components to `components/`
   - Use context from `context/`

4. **Test changes**
   ```bash
   pytest tests/
   cd pathos-ui && npm run lint
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/my-feature
   ```

### Debugging

**Backend**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugger in IDE
# Configure: python -m debugpy --listen 5678 -m pathos.api
```

**Frontend**
```typescript
// Add debugging
console.log('Debug:', value);

// Use React DevTools browser extension
// Check Network tab for API calls
```

**Logs**
```bash
# View real-time logs
tail -f logs/pathos.log

# Backend logs
grep "ERROR" logs/pathos.log
grep "pathos.services" logs/pathos.log
```

## Configuration

### Environment Variables

```bash
# Deployment
ENVIRONMENT=development|testing|production

# API
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# LLM
ANTHROPIC_API_KEY=sk-...
MODEL_NAME=claude-opus-4-5
MODEL_MAX_TOKENS=1024

# Parser
PARSER_MAX_FILE_SIZE_MB=10
PARSER_SKIP_NODE_MODULES=true
PARSER_SKIP_GIT=true

# Caching
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600

# Logging
LOG_FILE=logs/pathos.log
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
LOG_CONSOLE=true
```

### Configuration Hierarchy

1. `.env` file (highest priority)
2. Environment variables
3. Defaults in code (lowest priority)

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_analysis_service.py

# Run specific test
pytest tests/test_analysis_service.py::test_analyze_code_string

# Verbose output
pytest tests/ -v

# Show print statements
pytest tests/ -s

# Coverage
pytest tests/ --cov=pathos
```

### Test Fixtures

Standard fixtures available in `tests/conftest.py`:
- `temp_dir` - Temporary directory
- `simple_graph` - Basic graph
- `circular_graph` - Graph with cycles

## Performance

### Profiling

```bash
# CPU profiling
python -m cProfile -s cumtime -m pathos.api

# Memory profiling
pip install memory-profiler
python -m memory_profiler pathos/api.py
```

### Optimization

- Tree-sitter parsing is O(n)
- Cycle detection is O(V + E)
- Use `@cache` decorator for repeated operations
- Implement result caching system

## Troubleshooting

### Import Errors

```bash
# Reinstall in development mode
pip install -e .

# Add to PYTHONPATH
export PYTHONPATH=$PWD
```

### Claude API Issues

```bash
# Verify API key
echo $ANTHROPIC_API_KEY

# Test API
python -c "from pathos.ai.claude import ClaudeSynthesizer; print('OK')"
```

### Parser Issues

```bash
# Check tree-sitter parsers
python -c "import tree_sitter_python; print('Python OK')"
python -c "import tree_sitter_javascript; print('JavaScript OK')"
```

### Frontend Issues

```bash
# Clear cache
rm -rf .next node_modules
npm install && npm run build

# Check environment
echo $NEXT_PUBLIC_API_URL
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style
- Commit messages
- Pull request process
- Issue reporting
