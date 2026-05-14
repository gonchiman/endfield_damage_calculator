from src.constants.attack_types import AttackTypes


class DamageCalculator:
    @classmethod
    def get_hit_damage(
        cls,
        operator,
        attack_type: AttackTypes,
        attack_step: int = 1,
        defense_coef: float = 0.5,
        resistance_coef: float = 1.0,
    ) -> int:
        attack_hit = cls._get_attack_hit(
            operator=operator,
            attack_type=attack_type,
            attack_step=attack_step,
        )

        raw_damage = (
            operator.base_atk
            * (attack_hit.multiplier / 100)
            * defense_coef
            * resistance_coef
        )

        return round(raw_damage)

    @staticmethod
    def _get_attack_hit(operator, attack_type: AttackTypes, attack_step: int):
        if attack_type == AttackTypes.BASIC_ATTACK:
            attack_sequence = operator.basic_attack.attack_sequence
        elif attack_type == AttackTypes.FINAL_STRIKE:
            attack_sequence = operator.final_strike.attack_sequence
        elif attack_type == AttackTypes.DIVE_ATTACK:
            attack_sequence = operator.dive_attack.attack_sequence
        else:
            raise ValueError(f"Unsupported attack_type: {attack_type}")

        return attack_sequence[attack_step - 1]
