"""Gameplay display localization must not alter canonical game data."""

import copy
from string import Formatter

import pytest

from pokete.classes.asset_service.service import asset_service
from pokete.classes.attack import Attack
from pokete.classes.poke.nature import PokeNature
from pokete.classes.types import types
from pokete.i18n import set_language


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
    from pokete.classes.detail import detail
    from pokete.classes.inv.buy import buy
    from pokete.classes.localized_views import refresh_localized_views
    from pokete.classes.movemap import movemap

    refresh_localized_views()
    assert detail.name_label.text == "Szczegóły"
    assert buy.name_label.text == "Sklep"
    assert any("Druż." in label.text for label in movemap.labels)
    assert sum(label.width + 2 for label in movemap.labels) <= 80


def test_source_and_bundled_data_have_catalog_entries():
    import ast
    from pathlib import Path

    import pokete.data as data
    from pokete import i18n

    catalog = i18n._translation._catalog

    def check(message, context=None):
        if message:
            assert ((context + "\x04" + message) if context else message) in catalog, (
                message
            )

    for path in Path(i18n.__file__).parent.rglob("*.py"):
        if "resources" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in ("_", "tr")
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                check(node.args[0].value)
    for collection, fields in (
        (data.attacks, ("name", "desc")),
        (data.pokes, ("desc",)),
        (data.items, ("pretty_name", "desc")),
        (data.weathers, ("info",)),
        (data.achievements, ("title", "desc")),
        (data.maps, ("pretty_name",)),
    ):
        for resource in collection.values():
            for field in fields:
                check(resource.get(field))

    def chat(value):
        for question in value.get("q", []):
            check(question)
        for answer, reply in value.get("a", {}).items():
            check(answer)
            chat(reply)

    for npc in data.npcs.values():
        for text in npc["texts"]:
            check(text)
        chat(npc.get("chat", {}))
    for group in data.trainers.values():
        for trainer in group["trainers"]:
            for field in ("texts", "lose_texts", "win_texts"):
                for text in trainer["args"][field]:
                    check(text)
    for station in data.stations.values():
        check(station["gen"]["desc"])
    for nature in data.natures:
        check(nature, context="nature")


def test_choice_labels_translate_without_changing_return_values():
    from pokete.classes.interactions.multi_text_choose_box import MultiTextChooseBox

    menu = MultiTextChooseBox(["Where are you from?", "No"], "Answer")
    assert menu.elems[0].text == "Skąd jesteś?"
    assert menu.choose(None, 0) == (0, "Where are you from?")
    assert menu.name_label.text == "Odpowiedź"
    assert all(label.width + 6 <= menu.width for label in menu.elems)


def test_signs_keep_collision_geometry():
    from pokete.data.map_data import CENTER, SHOP
    from pokete.i18n import localize_sign

    for text in (CENTER, SHOP):
        localized = localize_sign(text)
        assert [len(line) for line in localized.splitlines()] == [
            len(line) for line in text.splitlines()
        ]
        assert [i for i, char in enumerate(text) if char.isspace()] == [
            i for i, char in enumerate(localized) if char.isspace()
        ]
    assert "Centrum" in localize_sign(CENTER)
    assert "Sklep" in localize_sign(SHOP)


def test_questions_wrap_before_layout():
    from pokete.base.input_loops.ask.bool import AskBoolBox
    from pokete.base.input_loops.ask.ok import AskOkBox

    for cls in (AskBoolBox, AskOkBox):
        box = cls(
            "Czy przyjąć ten niezwykle potężny przedmiot od starszego mieszkańca wioski?",
            max_width=66,
        )
        assert box.width <= 70
        assert box.height > 4


@pytest.mark.parametrize(
    "count, ending",
    [
        (1, "1 mod:"),
        (2, "2 mody:"),
        (5, "5 modów:"),
        (12, "12 modów:"),
        (22, "22 mody:"),
    ],
)
def test_mod_count_uses_polish_plural_forms(count, ending):
    from pokete.i18n import ngettext

    text = ngettext(
        "Currently {count} mod is loaded:", "Currently {count} mods are loaded:", count
    ).format(count=count)
    assert text.endswith(ending)


@pytest.mark.parametrize("language, heading", [("pl", "Użycie:"), ("en", "Usage:")])
def test_cli_help_works_without_terminal(language, heading, tmp_path):
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pokete",
            "--language",
            language,
            "--save_dir",
            str(tmp_path),
            "--help",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert heading in result.stdout
    assert not result.stderr


def test_cli_help_uses_saved_language(tmp_path):
    import json
    import subprocess
    import sys

    (tmp_path / "pokete.json").write_text(json.dumps({"settings": {"language": "pl"}}))
    result = subprocess.run(
        [sys.executable, "-m", "pokete", "--save_dir", str(tmp_path), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Użycie:" in result.stdout


def test_empty_messages_never_expose_gettext_header():
    from pokete.classes.multiplayer.menu import ModeChooser
    from pokete.classes.pre_game import PreGameMap
    from pokete.i18n import _ as tr

    assert tr("") == ""
    menu = ModeChooser()
    for row in menu.nest_label_obs:
        for item in row:
            assert item.name_label.text == ""
    menu.center_add(PreGameMap())
    menu.remove()


def test_short_ok_message_fits_key_label():
    from pokete.base.input_loops.ask.ok import AskOkBox
    from pokete.classes.pre_game import PreGameMap

    box = AskOkBox("OK")
    assert all(getattr(obj, "width", 0) + obj.rx <= box.width for obj in box.obs)
    box.center_add(PreGameMap())
    box.remove()


def test_bundled_multiplayer_messages_have_translations():
    import json
    from pathlib import Path

    from pokete import i18n

    root = Path(__file__).resolve().parents[4]
    catalog = i18n._translation._catalog

    def check(value, field=""):
        if isinstance(value, dict):
            if field == "a":
                for answer in value:
                    assert answer in catalog, answer
            for key, child in value.items():
                check(child, key)
        elif isinstance(value, list):
            for child in value:
                check(child, field)
        elif (
            isinstance(value, str)
            and field
            in (
                "desc",
                "pretty_name",
                "title",
                "info",
                "texts",
                "win_texts",
                "lose_texts",
                "q",
            )
            and value
        ):
            assert value in catalog, value

    for name in ("base_assets.json", "assets.json"):
        check(json.loads((root / "pkg/server/res" / name).read_text()))


def test_hotkey_action_names_are_display_only():
    from pokete.base.input.hotkeys import Action

    assert Action.LEFT.name == "LEFT"
    assert Action.LEFT.display_name == "W lewo"
    assert Action.ACT_1.display_name == "Akcja 1"
    assert Action.QUICK_ATC_1.display_name == "Szybki atak 1"


def test_evolution_reports_and_replaces_the_actual_pokete(monkeypatch):
    import importlib
    from types import SimpleNamespace

    from pokete.base.context import Context
    from pokete.base.periodic_event_manager import PeriodicEventManager
    from pokete.classes.moves import Moves
    from pokete.classes.poke import Poke, Stats
    from pokete.data import pokes

    module = importlib.import_module("pokete.classes.poke.evomap")
    identifier = next(
        name for name, resource in pokes.items() if resource["evolve_poke"]
    )
    poke = Poke(identifier, 10000)
    poke.set_poke_stats(Stats(poke.name, None))
    figure = SimpleNamespace(pokes=[poke], caught_pokes=[identifier])
    view = module.EvoMap(24, 80)
    outputs = []
    monkeypatch.setattr(module.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(module.loops, "std", lambda ctx: None)
    monkeypatch.setattr(module.achievements, "achieve", lambda identifier: None)
    monkeypatch.setattr(Moves, "shine", lambda self: None)
    monkeypatch.setattr(view, "show", lambda *args, **kwargs: None)
    monkeypatch.setattr(view.outp, "outp", outputs.append)
    monkeypatch.setattr(module, "LearnAttack", lambda new: lambda ctx: None)
    assert view(Context(PeriodicEventManager([]), view, view, figure), poke)
    assert figure.pokes[0].identifier == poke.evolve_poke
    assert figure.pokes[0].identifier in figure.caught_pokes
    assert outputs[-1] == f"{poke.name} ewoluuje w {figure.pokes[0].name}!"
