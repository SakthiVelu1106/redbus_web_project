"""
Configuration reader utility.
Reads config/config.yaml and exposes a singleton dict.
"""
import os
import yaml
from functools import lru_cache

# Resolve path relative to project root (two levels up from this file)
_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "config.yaml",
)


@lru_cache(maxsize=1)
def get_config() -> dict:
    """
    Load and cache config.yaml.

    Returns:
        Parsed YAML as a nested dict.

    Raises:
        FileNotFoundError: If config.yaml does not exist.
    """
    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(
            f"Configuration file not found at: {_CONFIG_PATH}"
        )

    with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh)

    return config
