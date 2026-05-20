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
            operator.static_final_atk
            * (attack_hit.multiplier / 100)
            * defense_coef
            * resistance_coef
        )

        return round(raw_damage)
    

    @classmethod
    def get_total_damage(
        cls,
        operator,
        attack_type: AttackTypes,
        defense_coef: float = 0.5,
        resistance_coef: float = 1.0,
    ) -> int:
        total_damage = 0
        attack_sequence = cls._get_attack_sequence(operator, attack_type)
        
        for attack_step in range(1, len(attack_sequence) + 1):
            total_damage += cls.get_hit_damage(
                operator=operator,
                attack_type=attack_type,
                attack_step=attack_step,
                defense_coef=defense_coef,
                resistance_coef=resistance_coef,
            )

        return total_damage


    @staticmethod
    def _get_attack_sequence(operator, attack_type: AttackTypes):
        if attack_type == AttackTypes.BASIC_ATTACK:
            return operator.basic_attack.attack_sequence
        elif attack_type == AttackTypes.FINAL_STRIKE:
            return operator.final_strike.attack_sequence
        elif attack_type == AttackTypes.DIVE_ATTACK:
            return operator.dive_attack.attack_sequence
        else:
            raise ValueError(f"Unsupported attack_type: {attack_type}")

    @classmethod
    def _get_attack_hit(cls, operator, attack_type: AttackTypes, attack_step: int):
        attack_sequence = cls._get_attack_sequence(operator, attack_type)
        return attack_sequence[attack_step - 1]
