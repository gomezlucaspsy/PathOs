"# PathOs

A **topological abstraction layer** for understanding IoT, code structures, and social engineering patterns through dialectical analysis.

PathOs reads codebases as topological spaces, detects structural contradictions using graph theory and Lacanian psychoanalysis, and synthesizes interpretations via Claude AI.

## Key Concepts

- **Topology**: Code as simplicial complex — symbols as nodes, dependencies as edges, cycles as topological holes
- **Dialectical Materialism**: Contradictions (thesis/antithesis) drive synthesis and evolution
- **Lacanian Psychoanalysis**: The gap between Symbolic (syntax), Imaginary (intent), and Real (runtime) is constitutive
- **IoT & Social Engineering**: Analyzes not just code but system architectures and organizational patterns

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 20+

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/PathOs.git
cd PathOs

# Backend setup
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -e ".[dev]"

# Frontend setup
cd pathos-ui
npm install
cd ..

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY from https://console.anthropic.com
```

### Running Locally

**Terminal 1 - Backend API:**
```bash
source venv/bin/activate
python run_dev.py
# API running at http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd pathos-ui
npm run dev
# UI running at http://localhost:3000
```

### CLI Usage

```bash
# Analyze a file or directory
pathos check .

# With interpretation (calls Claude)
pathos check . --interpret

# Interpret all contradictions
pathos check . --all-interpret
```

### Docker Deployment

```bash
# Production
docker-compose up

# Development with watch mode
docker-compose --profile dev up
```

## Architecture Overview

PathOs is organized in **6 architectural layers**:

```
Layer 6: CLI Interface & REST API
         ↓
Layer 5: Services (Orchestration)
         ↓
Layer 4: Infrastructure (Config, Logging, Plugins)
         ↓
Layer 3: AI/Synthesis (Claude Integration)
         ↓
Layer 2: Domain (Graph Analysis, Contradiction Detection)
         ↓
Layer 1: Code Parsing (Tree-sitter)
```

### Key Components

| Layer | Module | Purpose |
|-------|--------|---------|
| **Domain** | `core/graph.py` | Topological graph model |
| | `core/parser.py` | Multi-language code parsing |
| | `core/contradiction.py` | Contradiction detection engine |
| **AI** | `ai/claude.py` | Interpretation synthesis |
| **Infrastructure** | `infrastructure/config/` | Configuration management |
| | `infrastructure/logging/` | Structured logging |
| | `infrastructure/plugins/` | Plugin system for extensibility |
| **Services** | `services/analysis_service.py` | Orchestration & business logic |
| **API** | `api/v1/` | REST endpoints |
| **CLI** | `cli.py` | Command-line interface |

## Contradiction Types

PathOs detects and interprets four types of structural contradictions:

### 1. **Circular Dependency**
Code forms cycles where A→B→C→A, preventing independent reasoning.
- **Lacanian Register**: Symbolic (structural)
- **Meaning**: Desire circulating around unfillable lack (Borromean knot)

### 2. **Dead Code**
Unreachable nodes: defined but never used.
- **Lacanian Register**: Imaginary (historical artifact)
- **Meaning**: The system's shadow; what it refuses to integrate

### 3. **Deep Chain**
Call chains exceeding threshold (default: 5 levels).
- **Lacanian Register**: Symbolic (mediation depth)
- **Meaning**: Excessive indirection; missing abstraction

### 4. **Entangled Cluster**
Strongly connected components: everything depends on everything.
- **Lacanian Register**: Real (behavioral entanglement)
- **Meaning**: Holistic coupling; cannot be reasoned about in parts

## API Endpoints

```bash
# Analyze code files
POST /analyze/code
{
  "files": {"app.py": "def foo(): ..."},
  "code": "string (alternative)",
  "language": "python",
  "interpret": true
}

# Analyze GitHub repository
POST /analyze/github
{
  "url": "https://github.com/user/repo",
  "interpret": true
}

# Get graph for visualization
POST /graph/visualization
{ "files": {...} }

# Health check
GET /health

# API docs
GET /
```

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed system design and layers
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development workflow and testing
- **[THEORY.md](THEORY.md)** - Topological and theoretical foundations
- **[PLUGINS.md](PLUGINS.md)** - Extending with custom plugins

## Theoretical Foundation

PathOs combines three theoretical frameworks:

### Topological Mathematics
Represents code as a **simplicial complex** with topological invariants:
- Holes (cycles in dependency graph)
- Components (strongly connected sets)
- Depth (longest paths from entry points)

### Dialectical Analysis
Uses **thesis-antithesis-synthesis** to understand contradictions:
- **Thesis**: Intended code structure
- **Antithesis**: Detected topological contradiction
- **Synthesis**: Claude's interpretation of structural tension

### Lacanian Psychoanalysis
Maps contradictions to three orders:
- **Symbolic**: Syntax and structural relationships
- **Imaginary**: Intent and developer's mental model
- **Real**: Actual runtime behavior

## Use Cases

### Code Analysis
- Detect architectural problems before they become critical
- Understand complex codebases through topological lens
- Identify refactoring opportunities

### Team Dynamics
- Analyze code ownership and knowledge distribution
- Detect single points of failure (key person dependencies)
- Understand team communication through code dependencies

### IoT Systems
- Analyze sensor networks as topological graphs
- Detect feedback loops and control issues
- Understand data flow in distributed systems

### Social Engineering
- Trace how code structure reflects organizational structure
- Identify isolated teams (topological isolation)
- Detect dependencies that create organizational friction

## Dependencies

### Backend
- `tree-sitter` - Code parsing
- `networkx` - Graph algorithms
- `anthropic` - Claude AI integration
- `flask` - REST API
- `click` - CLI framework
- `rich` - Terminal UI

### Frontend
- `next.js` - React framework
- `d3.js` - Graph visualization
- `three.js` - 3D visualization (optional)
- `react-syntax-highlighter` - Code display

## Contributing

1. Read [DEVELOPMENT.md](DEVELOPMENT.md)
2. Fork and create feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Run tests: `pytest tests/ && cd pathos-ui && npm run lint`
5. Commit: `git commit -m "feat: description"`
6. Push and create pull request

## Configuration

All behavior controlled via environment variables. See [.env.example](.env.example):

```bash
ENVIRONMENT=development          # deployment environment
ANTHROPIC_API_KEY=sk-...        # Claude API key
API_PORT=5000                   # API server port
LOG_LEVEL=DEBUG                 # logging level
PARSER_MAX_FILE_SIZE_MB=10      # parser limit
```

## Known Limitations

- JavaScript/TypeScript parsing is basic (contributes welcome!)
- Large monoliths (>5000 nodes) require optimization
- Claude synthesis requires valid API key
- Circular dependency detection is O(V+E) on first run

## Roadmap

- [ ] TypeScript/Node.js parsing improvements
- [ ] Java/Kotlin support
- [ ] Performance optimizations for large codebases
- [ ] Result caching and persistence
- [ ] Real-time WebSocket visualization
- [ ] Git history analysis (temporal topology)
- [ ] Team metrics integration
- [ ] Advanced 3D visualization

## License

MIT License - See LICENSE file

## Citation

```bibtex
@software{pathos2024,
  title={PathOs: Topological Abstraction Layer for Code Analysis},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/PathOs}
}
```

## Acknowledgments

- **Lacan, Jacques** - Lacanian topology and psychoanalytic theory
- **Hillman, James** - Archetypal psychology of systems
- **Griesemer, Rob & Pike, Ken** - Graph algorithms
- **Anthropic** - Claude AI for synthesis

## Support

- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas
- Documentation: See ARCHITECTURE.md and THEORY.md

---

**PathOs** transforms how we understand code. Not as sequences of instructions, but as topological spaces where contradictions reveal truth." 
