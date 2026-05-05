import sqlite3

from src.constants.paths import DB_PATH


class Repository:
    TABLE_NAME: str = ""

    @classmethod
    def find_all(cls) -> list[dict]:
        if not cls.TABLE_NAME:
            raise ValueError("table_name is not defined")
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                f"SELECT * FROM {cls.TABLE_NAME}"
            ).fetchall()

            return [dict(row) for row in rows]
        
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