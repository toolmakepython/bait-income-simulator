from math import ceil
from flask import Flask, render_template, request

app = Flask(__name__)

WEEKS_PER_MONTH = 4.3


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_yen(value):
    return f"{round(value):,}"


def calculate_income(hourly_wage, hours_per_day, days_per_week, target_monthly_income):
    daily_income_raw = hourly_wage * hours_per_day
    weekly_income_raw = daily_income_raw * days_per_week
    monthly_income_raw = weekly_income_raw * WEEKS_PER_MONTH
    annual_income_raw = monthly_income_raw * 12

    required_days_for_target = ceil(target_monthly_income / daily_income_raw) if daily_income_raw > 0 else 0
    required_hours_for_target = round(target_monthly_income / hourly_wage, 1) if hourly_wage > 0 else 0

    walls = [
        {"name": "106万円", "amount": 1060000},
        {"name": "123万円", "amount": 1230000},
        {"name": "130万円", "amount": 1300000},
    ]

    wall_status = []
    for wall in walls:
        diff = wall["amount"] - annual_income_raw
        if diff > 0:
            wall_status.append({
                "name": wall["name"],
                "status": f"あと {format_yen(diff)}円 で到達"
            })
        else:
            wall_status.append({
                "name": wall["name"],
                "status": f"{format_yen(abs(diff))}円 超過"
            })

    if annual_income_raw < 1060000:
        wall_message = "106万円未満: 社会保険の加入目安より下です。"
    elif annual_income_raw < 1230000:
        wall_message = "106万円以上123万円未満: 社会保険条件や扶養条件を確認した方がいい水準です。"
    elif annual_income_raw < 1300000:
        wall_message = "123万円以上130万円未満: 税制上の扶養や勤労学生控除の目安に近い水準です。"
    else:
        wall_message = "130万円以上: 社会保険や扶養の扱いが変わる可能性が高いです。"

    return {
        "daily_income": round(daily_income_raw),
        "weekly_income": round(weekly_income_raw),
        "monthly_income": round(monthly_income_raw),
        "annual_income": round(annual_income_raw),
        "required_days_for_target": required_days_for_target,
        "required_hours_for_target": required_hours_for_target,
        "wall_message": wall_message,
        "wall_status": wall_status,
    }


@app.route("/", methods=["GET", "POST"])
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
            result = calculate_income(
                hourly_wage=hourly_wage,
                hours_per_day=hours_per_day,
                days_per_week=days_per_week,
                target_monthly_income=target_monthly_income,
            )

    return render_template(
        "index.html",
        result=result,
        form_data=form_data,
        errors=errors,
        weeks_per_month=WEEKS_PER_MONTH
    )


if __name__ == "__main__":
    app.run(debug=True)