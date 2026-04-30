import csv
import sqlite3
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.constants.paths import DB_PATH, INSERT_OPERATOR_MASTER_SQL_PATH, INSERT_OPERATOR_STATUSES_SQL_PATH, OPERATOR_MASTER_CSV_PATH, OPERATOR_STATUSES_CSV_PATH, SCHEMA_PATH # noqa: E402
from src.constants.database_columns import ( # noqa: E402
    OperatorStatusesColumns, 
    OperatorMasterColumns,
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
    with open(OPERATOR_MASTER_CSV_PATH, encoding="utf-8", newline="") as f_csv, \
        open(INSERT_OPERATOR_MASTER_SQL_PATH, encoding="utf-8") as f_sql:
        reader = csv.DictReader(f_csv)
        insert_sql = f_sql.read()

        for row in reader:
            conn.execute(
                insert_sql, 
                (
                    row[OperatorMasterColumns.OPERATOR_ID],
                    row[OperatorMasterColumns.OPERATOR_NAME],
                 ),
            )


def insert_operator_statuses(conn):
    with open(OPERATOR_STATUSES_CSV_PATH, encoding="utf-8", newline="") as f_csv, \
        open(INSERT_OPERATOR_STATUSES_SQL_PATH, encoding="utf-8") as f_sql:
        reader = csv.DictReader(f_csv)
        insert_sql = f_sql.read()

        for row in reader:
            conn.execute(
                insert_sql,
                (
                    row[OperatorStatusesColumns.OPERATOR_ID],
                    int(row[OperatorStatusesColumns.LEVEL]),
                    int(row[OperatorStatusesColumns.STRENGTH]),
                    int(row[OperatorStatusesColumns.AGILITY]),
                    int(row[OperatorStatusesColumns.INTELLECT]),
                    int(row[OperatorStatusesColumns.WILL]),
                    int(row[OperatorStatusesColumns.BASE_ATK]),
                ),
            )


if __name__ == "__main__":
    init_db()