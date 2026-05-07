from src.entities.operator_condition import OperatorCondition
from src.repositories.operator_master_repository import OperatorMasterRepository
from src.constants.database_columns import OperatorMasterColumns


def test_find_by_operator_id_and_column():
    cond = OperatorCondition(operator_id="lifeng", level=1)
    attr = OperatorMasterColumns.MAIN_STAT

    main_stat = OperatorMasterRepository.find_value(
        cond,
        attr,
    )
    expected = "agility"

    assert main_stat == expected