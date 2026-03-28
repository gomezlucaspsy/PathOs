from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pathos.core.graph import TopologyGraph


class ContradictionKind(str, Enum):
    CIRCULAR_DEPENDENCY = "circular_dependency"
    DEAD_CODE = "dead_code"
    DEEP_CHAIN = "deep_chain"
    ENTANGLED_CLUSTER = "entangled_cluster"


@dataclass
class Contradiction:
    kind: ContradictionKind
    description: str
    nodes: list[str]
    severity: int  # 1=low, 2=medium, 3=high
    lacanian_register: str  # "Symbolic", "Imaginary", "Real"
    metadata: dict[str, Any]


class ContradictionDetector:
    """
    The dialectical engine.

    Reads the topology graph and surfaces structural contradictions —
    points where the Symbolic order (code structure) contains a 'lack':
    a hole, a loop, a dead end, a tangle.

    These are not bugs. They are structural tensions that require
    interpretation, not just fixing.
    """

    DEEP_CHAIN_THRESHOLD = 5

    def detect(self, graph: TopologyGraph) -> list[Contradiction]:
        contradictions: list[Contradiction] = []
        contradictions.extend(self._detect_circular_dependencies(graph))
        contradictions.extend(self._detect_dead_code(graph))
        contradictions.extend(self._detect_deep_chains(graph))
        contradictions.extend(self._detect_entangled_clusters(graph))
        return sorted(contradictions, key=lambda c: c.severity, reverse=True)

    # -------------------------------------------------------- Circular dependency

    def _detect_circular_dependencies(
        self, graph: TopologyGraph
    ) -> list[Contradiction]:
        results = []
        for cycle in graph.cycles():
            results.append(
                Contradiction(
                    kind=ContradictionKind.CIRCULAR_DEPENDENCY,
                    description=(
                        f"Circular dependency detected across {len(cycle)} nodes. "
                        f"The signifier chain folds back on itself — a topological loop "
                        f"where each element requires the next, which requires the first. "
                        f"Lacan's torus: desire circulating around an unfillable lack."
                    ),
                    nodes=cycle,
                    severity=3,
                    lacanian_register="Symbolic",
                    metadata={"cycle_length": len(cycle)},
                )
            )
        return results

    # ----------------------------------------------------------------- Dead code

    def _detect_dead_code(self, graph: TopologyGraph) -> list[Contradiction]:
        isolated = graph.unreachable_nodes()
        if not isolated:
            return []
        return [
            Contradiction(
                kind=ContradictionKind.DEAD_CODE,
                description=(
                    f"{len(isolated)} isolated node(s) detected — unreachable, uncalled, "
                    f"unconnected to the symbolic chain. These are the shadow of the codebase: "
                    f"what the system has defined but refuses to integrate. "
                    f"Hillman: the underworld of code, waiting to be reclaimed or released."
                ),
                nodes=isolated,
                severity=1,
                lacanian_register="Imaginary",
                metadata={"count": len(isolated)},
            )
        ]

    # ---------------------------------------------------------------- Deep chains

    def _detect_deep_chains(self, graph: TopologyGraph) -> list[Contradiction]:
        depths = graph.dependency_depth()
        deep = {n: d for n, d in depths.items() if d >= self.DEEP_CHAIN_THRESHOLD}
        if not deep:
            return []
        worst = max(deep, key=lambda n: deep[n])
        return [
            Contradiction(
                kind=ContradictionKind.DEEP_CHAIN,
                description=(
                    f"{len(deep)} node(s) have dependency depth >= {self.DEEP_CHAIN_THRESHOLD}. "
                    f"The deepest chain ({deep[worst]}) originates at '{worst}'. "
                    f"The Symbolic order has become overextended — "
                    f"each signifier defers meaning to the next, indefinitely. "
                    f"A chain this long means a rupture anywhere propagates everywhere."
                ),
                nodes=list(deep.keys()),
                severity=2,
                lacanian_register="Symbolic",
                metadata={"max_depth": max(deep.values()), "deepest_node": worst},
            )
        ]

    # ------------------------------------------------------------- Entangled clusters

    def _detect_entangled_clusters(
        self, graph: TopologyGraph
    ) -> list[Contradiction]:
        results = []
        for scc in graph.strongly_connected_components():
            if len(scc) >= 3:
                results.append(
                    Contradiction(
                        kind=ContradictionKind.ENTANGLED_CLUSTER,
                        description=(
                            f"Strongly connected cluster of {len(scc)} nodes detected. "
                            f"These units are mutually constitutive — Borromean: "
                            f"none can be understood independently of the others. "
                            f"The Real intrudes: this cluster cannot be fully symbolized "
                            f"without the whole holding together."
                        ),
                        nodes=list(scc),
                        severity=2,
                        lacanian_register="Real",
                        metadata={"cluster_size": len(scc)},
                    )
                )
        return results
