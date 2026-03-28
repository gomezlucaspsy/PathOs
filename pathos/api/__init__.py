"""
API application factory.

Creates and configures the Flask application with routes.
"""

from __future__ import annotations
from flask import Flask, jsonify
from flask_cors import CORS

from pathos.infrastructure.config import load_settings
from pathos.infrastructure.logging import configure_logging, get_logger
from pathos.api.v1 import analysis, visualization

logger = get_logger("api")


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Load settings
    settings = load_settings()
    
    # Configure logging
    configure_logging(settings)
    logger.info(f"Starting PathOs API in {settings.environment.value} mode")
    
    # Create app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=settings.api.cors_origins)
    logger.info(f"CORS configured for origins: {settings.api.cors_origins}")
    
    # Root endpoint
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "name": "PathOs API",
            "description": "Topological code analysis via REST",
            "version": "1.0.0",
            "endpoints": {
                "POST /analyze/code": "Analyze code (JSON: {files: {...}|code:string, interpret:bool})",
                "POST /analyze/github": "Analyze GitHub repo (JSON: {url: 'github_url', interpret:bool})",
                "POST /graph/visualization": "Get D3.js graph data",
            }
        })
    
    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})
    
    # Register blueprints
    app.register_blueprint(analysis.bp)
    app.register_blueprint(visualization.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
    
    return app


if __name__ == "__main__":
    app = create_app()
    settings = load_settings()
    app.run(host=settings.api.host, port=settings.api.port, debug=settings.api.debug)
