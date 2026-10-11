"""Regressions found while reviewing the complete localization change."""

import pytest
import scrap_engine as se

from pokete.classes.poke.poke import Poke
from pokete.i18n import set_language


@pytest.fixture(autouse=True)
def polish_language():
    set_language("pl")
    yield
    set_language("en")


@pytest.mark.parametrize(
    "mapping", ["Key.esc", "Key.backspace", "Key.enter", "Key.space"]
)
def test_special_key_labels_survive_view_refresh_and_mouse_click(monkeypatch, mapping):
    from types import SimpleNamespace

    from pokete.base.input import hotkeys
    from pokete.base.input.event import _ev
    from pokete.base.input.hotkeys import Action, ActionList, get_action
    from pokete.base.input.mouse import MouseEventType
    from pokete.base.ui.elements.labels import CloseLabel
    from pokete.classes.localized_views import refresh_localized_views

    mappings = {
        key: ActionList(action for action in actions if action != Action.CANCEL)
        for key, actions in hotkeys.hotkey_mappings.items()
    }
    mappings[mapping] = ActionList([Action.CANCEL])
    monkeypatch.setattr(
        hotkeys, "hotkey_mappings", {mapping: mappings.pop(mapping), **mappings}
    )
    monkeypatch.setattr(_ev, "emit_fn", lambda: None, raising=False)
    try:
        refresh_localized_views()
        label = CloseLabel()
        assert label.key.marshall() == mapping
        assert "Key." not in label.text
        label.interact(None, 0, SimpleNamespace(type=MouseEventType.LEFT, pressed=True))
        assert get_action()[0].triggers(Action.CANCEL)
    finally:
        _ev.clear()
        monkeypatch.undo()
        refresh_localized_views()


def test_all_bundled_signs_preserve_solid_cells():
    from pokete import data
    from pokete.i18n import localize_sign

    found_care = False
    for map_data in data.map_data.values():
        for collection in ("hard_obs", "soft_obs"):
            for obj in map_data[collection].values():
                original = obj["txt"]
                localized = localize_sign(original)
                assert len(localized) == len(original)
                assert [i for i, c in enumerate(original) if c.isspace()] == [
                    i for i, c in enumerate(localized) if c.isspace()
                ]
                if "Pokete-Care" in original:
                    found_care = True
                    assert "Opieka" in localized
    assert found_care


@pytest.mark.parametrize(
    "text",
    ["Bardzodluganiespodziewananazwa" * 3, "Pierwsza linia\n" + "dalsza czesc " * 12],
)
def test_output_and_questions_bound_every_line(monkeypatch, text):
    from pokete.base.input_loops.ask.bool import AskBoolBox
    from pokete.base.input_loops.ask.ok import AskOkBox
    from pokete.classes.classes import OutP

    for cls in (AskBoolBox, AskOkBox):
        box = cls(text, max_width=26)
        assert box.width <= 30
        assert (
            box._AskBoolBox__text_label.width <= 26
            if cls is AskBoolBox
            else box._AskOkBox__text_label.width <= 26
        )
    from pokete.base.game_map import GameMap

    screen = GameMap(50, 30)
    monkeypatch.setattr(screen, "full_show", lambda: None)
    output = OutP("")
    output.add(screen, 1, 0)
    output.outp(text)
    assert output.width <= 28
    assert "".join(output.text.splitlines()) == "".join(text.splitlines())


def test_learning_choices_fit_for_every_bundled_attack():
    from pokete.classes.asset_service.service import asset_service
    from pokete.classes.attack import Attack
    from pokete.classes.learnattack import LearnAttack

    poke = Poke("steini", 10, 0)
    attacks = list(asset_service.get_base_assets().attacks)
    for start in range(0, len(attacks), 4):
        poke.attack_obs = [Attack(name) for name in attacks[start : start + 4]]
        learning = LearnAttack(poke)
        learning.box.add_c_obs(
            [
                se.Text(f"{i + 1}: {attack.name}")
                for i, attack in enumerate(poke.attack_obs)
            ]
        )
        for label in learning.box.c_obs + learning.box.info_labels:
            assert label.rx + label.width <= learning.box.width - 1


def test_catalog_audit_rejects_wrong_keys_and_incomplete_plural_templates():
    import importlib.util
    from pathlib import Path

    polib = pytest.importorskip("polib")
    path = Path(__file__).resolve().parents[4] / "tools/localization_catalog.py"
    spec = importlib.util.spec_from_file_location("localization_catalog", path)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    plural = "{count} items"
    entry = polib.POEntry(
        msgid="{count} item",
        msgid_plural=plural,
        msgstr_plural={
            0: "{count} przedmiot",
            1: "{count} przedmioty",
            2: "{count} przedmiotów",
        },
    )
    assert audit.translation_complete(entry, None, entry.msgid, plural)
    entry.msgstr_plural[2] = "przedmiotów"
    assert not audit.translation_complete(entry, None, entry.msgid, plural)
    entry.msgstr_plural[2] = "{count} przedmiotów"
    entry.msgid_plural = "other items"
    assert not audit.translation_complete(entry, None, entry.msgid, plural)
    entry = polib.POEntry(msgid="brave", msgctxt="nature", msgstr="odważny")
    assert not audit.translation_complete(entry, None, "brave", None)
    assert audit.translation_complete(entry, "nature", "brave", None)


def test_active_notification_survives_view_refresh(monkeypatch):
    import pokete.base.ui.notify as notifications
    from pokete.base.ui.notify import Notifier
    from pokete.base.ui.util import get_nested
    from pokete.classes.localized_views import refresh_localized_views
    from pokete.classes.movemap import movemap

    notifier = Notifier()
    monkeypatch.setattr(notifications, "notifier", notifier)
    refresh_localized_views()
    notifier.set_vars(movemap)
    notifier.notify("Pierwsze", "Info", "Krótki komunikat")
    notifier.notify("Drugie", "Info", "Komunikat w kolejce")
    notification = notifier.notification
    for _ in range(2):
        refresh_localized_views()
        assert notifier.notified
        assert notifier.notification is notification
        assert len(notifier.wait) == 1
        assert all(obj in movemap.obs for obj in get_nested(notification))
        assert notification.x == movemap.width - notification.width
    notification.remove()
    notifier.notified = False


@pytest.mark.parametrize("language", ["pl", "en"])
def test_fight_attack_choices_and_info_fit_minimum_terminal(monkeypatch, language):
    from types import SimpleNamespace

    from pokete.base.game_map import GameMap
    from pokete.base.ui.util import get_nested
    from pokete.base.ui.views.choose_box import ChooseBoxView
    from pokete.classes.asset_service.service import asset_service
    from pokete.classes.attack import Attack
    from pokete.classes.fight.fightmap.attack import AttackBox

    set_language(language)
    screen = GameMap(19, 70)
    monkeypatch.setattr(screen, "show", lambda *args, **kwargs: None)
    box = AttackBox()
    attacks = [
        Attack(name, (i % 4) + 1)
        for i, name in enumerate(asset_service.get_base_assets().attacks)
    ]

    def check_layout(view, ctx):
        for label in view.elems:
            assert label.rx + label.width <= view.width - 1
        view.toggle_atk_box()
        for index in range(len(view.attack_obs)):
            view.on_index_change(index)
            for _ in range(2):
                for obj in get_nested(view):
                    assert 0 <= obj.x < screen.width
                    assert 0 <= obj.y < screen.height
                view.attack_info_box.toggle()
        return view.attack_obs[0]

    monkeypatch.setattr(ChooseBoxView, "__call__", check_layout)
    ctx = SimpleNamespace(map=screen, overview=None)
    for start in range(0, len(attacks), 4):
        group = attacks[start : start + 4]
        assert box(ctx, group) is group[0]
        assert not box.attack_info_box.added
