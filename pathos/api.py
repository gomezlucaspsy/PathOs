from flask import Flask, request, jsonify
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
from git import Repo
import shutil

from pathos.core.graph import TopologyGraph
from pathos.core.parser import CodeParser
from pathos.core.contradiction import ContradictionDetector
from pathos.ai.claude import ClaudeSynthesizer

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """API documentation."""
    return jsonify({
        "name": "PathOs API",
        "description": "Topological code analysis via REST",
        "endpoints": {
            "POST /analyze": "Analyze code (JSON: {files: {...}, interpret: bool})",
            "POST /analyze/github": "Analyze GitHub repo (JSON: {url: 'github_url', interpret: bool})",
            "POST /graph/visualization": "Get D3.js graph data",
        }
    })


def _analyze_directory(tmppath, interpret=False):
    """Helper function to analyze a directory."""
    try:
        graph = TopologyGraph()
        parser = CodeParser()
        
        print(f"Parsing directory: {tmppath}")
        parser.parse_directory(tmppath, graph)
        print(f"Parsing complete. Graph has {len(graph._graph.nodes)} nodes")
        
        detector = ContradictionDetector()
        print("Detecting contradictions...")
        contradictions = detector.detect(graph)
        print(f"Found {len(contradictions)} contradictions")
        
        result = {
            "summary": graph.summary(),
            "graph": {
                "nodes": graph.nodes(),
                "edges": graph.edges(),
            },
            "contradictions": []
        }
        
        for c in contradictions:
            c_data = {
                "kind": c.kind.value,
                "description": c.description,
                "severity": c.severity,
                "register": c.lacanian_register,
                "nodes": c.nodes,
                "metadata": c.metadata,
            }
            
            if interpret:
                try:
                    synthesizer = ClaudeSynthesizer()
                    c_data["interpretation"] = synthesizer.interpret(c, graph.summary())
                except Exception as e:
                    c_data["interpretation"] = f"Error: {str(e)}"
            
            result["contradictions"].append(c_data)
        
        return result
    except Exception as e:
        print(f"Error in _analyze_directory: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


@app.route("/analyze/github", methods=["POST"])
def analyze_github():
    """Analyze a GitHub repository."""
    try:
        data = request.json
        github_url = data.get("url", "").strip()
        interpret = data.get("interpret", False)
        
        if not github_url:
            return jsonify({"error": "GitHub URL is required"}), 400
        
        # Validate GitHub URL format
        if "github.com" not in github_url:
            return jsonify({"error": "Invalid GitHub URL"}), 400
        
        # Normalize URL (remove .git if present, ensure https)
        if github_url.endswith(".git"):
            github_url = github_url[:-4]
        if not github_url.startswith("https://"):
            if github_url.startswith("git@"):
                # Convert SSH to HTTPS
                github_url = github_url.replace(":", "/").replace("git@github.com/", "https://github.com/")
            elif github_url.startswith("http://"):
                github_url = github_url.replace("http://", "https://")
            else:
                github_url = "https://" + github_url
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            try:
                # Clone the repository
                repo_path = tmppath / "repo"
                print(f"Cloning repository from {github_url}...")
                Repo.clone_from(github_url, str(repo_path))
                print(f"Repository cloned successfully to {repo_path}")
            except Exception as e:
                print(f"Clone error: {str(e)}")
                return jsonify({"error": f"Failed to clone repository: {str(e)}"}), 400
            
            try:
                # Analyze the cloned repository
                print(f"Starting analysis of {repo_path}")
                result = _analyze_directory(repo_path, interpret)
                print(f"Analysis complete: {result['summary']}")
                result["source"] = "github"
                result["url"] = github_url
                
                return jsonify(result)
            except Exception as e:
                print(f"Analysis error: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({"error": f"Failed to analyze repository: {str(e)}"}), 500
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze code files passed as JSON."""
    try:
        data = request.json
        files = data.get("files", {})
        interpret = data.get("interpret", False)
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Write files
            for fname, content in files.items():
                fpath = tmppath / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content)
            
            # Analyze
            result = _analyze_directory(tmppath, interpret)
            result["source"] = "code"
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/graph/visualization", methods=["POST"])
def graph_visualization():
    """Return graph data in format suitable for D3.js visualization."""
    try:
        data = request.json
        files = data.get("files", {})
        
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            for fname, content in files.items():
                fpath = tmppath / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content)
            
            graph = TopologyGraph()
            parser = CodeParser()
            parser.parse_directory(tmppath, graph)
            
            # Format for D3.js
            nodes_list = graph.nodes()
            edges_list = graph.edges()
            
            # Map node IDs to indices for D3
            node_map = {n["id"]: i for i, n in enumerate(nodes_list)}
            
            d3_nodes = [
                {
                    "id": n["id"],
                    "label": n["name"],
                    "kind": n["kind"],
                    "group": n["kind"],
                }
                for n in nodes_list
            ]
            
            d3_links = [
                {
                    "source": node_map.get(e["source"], 0),
                    "target": node_map.get(e["target"], 0),
                    "type": e["kind"],
                }
                for e in edges_list
                if e["source"] in node_map and e["target"] in node_map
            ]
            
            return jsonify({
                "nodes": d3_nodes,
                "links": d3_links,
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
