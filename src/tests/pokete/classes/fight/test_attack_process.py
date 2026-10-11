from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pokete.classes.attack import Attack
from pokete.classes.fight.attack_process import AttackProcess
from pokete.classes.poke import Poke
from pokete.data.attacks import attacks
from pokete.i18n import get_language, set_language


def make_attacker(atc: int):
    return SimpleNamespace(atc=atc)


def make_defender(defense: int):
    return SimpleNamespace(defense=defense)


def make_attack(factor: float):
    return SimpleNamespace(factor=factor)


def test_get_hp_returns_zero_on_miss():
    attacker = make_attacker(10)
    defender = make_defender(2)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=0, eff=1)

    assert damage == 0


def test_get_hp_has_minimum_damage_floor_of_3_on_damaging_hit():
    attacker = make_attacker(2)
    defender = make_defender(10)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 3


def test_get_hp_keeps_higher_damage_values():
    attacker = make_attacker(12)
    defender = make_defender(2)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 6


def test_get_hp_treats_zero_defense_as_one():
    attacker = make_attacker(5)
    defender = make_defender(0)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 5


@pytest.mark.parametrize(
    "name", [name for name, data in attacks.items() if data["factor"] == 0]
)
def test_zero_power_moves_do_not_get_minimum_damage(name):
    attack = Attack(name)
    for random_factor in (0.75, 1, 1.26):
        for effectiveness in (0.5, 1, 1.3, 2):
            assert (
                AttackProcess.get_hp(
                    make_attacker(100),
                    make_defender(0),
                    attack,
                    random_factor=random_factor,
                    eff=effectiveness,
                )
                == 0
            )


@pytest.mark.parametrize("language", ["en", "pl"])
@pytest.mark.parametrize("hit", [True, False])
def test_polish_changes_stats_without_hurting_opponent(monkeypatch, language, hit):
    previous_language = get_language()
    set_language(language)
    try:
        attacker = Poke("steini", 50)
        defender = Poke("steini", 50)
        attack = Attack("politure")
        before = (attacker.atc, attacker.defense, attacker.hp, defender.hp, attack.ap)
        attacker.moves = Mock()
        attacker.hp_bar = Mock()
        defender.hp_bar = Mock()
        fightmap = Mock()
        monkeypatch.setattr(
            "pokete.classes.fight.attack_process.time.sleep", lambda _: None
        )
        monkeypatch.setattr(
            AttackProcess, "get_random_factor", staticmethod(lambda *_: 1 if hit else 0)
        )
        AttackProcess(fightmap)(
            attacker,
            defender,
            attack,
            [SimpleNamespace(map=SimpleNamespace(weather=None))],
        )
        assert attacker.atc == before[0] + int(hit)
        assert attacker.defense == before[1] + int(hit)
        assert (attacker.hp, defender.hp) == before[2:4]
        assert attack.ap == before[4] - 1
        assert attack.index == "politure"
        assert attack.name == ("Polerowanie" if language == "pl" else "Polish")
        assert fightmap.show_effectivity.call_args.args[1] == 0
    finally:
        set_language(previous_language)


@pytest.mark.parametrize("name, damage", [("sucker", 1), ("super_sucker", 2)])
def test_zero_power_drain_keeps_its_explicit_damage(monkeypatch, name, damage):
    attacker = Poke("steini", 50)
    defender = Poke("steini", 50)
    attacker.hp -= 5
    before = (attacker.hp, defender.hp)
    attacker.moves = Mock()
    attacker.hp_bar = Mock()
    defender.hp_bar = Mock()
    monkeypatch.setattr(
        "pokete.classes.fight.attack_process.time.sleep", lambda _: None
    )
    monkeypatch.setattr(AttackProcess, "get_random_factor", staticmethod(lambda *_: 1))
    AttackProcess(Mock())(
        attacker,
        defender,
        Attack(name),
        [SimpleNamespace(map=SimpleNamespace(weather=None))],
    )
    assert attacker.hp == before[0] + damage
    assert defender.hp == before[1] - damage
