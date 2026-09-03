def calculate_job_quote(
        acres: float,
        fuel_price: float,
        hourly_rate: float,
        implement_data: dict,
        tractor_data: dict
) -> dict:

    # Extract specs #

    width = implement_data.get("width", 5)
    speed_mph = implement_data.get("working_speed_mph", 2.5)
    implement_pto_speed = implement_data.get("pto_speed")
    impl_wear = implement_data.get("wear_cost", 5)
    min_hp = implement_data.get("min_hp", 0)
    max_hp = implement_data.get("max_hp", 999)

    gph = tractor_data.get("fuel_burn_hour", 3)
    tractor_wear = tractor_data.get("wear_cost", 5)
    tractor_hp = tractor_data.get("HP", None)

    # Math Engine #

    field_capacity = (width * speed_mph * 0.80) / 8.25
    job_hours = acres / field_capacity

    fuel_used = job_hours * gph
    fuel_cost = fuel_used * fuel_price

    total_wear_rate = impl_wear + tractor_wear
    wear_cost = job_hours + total_wear_rate

    labor_cost = hourly_rate * job_hours
    total_quote = fuel_cost + wear_cost + labor_cost

    return {
        "field_capacity": field_capacity,
        "job_hours": job_hours,
        "fuel_used": fuel_used,
        "fuel_cost": fuel_cost,
        "total_wear_rate": total_wear_rate,
        "wear_cost": wear_cost,
        "labor_cost": labor_cost,
        "total_quote": total_quote,
        "cost_per_acre": total_quote / acres,
        "hp_warning_low": tractor_hp < min_hp,
        "hp_warning_high": tractor_hp > max_hp,
        "implement_pto_speed": implement_pto_speed,
        "tractor_hp": tractor_hp,
        "min_hp": min_hp,
        "max_hp": max_hp,
}
