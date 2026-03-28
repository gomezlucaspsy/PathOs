"""
V1 API routes - Visualization endpoints.

Handles graph visualization requests.
"""

from __future__ import annotations
from flask import Blueprint, request, jsonify
from pathlib import Path
import tempfile

from pathos.services import AnalysisService
from pathos.infrastructure.logging import get_logger

logger = get_logger("api.v1.visualization")
bp = Blueprint("visualization", __name__, url_prefix="/graph")


@bp.route("/visualization", methods=["POST"])
def graph_visualization():
    """Get graph data formatted for D3.js visualization."""
    try:
        data = request.json or {}
        files = data.get("files", {})
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        service = AnalysisService()
        result = service.analyze_file_dict(files)
        
        # Format for D3.js
        nodes_list = result.graph.nodes()
        edges_list = result.graph.edges()
        
        # Add group based on node kind
        node_kind_map = {n["id"]: n.get("kind") for n in nodes_list}
        kind_to_group = {
            "function": 1,
            "class": 2,
            "module": 3,
            "variable": 4,
            "import": 5,
        }
        
        nodes = [
            {
                "id": n["id"],
                "name": n.get("name", n["id"]),
                "group": kind_to_group.get(n.get("kind"), 0),
                "kind": n.get("kind"),
            }
            for n in nodes_list
        ]
        
        links = [
            {
                "source": e["source"],
                "target": e["target"],
                "kind": e.get("kind"),
            }
            for e in edges_list
        ]
        
        return jsonify({
            "nodes": nodes,
            "links": links,
            "summary": result.summary,
        })
    
    except Exception as e:
        logger.error(f"Visualization error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
