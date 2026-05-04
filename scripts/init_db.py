import csv
import sqlite3
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.constants.paths import ( # noqa: E402
    DB_PATH, 
    OPERATOR_MASTER_CSV_PATH, 
    OPERATOR_STATUSES_CSV_PATH, 
    SCHEMA_PATH
)


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, encoding="utf-8", newline="") as f:
        conn.executescript(f.read())

    insert_operators(conn)
    insert_operator_statuses(conn)

    conn.commit()
    conn.close()


def insert_operators(conn):
    with open(OPERATOR_MASTER_CSV_PATH, encoding="utf-8", newline="") as f_csv:
        reader = csv.DictReader(f_csv)
        columns = reader.fieldnames

        columns_text = ", ".join(columns)
        placeholder_text = ", ".join(["?"] * len(columns))

        sql = f"""
            INSERT OR REPLACE INTO operator_master (
                {columns_text}
            ) VALUES (
                {placeholder_text}
            )
        """

        for row in reader:
            values = [row[column] for column in columns]
            conn.execute(sql, values)


def insert_operator_statuses(conn):
    with open(OPERATOR_STATUSES_CSV_PATH, encoding="utf-8", newline="") as f_csv:
        reader = csv.DictReader(f_csv)
        columns = reader.fieldnames

        columns_text = ", ".join(columns)
        placeholder_text = ", ".join(["?"] * len(columns))

        sql = f"""
            INSERT OR REPLACE INTO operator_statuses (
                {columns_text}
            ) VALUES (
                {placeholder_text}
            )
        """

        for row in reader:
            values = [row[column] for column in columns]
            conn.execute(sql, values)


if __name__ == "__main__":
    init_db()