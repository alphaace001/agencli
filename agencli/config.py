import json
import os

from typing import Dict, Any
from pathlib import Path

from agencli.constants import DEFAULT_USER_CONFIG


class ConfigError(Exception):
    """Custom exception for configuration errors."""

    pass


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""

    pass


def get_config_path() -> Path:
    " Get the path to the config file. " ""
    return Path.home() / ".config" / "sidekick.json"


def config_exists() -> bool:
    """Check if the config file exists."""
    return get_config_path().exists()


def read_config_file() -> Dict[str, Any]:
    """Read and parse the config file.

    Returns:
        dict: Parsed configuration

    Raises:
        ConfigError: If config file doesn't exist or can't be accessed
        ConfigValidationError: If config file contains invalid JSON
    """
    config_path = get_config_path()

    if not config_path.exists():
        raise ConfigError(f"Configuration file not found at {config_path}")

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except PermissionError as e:
        raise ConfigError(f"Cannot access config file at {config_path}") from e
    except json.JSONDecodeError as e:
        raise ConfigValidationError(
            f"Invalid JSON in config file at {config_path}"
        ) from e


def deep_merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries, preserving existing values in update.

    Args:
        base: Base dictionary with default values
        update: Dictionary with user values to preserve

    Returns:
        Merged dictionary with all keys from base and values from update where they exist
    """
    result = base.copy()

    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def ensure_config_structure() -> Dict[str, Any]:
    """Ensure the config file has all expected keys with defaults for missing ones.

    This function reads the existing config, merges it with the default structure,
    and writes back the updated config if any keys were missing.

    Returns:
        The updated configuration dictionary

    Raises:
        ConfigError: If config file cannot be read or written
    """
    try:
        config = read_config_file()
    except ConfigError:
        raise

    original_config = json.dumps(config, sort_keys=True)
    merged_config = deep_merge_dicts(DEFAULT_USER_CONFIG, config)
    updated_config = json.dumps(merged_config, sort_keys=True)

    if original_config != updated_config:
        try:
            config_path = get_config_path()
            with open(config_path, "w") as f:
                json.dump(merged_config, f, indent=2)
        except (PermissionError, IOError) as e:
            raise ConfigError(f"Failed to update config file with missing keys: {e}")

    return merged_config


def set_env_vars(env_vars: Dict[str, str]) -> None:
    """Set environment variables from the config.

    Args:
        env_vars: Dictionary of environment variables to set
    """
    for key, value in env_vars.items():
        if value and isinstance(value, str):
            os.environ[key] = value


def validate_config_structure(config: Dict[str, Any]) -> None:
    """Validate the configuration structure.

    Args:
        config: Configuration dictionary to validate

    Raises:
        ConfigValidationError: If required fields are missing or invalid
    """
    if not isinstance(config, dict):
        raise ConfigValidationError("Configuration must be a JSON object")

    if "default_model" not in config:
        raise ConfigValidationError("Config missing required field 'default_model'")

    if not isinstance(config["default_model"], str):
        raise ConfigValidationError("Field 'default_model' must be a string")

    if "env" not in config:
        raise ConfigValidationError("Config missing required field 'env'")

    if not isinstance(config["env"], dict):
        raise ConfigValidationError("Field 'env' must be a JSON object")
