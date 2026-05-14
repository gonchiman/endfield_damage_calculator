import csv
import sqlite3
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.constants.paths import (  # noqa: E402
    DB_PATH,
    OPERATOR_ATTACK_HITS_CSV_PATH,
    OPERATOR_ATTACK_HITS_SQL_PATH,
    OPERATOR_MASTER_CSV_PATH,
    OPERATOR_MASTER_SQL_PATH,
    OPERATOR_STATUSES_CSV_PATH,
    OPERATOR_STATUSES_SQL_PATH,
)


TABLE_DEFINITIONS = (
    OPERATOR_MASTER_SQL_PATH,
    OPERATOR_STATUSES_SQL_PATH,
    OPERATOR_ATTACK_HITS_SQL_PATH,
)

CSV_IMPORTS = (
    ("operator_master", OPERATOR_MASTER_CSV_PATH),
    ("operator_statuses", OPERATOR_STATUSES_CSV_PATH),
    ("operator_attack_hits", OPERATOR_ATTACK_HITS_CSV_PATH),
)


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    create_tables(conn)

    for table_name, csv_path in CSV_IMPORTS:
        insert_csv(conn, table_name, csv_path)

    conn.commit()
    conn.close()


def create_tables(conn):
    for sql_path in TABLE_DEFINITIONS:
        with open(sql_path, encoding="utf-8", newline="") as f_sql:
            conn.executescript(f_sql.read())


def insert_csv(conn, table_name, csv_path):
    with open(csv_path, encoding="utf-8", newline="") as f_csv:
        reader = csv.DictReader(f_csv)
        columns = reader.fieldnames

        columns_text = ", ".join(columns)
        placeholder_text = ", ".join(["?"] * len(columns))

        sql = f"""
            INSERT OR REPLACE INTO {table_name} (
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
