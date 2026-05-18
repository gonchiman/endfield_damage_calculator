from src.constants.attack_attributes import AttackAttributes
from src.constants.attack_types import AttackTypes
from src.constants.operator_ids import OperatorIds
from src.entities.attack_hit import AttackHit
from src.repositories.operator_attack_hits_repository import (
    OperatorAttackHitsRepository,
)


def test_find_attack_hit():
    attack_hit = OperatorAttackHitsRepository.find_attack_hit(
        OperatorIds.LIFENG,
        AttackTypes.BASIC_ATTACK,
        1,
        3,
    )

    assert attack_hit == AttackHit(
        multiplier=35,
        attribute=AttackAttributes.PHYSICAL,
    )


def test_find_attack_hits():
    attack_hits = OperatorAttackHitsRepository.find_attack_hits(
        OperatorIds.LIFENG,
        AttackTypes.BASIC_ATTACK,
        1,
    )

    assert attack_hits == [
        AttackHit(multiplier=24, attribute=AttackAttributes.PHYSICAL),
        AttackHit(multiplier=29, attribute=AttackAttributes.PHYSICAL),
        AttackHit(multiplier=35, attribute=AttackAttributes.PHYSICAL),
        AttackHit(multiplier=68, attribute=AttackAttributes.PHYSICAL),
    ]


def test_find_lifeng_final_strike_hits():
    attack_hits = OperatorAttackHitsRepository.find_attack_hits(
        OperatorIds.LIFENG,
        AttackTypes.FINAL_STRIKE,
        1,
    )

    assert attack_hits == [
        AttackHit(multiplier=400, attribute=AttackAttributes.PHYSICAL),
    ]


def test_find_lifeng_dive_attack_hits():
    attack_hits = OperatorAttackHitsRepository.find_attack_hits(
        OperatorIds.LIFENG,
        AttackTypes.DIVE_ATTACK,
        1,
    )

    assert attack_hits == [
        AttackHit(multiplier=80, attribute=AttackAttributes.PHYSICAL),
    ]

def test_get_step_count():
    step_count_basic_attack = OperatorAttackHitsRepository.get_step_count(
        OperatorIds.LIFENG,
        AttackTypes.BASIC_ATTACK,
        1,
    )
    step_count_final_strike = OperatorAttackHitsRepository.get_step_count(
        OperatorIds.LIFENG,
        AttackTypes.FINAL_STRIKE,
        1,
    )
    step_count_dive_attack = OperatorAttackHitsRepository.get_step_count(
        OperatorIds.LIFENG,
        AttackTypes.DIVE_ATTACK,
        1,
    )

    assert step_count_basic_attack == 4
    assert step_count_final_strike == 1
    assert step_count_dive_attack == 1
