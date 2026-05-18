from flask import Flask, render_template, request

from src.constants.skill_levels import SKILL_RANKS
from src.repositories.operator_attack_hits_repository import OperatorAttackHitsRepository
from src.repositories.operator_status_repository import OperatorStatusRepository
from src.constants.attack_types import AttackTypes
from src.constants.operator_ids import OperatorIds
from src.operators.lifeng import Lifeng
from src.services.damage_calculator import DamageCalculator


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html", 
        page_title="Endfield Damage Calculator"
    )


@app.route("/damage_calculator_1", methods=["GET", "POST"])
def damage_calculator_1():
    selected_operator_id = request.form.get("operator_id", OperatorIds.LIFENG.value)
    selected_level = int(request.form.get("operator_level", 1))
    selected_basic_attack_level = int(request.form.get("basic_attack_level", 1))
    
    selected_attack_type = request.form.get(
        "attack_type",
        AttackTypes.BASIC_ATTACK.value,
    )
    selected_attack_type_enum = AttackTypes(selected_attack_type)

    max_attack_step = OperatorAttackHitsRepository.get_step_count(
        OperatorIds(selected_operator_id),
        selected_attack_type_enum,
        selected_basic_attack_level,
    ) or 1
    selected_attack_step = min(
        int(request.form.get("attack_step", 1)),
        max_attack_step,
    )

    lifeng = Lifeng(
        operator_level=selected_level,
        basic_attack_level=selected_basic_attack_level,
    )

    damage = DamageCalculator.get_hit_damage(
        operator=lifeng,
        attack_type=selected_attack_type_enum,
        attack_step=selected_attack_step,
    )

    return render_template(
        "damage_calculator_1.html",
        page_title="Damage Calculator 1",
        selected_operator_id=selected_operator_id,
        selected_level=selected_level,
        selected_basic_attack_level=selected_basic_attack_level,
        selected_attack_type=selected_attack_type,
        selected_attack_step=selected_attack_step,
        operator_ids=[OperatorIds.LIFENG],
        attack_types=[
            AttackTypes.BASIC_ATTACK,
            AttackTypes.FINAL_STRIKE,
            AttackTypes.DIVE_ATTACK,
        ],
        attack_steps=range(1, max_attack_step + 1),
        basic_attack_levels=SKILL_RANKS,
        operator_levels=OperatorStatusRepository.find_levels_by_operator_id(selected_operator_id),
        damage=damage
    )


if __name__ == "__main__":
    app.run(debug=True)
