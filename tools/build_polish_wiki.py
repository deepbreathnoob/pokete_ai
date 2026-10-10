#!/usr/bin/env python3
"""Generate the Polish player encyclopedia from canonical game data."""

from pathlib import Path

import pokete.data as data
from pokete.classes.effects import effect_list
from pokete.i18n import _, pgettext, set_language
from pokete.release import VERSION


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headings, rows):
    return (
        "| "
        + " | ".join(headings)
        + " |\n|"
        + "|".join(" --- " for _ in headings)
        + "|\n"
        + "".join("| " + " | ".join(cell(v) for v in row) + " |\n" for row in rows)
        + "\n"
    )


def build():
    set_language("pl")
    out = f"# Pokete — encyklopedia\n\nWersja {VERSION}. Dane pochodzą z tej gałęzi repozytorium.\n\n[Instrukcja](HowToPlay.pl.md) · [Uruchamianie](../README.pl.md)\n\n"
    out += "## Typy\n\n"
    out += table(
        ["Typ", "Skuteczny przeciw", "Mało skuteczny przeciw"],
        (
            (
                _(name).capitalize(),
                ", ".join(_(i) for i in value["effective"]) or "—",
                ", ".join(_(i) for i in value["ineffective"]) or "—",
            )
            for name, value in data.types.items()
        ),
    )
    out += "## Pokete\n\nNazwy własne gatunków pozostają oryginalne. HP, atak, obrona i inicjatywa to wartości bazowe.\n\n"
    for identifier, poke in data.pokes.items():
        if identifier == "__fallback__":
            continue
        out += f"### {poke['name']}\n\n{_(poke['desc'])}\n\n"
        out += table(
            ["Typ", "HP", "Atak", "Obrona", "Inicjatywa", "Aktywność"],
            [
                [
                    ", ".join(_(t) for t in poke["types"]),
                    poke["hp"],
                    poke["atc"],
                    poke["defense"],
                    poke["initiative"],
                    {True: "Noc", False: "Dzień", None: "Zawsze"}[poke["night_active"]],
                ]
            ],
        )
        out += (
            "Ataki początkowe: "
            + ", ".join(_(data.attacks[a]["name"]) for a in poke["attacks"])
            + ".\n\n"
        )
        evolution = poke.get("evolve_poke")
        if evolution:
            out += f"Ewolucja: {data.pokes[evolution]['name']} na poziomie {poke['evolve_lvl']}.\n\n"
    out += "## Ataki\n\n"
    out += table(
        ["Atak", "Typ", "Mnożnik", "AP", "Min. poziom", "Opis"],
        (
            (
                _(a["name"]),
                ", ".join(_(t) for t in a["types"]),
                a["factor"],
                a["ap"],
                a["min_lvl"],
                _(a["desc"]),
            )
            for a in data.attacks.values()
        ),
    )
    out += "## Przedmioty\n\n"
    out += table(
        ["Przedmiot", "Cena", "Opis"],
        (
            (
                _(i["pretty_name"]),
                "$" + str(i["price"])
                if i["price"] is not None
                else "nie jest na sprzedaż",
                _(i["desc"]),
            )
            for i in data.items.values()
        ),
    )
    out += "Płytki nauki oznaczone „PN” uczą wskazanego ataku.\n\n## Natury\n\n"
    out += table(
        ["Natura", "Atak", "Obrona", "Inicjatywa"],
        (
            (
                pgettext("nature", name),
                n.get("atc", 1),
                n.get("def_", 1),
                n.get("init", 1),
            )
            for name, n in data.natures.items()
        ),
    )
    out += "Mnożniki natury są podnoszone do potęgi jej stopnia (1 lub 2).\n\n## Efekty\n\n"
    for effect in effect_list:
        out += _(effect.desc) + "\n\n"
    out += "## Pogoda\n\n"
    for weather in data.weathers.values():
        out += (
            _(weather["info"])
            + " Mnożniki ataków: "
            + ", ".join(
                f"{_(name)} × {factor}" for name, factor in weather["effected"].items()
            )
            + ".\n\n"
        )
    out += "## Osiągnięcia\n\n"
    out += table(
        ["Osiągnięcie", "Warunek"],
        ((_(a["title"]), _(a["desc"])) for a in data.achievements.values()),
    )
    out += "## Świat\n\n"
    for name, station in data.stations.items():
        out += (
            f"- **{_(data.maps[name]['pretty_name'])}**: {_(station['gen']['desc'])}\n"
        )
    path = Path(__file__).resolve().parents[1] / "docs/wiki.pl.md"
    path.write_text(out)
    print(path)


if __name__ == "__main__":
    build()
