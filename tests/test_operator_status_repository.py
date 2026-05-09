from src.entities.operator_condition import OperatorCondition
from src.repositories.operator_status_repository import OperatorStatusRepository


def test_find_value():
    cond = OperatorCondition(operator_id="lifeng", level=1)
    attr = "base_atk"

    base_atk = OperatorStatusRepository.find_value(cond, attr)

    assert base_atk == 30


def test_find_levels_by_operator_id():
    operator_id = "lifeng"

    levels = OperatorStatusRepository.find_levels_by_operator_id(operator_id)

    assert levels == [1, 20, 40, 60, 80, 90]