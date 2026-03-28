#!/usr/bin/env python
"""Development server runner with auto-reload."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pathos.api import create_app
from pathos.infrastructure.config import load_settings
from pathos.infrastructure.logging import configure_logging

if __name__ == "__main__":
    # Load configuration
    settings = load_settings()
    configure_logging(settings)
    
    # Create app
    app = create_app()
    
    # Run with auto-reload
    app.run(
        host=settings.api.host,
        port=settings.api.port,
        debug=settings.api.debug,
        use_reloader=True,
    )
