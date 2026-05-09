from src.entities.operator_condition import OperatorCondition
from src.services.static_final_atk_calculator import StaticFinalAtkCalculater


def test_get_final_atk():
    operator_id = "lifeng"
    operator_level = 1

    operator_condition = OperatorCondition(
        operator_id,
        operator_level
    )

    static_final_atk = StaticFinalAtkCalculater.get_final_atk(operator_condition)
    expected = 30 * (1 + (20*0.005) + (14*0.002))

    assert static_final_atk == expected