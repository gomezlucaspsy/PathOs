from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import networkx as nx


class NodeKind(str, Enum):
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    VARIABLE = "variable"
    IMPORT = "import"


class EdgeKind(str, Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    INHERITS = "inherits"
    ASSIGNS = "assigns"
    DEFINES = "defines"


@dataclass
class CodeNode:
    id: str
    kind: NodeKind
    name: str
    language: str
    source_file: str
    line_start: int
    line_end: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeEdge:
    source: str
    target: str
    kind: EdgeKind
    metadata: dict[str, Any] = field(default_factory=dict)


class TopologyGraph:
    """
    Represents a codebase as a directed simplicial complex.

    Nodes are symbolic units (functions, classes, modules).
    Edges are relations (calls, imports, inherits).
    Invariant groups (cycles, strongly connected components) are
    the topological 'holes' — Lacanian lacks — in the system.
    """

    def __init__(self) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()

    def add_node(self, node: CodeNode) -> None:
        self._graph.add_node(
            node.id,
            kind=node.kind,
            name=node.name,
            language=node.language,
            source_file=node.source_file,
            line_start=node.line_start,
            line_end=node.line_end,
            metadata=node.metadata,
        )

    def add_edge(self, edge: CodeEdge) -> None:
        self._graph.add_edge(
            edge.source,
            edge.target,
            kind=edge.kind,
            metadata=edge.metadata,
        )

    def nodes(self) -> list[dict[str, Any]]:
        return [{"id": n, **self._graph.nodes[n]} for n in self._graph.nodes]

    def edges(self) -> list[dict[str, Any]]:
        return [
            {"source": u, "target": v, **self._graph.edges[u, v]}
            for u, v in self._graph.edges
        ]

    def cycles(self) -> list[list[str]]:
        """Detect topological holes: circular dependencies."""
        return list(nx.simple_cycles(self._graph))

    def strongly_connected_components(self) -> list[set[str]]:
        """SCCs larger than 1 are Borromean knot candidates — entangled units."""
        return [
            scc
            for scc in nx.strongly_connected_components(self._graph)
            if len(scc) > 1
        ]

    def unreachable_nodes(self) -> list[str]:
        """Nodes with no incoming edges and no outgoing edges — dead code."""
        return [
            n
            for n in self._graph.nodes
            if self._graph.in_degree(n) == 0 and self._graph.out_degree(n) == 0
        ]

    def dependency_depth(self) -> dict[str, int]:
        """Maximum depth from each node — measures symbolic chain length."""
        depths: dict[str, int] = {}
        for node in self._graph.nodes:
            try:
                paths = nx.single_source_shortest_path_length(self._graph, node)
                depths[node] = max(paths.values()) if paths else 0
            except nx.NetworkXError:
                depths[node] = 0
        return depths

    def summary(self) -> dict[str, Any]:
        return {
            "node_count": self._graph.number_of_nodes(),
            "edge_count": self._graph.number_of_edges(),
            "cycle_count": len(self.cycles()),
            "scc_count": len(self.strongly_connected_components()),
            "isolated_nodes": len(self.unreachable_nodes()),
        }
