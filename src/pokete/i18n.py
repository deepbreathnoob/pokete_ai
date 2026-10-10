"""Display-only translations; game identifiers and save keys stay unchanged."""

import gettext
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = ("en", "pl")
LOCALE_DIR = Path(__file__).with_name("locales")
_language = "en"
_translation: gettext.NullTranslations = gettext.NullTranslations()


def resolve_language(cli_language=None, saved_language=None):
    """CLI overrides saved preference, then POKETE_LANGUAGE, then English."""
    for value in (cli_language, saved_language, os.getenv("POKETE_LANGUAGE"), "en"):
        if value in SUPPORTED_LANGUAGES:
            return value
    return "en"


def set_language(language):
    """Select a catalog. Unknown languages and missing messages use English."""
    global _language, _translation
    _language = language if language in SUPPORTED_LANGUAGES else "en"
    try:
        _translation = gettext.translation(
            "pokete", localedir=LOCALE_DIR, languages=[_language], fallback=True
        )
    except (OSError, EOFError, ValueError):
        logger.warning("Could not load %s translations", _language)
        _translation = gettext.NullTranslations()
    return _language


def get_language():
    return _language


def _(message):
    """Translate a complete message before interpolating named parameters."""
    return _translation.gettext(message)


def ngettext(singular, plural, count):
    return _translation.ngettext(singular, plural, count)
