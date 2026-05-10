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
