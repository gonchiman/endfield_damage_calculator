import sqlite3

from src.constants.paths import DB_PATH
from src.constants.database_table_names import TableNames
from src.repositories.repository import Repository


class OperatorMasterRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_MASTER

    @classmethod
    def find_main_stat_by_operator_id(
        cls,
        operator_id: str,
    ) -> int | None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                f"""
                SELECT base_atk
                FROM {cls.TABLE_NAME}
                WHERE operator_id = ?
                """,
                (operator_id),
            ).fetchone()

            if row is None:
                return None
            
            return row["base_atk"]
        
    @classmethod
    def find_by_operator_id_and_column(
        cls,
        operator_id: str,
        column: str,
    ) -> int | None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                f"""
                SELECT {column}
                FROM {cls.TABLE_NAME}
                WHERE operator_id = ?
                """,
                (operator_id,),
            ).fetchone()

            if row is None:
                return None
            
            return row[column]