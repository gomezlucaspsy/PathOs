"""Test fixtures and utilities."""

import pytest
from pathlib import Path
import tempfile
from typing import Generator

from pathos.core.graph import TopologyGraph, CodeNode, NodeKind


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def simple_graph() -> TopologyGraph:
    """A simple graph for testing."""
    graph = TopologyGraph()
    
    # Add some nodes
    graph.add_node(CodeNode(
        id="main",
        kind=NodeKind.FUNCTION,
        name="main",
        language="python",
        source_file="app.py",
        line_start=1,
        line_end=10,
    ))
    
    graph.add_node(CodeNode(
        id="helper",
        kind=NodeKind.FUNCTION,
        name="helper",
        language="python",
        source_file="app.py",
        line_start=12,
        line_end=20,
    ))
    
    return graph


@pytest.fixture
def circular_graph() -> TopologyGraph:
    """A graph with circular dependencies."""
    from pathos.core.graph import CodeEdge, EdgeKind
    
    graph = TopologyGraph()
    
    # Create a cycle: A -> B -> C -> A
    for name in ["A", "B", "C"]:
        graph.add_node(CodeNode(
            id=name,
            kind=NodeKind.FUNCTION,
            name=name,
            language="python",
            source_file="app.py",
            line_start=1,
            line_end=10,
        ))
    
    # Add edges to create cycle
    graph.add_edge(CodeEdge("A", "B", EdgeKind.CALLS))
    graph.add_edge(CodeEdge("B", "C", EdgeKind.CALLS))
    graph.add_edge(CodeEdge("C", "A", EdgeKind.CALLS))
    
    return graph
