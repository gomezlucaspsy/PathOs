# Extending PathOs: Plugin Development Guide

## Plugin System Overview

PathOs uses a plugin architecture for extensibility:

```
PluginRegistry
├─ LanguagePlugin (for code parsing)
└─ AnalysisPlugin (for custom analysis)
```

## Adding Language Support

### Step 1: Create Language Plugin

Create a new file: `pathos/infrastructure/plugins/python_plugin.py`

```python
from __future__ import annotations
from typing import Any
from tree_sitter import Language, Parser, Node
import tree_sitter_python as tspython

from pathos.infrastructure.plugins import LanguagePlugin
from pathos.core.graph import CodeNode, CodeEdge, NodeKind, EdgeKind, TopologyGraph

class PythonLanguagePlugin(LanguagePlugin):
    """Python language support via tree-sitter."""
    
    @property
    def language_name(self) -> str:
        return "python"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".py"]
    
    def __init__(self):
        language = Language(tspython.language())
        self._parser = Parser(language)
    
    def parse(self, source: bytes, path: str) -> dict[str, Any]:
        """Parse Python source code."""
        tree = self._parser.parse(source)
        
        # Extract nodes and edges
        nodes = []
        edges = []
        
        # Your parsing logic here...
        # Walk the tree, extract definitions and calls
        
        return {
            "nodes": nodes,
            "edges": edges,
        }
    
    def get_parser(self):
        """Return the underlying parser."""
        return self._parser
```

### Step 2: Register Plugin

In `pathos/infrastructure/plugins/__init__.py`:

```python
from pathos.infrastructure.plugins.python_plugin import PythonLanguagePlugin

def register_builtin_plugins():
    """Register built-in plugins."""
    registry = get_registry()
    registry.register_language(PythonLanguagePlugin())

# Call during initialization
register_builtin_plugins()
```

### Step 3: Update Parser

Modify `pathos/core/parser.py` to use plugins:

```python
class CodeParser:
    def detect_language(self, path: Path) -> str | None:
        """Detect language using plugin registry."""
        registry = get_registry()
        plugin = registry.get_language_plugin_by_extension(path.suffix.lower())
        return plugin.language_name if plugin else None
    
    def parse_file(self, path: Path, graph: TopologyGraph) -> None:
        """Parse using appropriate plugin."""
        registry = get_registry()
        plugin = registry.get_language_plugin_by_extension(path.suffix.lower())
        
        if plugin is None:
            return
        
        source = path.read_bytes()
        result = plugin.parse(source, str(path))
        
        for node_dict in result["nodes"]:
            graph.add_node(CodeNode(**node_dict))
        
        for edge_dict in result["edges"]:
            graph.add_edge(CodeEdge(**edge_dict))
```

### Step 4: Implement Custom Parser

Example: Go language plugin

```python
# pathos/infrastructure/plugins/go_plugin.py

from pathos.infrastructure.plugins import LanguagePlugin

class GoLanguagePlugin(LanguagePlugin):
    @property
    def language_name(self) -> str:
        return "go"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".go"]
    
    def parse(self, source: bytes, path: str) -> dict[str, Any]:
        """Parse Go source code."""
        # Use tree-sitter-go or custom parser
        tree = self._parser.parse(source)
        
        nodes = []
        edges = []
        
        # Extract functions, structs, interfaces
        # Extract imports, function calls, struct fields
        
        return {"nodes": nodes, "edges": edges}
```

## Adding Analysis Plugins

### Step 1: Create Analysis Plugin

Create `pathos/infrastructure/plugins/metrics_plugin.py`:

```python
from pathos.infrastructure.plugins import AnalysisPlugin

class MetricsAnalysisPlugin(AnalysisPlugin):
    """Compute code metrics."""
    
    @property
    def plugin_name(self) -> str:
        return "metrics"
    
    def analyze(self, graph: Any) -> list[dict[str, Any]]:
        """Compute metrics on graph."""
        from pathos.core.graph import TopologyGraph
        
        findings = []
        
        # Cyclometric complexity
        cyclomatic = len(graph.cycles())
        
        # Coupling metrics
        avg_degree = sum(g.degree for g in graph._graph.nodes()) / len(graph._graph.nodes()) if graph._graph.nodes() else 0
        
        # Cohesion metrics
        sccs = graph.strongly_connected_components()
        
        findings.append({
            "name": "Code Metrics",
            "metrics": {
                "cyclomatic_complexity": cyclomatic,
                "average_coupling": avg_degree,
                "scc_count": len(sccs),
            }
        })
        
        return findings
```

### Step 2: Register Plugin

```python
from pathos.infrastructure.plugins.metrics_plugin import MetricsAnalysisPlugin

def register_builtin_plugins():
    registry = get_registry()
    registry.register_analysis(MetricsAnalysisPlugin())
```

### Step 3: Use in Service

Update `AnalysisService`:

```python
class AnalysisService:
    def _finalize_analysis(self, graph, options):
        # ... existing code ...
        
        # Run analysis plugins
        registry = get_registry()
        for plugin_name in registry.list_analysis_plugins():
            plugin = registry.get_analysis_plugin(plugin_name)
            findings = plugin.analyze(graph)
            result.additional_findings[plugin_name] = findings
        
        return result
```

## Best Practices

### 1. Plugin Interface Compliance

- Implement all abstract methods
- Document expected behavior
- Follow naming conventions
- Support edge cases gracefully

### 2. Error Handling

```python
def parse(self, source: bytes, path: str) -> dict[str, Any]:
    try:
        tree = self._parser.parse(source)
        nodes, edges = self._extract(tree, path)
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        logger.warning(f"Parse error in {path}: {e}")
        return {"nodes": [], "edges": []}  # Graceful fallback
```

### 3. Performance Considerations

- Cache parser instances
- Handle large files (use streaming if needed)
- Profile expensive operations

### 4. Documentation

```python
class MyLanguagePlugin(LanguagePlugin):
    """Support for MyLanguage.
    
    Extracts:
    - Functions and methods
    - Classes and structs
    - Module imports
    - Function calls
    - Property references
    
    Limitations:
    - Macros not supported
    - Generic types simplified
    """
```

## Testing Plugins

Create `tests/test_my_plugin.py`:

```python
import pytest
from pathos.infrastructure.plugins.my_plugin import MyPlugin

def test_plugin_registration():
    plugin = MyPlugin()
    assert plugin.language_name == "mylang"
    assert ".myl" in plugin.file_extensions

def test_basic_parsing():
    plugin = MyPlugin()
    source = b"function foo() { }"
    result = plugin.parse(source, "test.myl")
    
    assert len(result["nodes"]) >= 1
    assert result["nodes"][0]["name"] == "foo"

def test_error_handling():
    plugin = MyPlugin()
    bad_source = b"this is not valid code !!! {{{{"
    result = plugin.parse(bad_source, "bad.myl")
    
    assert isinstance(result, dict)
    assert "nodes" in result
```

## Publishing Plugins

### Community Plugin Workflow

1. Create repository: `pathos-plugin-<language>`
2. Follow plugin interface
3. Include comprehensive tests
4. Document in README
5. Submit PR to PathOs with plugin registry entry

### Distribution

```python
# setup.py or pyproject.toml for plugin package
[project]
name = "pathos-plugin-rust"
entry-points = "pathos.plugins"

[project.entry-points."pathos.plugins"]
rust = "pathos_plugin_rust:RustLanguagePlugin"
```

## Advanced: Custom Graph Analysis

Extend `ContradictionDetector`:

```python
# pathos/infrastructure/plugins/advanced_detector.py

from pathos.core.contradiction import Contradiction, ContradictionKind

class AdvancedDetector(AnalysisPlugin):
    @property
    def plugin_name(self) -> str:
        return "advanced"
    
    def analyze(self, graph) -> list[dict]:
        findings = []
        
        # Custom contradiction detection
        problematic = self._find_god_objects(graph)
        findings.extend(problematic)
        
        # Custom metrics
        metrics = self._compute_metrics(graph)
        findings.append(metrics)
        
        return findings
    
    def _find_god_objects(self, graph):
        """Detect overly large, coupled classes."""
        findings = []
        
        for node_id, node in graph._graph.nodes(data=True):
            in_degree = graph._graph.in_degree(node_id)
            out_degree = graph._graph.out_degree(node_id)
            
            if in_degree + out_degree > 50:  # Threshold
                findings.append({
                    "type": "god_object",
                    "node": node_id,
                    "coupling": in_degree + out_degree,
                })
        
        return findings
```

## Roadmap

Plugins to implement:

- [ ] TypeScript/JavaScript (enhanced)
- [ ] Java/Kotlin support
- [ ] C/C++ support (basic)
- [ ] Rust support
- [ ] GraphQL schema analysis
- [ ] API endpoint dependency analysis
- [ ] Database schema dependency mapping
- [ ] CI/CD configuration analysis

## Plugin Resources

- **Tree-Sitter**: https://tree-sitter.github.io/tree-sitter/
- **Available Parsers**: https://github.com/topics/tree-sitter-grammar
- **Grammar Development**: https://tree-sitter.github.io/tree-sitter/creating-parsers
