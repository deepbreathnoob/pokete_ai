#!/usr/bin/env python3
"""Rebuild POT and check bundled player-facing messages (development: polib)."""

import ast
from pathlib import Path

import polib

import pokete.data as data

ROOT = Path(__file__).resolve().parents[1]
POT = ROOT / "src/pokete/locales/pokete.pot"
PO = ROOT / "src/pokete/locales/pl/LC_MESSAGES/pokete.po"


def messages():
    result = {}

    def add(message, context=None, plural=None, source="data"):
        if message:
            result.setdefault((context, message, plural), set()).add(source)

    for path in (ROOT / "src/pokete").rglob("*.py"):
        if "resources" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Call):
                continue
            fn = ast.unparse(node.func).split(".")[-1]
            args = node.args
            source = f"{path.relative_to(ROOT)}:{node.lineno}"
            if (
                fn in ("_", "tr")
                and args
                and isinstance(args[0], ast.Constant)
                and isinstance(args[0].value, str)
            ):
                add(args[0].value, source=source)
            elif (
                fn == "ngettext"
                and len(args) >= 2
                and all(isinstance(a, ast.Constant) for a in args[:2])
            ):
                add(args[0].value, plural=args[1].value, source=source)
            elif (
                fn == "pgettext"
                and len(args) >= 2
                and all(isinstance(a, ast.Constant) for a in args[:2])
            ):
                add(args[1].value, context=args[0].value, source=source)

    for collection, fields in (
        (data.attacks, ("name", "desc")),
        (data.pokes, ("desc",)),
        (data.items, ("pretty_name", "desc")),
        (data.weathers, ("info",)),
        (data.achievements, ("title", "desc")),
        (data.maps, ("pretty_name",)),
    ):
        for value in collection.values():
            for field in fields:
                add(value.get(field))
    for station in data.stations.values():
        add(station["gen"]["desc"])

    def chat(value):
        for question in value.get("q", []):
            add(question)
        for answer, reply in value.get("a", {}).items():
            add(answer)
            chat(reply)

    for npc in data.npcs.values():
        for text in npc.get("texts", []):
            add(text)
        chat(npc.get("chat", {}))
    for trainers in data.trainers.values():
        for trainer in trainers["trainers"]:
            args = trainer["args"]
            add(args["name"])
            add(args["gender"])
            for field in ("texts", "lose_texts", "win_texts"):
                for text in args[field]:
                    add(text)
    for typ in list(data.types) + data.sub_types:
        add(typ)
    for nature in data.natures:
        add(nature, context="nature")

    from pokete.base.input.hotkeys import Action

    for action in Action:
        if not action.name.startswith(("ACT_", "QUICK_ATC_")):
            add(action.name)

    from pokete.classes.effects import effect_list
    from pokete.classes.map_additions.center import CUDDLE_MESSAGES
    from pokete.classes.multiplayer.interactions.context_menu import (
        OPTION_FIGHT,
        OPTION_QUIT,
        OPTION_TRADE,
    )
    from pokete.classes.npcs.data.actions import GiveBasic, actions

    for effect in effect_list:
        add(effect.desc)
    for text in CUDDLE_MESSAGES:
        add(text)
    for action in actions.values():
        if isinstance(action, GiveBasic):
            add(action.name)
    for label in (
        "Center!",
        "Shop!",
        "Pokete-Care",
        "Your deck",
        "Your full deck",
        "Inventory",
        "Shop",
        "Clock",
        "Nature",
        "Achievements",
        "Poketedex",
        "Attack Info",
        "Effect Info",
        "Roadmap",
        "Choose a Pokete to cuddle",
        "Interface language: en or pl",
        "Enables logging",
        "Disables mods",
        "Disables audio",
        "Shows help for a specific command",
        "Welcome to the server",
        "This server",
        "Welcome on the server!",
        OPTION_FIGHT,
        OPTION_TRADE,
        OPTION_QUIT,
    ):
        add(label)
    return result


def main():
    po = polib.pofile(PO)
    pot = polib.POFile()
    pot.metadata = dict(
        po.metadata,
        Language="",
        **{"Plural-Forms": "", "Project-Id-Version": "Pokete EN/PL"},
    )
    missing = []
    for (context, message, plural), refs in sorted(
        messages().items(), key=lambda pair: str(pair[0])
    ):
        pot.append(
            polib.POEntry(
                msgid=message,
                msgctxt=context,
                msgid_plural=plural or "",
                occurrences=[
                    tuple(ref.rsplit(":", 1)) if ":" in ref else (ref, "")
                    for ref in sorted(refs)
                ],
            )
        )
        entry = po.find(message, msgctxt=context)
        if (
            entry is None
            or entry.fuzzy
            or (
                not entry.msgstr
                and not all(entry.msgstr_plural.get(i) for i in range(3))
            )
        ):
            missing.append((context, message))
    pot.save(POT)
    if missing:
        for context, message in missing:
            print(f"MISSING [{context or 'default'}] {message!r}")
        raise SystemExit(1)
    print(f"{len(pot)} messages: complete Polish catalog, no fuzzy entries.")


if __name__ == "__main__":
    main()
