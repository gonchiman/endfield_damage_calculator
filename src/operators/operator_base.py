from src.constants.operator_ids import OperatorIds
from src.entities.operator_condition import OperatorCondition
from src.services.static_final_atk_calculator import StaticFinalAtkCalculater


class OperatorBase:
    ID: OperatorIds

    def __init__(self, level: int):
        self.level = level
        self.base_atk = StaticFinalAtkCalculater.get_final_atk(OperatorCondition(self.ID, self.level))