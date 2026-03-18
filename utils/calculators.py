import math


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


def calculate_income(hourly_wage, hours_per_day, days_per_week):
    daily_income = hourly_wage * hours_per_day
    weekly_income = daily_income * days_per_week
    monthly_income = weekly_income * WEEKS_PER_MONTH
    annual_income = monthly_income * 12

    return {
        "daily_income": int(daily_income),
        "weekly_income": int(weekly_income),
        "monthly_income": int(monthly_income),
        "annual_income": int(annual_income),
    }


def calculate_target(monthly_target, daily_income, hourly_wage):
    if daily_income <= 0 or hourly_wage <= 0:
        return 0, 0

    required_days = math.ceil(monthly_target / daily_income)
    required_hours = round(monthly_target / hourly_wage, 1)

    return required_days, required_hours


def calculate_wall_status(annual_income):
    walls = [
        ("106万円", 1060000),
        ("123万円", 1230000),
        ("130万円", 1300000),
    ]

    results = []

    for name, value in walls:
        if annual_income < value:
            diff = value - annual_income
            results.append({
                "name": name,
                "status": f"あと {diff:,}円 で到達"
            })
        else:
            diff = annual_income - value
            results.append({
                "name": name,
                "status": f"{diff:,}円 超過"
            })

    return results


def calculate_wall_info(hourly_wage, hours_per_day, days_per_week):
    income_result = calculate_income(
        hourly_wage=hourly_wage,
        hours_per_day=hours_per_day,
        days_per_week=days_per_week,
    )

    daily_income = income_result["daily_income"]
    annual_income = income_result["annual_income"]

    walls = [
        ("106万円", 1060000),
        ("123万円", 1230000),
        ("130万円", 1300000),
    ]

    wall_results = []

    for name, value in walls:
        if annual_income < value:
            remaining_yen = value - annual_income
            remaining_hours = round(remaining_yen / hourly_wage, 1) if hourly_wage > 0 else 0
            remaining_days = math.ceil(remaining_yen / daily_income) if daily_income > 0 else 0

            wall_results.append({
                "name": name,
                "status": "未到達",
                "remaining_yen": remaining_yen,
                "remaining_hours": remaining_hours,
                "remaining_days": remaining_days,
            })
        else:
            over_yen = annual_income - value
            over_hours = round(over_yen / hourly_wage, 1) if hourly_wage > 0 else 0
            over_days = math.ceil(over_yen / daily_income) if daily_income > 0 else 0

            wall_results.append({
                "name": name,
                "status": "超過",
                "remaining_yen": over_yen,
                "remaining_hours": over_hours,
                "remaining_days": over_days,
            })

    return {
        "daily_income": income_result["daily_income"],
        "weekly_income": income_result["weekly_income"],
        "monthly_income": income_result["monthly_income"],
        "annual_income": income_result["annual_income"],
        "wall_results": wall_results,
    }