"""Small channel catalog adapter used by the uploaded bot.

The original script expects a separate Channel.py module. This adapter keeps
that interface while allowing channel data to be supplied safely through a
JSON file or CHANNELS_JSON. No private stream URLs are embedded in the code.

Supported JSON shapes:
  {"Channel Name": "https://..."}
  {"Channel Name": {"url": "https://...", "variants": {"1": "https://..."}}}
  [{"name": "Channel Name", "url": "https://..."}]
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


_DEFAULT_FILE = Path(os.getenv("CHANNELS_FILE", "data/channels.json"))


def _load_raw() -> Any:
    inline = os.getenv("CHANNELS_JSON", "").strip()
    if inline:
        try:
            return json.loads(inline)
        except json.JSONDecodeError:
            return {}
    if not _DEFAULT_FILE.exists():
        return {}
    try:
        return json.loads(_DEFAULT_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _entries() -> dict[str, Any]:
    raw = _load_raw()
    if isinstance(raw, dict):
        return {str(key).strip(): value for key, value in raw.items()}
    if isinstance(raw, list):
        result: dict[str, Any] = {}
        for item in raw:
            if isinstance(item, dict) and item.get("name"):
                result[str(item["name"]).strip()] = item
        return result
    return {}


def get_public_channels() -> list[str]:
    """Return configured channel names for the bot's menus."""
    return list(_entries())


def get_channel_url(channel_name: str, variant: int | str | None = None) -> str | None:
    """Resolve a configured channel name and optional numbered variant."""
    entries = _entries()
    requested = str(channel_name or "").strip()
    if not requested:
        return None

    def find_key(key: str) -> Any:
        for name, value in entries.items():
            if name.casefold() == key.casefold():
                return value
        return None

    value = find_key(requested)
    if variant is not None:
        variant_text = str(variant).strip()
        for candidate in (
            f"{requested} {variant_text}",
            f"{requested}_{variant_text}",
            f"{requested}-{variant_text}",
        ):
            variant_value = find_key(candidate)
            if variant_value is not None:
                value = variant_value
                break

        if isinstance(value, dict):
            variants = value.get("variants", {})
            if isinstance(variants, dict):
                value = variants.get(variant_text, variants.get(str(variant)))

    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        url = value.get("url")
        return str(url).strip() if url else None
    return None