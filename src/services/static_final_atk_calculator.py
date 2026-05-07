from src.constants.database_columns import OperatorMasterColumns, OperatorStatusColumns
from src.entities.operator_condition import OperatorCondition
from src.repositories.operator_master_repository import OperatorMasterRepository
from src.repositories.operator_status_repository import OperatorStatusRepository


class StaticFinalAtkCalculater:
    @staticmethod
    def get_final_atk(
        cond: OperatorCondition,
    ) -> float:
        base_atk = StaticFinalAtkCalculater._get_base_atk(cond)
        atk_bonus = StaticFinalAtkCalculater._get_atk_bonus(cond)

        return base_atk * atk_bonus

    @staticmethod
    def _get_base_atk(
        cond: OperatorCondition
    ) -> int:
        return OperatorStatusRepository.find_value(
            cond,
            OperatorStatusColumns.BASE_ATK
        )

    @staticmethod
    def _get_atk_bonus(
        cond: OperatorCondition
    ) -> int:
        main_attr = OperatorMasterRepository.find_value(cond, OperatorMasterColumns.MAIN_STAT)
        sub_attr = OperatorMasterRepository.find_value(cond, OperatorMasterColumns.SUB_STAT)

        main_stat = OperatorStatusRepository.find_value(cond, main_attr)
        sub_stat = OperatorStatusRepository.find_value(cond, sub_attr)

        return 1 + main_stat * 0.5 + sub_stat * 0.2