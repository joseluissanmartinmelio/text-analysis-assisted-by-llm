import os
from typing import Dict, Any


def get_openrouter_config() -> Dict[str, Any]:

    api_key = os.environ.get("OPENROUTER_API_KEY", "")

    if not api_key:
        try:
            import sys
            from pathlib import Path

            if getattr(sys, "frozen", False):
                config_path = Path(os.path.dirname(sys.executable)) / "config.ini"
            else:
                config_path = Path(__file__).parent.parent / "config.ini"

            if config_path.exists():
                with open(config_path, "r") as f:
                    for line in f:
                        if "OPENROUTER_API_KEY" in line:
                            api_key = line.split("=")[1].strip()
                            os.environ["OPENROUTER_API_KEY"] = api_key
                            break
        except Exception:
            pass

    return {
        "api_key": api_key,
        "base_url": "https://openrouter.ai/api/v1",
        "headers": {
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Text Analysis LLM Assistant",
        },
    }


def get_available_models() -> Dict[str, str]:

    return {
        "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
        "claude-3-opus": "anthropic/claude-3-opus",
        "gpt-4-turbo": "openai/gpt-4-turbo",
        "gpt-4o": "openai/gpt-4o",
        "deepseek-r1": "deepseek/deepseek-r1",
        "gemini-pro": "google/gemini-pro-1.5",
        "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct",
    }


def validate_api_key(api_key: str = None) -> bool:

    if api_key:
        return len(api_key) > 20

    config = get_openrouter_config()
    return len(config["api_key"]) > 20
