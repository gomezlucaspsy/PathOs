"""
Analysis service - orchestrates the analysis pipeline.

Coordinates parsing, graph building, contradiction detection, and synthesis.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pathos.infrastructure.logging import get_logger
from pathos.core.graph import TopologyGraph
from pathos.core.parser import CodeParser
from pathos.core.contradiction import ContradictionDetector, Contradiction
from pathos.ai.claude import ClaudeSynthesizer

logger = get_logger("services.analysis")


@dataclass
class AnalysisOptions:
    """Options for analysis execution."""
    interpret: bool = False
    interpret_all: bool = False
    include_deep_chain_threshold: int = 5


@dataclass
class AnalysisResult:
    """Result of code analysis."""
    graph: TopologyGraph
    contradictions: list[Contradiction]
    summary: dict
    interpretations: dict[str, str] = None
    
    def __post_init__(self):
        if self.interpretations is None:
            self.interpretations = {}


class AnalysisService:
    """Orchestrates topological code analysis."""
    
    def __init__(self):
        self._parser = CodeParser()
        self._detector = ContradictionDetector()
        self._synthesizer = ClaudeSynthesizer()
    
    def analyze_file(
        self,
        path: Path,
        options: AnalysisOptions | None = None,
    ) -> AnalysisResult:
        """Analyze a single file."""
        if options is None:
            options = AnalysisOptions()
        
        logger.info(f"Analyzing file: {path}")
        graph = TopologyGraph()
        self._parser.parse_file(path, graph)
        
        return self._finalize_analysis(graph, options)
    
    def analyze_directory(
        self,
        root: Path,
        options: AnalysisOptions | None = None,
    ) -> AnalysisResult:
        """Analyze a directory recursively."""
        if options is None:
            options = AnalysisOptions()
        
        logger.info(f"Analyzing directory: {root}")
        graph = TopologyGraph()
        self._parser.parse_directory(root, graph)
        
        return self._finalize_analysis(graph, options)
    
    def analyze_code_string(
        self,
        code: str,
        language: str,
        filename: str = "unknown",
        options: AnalysisOptions | None = None,
    ) -> AnalysisResult:
        """Analyze code passed as a string."""
        if options is None:
            options = AnalysisOptions()
        
        logger.info(f"Analyzing code string ({language})")
        
        # Write to temp location and parse
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            filepath = tmppath / filename
            filepath.write_text(code)
            
            graph = TopologyGraph()
            self._parser.parse_file(filepath, graph)
        
        return self._finalize_analysis(graph, options)
    
    def analyze_file_dict(
        self,
        files: dict[str, str],
        options: AnalysisOptions | None = None,
    ) -> AnalysisResult:
        """
        Analyze a dictionary of file paths to content.
        
        Args:
            files: Dict mapping file paths to content
            options: Analysis options
            
        Returns:
            AnalysisResult
        """
        if options is None:
            options = AnalysisOptions()
        
        logger.info(f"Analyzing {len(files)} files")
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Write all files
            for fname, content in files.items():
                fpath = tmppath / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content)
            
            graph = TopologyGraph()
            self._parser.parse_directory(tmppath, graph)
        
        return self._finalize_analysis(graph, options)
    
    def _finalize_analysis(
        self,
        graph: TopologyGraph,
        options: AnalysisOptions,
    ) -> AnalysisResult:
        """Detect contradictions and optionally synthesize."""
        logger.debug("Detecting contradictions...")
        contradictions = self._detector.detect(graph)
        logger.info(f"Found {len(contradictions)} contradictions")
        
        result = AnalysisResult(
            graph=graph,
            contradictions=contradictions,
            summary=graph.summary(),
        )
        
        # Synthesis
        if options.interpret or options.interpret_all:
            target = contradictions if options.interpret_all else contradictions[:1]
            for c in target:
                try:
                    logger.debug(f"Synthesizing interpretation for: {c.kind}")
                    interpretation = self._synthesizer.interpret(c, result.summary)
                    result.interpretations[c.kind.value] = interpretation
                except Exception as e:
                    logger.warning(f"Synthesis failed: {e}")
                    result.interpretations[c.kind.value] = f"Error: {str(e)}"
        
        return result
