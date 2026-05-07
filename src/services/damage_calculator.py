from src.entities.operator_condition import OperatorCondition
from src.services.static_final_atk_calculator import StaticFinalAtkCalculater


class DamageCalculater:
    @staticmethod
    def get_damage(
        cond: OperatorCondition,
    ) -> float:
        return StaticFinalAtkCalculater.get_final_atk(cond)