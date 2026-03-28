"""Tests for the analysis service."""

import pytest
from pathlib import Path

from pathos.services import AnalysisService, AnalysisOptions


def test_analysis_service_creation():
    """Test that analysis service can be instantiated."""
    service = AnalysisService()
    assert service is not None


def test_analyze_code_string():
    """Test analyzing a code string."""
    service = AnalysisService()
    
    code = """
def foo():
    return bar()

def bar():
    return foo()
"""
    
    result = service.analyze_code_string(code, "python")
    
    assert result.graph is not None
    assert result.summary is not None
    assert "node_count" in result.summary


def test_analyze_with_options():
    """Test analysis with options."""
    service = AnalysisService()
    options = AnalysisOptions(interpret=False)
    
    code = "def foo(): pass"
    result = service.analyze_code_string(code, "python", options=options)
    
    assert result is not None


def test_analyze_file_dict():
    """Test analyzing a dict of files."""
    service = AnalysisService()
    
    files = {
        "main.py": "from helper import foo\nfoo()",
        "helper.py": "def foo(): pass",
    }
    
    result = service.analyze_file_dict(files)
    
    assert result.graph is not None
    assert result.summary["node_count"] >= 2
