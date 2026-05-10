from src.constants.operator_ids import OperatorIds
from src.entities.basic_attack import BasicAttack
from src.entities.operator_condition import OperatorCondition
from src.services.static_final_atk_calculator import StaticFinalAtkCalculater


class Lifeng:
    ID = OperatorIds.LIFENG

    def __init__(self, operator_level: int, basic_attack_level: int):
        self.level = operator_level
        self.base_atk = StaticFinalAtkCalculater.get_final_atk(
            OperatorCondition(self.ID, self.level)
        )
        self.basic_attack = BasicAttack(self.ID, basic_attack_level)
