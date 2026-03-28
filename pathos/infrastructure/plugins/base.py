"""
Plugin system for PathOs.

Allows extensible language support and analysis strategies.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class LanguagePlugin(ABC):
    """Abstract base class for language plugins."""
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """Name of the language."""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> list[str]:
        """File extensions supported by this plugin."""
        pass
    
    @abstractmethod
    def parse(self, source: bytes, path: str) -> dict[str, Any]:
        """
        Parse source code and return AST-like structure.
        
        Returns:
            Dict with keys:
            - 'nodes': List of CodeNode dicts
            - 'edges': List of CodeEdge dicts
        """
        pass
    
    @abstractmethod
    def get_parser(self):
        """Get the underlying parser instance."""
        pass


class AnalysisPlugin(ABC):
    """Abstract base class for analysis plugins."""
    
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Name of the analysis."""
        pass
    
    @abstractmethod
    def analyze(self, graph: Any) -> list[dict[str, Any]]:
        """
        Run analysis on the topology graph.
        
        Args:
            graph: TopologyGraph instance
            
        Returns:
            List of findings/results
        """
        pass


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(self):
        self._language_plugins: dict[str, LanguagePlugin] = {}
        self._analysis_plugins: dict[str, AnalysisPlugin] = {}
    
    def register_language(self, plugin: LanguagePlugin) -> None:
        """Register a language plugin."""
        self._language_plugins[plugin.language_name] = plugin
    
    def register_analysis(self, plugin: AnalysisPlugin) -> None:
        """Register an analysis plugin."""
        self._analysis_plugins[plugin.plugin_name] = plugin
    
    def get_language_plugin(self, name: str) -> Optional[LanguagePlugin]:
        """Get a language plugin by name."""
        return self._language_plugins.get(name)
    
    def get_language_plugin_by_extension(self, ext: str) -> Optional[LanguagePlugin]:
        """Get a language plugin by file extension."""
        for plugin in self._language_plugins.values():
            if ext in plugin.file_extensions:
                return plugin
        return None
    
    def get_analysis_plugin(self, name: str) -> Optional[AnalysisPlugin]:
        """Get an analysis plugin by name."""
        return self._analysis_plugins.get(name)
    
    def list_language_plugins(self) -> list[str]:
        """List all registered language plugins."""
        return list(self._language_plugins.keys())
    
    def list_analysis_plugins(self) -> list[str]:
        """List all registered analysis plugins."""
        return list(self._analysis_plugins.keys())


# Global registry
_registry: Optional[PluginRegistry] = None


def get_registry() -> PluginRegistry:
    """Get the global plugin registry."""
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry
