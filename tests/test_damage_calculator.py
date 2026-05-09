from src.entities.operator_condition import OperatorCondition
from src.services.damage_calculator import DamageCalculater


def test_get_damage():
    operator_id = "lifeng"
    operator_level = 1

    operator_condition = OperatorCondition(
        operator_id,
        operator_level
    )

    damage = DamageCalculater.get_damage(operator_condition)
    expected = 30 * (1 + (20*0.005) + (14*0.002))

    assert damage == expected