from src.constants.attack_types import AttackTypes
from src.constants.operator_ids import OperatorIds
from src.entities.operator_condition import OperatorCondition
from src.repositories.operator_attack_hits_repository import OperatorAttackHitsRepository
from src.services.static_final_atk_calculator import StaticFinalAtkCalculater


class Lifeng:
    ID = OperatorIds.LIFENG

    def __init__(self, operator_level: int, basic_attack_level: int):
        self.level = operator_level
        self.base_atk = StaticFinalAtkCalculater.get_final_atk(OperatorCondition(self.ID, self.level))
        self.basic_attack = BasicAttack(self.ID, basic_attack_level)


class BasicAttack:
    TOTAL_HITS = 4

    def __init__(self, id: OperatorIds, basic_attack_level: int):
        self.attack_sequence = [
            OperatorAttackHitsRepository.find_attack_hit(id, AttackTypes.BASIC_ATTACK, basic_attack_level, i)
            for i in range(1, self.TOTAL_HITS + 1)
        ]