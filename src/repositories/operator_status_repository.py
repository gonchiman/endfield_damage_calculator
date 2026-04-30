from src.constants.database_table_names import TableNames
from src.repositories.repository import Repository


class OperatorStatusRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_STATUSES