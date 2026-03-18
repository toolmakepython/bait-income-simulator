from flask import Blueprint, render_template, request

from utils.calculators import calculate_hourly_month_income, to_float, to_int

hourly_month_bp = Blueprint("hourly_month", __name__)


@hourly_month_bp.route("/hourly-month", methods=["GET", "POST"])
def hourly_month():
    result = None
    errors = []

    form_data = {
        "hourly_wage": "1200",
        "hours_per_day": "5",
        "days_per_month": "12",
    }

    if request.method == "POST":
        form_data["hourly_wage"] = request.form.get("hourly_wage", "").strip()
        form_data["hours_per_day"] = request.form.get("hours_per_day", "").strip()
        form_data["days_per_month"] = request.form.get("days_per_month", "").strip()

        hourly_wage = to_int(form_data["hourly_wage"], -1)
        hours_per_day = to_float(form_data["hours_per_day"], -1)
        days_per_month = to_int(form_data["days_per_month"], -1)

        if hourly_wage <= 0:
            errors.append("時給は1円以上で入力してください。")

        if hours_per_day <= 0:
            errors.append("1日の勤務時間は0.5時間以上で入力してください。")
        elif (hours_per_day * 2) % 1 != 0:
            errors.append("1日の勤務時間は0.5時間刻みで入力してください。")

        if days_per_month <= 0:
            errors.append("月の勤務日数は1日以上で入力してください。")

        if not errors:
            result = calculate_hourly_month_income(
                hourly_wage=hourly_wage,
                hours_per_day=hours_per_day,
                days_per_month=days_per_month,
            )

    return render_template(
        "hourly_month.html",
        result=result,
        form_data=form_data,
        errors=errors,
    )