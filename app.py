from flask import Flask, render_template, request

from src.repositories.operator_status_repository import OperatorStatusRepository
from src.constants.operator_ids import OperatorIds
from src.entities.operator_condition import OperatorCondition
from src.services.damage_calculator import DamageCalculater


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html", 
        page_title="Endfield Damage Calculator"
    )


@app.route("/damage_calculator_1", methods=["GET", "POST"])
def damage_calculator_1():
    selected_operator_id = request.form.get("operator_id", list(OperatorIds)[0].value)
    selected_level = int(request.form.get("level", 1))

    cond = OperatorCondition(
        operator_id=selected_operator_id,
        level=selected_level
    )

    damage = DamageCalculater.get_damage(cond)

    return render_template(
        "damage_calculator_1.html",
        page_title="Damage Calculator 1",
        selected_operator_id=selected_operator_id,
        selected_level=selected_level,
        operator_ids=OperatorIds,
        levels=OperatorStatusRepository.find_levels_by_operator_id(selected_operator_id),
        damage=damage
    )


if __name__ == "__main__":
    app.run(debug=True)