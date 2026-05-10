from src.constants.attack_types import AttackTypes
from src.constants.operator_ids import OperatorIds
from src.repositories.operator_attack_hits_repository import (
    OperatorAttackHitsRepository,
)


class BasicAttack:
    def __init__(self, operator_id: OperatorIds, basic_attack_level: int):
        self.attack_sequence = OperatorAttackHitsRepository.find_attack_hits(
            operator_id,
            AttackTypes.BASIC_ATTACK,
            basic_attack_level,
        )
