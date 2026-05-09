import sqlite3

from src.entities.operator_condition import OperatorCondition
from src.constants.paths import DB_PATH
from src.constants.database_table_names import TableNames
from src.repositories.repository import Repository


class OperatorStatusRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_STATUSES
        

    @classmethod
    def find_value(
        cls,
        cond: OperatorCondition,
        attr: str,
    ) -> int | None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                f"""
                SELECT {attr}
                FROM {cls.TABLE_NAME}
                WHERE operator_id = ?
                AND level = ?
                """,
                (
                    cond.operator_id, 
                    cond.level
                ),
            ).fetchone()

            if row is None:
                return None
            
            return row[attr]
        
    
    @classmethod
    def find_levels_by_operator_id(
        cls,
        operator_id: str,
    ) -> list[int]:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                f"""
                SELECT DISTINCT level
                FROM {cls.TABLE_NAME}
                WHERE operator_id = ?
                ORDER BY level ASC
                """,
                (operator_id,)
            ).fetchall()

        return [row["level"] for row in rows]