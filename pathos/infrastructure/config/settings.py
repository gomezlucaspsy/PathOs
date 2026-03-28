"""
Configuration management for PathOs.

Supports environment-based settings with inheritance.
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Environment(str, Enum):
    """Deployment environment."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class ApiConfig:
    """API server configuration."""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    cors_origins: list[str] = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:3000", "http://localhost:5000"]


@dataclass
class ModelConfig:
    """LLM model configuration."""
    model: str = "claude-opus-4-5"
    max_tokens: int = 1024
    api_key: Optional[str] = None
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")


@dataclass
class ParserConfig:
    """Code parser configuration."""
    max_file_size_mb: int = 10
    supported_languages: list[str] = None
    skip_node_modules: bool = True
    skip_git: bool = True
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["python", "javascript"]


@dataclass
class CacheConfig:
    """Cache configuration."""
    enabled: bool = True
    max_size_mb: int = 100
    ttl_seconds: int = 3600


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    console: bool = True


@dataclass
class Settings:
    """Root configuration object."""
    environment: Environment = Environment.DEVELOPMENT
    api: ApiConfig = None
    model: ModelConfig = None
    parser: ParserConfig = None
    cache: CacheConfig = None
    logging: LoggingConfig = None
    
    def __post_init__(self):
        if self.api is None:
            self.api = ApiConfig()
        if self.model is None:
            self.model = ModelConfig()
        if self.parser is None:
            self.parser = ParserConfig()
        if self.cache is None:
            self.cache = CacheConfig()
        if self.logging is None:
            self.logging = LoggingConfig()


def get_settings() -> Settings:
    """Load settings from environment variables."""
    load_dotenv()
    
    env = os.getenv("ENVIRONMENT", "development").lower()
    try:
        environment = Environment(env)
    except ValueError:
        environment = Environment.DEVELOPMENT
    
    # Production-specific settings
    if environment == Environment.PRODUCTION:
        api_debug = False
        cache_enabled = True
        log_level = "WARNING"
    elif environment == Environment.TESTING:
        api_debug = True
        cache_enabled = False
        log_level = "DEBUG"
    else:  # development
        api_debug = True
        cache_enabled = True
        log_level = "DEBUG"
    
    settings = Settings(
        environment=environment,
        api=ApiConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", 5000)),
            debug=api_debug,
            cors_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5000").split(","),
        ),
        model=ModelConfig(
            model=os.getenv("MODEL_NAME", "claude-opus-4-5"),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS", 1024)),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        parser=ParserConfig(
            max_file_size_mb=int(os.getenv("PARSER_MAX_FILE_SIZE_MB", 10)),
            skip_node_modules=os.getenv("PARSER_SKIP_NODE_MODULES", "true").lower() == "true",
            skip_git=os.getenv("PARSER_SKIP_GIT", "true").lower() == "true",
        ),
        cache=CacheConfig(
            enabled=cache_enabled,
            max_size_mb=int(os.getenv("CACHE_MAX_SIZE_MB", 100)),
            ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", 3600)),
        ),
        logging=LoggingConfig(
            level=log_level,
            file=os.getenv("LOG_FILE"),
            console=os.getenv("LOG_CONSOLE", "true").lower() == "true",
        ),
    )
    
    return settings


# Singleton instance
_settings: Optional[Settings] = None


def load_settings() -> Settings:
    """Load and cache settings."""
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings
