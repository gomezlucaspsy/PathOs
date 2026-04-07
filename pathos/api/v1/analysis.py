"""
V1 API routes - Analysis endpoints.

Handles code analysis requests with proper error handling.
"""

from __future__ import annotations
from flask import Blueprint, request, jsonify
from pathlib import Path
import tempfile

from pathos.services import AnalysisService, AnalysisOptions
from pathos.infrastructure.logging import get_logger

logger = get_logger("api.v1.analysis")
bp = Blueprint("analysis", __name__, url_prefix="/analyze")


@bp.route("/code", methods=["POST"])
def analyze_code():
    """Analyze code passed as JSON."""
    try:
        data = request.json or {}
        files = data.get("files", {})
        code = data.get("code")
        language = data.get("language", "python")
        interpret = data.get("interpret", False)
        
        if not files and not code:
            return jsonify({"error": "Either 'files' or 'code' is required"}), 400
        
        options = AnalysisOptions(interpret=interpret)
        service = AnalysisService()
        
        if code:
            result = service.analyze_code_string(code, language, options=options)
        else:
            result = service.analyze_file_dict(files, options=options)
        
        # Serialize graph nodes and edges properly
        # TopologyGraph.nodes() returns list of dicts, edges() returns list of dicts
        nodes = result.graph.nodes()  # Already formatted with "id" key
        edges = result.graph.edges()  # Already formatted with "source", "target" keys
        
        return jsonify({
            "source": "code",
            "summary": result.summary,
            "graph": {
                "nodes": nodes,
                "links": edges,
            },
            "contradictions": [
                {
                    "kind": c.kind.value,
                    "description": c.description,
                    "severity": c.severity,
                    "register": c.lacanian_register,
                    "nodes": c.nodes,
                    "metadata": c.metadata,
                    "interpretation": result.interpretations.get(c.kind.value),
                }
                for c in result.contradictions
            ],
            "conductivity_analysis": result.conductivity_findings,
        })
    
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@bp.route("/github", methods=["POST"])
def analyze_github():
    """Analyze a GitHub repository."""
    try:
        from git import Repo
        
        data = request.json or {}
        github_url = data.get("url", "").strip()
        interpret = data.get("interpret", False)
        
        if not github_url:
            return jsonify({"error": "GitHub URL is required"}), 400
        
        if "github.com" not in github_url:
            return jsonify({"error": "Invalid GitHub URL"}), 400
        
        # Normalize URL
        if github_url.endswith(".git"):
            github_url = github_url[:-4]
        if not github_url.startswith("https://"):
            if github_url.startswith("git@"):
                github_url = github_url.replace(":", "/").replace("git@github.com/", "https://github.com/")
            elif github_url.startswith("http://"):
                github_url = github_url.replace("http://", "https://")
            else:
                github_url = "https://" + github_url
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            repo_path = tmppath / "repo"
            
            try:
                logger.info(f"Cloning repository: {github_url}")
                Repo.clone_from(github_url, str(repo_path))
            except Exception as e:
                logger.error(f"Clone failed: {e}")
                return jsonify({"error": f"Failed to clone repository: {str(e)}"}), 400
            
            try:
                options = AnalysisOptions(interpret=interpret)
                service = AnalysisService()
                result = service.analyze_directory(repo_path, options=options)
                
                # Serialize graph nodes and edges properly
                # TopologyGraph.nodes() returns list of dicts, edges() returns list of dicts
                nodes = result.graph.nodes()  # Already formatted with "id" key
                edges = result.graph.edges()  # Already formatted with "source", "target" keys
                
                return jsonify({
                    "source": "github",
                    "url": github_url,
                    "summary": result.summary,
                    "graph": {
                        "nodes": nodes,
                        "links": edges,
                    },
                    "contradictions": [
                        {
                            "kind": c.kind.value,
                            "description": c.description,
                            "severity": c.severity,
                            "register": c.lacanian_register,
                            "nodes": c.nodes,
                            "metadata": c.metadata,
                            "interpretation": result.interpretations.get(c.kind.value),
                        }
                        for c in result.contradictions
                    ],
                    "conductivity_analysis": result.conductivity_findings,
                })
            except Exception as e:
                logger.error(f"Analysis failed: {e}", exc_info=True)
                return jsonify({"error": f"Failed to analyze repository: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
