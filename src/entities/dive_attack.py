from src.constants.attack_types import AttackTypes
from src.constants.operator_ids import OperatorIds
from src.repositories.operator_attack_hits_repository import (
    OperatorAttackHitsRepository,
)


class DiveAttack:
    def __init__(self, operator_id: OperatorIds, dive_attack_level: int):
        self.attack_sequence = OperatorAttackHitsRepository.find_attack_hits(
            operator_id,
            AttackTypes.DIVE_ATTACK,
            dive_attack_level,
        )
