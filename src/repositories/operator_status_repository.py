import sqlite3

from src.constants.paths import DB_PATH
from src.constants.database_table_names import TableNames
from src.repositories.repository import Repository


class OperatorStatusRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_STATUSES

    @classmethod
    def find_base_atk_by_operator_id_and_level(
        cls,
        operator_id: str,
        level: int,
    ) -> int | None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                f"""
                SELECT base_atk
                FROM {cls.TABLE_NAME}
                WHERE operator_id = ?
                AND level = ?
                """,
                (operator_id, level),
            ).fetchone()

            if row is None:
                return None
            
            return row["base_atk"]