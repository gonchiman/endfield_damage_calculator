from src.entities.operator_condition import OperatorCondition
from src.repositories.operator_status_repository import OperatorStatusRepository


def test_find_value():
    cond = OperatorCondition(operator_id="lifeng", level=1)
    attr = "base_atk"

    base_atk = OperatorStatusRepository.find_value(cond, attr)

    assert base_atk == 30