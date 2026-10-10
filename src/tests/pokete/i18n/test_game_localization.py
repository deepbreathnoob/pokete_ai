"""Gameplay display localization must not alter canonical game data."""

import copy
from string import Formatter

import pytest

from pokete.i18n import _, set_language
from pokete.classes.asset_service.service import asset_service
from pokete.classes.attack import Attack
from pokete.classes.items import LearnDisc
from pokete.classes.poke.nature import PokeNature
from pokete.classes.types import types


@pytest.fixture(autouse=True)
def restore_language():
    set_language("pl")
    yield
    set_language("en")


def test_translated_assets_keep_identifiers_and_mechanics():
    set_language("en")
    source = copy.deepcopy(asset_service.get_base_assets().to_dict())
    set_language("pl")
    localized = asset_service.get_base_assets().to_dict()
    for collection in source:
        assert (
            source[collection].keys() == localized[collection].keys()
            if isinstance(source[collection], dict)
            else source[collection] == localized[collection]
        )
    for collection, fields in (
        ("pokes", ("desc",)),
        ("attacks", ("name", "desc")),
        ("achievements", ("title", "desc")),
        ("weathers", ("info",)),
    ):
        for identifier, resource in source[collection].items():
            for field, value in resource.items():
                if field not in fields:
                    assert localized[collection][identifier][field] == value
    set_language("en")
    assert asset_service.get_base_assets().to_dict() == source


def test_attack_and_type_ids_are_canonical():
    attack = Attack("tackle")
    assert attack.index == "tackle"
    assert attack.name == "Natarcie"
    assert types.fire.name == "fire"
    assert types.fire.display_name == "ognisty"
    assert PokeNature.from_dict({"nature": "brave", "grade": 2}).dict() == {
        "nature": "brave",
        "grade": 2,
    }


def test_early_items_follow_selected_locale():
    item = asset_service.get_items()["healing_potion"]
    assert item.name == "healing_potion"
    assert item.pretty_name == "Mikstura lecznicza"
    set_language("en")
    assert item.pretty_name == "Healing potion"
    set_language("pl")
    disc = asset_service.get_items()["ld_flying"]
    assert disc.name == "ld_flying"
    assert "Lot" in disc.pretty_name
    assert "Lot" in disc.desc


def test_every_catalog_template_preserves_parameters():
    from pokete import i18n

    formatter = Formatter()
    for key, translated in i18n._translation._catalog.items():
        if not isinstance(key, str) or not key:
            continue
        original = key.split("\x04")[-1]
        expected = {
            field for _, field, _, _ in formatter.parse(original) if field is not None
        }
        actual = {
            field for _, field, _, _ in formatter.parse(translated) if field is not None
        }
        assert actual == expected, original


def test_dormant_views_are_rebuilt_in_polish():
    from pokete.classes.localized_views import refresh_localized_views
    from pokete.classes.movemap import movemap
    from pokete.classes.detail import detail
    from pokete.classes.inv.buy import buy

    refresh_localized_views()
    assert detail.name_label.text == "Szczegóły"
    assert buy.name_label.text == "Sklep"
    assert any("Druż." in label.text for label in movemap.labels)
    assert sum(label.width + 2 for label in movemap.labels) <= 80
