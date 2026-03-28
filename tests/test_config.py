"""Tests for the infrastructure configuration."""

import pytest
from pathos.infrastructure.config import load_settings, Environment


def test_settings_load():
    """Test that settings load successfully."""
    settings = load_settings()
    assert settings is not None
    assert settings.api is not None
    assert settings.model is not None
    assert settings.parser is not None


def test_settings_environment():
    """Test environment detection."""
    settings = load_settings()
    assert settings.environment in [
        Environment.DEVELOPMENT,
        Environment.TESTING,
        Environment.PRODUCTION,
    ]


def test_api_config():
    """Test API configuration."""
    settings = load_settings()
    assert settings.api.port > 0
    assert settings.api.host
    assert isinstance(settings.api.cors_origins, list)


def test_model_config():
    """Test model configuration."""
    settings = load_settings()
    assert settings.model.model
    assert settings.model.max_tokens > 0


def test_parser_config():
    """Test parser configuration."""
    settings = load_settings()
    assert isinstance(settings.parser.supported_languages, list)
    assert len(settings.parser.supported_languages) > 0
