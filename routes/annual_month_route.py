from flask import Blueprint, render_template, request

from utils.calculators import to_int

annual_month_bp = Blueprint("annual_month", __name__)


@annual_month_bp.route("/annual-month", methods=["GET", "POST"])
def annual_month():

    result = None
    errors = []

    form_data = {
        "annual_income": "3000000",
    }

    if request.method == "POST":
        form_data["annual_income"] = request.form.get("annual_income", "").strip()

        annual_income = to_int(form_data["annual_income"], -1)

        if annual_income <= 0:
            errors.append("年収は1円以上で入力してください。")

        if not errors:

            monthly_income = annual_income / 12

            result = {
                "monthly_income": int(monthly_income)
            }

    return render_template(
        "annual_month.html",
        result=result,
        form_data=form_data,
        errors=errors,
    )