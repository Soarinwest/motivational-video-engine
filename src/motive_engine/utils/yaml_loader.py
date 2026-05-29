"""Small YAML loading helper.

Uses safe_load only and surfaces clear errors with the file path attached.
"""

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    """Load a YAML file as Python data.

    Raises:
        FileNotFoundError: if ``path`` does not exist.
        yaml.YAMLError: with the offending file path included in the message.
    """
    if not path.is_file():
        raise FileNotFoundError(f"YAML file not found: {path}")

    text = path.read_text(encoding="utf-8")
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse YAML at {path}: {e}") from e
