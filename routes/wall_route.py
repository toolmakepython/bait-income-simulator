from flask import Blueprint, render_template, request

from utils.calculators import (
    WEEKS_PER_MONTH,
    calculate_wall_info,
    to_float,
    to_int,
)

wall_bp = Blueprint("wall", __name__)


@wall_bp.route("/wall", methods=["GET", "POST"])
def wall():
    result = None
    errors = []

    form_data = {
        "hourly_wage": "1200",
        "hours_per_day": "5",
        "days_per_week": "3",
    }

    if request.method == "POST":
        form_data["hourly_wage"] = request.form.get("hourly_wage", "").strip()
        form_data["hours_per_day"] = request.form.get("hours_per_day", "").strip()
        form_data["days_per_week"] = request.form.get("days_per_week", "").strip()

        hourly_wage = to_int(form_data["hourly_wage"], -1)
        hours_per_day = to_float(form_data["hours_per_day"], -1)
        days_per_week = to_int(form_data["days_per_week"], -1)

        if hourly_wage <= 0:
            errors.append("時給は1円以上で入力してください。")

        if hours_per_day <= 0:
            errors.append("1日の勤務時間は0.5時間以上で入力してください。")
        elif (hours_per_day * 2) % 1 != 0:
            errors.append("1日の勤務時間は0.5時間刻みで入力してください。")

        if days_per_week <= 0:
            errors.append("週の勤務日数は1日以上で入力してください。")

        if not errors:
            result = calculate_wall_info(
                hourly_wage=hourly_wage,
                hours_per_day=hours_per_day,
                days_per_week=days_per_week,
            )

    return render_template(
        "wall.html",
        result=result,
        form_data=form_data,
        errors=errors,
        weeks_per_month=WEEKS_PER_MONTH,
    )