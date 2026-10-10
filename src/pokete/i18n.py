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
    return _translation.gettext(message) if message else ""


def ngettext(singular, plural, count):
    return _translation.ngettext(singular, plural, count)


def localize_base_assets(assets):
    """Copy display fields only. Keys and mechanics remain canonical.

    No generated schema or protocol object is modified in place. Resources are
    cached per language; choosing another language requires restarting the game.
    """
    import copy

    key = (assets, get_language())
    if key not in _asset_cache:
        result = copy.deepcopy(assets)
        for collection, fields in (
            (result.pokes, ("desc",)),
            (result.attacks, ("name", "desc")),
            (result.achievements, ("title", "desc")),
            (result.weathers, ("info",)),
        ):
            for resource in collection.values():
                for field in fields:
                    setattr(resource, field, _(getattr(resource, field)))
        _asset_cache[key] = result
    return _asset_cache[key]


_asset_cache = {}


def pgettext(context, message):
    return _translation.pgettext(context, message)


def localize_sign(text):
    """Translate signs within their existing collision footprint."""
    for label in ("Center!", "Shop!", "Pokete-Care"):
        translated = _(label)
        if len(translated) <= len(label):
            text = text.replace(label, translated.ljust(len(label)))
    return text
