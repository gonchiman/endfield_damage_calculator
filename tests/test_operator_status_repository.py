from src.repositories.operator_status_repository import OperatorStatusRepository


def test_find_base_atk_by_operator_id_and_level():
    operator_id = "lifeng"
    level = 1

    base_atk = OperatorStatusRepository.find_base_atk_by_operator_id_and_level(operator_id, level)

    assert base_atk == 30