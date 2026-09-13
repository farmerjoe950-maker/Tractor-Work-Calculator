def calculate_job_quote(
        acres: float,
        fuel_price: float,
        hourly_rate: float,
        speed : float,
        width : float,
        implement_data: dict,
        tractor_data: dict,
        overlap_ft: float = 1.0,
        field_efficiency: float = 0.80,
        loading_fee: float = 50,
        round_trip_miles: float = 0,
        mileage_rate: float = 1.50,
        min_job_charge: float = 150,
        target_margin: float = .35
) -> dict:
    if implement_data is None:
        implement_data = {}
    if tractor_data is None:
        tractor_data = {}


    # Extract specs #

    working_width = width if width is not None else implement_data.get("width", 5)
    working_speed = speed if speed is not None else implement_data.get("speed", 3)
    implement_pto_speed = implement_data.get("pto_speed")
    implement_wear = implement_data.get("wear_cost", 5)
    min_hp = implement_data.get("min_hp", 0)
    max_hp = implement_data.get("max_hp", 999)

    gph = tractor_data.get("fuel_burn_hour", 3)
    tractor_wear = tractor_data.get("wear_cost", 5)
    tractor_hp = tractor_data.get("hp", tractor_data.get("HP", 0))

    # Math Engine #


    effective_width = max(1.0, float(working_width) - float(overlap_ft))
    field_capacity = (effective_width * float(working_speed) * float(field_efficiency)) / 8.25
    job_hours = acres / field_capacity if field_efficiency > 0 else 0.0

    fuel_used = job_hours * gph
    fuel_cost = fuel_used * fuel_price

    total_wear_rate = implement_wear + tractor_wear
    wear_cost = job_hours * total_wear_rate

    labor_cost = hourly_rate * job_hours
    hauling_cost = loading_fee + (round_trip_miles * mileage_rate)

    total_operating_cost = fuel_cost + wear_cost + labor_cost + hauling_cost

    machine_rate_hr = float(tractor_hp) * 1.0 if tractor_hp else 0.0

    hourly_billing_quote = (machine_rate_hr + hourly_rate) * job_hours
    raw_quote = hourly_billing_quote +hauling_cost

    margin_based_quote = total_operating_cost / (1.0 - target_margin) if target_margin < 1.0 else total_operating_cost

    total_quote = max(raw_quote, margin_based_quote, min_job_charge)
    net_profit = total_quote - total_operating_cost

    hp_warning_low = tractor_hp < min_hp if tractor_hp is not None else False
    hp_warning_high = tractor_hp > max_hp if tractor_hp is not None else False

    print(f"DEBUG MATH: -> fuel: {fuel_cost}, wear: {wear_cost}, labor {labor_cost}, SUM: {total_quote}")

    return {
        "field_capacity": round(field_efficiency, 2),
        "job_hours": round(job_hours, 2),
        "fuel_used": round(fuel_used , 2),
        "fuel_cost": round(fuel_cost, 2),
        "total_wear_rate": round(total_wear_rate, 20),
        "wear_cost": round(wear_cost, 2),
        "labor_cost": round(labor_cost, 2),
        "hauling_cost": round(hauling_cost, 2),
        "total_operating_cost": round(total_operating_cost, 2),
        "total_quote": round(total_quote, 2),
        "net_profit": round(net_profit, 2),
        "cost_per_acre": round(total_quote / acres, 2) if acres > 0 else 0.0,
        "hp_warning_low": hp_warning_low,
        "hp_warning_high": hp_warning_high,
        "implement_pto_speed": implement_pto_speed,
        "tractor_hp": tractor_hp,
        "min_hp": min_hp,
        "max_hp": max_hp,
}
