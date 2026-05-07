from src.repositories.operator_master_repository import OperatorMasterRepository
from src.constants.database_columns import OperatorMasterColumns


def test_find_by_operator_id_and_column():
    operator_id = "lifeng"
    column = OperatorMasterColumns.MAIN_STAT

    main_stat = OperatorMasterRepository.find_by_operator_id_and_column(
        operator_id,
        column,
    )
    expected = "agility"

    assert main_stat == expected