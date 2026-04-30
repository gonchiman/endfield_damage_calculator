from src.constants.database_table_names import TableNames
from src.repositories.repository import Repository


class OperatorMasterRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_MASTER