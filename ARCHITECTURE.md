# PathOs Architecture

## Overview

PathOs is a topological abstraction layer for understanding IoT, code structures, and social engineering patterns through dialectical analysis. The system analyzes code as a topological space, detects structural contradictions, and synthesizes interpretations via Claude AI.

## Architecture Layers

### Layer 1: Domain/Core

The pure domain logic representing the topological model.

- **`pathos/core/graph.py`** - `TopologyGraph`
  - Represents code as a directed simplicial complex
  - Nodes: symbolic units (functions, classes, modules)
  - Edges: relations (calls, imports, inherits, etc.)
  - Methods for detecting cycles, SCCs, unreachable nodes

- **`pathos/core/parser.py`** - `CodeParser`
  - Tree-sitter based parsing for multiple languages
  - Two-pass approach: definitions → references
  - Support for Python and JavaScript (extensible)

- **`pathos/core/contradiction.py`** - `ContradictionDetector`
  - Detects topological contradictions
  - Types: circular dependencies, dead code, deep chains, entangled clusters
  - Each mapped to Lacanian registers (Symbolic/Imaginary/Real)

### Layer 2: AI/Synthesis

Interpretation and synthesis layer.

- **`pathos/ai/claude.py`** - `ClaudeSynthesizer`
  - Anthropic Claude integration
  - Interprets contradictions as structural tensions
  - Provides narrative analysis rather than automated fixes

### Layer 3: Infrastructure

Cross-cutting concerns and system configuration.

#### Configuration System (`pathos/infrastructure/config/`)

- **`settings.py`** - Environment-based configuration
  - `ApiConfig`: Server settings (host, port, CORS)
  - `ModelConfig`: LLM parameters
  - `ParserConfig`: Language support settings
  - `CacheConfig`: Caching behavior
  - `LoggingConfig`: Logging configuration
  - `Settings`: Root configuration dataclass
  - `get_settings()`: Load from environment
  - `load_settings()`: Singleton pattern

Environment variables:
```
ENVIRONMENT=development|testing|production
API_HOST=0.0.0.0
API_PORT=5000
ANTHROPIC_API_KEY=...
LOG_FILE=logs/pathos.log
LOG_LEVEL=DEBUG|INFO|WARNING
```

#### Logging System (`pathos/infrastructure/logging/`)

- **`logger.py`** - Centralized logging
  - `configure_logging()`: Set up structured logging
  - `get_logger()`: Get named loggers
  - Supports console and file handlers
  - Rotating file handler with 10MB max

#### Plugin System (`pathos/infrastructure/plugins/`)

- **`base.py`** - Plugin abstractions
  - `LanguagePlugin`: Extensible language support
  - `AnalysisPlugin`: Extensible analysis strategies
  - `PluginRegistry`: Plugin discovery and registration

### Layer 4: Services

High-level orchestration of domain logic.

- **`pathos/services/analysis_service.py`** - `AnalysisService`
  - Orchestrates parsing → contradiction detection → synthesis
  - Methods:
    - `analyze_file()`: Single file
    - `analyze_directory()`: Recursive directory
    - `analyze_code_string()`: String input
    - `analyze_file_dict()`: Multiple files (dict)
  - Returns `AnalysisResult` with graph, contradictions, interpretations
  - `AnalysisOptions`: Control synthesis behavior

### Layer 5: API

REST API layer with proper separation of concerns.

#### API Structure

```
/api/
  v1/
    analysis.py    # Analysis endpoints
    visualization.py  # Graph visualization
```

#### Endpoints

- `POST /analyze/code` - Analyze code/files
  - Request: `{files: {...}, code: "...", language: "...", interpret: bool}`
  - Response: `{summary, graph, contradictions}`

- `POST /analyze/github` - Analyze GitHub repository
  - Request: `{url: "...", interpret: bool}`
  - Response: `{summary, graph, contradictions, source, url}`

- `POST /graph/visualization` - D3.js formatted graph
  - Request: `{files: {...}}`
  - Response: `{nodes, links, summary}`

- `GET /health` - Health check
- `GET /` - API documentation

#### Error Handling

- Centralized error handlers
- Structured JSON responses
- Logging of all errors
- Request/response validation

### Layer 6: CLI

Command-line interface using Click.

- **`pathos/cli.py`** - CLI commands
  - `pathos check <path>` - Analyze code
  - `--interpret` - Single Claude interpretation
  - `--all-interpret` - All contradictions
  - Uses `AnalysisService` internally
  - Rich terminal output with tables and panels

## Frontend Architecture

### Structure

```
pathos-ui/
  types/           # TypeScript types
  context/         # React context
  hooks/           # Custom React hooks
  lib/             # Utilities
  components/      # React components
  app/             # Next.js app
```

### State Management

**`context/AnalysisContext.tsx`**
- Global analysis state
- Mode (code/github)
- Results and loading state
- Error handling

**Hooks**
- `useApi()` - API communication
- `useAnalysisOrchestrator()` - High-level analysis orchestration

### Types (`types/index.ts`)

```typescript
GraphNode, GraphEdge, Contradiction
TopoGraphySummary
AnalysisResponse
AnalysisMode, CodeEditorState, GitHubInputState
```

### Utilities (`lib/utils.ts`)

- `groupBy<T, K>()` - Grouping utility
- `formatBytes()` - Byte formatting
- `formatDuration()` - Duration formatting

## Data Flow

### Analysis Flow

```
    Input (code/file/github)
         ↓
    CodeParser (tree-sitter)
         ↓
    TopologyGraph (build AST)
         ↓
    ContradictionDetector (detect issues)
         ↓
    [Optional] ClaudeSynthesizer
         ↓
    AnalysisResult (aggregated)
         ↓
    REST/CLI Output
```

### Request Flow (API)

```
HTTP Request
    ↓
Route Handler (v1/analysis.py or v1/visualization.py)
    ↓
AnalysisService (orchestration)
    ↓
Domain Logic (Parser, Graph, Detector, Synthesizer)
    ↓
JSON Response
```

## Configuration & Deployment

### Development

```bash
# Run API
python -m pathos.api    # Or: flask --app pathos.api run

# Run CLI
pathos check <path>

# Run frontend
cd pathos-ui && npm run dev
```

### Docker Deployment

```bash
# All services
docker-compose up

# Backend only
docker-compose build backend
docker-compose run backend

# Development with watch
docker-compose --profile dev up backend-dev frontend-dev
```

### Environment Setup

Create `.env`:
```
ENVIRONMENT=development
ANTHROPIC_API_KEY=sk-...
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=DEBUG
```

## Extension Points

### Adding Language Support

1. Implement `LanguagePlugin` in `infrastructure/plugins/`
2. Register with `PluginRegistry`
3. Update `CodeParser` to use plugin
4. Add to `LANGUAGES` dict

### Adding Analysis Strategy

1. Implement `AnalysisPlugin`
2. Register with `PluginRegistry`
3. Call from service layer

### Adding API Endpoints

1. Create route handler in `api/v1/`
2. Register blueprint in `api/__init__.py`
3. Follow error handling patterns

## Testing

Tests organized by layer:

- `tests/conftest.py` - Shared fixtures
- `tests/test_analysis_service.py` - Service layer
- `tests/test_config.py` - Configuration
- `tests/sample_contradictions.py` - Domain samples

Run tests:
```bash
pytest tests/
pytest tests/test_analysis_service.py::test_analyze_code_string
```

## Key Principles

1. **Separation of Concerns** - Each layer has clear responsibilities
2. **Dependency Injection** - Services are injected, not created
3. **Configuration Over Code** - Behavior via environment/config
4. **Extensibility** - Plugin system for languages and analysis
5. **Error Handling** - Structured errors with logging
6. **Type Safety** - Type hints throughout Python, TypeScript in frontend
7. **Documentation** - Code is self-documenting with docstrings

## Monitoring & Logging

- Structured logging with `logging` module
- Log levels: DEBUG, INFO, WARNING, ERROR
- File and console handlers
- Rotating file handler (10MB max)
- API health endpoint at `/health`

## Future Enhancements

- [ ] Caching layer for repeated analyses
- [ ] Result persistence (database)
- [ ] Real-time WebSocket updates
- [ ] Advanced visualization with Three.js
- [ ] Multi-language plugin ecosystem
- [ ] Performance metrics and profiling
- [ ] Advanced contradiction synthesis
