"""
Critical Conductism Plugin for PathOs

Analyzes ideological conductivity, resistance patterns, and autonomy frequencies
using Frankfurt School critical theory + electrical/resonance metaphor.

Theoretical Framework (Frankfurt School + Nikola Tesla):

1. IDEOLOGICAL CONDUCTIVITY (Adorno & Horkheimer)
   Power flows through administered, standardized pathways that foreclose alternatives.
   - Instrumental Rationality: code optimized for efficiency without questioning purpose
   - Reification: treating dynamic behaviors as static, unchangeable structures
   - Administered Society: patterns that reproduce dominant ideology
   
2. RESISTANCE & RECTIFICATION (Marcuse)
   Counter-dialectical patterns that interrupt administered thinking.
   - Critique of Instrumental Reason: code that exposes its own contradictions
   - One-Dimensional Thinking Detection: identifies foreclosed alternatives
   - Repressive Desublimation: code patterns that sublimate critical potential
   
3. FREQUENCY OF AUTONOMY (Habermas + Tesla)
   Critical consciousness (negating, dialogical) vs. administered consciousness.
   - Administered Thinking: conformist, predictable, standardized (synchronous)
   - Critical Thinking: resistant, dialectical, negating identity (asynchronous)
   - Communicative Rationality: code that enables authentic dialogue vs. mere transfer

Theory Sources:
- Adorno & Horkheimer: Dialectic of Enlightenment (Instrumental Rationality)
- Marcuse: One-Dimensional Man (Repressive Desublimation)
- Habermas: Theory of Communicative Action (System vs. Lifeworld)
- Tesla: Resonance, Conductivity, Autonomy Frequencies (Physics metaphor)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, List, Dict, Tuple
import networkx as nx

from pathos.infrastructure.plugins.base import AnalysisPlugin
from pathos.infrastructure.logging import get_logger

logger = get_logger("plugins.conductivity")


class LacunianRegister(Enum):
    """
    Three registers of psychoanalytic experience mapped to code architecture.
    """
    SYMBOLIC = "symbolic"      # Formal structure, rules, syntax
    IMAGINARY = "imaginary"    # Designer intent, patterns, ego-ideal
    REAL = "real"              # Runtime impossibility, entropy, actual behavior


class ConductivityLevel(Enum):
    """Conductivity assessment levels."""
    HIGHLY_CONDUCTIVE = "highly_conductive"      # Power flows smoothly
    MODERATELY_CONDUCTIVE = "moderately_conductive"  # Some friction
    RESISTANT = "resistant"                       # High friction, blocking
    CHAOTIC = "chaotic"                           # Non-linear, unpredictable


class AdministeredThinkingLevel(Enum):
    """
    Frankfurt School: Degree of administered/instrumental rationality.
    
    INSTRUMENTAL: Optimizes for efficiency alone; forecloses alternatives
    STRATEGIC: Purposive but not questioned; treats goals as given
    COMMUNICATIVE: Enables dialogue; questions its own assumptions
    CRITICAL: Negates administered thinking; opens alternatives
    """
    INSTRUMENTAL = "instrumental"          # Pure means-end rationality
    STRATEGIC = "strategic"                # Means-end with hidden ends
    COMMUNICATIVE = "communicative"        # Dialogical, consensual
    CRITICAL = "critical"                  # Self-negating, resistant


class ReificationMarker(Enum):
    """
    Lukács/MARXIST: Treating dynamic social processes as static things.
    
    Indicators in code:
    - Immutable by default (static data)
    - No feedback loops (one-way dependencies)
    - Hidden abstraction layers (reified complexity)
    - Singular paths vs. multiple valid solutions
    """
    IMMUTABLE_STRUCTURE = "immutable_structure"
    NO_FEEDBACK_LOOP = "no_feedback_loop"
    HIDDEN_COMPLEXITY = "hidden_complexity"
    SINGULAR_PATH = "singular_path"


@dataclass
class ConductivityMeasurement:
    """Quantifies ideological conductivity in a code node."""
    node_id: str
    resistance_level: float  # 0.0 (smooth, compliant) to 1.0 (resistant, chaotic)
    register: LacunianRegister
    conductivity_level: ConductivityLevel
    dominant_flow: str  # What power structure/pattern flows here?
    friction_points: List[str] = field(default_factory=list)
    centrality_score: float = 0.0  # How much does this control downstream?
    pattern_conformity: float = 0.0  # How much follows dominant patterns? (0-1)
    
    def is_high_conductivity(self) -> bool:
        """Returns True if power flows smoothly (low resistance)."""
        return self.resistance_level < 0.4
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dict."""
        return {
            "node_id": self.node_id,
            "resistance_level": round(self.resistance_level, 3),
            "register": self.register.value,
            "conductivity_level": self.conductivity_level.value,
            "dominant_flow": self.dominant_flow,
            "friction_points": self.friction_points,
            "centrality_score": round(self.centrality_score, 3),
            "pattern_conformity": round(self.pattern_conformity, 3),
        }


@dataclass
class ResistancePattern:
    """Detects where code resists dominant patterns."""
    node_id: str
    resistance_type: str  # "naming", "structure", "flow", "abstraction"
    description: str
    register: LacunianRegister
    severity: int  # 1-3: low to high
    contradiction_value: str  # What is this resisting?


@dataclass
class AutonomySignal:
    """Identifies authentic vs. imposed patterns."""
    node_id: str
    autonomy_score: float  # 0.0 (fully imposed) to 1.0 (purely authentic)
    pattern_type: str  # "conformist", "autonomous", "hybrid"
    register: LacunianRegister
    interpretation: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dict."""
        return {
            "node_id": self.node_id,
            "autonomy_score": round(self.autonomy_score, 3),
            "pattern_type": self.pattern_type,
            "register": self.register.value,
            "interpretation": self.interpretation,
        }


class ConductivityAnalyzer(AnalysisPlugin):
    """
    Analyzes power-flows and ideological structures through code using 
    electrical/resonance metaphor.
    
    Key insight: Behaviors flow along paths of least resistance.
    Dominant systems engineer low-resistance pathways to conformity.
    Resistance requires introducing friction, oscillation, and counter-frequency.
    """
    
    # Standard patterns that represent "conformity"
    CONFORMIST_PATTERNS = {
        "naming": ["get_", "set_", "init", "process_", "handle_", "on_"],
        "structure": ["MVC", "singleton", "factory", "decorator", "middleware"],
        "abstraction": ["class", "interface", "abstract"],
    }
    
    # Patterns that suggest autonomy/resistance
    AUTONOMOUS_PATTERNS = {
        "naming": ["custom_", "special_", "unique_", "_private", "custom"],
        "structure": ["plugin", "hook", "observer", "event", "callback"],
        "abstraction": ["protocol", "trait", "mixin", "context"],
    }
    
    @property
    def plugin_name(self) -> str:
        """Name of this analysis plugin."""
        return "critical_conductism"
    
    def __init__(self, graph: Any = None):
        """
        Initialize the analyzer.
        
        Args:
            graph: TopologyGraph instance (can be provided later via analyze())
        """
        self.graph = graph
        self.conductivity_map: Dict[str, ConductivityMeasurement] = {}
        self.resistance_patterns: List[ResistancePattern] = []
        self.autonomy_signals: List[AutonomySignal] = []
        self.administered_thinking_nodes: List[Dict[str, Any]] = []
        self.reification_markers: List[Dict[str, Any]] = []
        self.one_dimensional_patterns: List[Dict[str, Any]] = []
    
    def analyze(self, graph: Any) -> List[Dict[str, Any]]:
        """
        Run complete Critical Conductism analysis on the topology graph.
        
        Combines:
        - Conductivity mapping (power/efficiency flows)
        - Traditional contradiction detection (PathOs)
        - Frankfurt School critical analysis (ideology/administered thinking)
        
        Args:
            graph: TopologyGraph instance
            
        Returns:
            List of analysis findings as dicts
        """
        self.graph = graph
        logger.info("Starting Critical Conductism analysis (Frankfurt School)")
        
        # Run all analysis phases
        self._measure_all_conductivity()
        self._detect_resistance_patterns()
        self._measure_autonomy_frequencies()
        
        # Frankfurt School critical analysis
        self._detect_administered_thinking()
        self._detect_reification()
        self._detect_one_dimensional_thinking()
        
        # Compile findings
        findings = self._compile_findings()
        logger.info(f"Analysis complete: {len(findings)} findings")
        
        return findings
    
    def _measure_all_conductivity(self):
        """Measure conductivity for all nodes in the graph."""
        # Get underlying NetworkX graph from TopologyGraph wrapper
        nx_graph = self.graph._graph if hasattr(self.graph, '_graph') else self.graph
        
        node_ids = [n for n in nx_graph.nodes()]
        logger.debug(f"Measuring conductivity for {len(node_ids)} nodes")
        
        # Calculate centrality scores for all nodes
        try:
            betweenness = nx.betweenness_centrality(nx_graph)
        except Exception as e:
            logger.warning(f"Betweenness centrality failed: {e}")
            betweenness = {node: 0.0 for node in node_ids}
        
        try:
            closeness = nx.closeness_centrality(nx_graph)
        except Exception as e:
            logger.warning(f"Closeness centrality failed: {e}")
            closeness = {node: 0.0 for node in node_ids}
        
        for node_id in node_ids:
            measurement = self.measure_conductivity(
                node_id, 
                betweenness.get(node_id, 0.0),
                closeness.get(node_id, 0.0)
            )
            self.conductivity_map[node_id] = measurement
    
    def measure_conductivity(
        self, 
        node_id: str, 
        betweenness: float = 0.0,
        closeness: float = 0.0
    ) -> ConductivityMeasurement:
        """
        Measure ideological conductivity of a code node.
        
        High conductivity = power flows smoothly, system operates as designed.
        Low conductivity = resistance, friction, unexpected behavior.
        
        Factors considered:
        - Centrality (betweenness, closeness) - control downstream
        - Standardization - does it follow dominant patterns?
        - Abstraction level - how hidden from human inspection?
        - In/out degree - how integrated?
        """
        nx_graph = self.graph._graph if hasattr(self.graph, '_graph') else self.graph
        node_data = dict(nx_graph.nodes.get(node_id, {}))
        
        # Determine dominant register
        node_type = node_data.get("type", "unknown")
        if node_type in ["function", "method"]:
            register = LacunianRegister.SYMBOLIC
        elif node_type in ["variable", "constant"]:
            register = LacunianRegister.IMAGINARY
        else:
            register = LacunianRegister.REAL
        
        # Calculate pattern conformity
        pattern_conformity = self._calculate_pattern_conformity(node_id, node_data)
        
        # Calculate degree-based conductivity
        in_degree = nx_graph.in_degree(node_id)
        out_degree = nx_graph.out_degree(node_id)
        total_degree = in_degree + out_degree
        
        # Normalize centrality scores
        centrality = (betweenness * 0.6 + closeness * 0.4)
        
        # Resistance level: high centrality + high conformity = high conductivity (low resistance)
        # High uniqueness or isolation = high resistance
        resistance_level = 1.0 - (pattern_conformity * 0.5 + centrality * 0.5)
        
        # Determine conductivity level
        if resistance_level < 0.25:
            conductivity_level = ConductivityLevel.HIGHLY_CONDUCTIVE
            dominant_flow = "Standard conventions"
        elif resistance_level < 0.5:
            conductivity_level = ConductivityLevel.MODERATELY_CONDUCTIVE
            dominant_flow = "Mixed patterns"
        elif resistance_level < 0.75:
            conductivity_level = ConductivityLevel.RESISTANT
            dominant_flow = "Custom logic"
        else:
            conductivity_level = ConductivityLevel.CHAOTIC
            dominant_flow = "Unpredictable behavior"
        
        # Identify friction points
        friction_points = []
        if total_degree == 0:
            friction_points.append("isolated_node")
        if in_degree > 5 or out_degree > 5:
            friction_points.append("high_coupling")
        if pattern_conformity < 0.3:
            friction_points.append("non_standard_naming")
        
        return ConductivityMeasurement(
            node_id=node_id,
            resistance_level=resistance_level,
            register=register,
            conductivity_level=conductivity_level,
            dominant_flow=dominant_flow,
            friction_points=friction_points,
            centrality_score=centrality,
            pattern_conformity=pattern_conformity,
        )
    
    def _calculate_pattern_conformity(
        self, 
        node_id: str, 
        node_data: Dict[str, Any]
    ) -> float:
        """
        Calculate how much a node follows standard patterns (0.0-1.0).
        
        High conformity (1.0) = follows conventions
        Low conformity (0.0) = unique/custom approach
        """
        name = node_data.get("name", "")
        conformity_score = 0.0
        match_count = 0
        
        # Check naming patterns
        for pattern in self.CONFORMIST_PATTERNS["naming"]:
            if pattern in name.lower():
                conformity_score += 1.0
                match_count += 1
        
        # If no conformist patterns, check for autonomous patterns
        if match_count == 0:
            for pattern in self.AUTONOMOUS_PATTERNS["naming"]:
                if pattern in name.lower():
                    match_count += 1
        
        # Normalize
        if match_count > 0:
            conformity_score = conformity_score / match_count if match_count > 0 else 0.5
        else:
            conformity_score = 0.5  # Default neutral
        
        return min(1.0, max(0.0, conformity_score))
    
    def _detect_resistance_patterns(self):
        """Identify where code resists dominant patterns."""
        logger.debug("Detecting resistance patterns")
        
        for node_id, measurement in self.conductivity_map.items():
            # Look for resistant nodes
            if measurement.resistance_level > 0.6:
                node_data = self.graph._graph.nodes.get(node_id, {})
                name = node_data.get("name", "unknown")
                
                # Determine resistance type
                if measurement.pattern_conformity < 0.3:
                    resistance_type = "naming"
                    description = f"Non-standard naming convention: {name}"
                elif measurement.centrality_score < 0.2:
                    resistance_type = "structure"
                    description = f"Isolated or peripheral node: {name}"
                else:
                    resistance_type = "flow"
                    description = f"Unusual dependency pattern: {name}"
                
                pattern = ResistancePattern(
                    node_id=node_id,
                    resistance_type=resistance_type,
                    description=description,
                    register=measurement.register,
                    severity=int(measurement.resistance_level * 3),  # 0-3
                    contradiction_value=measurement.dominant_flow,
                )
                self.resistance_patterns.append(pattern)
    
    def _measure_autonomy_frequencies(self):
        """
        Measure autonomy frequency: degree to which patterns are authentic 
        vs. imposed/conformist.
        """
        logger.debug("Measuring autonomy frequencies")
        
        for node_id, measurement in self.conductivity_map.items():
            # Autonomy score: inverse of pattern conformity
            # High pattern conformity = low autonomy (imposed)
            # Low pattern conformity = high autonomy (authentic)
            autonomy_score = 1.0 - measurement.pattern_conformity
            
            # Determine pattern type
            if autonomy_score < 0.33:
                pattern_type = "conformist"
                interpretation = "Follows standard conventions and patterns"
            elif autonomy_score < 0.66:
                pattern_type = "hybrid"
                interpretation = "Mix of standard and custom approaches"
            else:
                pattern_type = "autonomous"
                interpretation = "High autonomy; custom logic and unique patterns"
            
            signal = AutonomySignal(
                node_id=node_id,
                autonomy_score=autonomy_score,
                pattern_type=pattern_type,
                register=measurement.register,
                interpretation=interpretation,
            )
            self.autonomy_signals.append(signal)
    
    def _detect_administered_thinking(self):
        """
        Frankfurt School (Adorno, Marcuse): Detect instrumental rationality.
        
        Administered thinking: code optimized for efficiency alone,
        forecloses alternatives, treats purposes as unchangeable.
        
        Markers:
        - High centrality + high conformity = instrumental
        - Multiple in/out degrees without feedback = one-way control
        - High abstraction without transparency = hidden domination
        """
        logger.debug("Detecting administered thinking patterns")
        
        nx_graph = self.graph._graph if hasattr(self.graph, '_graph') else self.graph
        
        for node_id, measurement in self.conductivity_map.items():
            administered_score = 0.0
            reasons = []
            
            # High centrality + high conformity = instrumental rationality
            if measurement.centrality_score > 0.6 and measurement.pattern_conformity > 0.7:
                administered_score += 0.7
                reasons.append("High centrality + high conformity (control without critique)")
            
            # Check for one-way dependencies (no feedback loops)
            in_degree = nx_graph.in_degree(node_id)
            out_degree = nx_graph.out_degree(node_id)
            
            if in_degree > 0 and out_degree == 0:
                administered_score += 0.3
                reasons.append("Consumer node: receives but doesn't feedback (one-way domination)")
            elif in_degree == 0 and out_degree > 3:
                administered_score += 0.2
                reasons.append("Production without input: imposes without listening")
            
            if administered_score > 0.4:
                self.administered_thinking_nodes.append({
                    "node_id": node_id,
                    "administered_score": round(min(1.0, administered_score), 3),
                    "thinking_level": self._classify_thinking_level(administered_score),
                    "reasons": reasons,
                    "register": measurement.register.value,
                })
    
    def _classify_thinking_level(self, score: float) -> str:
        """Classify administered thinking level."""
        if score > 0.8:
            return AdministeredThinkingLevel.INSTRUMENTAL.value
        elif score > 0.6:
            return AdministeredThinkingLevel.STRATEGIC.value
        elif score > 0.4:
            return AdministeredThinkingLevel.COMMUNICATIVE.value
        else:
            return AdministeredThinkingLevel.CRITICAL.value
    
    def _detect_reification(self):
        """
        Marxist/Lukács: Detect reification — treating dynamic processes 
        as static things.
        
        Indicators:
        - Immutable structures (no state changes)
        - No feedback loops (circular dependencies treated as problems)
        - Hidden abstraction layers
        - Singular solution paths (forecloses alternatives)
        """
        logger.debug("Detecting reification markers")
        
        nx_graph = self.graph._graph if hasattr(self.graph, '_graph') else self.graph
        
        for node_id in nx_graph.nodes():
            node_data = dict(nx_graph.nodes.get(node_id, {}))
            markers = []
            severity = 0
            
            # Check for immutability patterns
            if "const" in node_data.get("name", "").lower() or "static" in node_data.get("type", "").lower():
                markers.append(ReificationMarker.IMMUTABLE_STRUCTURE.value)
                severity += 1
            
            # Check for no feedback loops
            in_degree = nx_graph.in_degree(node_id)
            out_degree = nx_graph.out_degree(node_id)
            
            # If this node has all outgoing or all incoming (not bidirectional)
            if (in_degree == 0 and out_degree > 0) or (out_degree == 0 and in_degree > 0):
                markers.append(ReificationMarker.NO_FEEDBACK_LOOP.value)
                severity += 1
            
            # Hidden complexity: high abstraction
            abstraction_level = len(node_data.get("name", "")) / 20.0  # Rough heuristic
            if abstraction_level > 0.5:
                markers.append(ReificationMarker.HIDDEN_COMPLEXITY.value)
                severity += 1
            
            # Check for singular path (only one connection)
            if in_degree + out_degree == 1:
                markers.append(ReificationMarker.SINGULAR_PATH.value)
                severity += 1
            
            if markers:
                self.reification_markers.append({
                    "node_id": node_id,
                    "markers": markers,
                    "severity": min(3, severity),
                    "interpretation": "Treats dynamic processes as static structures; forecloses alternatives",
                })
    
    def _detect_one_dimensional_thinking(self):
        """
        Marcuse: Detect one-dimensional thinking — foreclosure of alternatives.
        
        In code, this appears as:
        - Nodes with very high conformity (no alternative patterns)
        - Nodes optimized for single metric (efficiency, speed)
        - No contradiction/tension (false harmony)
        - Repressive desublimation: pleasure in conformity
        """
        logger.debug("Detecting one-dimensional thinking patterns")
        
        for node_id, measurement in self.conductivity_map.items():
            one_dimensional_score = 0.0
            characteristics = []
            
            # Perfect conformity = no alternatives
            if measurement.pattern_conformity > 0.85:
                one_dimensional_score += 0.6
                characteristics.append("Perfect conformity: no alternative approaches")
            
            # High conductivity without resistance
            if measurement.is_high_conductivity() and len(measurement.friction_points) == 0:
                one_dimensional_score += 0.4
                characteristics.append("Smooth operation without friction (false harmony)")
            
            if one_dimensional_score > 0.4:
                self.one_dimensional_patterns.append({
                    "node_id": node_id,
                    "one_dimensional_score": round(min(1.0, one_dimensional_score), 3),
                    "characteristics": characteristics,
                    "critique": "Forecloses alternatives; appears as natural/inevitable",
                })
    
    def _compile_findings(self) -> List[Dict[str, Any]]:
        """Compile all analysis results into findings."""
        findings = []
        
        # Conductivity findings
        highly_conductive_nodes = [
            m for m in self.conductivity_map.values()
            if m.conductivity_level == ConductivityLevel.HIGHLY_CONDUCTIVE
        ]
        if highly_conductive_nodes:
            findings.append({
                "type": "conductivity_summary",
                "level": "info",
                "title": "High Conductivity Zones",
                "description": f"Found {len(highly_conductive_nodes)} nodes with smooth power flow (standard conventions)",
                "count": len(highly_conductive_nodes),
                "nodes": [m.node_id for m in highly_conductive_nodes[:5]],
            })
        
        # Resistance findings
        if self.resistance_patterns:
            findings.append({
                "type": "resistance_patterns",
                "level": "warning",
                "title": "Resistance & Friction Points",
                "description": f"Detected {len(self.resistance_patterns)} nodes resisting dominant patterns",
                "patterns": [
                    {
                        "node_id": p.node_id,
                        "type": p.resistance_type,
                        "description": p.description,
                        "severity": p.severity,
                    }
                    for p in self.resistance_patterns[:10]
                ],
            })
        
        # Autonomy findings
        autonomous_nodes = [
            s for s in self.autonomy_signals
            if s.pattern_type == "autonomous"
        ]
        if autonomous_nodes:
            findings.append({
                "type": "autonomy_frequencies",
                "level": "info",
                "title": "High Autonomy Nodes",
                "description": f"Found {len(autonomous_nodes)} nodes with authentic/custom patterns",
                "count": len(autonomous_nodes),
                "nodes": [
                    s.to_dict() for s in autonomous_nodes[:5]
                ],
            })
        
        # =========== Frankfurt School Critical Analysis ===========
        
        # Administered thinking findings
        if self.administered_thinking_nodes:
            findings.append({
                "type": "administered_thinking",
                "level": "warning",
                "title": "Instrumental Rationality (Frankfurt School)",
                "description": f"Detected {len(self.administered_thinking_nodes)} nodes exhibiting administered thinking",
                "theory": "Adorno & Horkheimer: Instrumental reason optimizes for efficiency without questioning purpose",
                "findings": self.administered_thinking_nodes[:10],
            })
        
        # Reification findings
        if self.reification_markers:
            findings.append({
                "type": "reification",
                "level": "warning",
                "title": "Reification (Marxist Analysis)",
                "description": f"Found {len(self.reification_markers)} reified structures (dynamic treated as static)",
                "theory": "Lukács: Treating changing social processes as unchangeable natural things",
                "markers": self.reification_markers[:10],
            })
        
        # One-dimensional thinking findings
        if self.one_dimensional_patterns:
            findings.append({
                "type": "one_dimensional_thinking",
                "level": "critical",
                "title": "One-Dimensional Society (Marcuse)",
                "description": f"Identified {len(self.one_dimensional_patterns)} nodes foreclosing alternatives",
                "theory": "Marcuse: Repressive desublimation where conformity appears natural/inevitable",
                "patterns": self.one_dimensional_patterns[:10],
            })
        
        # Detailed measurements available
        findings.append({
            "type": "conductivity_measurements",
            "all_measurements": [
                m.to_dict() for m in self.conductivity_map.values()
            ],
        })
        
        return findings
