from flask import Blueprint, render_template, request

from utils.calculators import (
    WEEKS_PER_MONTH,
    calculate_income,
    calculate_target,
    calculate_wall_status,
    to_float,
    to_int,
)

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    errors = []

    form_data = {
        "hourly_wage": "1200",
        "hours_per_day": "5",
        "days_per_week": "3",
        "target_monthly_income": "50000",
    }

    if request.method == "POST":
        form_data["hourly_wage"] = request.form.get("hourly_wage", "").strip()
        form_data["hours_per_day"] = request.form.get("hours_per_day", "").strip()
        form_data["days_per_week"] = request.form.get("days_per_week", "").strip()
        form_data["target_monthly_income"] = request.form.get("target_monthly_income", "").strip()

        hourly_wage = to_int(form_data["hourly_wage"], -1)
        hours_per_day = to_float(form_data["hours_per_day"], -1)
        days_per_week = to_int(form_data["days_per_week"], -1)
        target_monthly_income = to_int(form_data["target_monthly_income"], -1)

        if hourly_wage <= 0:
            errors.append("時給は1円以上で入力してください。")

        if hours_per_day <= 0:
            errors.append("1日の勤務時間は0.5時間以上で入力してください。")
        elif (hours_per_day * 2) % 1 != 0:
            errors.append("1日の勤務時間は0.5時間刻みで入力してください。")

        if days_per_week <= 0:
            errors.append("週の勤務日数は1日以上で入力してください。")

        if target_monthly_income <= 0:
            errors.append("目標月収は1円以上で入力してください。")

        if not errors:
            income_result = calculate_income(
                hourly_wage=hourly_wage,
                hours_per_day=hours_per_day,
                days_per_week=days_per_week,
            )

            required_days_for_target, required_hours_for_target = calculate_target(
                monthly_target=target_monthly_income,
                daily_income=income_result["daily_income"],
            )

            wall_status = calculate_wall_status(income_result["annual_income"])

            if income_result["annual_income"] < 1060000:
                wall_message = "106万円未満: 社会保険の加入目安より下です。"
            elif income_result["annual_income"] < 1230000:
                wall_message = "106万円以上123万円未満: 社会保険条件や扶養条件を確認した方がいい水準です。"
            elif income_result["annual_income"] < 1300000:
                wall_message = "123万円以上130万円未満: 税制上の扶養や勤労学生控除の目安に近い水準です。"
            else:
                wall_message = "130万円以上: 社会保険や扶養の扱いが変わる可能性が高いです。"

            result = {
                "daily_income": income_result["daily_income"],
                "weekly_income": income_result["weekly_income"],
                "monthly_income": income_result["monthly_income"],
                "annual_income": income_result["annual_income"],
                "required_days_for_target": required_days_for_target,
                "required_hours_for_target": required_hours_for_target,
                "wall_message": wall_message,
                "wall_status": wall_status,
            }

    return render_template(
        "index.html",
        result=result,
        form_data=form_data,
        errors=errors,
        weeks_per_month=WEEKS_PER_MONTH,
    )