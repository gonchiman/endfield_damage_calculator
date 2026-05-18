import sqlite3

from src.constants.attack_attributes import AttackAttributes
from src.constants.attack_types import AttackTypes
from src.constants.database_columns import OperatorAttackHitsColumns
from src.constants.database_table_names import TableNames
from src.constants.operator_ids import OperatorIds
from src.constants.paths import DB_PATH
from src.entities.attack_hit import AttackHit
from src.repositories.repository import Repository


class OperatorAttackHitsRepository(Repository):
    TABLE_NAME = TableNames.OPERATOR_ATTACK_HITS

    @classmethod
    def find_attack_hits(
        cls,
        operator_id: OperatorIds,
        attack_type: AttackTypes,
        rank: int,
    ) -> list[AttackHit]:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                f"""
                SELECT
                    {OperatorAttackHitsColumns.MULTIPLIER},
                    {OperatorAttackHitsColumns.DAMAGE_TYPE}
                FROM {cls.TABLE_NAME}
                WHERE {OperatorAttackHitsColumns.OPERATOR_ID} = ?
                AND {OperatorAttackHitsColumns.ATTACK_TYPE} = ?
                AND {OperatorAttackHitsColumns.RANK} = ?
                ORDER BY {OperatorAttackHitsColumns.ATTACK_STEP}
                """,
                (
                    operator_id.value,
                    attack_type.value,
                    rank,
                ),
            ).fetchall()

        return [cls._to_attack_hit(row) for row in rows]

    @classmethod
    def find_attack_hit(
        cls,
        operator_id: OperatorIds,
        attack_type: AttackTypes,
        rank: int,
        attack_step: int,
    ) -> AttackHit | None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                f"""
                SELECT
                    {OperatorAttackHitsColumns.MULTIPLIER},
                    {OperatorAttackHitsColumns.DAMAGE_TYPE}
                FROM {cls.TABLE_NAME}
                WHERE {OperatorAttackHitsColumns.OPERATOR_ID} = ?
                AND {OperatorAttackHitsColumns.ATTACK_TYPE} = ?
                AND {OperatorAttackHitsColumns.RANK} = ?
                AND {OperatorAttackHitsColumns.ATTACK_STEP} = ?
                """,
                (
                    operator_id.value,
                    attack_type.value,
                    rank,
                    attack_step,
                ),
            ).fetchone()

        if row is None:
            return None

        return cls._to_attack_hit(row)
    
    @classmethod
    def get_step_count(
        cls,
        operator_id: OperatorIds,
        attack_type: AttackTypes,
        rank: int,
    ) -> int:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            count = conn.execute(
                f"""
                SELECT COUNT(*)
                FROM {cls.TABLE_NAME}
                WHERE {OperatorAttackHitsColumns.OPERATOR_ID} = ?
                AND {OperatorAttackHitsColumns.ATTACK_TYPE} = ?
                AND {OperatorAttackHitsColumns.RANK} = ?
                """,
                (
                    operator_id.value,
                    attack_type.value,
                    rank,
                ),
            ).fetchone()[0]

        return count

    @classmethod
    def _to_attack_hit(cls, row: sqlite3.Row) -> AttackHit:
        return AttackHit(
            multiplier=row[OperatorAttackHitsColumns.MULTIPLIER],
            attribute=cls._to_attack_attribute(
                row[OperatorAttackHitsColumns.DAMAGE_TYPE]
            ),
        )

    @staticmethod
    def _to_attack_attribute(damage_type: str) -> AttackAttributes:
        return AttackAttributes[damage_type.upper()]
