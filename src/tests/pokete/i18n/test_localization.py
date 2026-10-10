import ast
import gettext
import os
from pathlib import Path
from string import Formatter
from types import SimpleNamespace

import pytest

from pokete import i18n
from pokete.startup.command import PoketeCommand


@pytest.fixture(autouse=True)
def reset_language():
    i18n.set_language("en")
    yield
    i18n.set_language("en")


def test_polish_catalog_and_english_fallback():
    i18n.set_language("pl")
    assert i18n._("Save") == "Zapisz"
    assert i18n._("Achievements") == "Osiągnięcia"
    assert i18n._("Untranslated message") == "Untranslated message"
    i18n.set_language("en")
    assert i18n._("Save") == "Save"


def test_missing_catalog_does_not_interrupt_game(monkeypatch, tmp_path):
    monkeypatch.setattr(i18n, "LOCALE_DIR", tmp_path)
    i18n.set_language("pl")
    assert i18n._("Save") == "Save"
    assert i18n.ngettext("item", "items", 2) == "items"


@pytest.mark.parametrize(
    "cli,saved,env,expected",
    [
        ("pl", "en", "en", "pl"),
        (None, "pl", "en", "pl"),
        (None, None, "pl", "pl"),
        (None, None, None, "en"),
        (None, "invalid", "pl", "pl"),
        (None, "invalid", "invalid", "en"),
    ],
)
def test_language_precedence(monkeypatch, cli, saved, env, expected):
    if env is None:
        monkeypatch.delenv("POKETE_LANGUAGE", raising=False)
    else:
        monkeypatch.setenv("POKETE_LANGUAGE", env)
    assert i18n.resolve_language(cli, saved) == expected


def test_language_flag_is_parsed(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pokete", "--language", "pl", "--no_audio"])
    command = PoketeCommand(SimpleNamespace())
    command.run()
    assert command.language == "pl"
    assert command.audio.use_audio is False


@pytest.mark.parametrize("values", [[], ["de"], ["pl", "en"]])
def test_language_flag_rejects_invalid_arguments(values):
    command = PoketeCommand(SimpleNamespace())
    with pytest.raises(SystemExit) as exc:
        command.root_fn("pokete", [], {"--language": values})
    assert exc.value.code == 2


def test_catalog_preserves_named_placeholders_and_polish_plural_rules():
    catalog = gettext.translation("pokete", i18n.LOCALE_DIR, languages=["pl"])
    # Covers 1, 2-4, 5+, teens, zero and numbers such as 22/112.
    assert [catalog.plural(n) for n in (0, 1, 2, 4, 5, 12, 22, 112)] == [
        2,
        0,
        1,
        1,
        2,
        2,
        1,
        2,
    ]
    formatter = Formatter()
    source_root = Path(i18n.__file__).parent
    count = 0
    for path in source_root.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                msg = node.args[0].value
                translated = catalog.gettext(msg)

                def fields(text):
                    return {
                        field
                        for _, field, _, _ in formatter.parse(text)
                        if field is not None
                    }

                assert fields(msg) == fields(translated), (path, msg)
                count += 1
    assert count >= 43


def test_old_save_keeps_identifiers_and_adds_language(monkeypatch, tmp_path):
    monkeypatch.setattr(
        os, "get_terminal_size", lambda *args: os.terminal_size((80, 24))
    )
    from pokete import release
    from pokete.classes.save import read_save
    from pokete.classes.settings import Settings

    monkeypatch.setattr(release, "SAVEPATH", tmp_path)
    import json

    old_save = {
        "settings": {"autosave": False},
        "pokes": {"0": {"name": "steini", "attacks": ["tackle"]}},
        "used_npcs": ["Leader Sebastian"],
    }
    (tmp_path / "pokete.json").write_text(json.dumps(old_save))
    loaded = read_save()
    settings = Settings()
    settings.from_dict(loaded["settings"])
    assert settings("language").val == "en"
    settings("language").val = "pl"
    loaded["settings"] = settings.to_dict()
    (tmp_path / "pokete.json").write_text(json.dumps(loaded))
    reread = read_save()
    assert reread["settings"]["language"] == "pl"
    assert reread["settings"]["autosave"] is False
    assert reread["pokes"] == old_save["pokes"]
    assert reread["used_npcs"] == old_save["used_npcs"]


@pytest.mark.parametrize("language", ["pl", "en"])
def test_menu_and_dialog_labels_fit_and_follow_current_keys(monkeypatch, language):
    monkeypatch.setattr(
        os, "get_terminal_size", lambda *args: os.terminal_size((80, 24))
    )
    from pokete.base.input import hotkeys
    from pokete.base.input.hotkeys import Action, ActionList
    from pokete.base.input_loops.ask.bool import AskBoolBox
    from pokete.base.ui.views.boxes import InfoBoxView
    from pokete.classes.menu import Menu
    from pokete.classes.settings import settings
    from pokete.classes.side_loops import Help

    settings.from_dict({"language": language})
    i18n.set_language(language)
    menu = Menu()
    menu.add_elems()
    assert menu.save_label.text == ("Zapisz" if language == "pl" else "Save")
    for element in menu.c_obs:
        assert element.rx + element.width <= menu.width - 1
    monkeypatch.setattr(
        hotkeys,
        "hotkey_mappings",
        {
            "t": ActionList([Action.ACCEPT]),
            "n": ActionList([Action.CANCEL]),
            "k": ActionList([Action.UP]),
            "j": ActionList([Action.DOWN]),
            "h": ActionList([Action.LEFT]),
            "l": ActionList([Action.RIGHT]),
            "e": ActionList([Action.MENU]),
        },
    )
    box = AskBoolBox("OK?")
    # Short translated questions are allowed; labels must not overlap.
    labels = box._AskBoolBox__labels
    assert labels[0].text.startswith("[t]")
    assert labels[1].text.startswith("[n]")
    assert labels[0].rx + labels[0].width < labels[1].rx
    assert "k:" in Help().box.label.text
    assert (
        InfoBoxView("test")
        .info_labels[0]
        .text.endswith("zamknij" if language == "pl" else "close")
    )
    assert InfoBoxView("test", info=None).info_labels == []
