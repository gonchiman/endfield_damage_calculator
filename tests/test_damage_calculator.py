import pytest

from src.constants.attack_attributes import AttackAttributes
from src.constants.attack_types import AttackTypes
from src.entities.attack_hit import AttackHit
from src.services.damage_calculator import DamageCalculator


class Attack:
    def __init__(self, attack_sequence):
        self.attack_sequence = attack_sequence


class DummyOperator:
    def __init__(self):
        self.static_final_atk = 1000
        self.basic_attack = Attack(
            [
                AttackHit(multiplier=24, attribute=AttackAttributes.PHYSICAL),
                AttackHit(multiplier=29, attribute=AttackAttributes.PHYSICAL),
            ]
        )
        self.final_strike = Attack(
            [
                AttackHit(multiplier=400, attribute=AttackAttributes.PHYSICAL),
            ]
        )
        self.dive_attack = Attack(
            [
                AttackHit(multiplier=80, attribute=AttackAttributes.PHYSICAL),
            ]
        )


def test_get_basic_attack_hit_damage():
    damage = DamageCalculator.get_hit_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.BASIC_ATTACK,
        attack_step=1,
    )

    assert damage == 120


def test_get_basic_attack_second_step_hit_damage():
    damage = DamageCalculator.get_hit_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.BASIC_ATTACK,
        attack_step=2,
    )

    assert damage == 145


def test_get_final_strike_hit_damage():
    damage = DamageCalculator.get_hit_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.FINAL_STRIKE,
    )

    assert damage == 2000


def test_get_dive_attack_hit_damage():
    damage = DamageCalculator.get_hit_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.DIVE_ATTACK,
    )

    assert damage == 400


def test_get_hit_damage_uses_resistance_coef():
    damage = DamageCalculator.get_hit_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.BASIC_ATTACK,
        attack_step=1,
        resistance_coef=0.8,
    )

    assert damage == 96


def test_get_hit_damage_rejects_unsupported_attack_type():
    with pytest.raises(ValueError):
        DamageCalculator.get_hit_damage(
            operator=DummyOperator(),
            attack_type=AttackTypes.BATTLE_SKILL,
        )


def test_get_total_damage():
    total_damage = DamageCalculator.get_total_damage(
        operator=DummyOperator(),
        attack_type=AttackTypes.BASIC_ATTACK,
    )

    expected_total_damage = 1000 * (24 / 100) * 0.5 + 1000 * (29 / 100) * 0.5

    assert total_damage == expected_total_damage