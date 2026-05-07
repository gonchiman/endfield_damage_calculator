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