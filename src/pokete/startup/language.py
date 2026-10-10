"""Read language preference without importing UI or executing legacy saves."""

import json
from pathlib import Path

from pokete.i18n import resolve_language, set_language


def configure_language(cli_language, save_dir):
    saved_language = None
    for path in (save_dir / "pokete.json", Path.home() / ".cache/pokete/pokete.json"):
        try:
            data = json.loads(path.read_text())
            saved_language = data.get("settings", {}).get("language")
            break
        except (OSError, ValueError, AttributeError):
            continue
    return set_language(resolve_language(cli_language, saved_language))
