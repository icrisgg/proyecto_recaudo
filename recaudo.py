DISCOUNT_RATE = 0.20

def is_minor(age):
    return age < 18

def net_amount(base_fare, age):
    d = base_fare * DISCOUNT_RATE if is_minor(age) else 0.0
    return base_fare - d, d

def compute_stats(tickets):
    total_revenue = 0.0
    total_discount = 0.0
    total_discount_female_minors = 0.0

    revenue_by_vehicle_intermunicipal = {}
    revenue_by_route = {}
    revenue_by_transport = {}

    for t in tickets:
        paid, disc = net_amount(t["base_fare"], t["passenger_age"])
        total_revenue += paid
        total_discount += disc
        if t["passenger_gender"] == "F" and is_minor(t["passenger_age"]):
            total_discount_female_minors += disc
        if t["transport_type"] == "intermunicipal":
            revenue_by_vehicle_intermunicipal[t["vehicle_id"]] = revenue_by_vehicle_intermunicipal.get(t["vehicle_id"], 0.0) + paid
        revenue_by_route[t["route_id"]] = revenue_by_route.get(t["route_id"], 0.0) + paid
        revenue_by_transport[t["transport_type"]] = revenue_by_transport.get(t["transport_type"], 0.0) + paid

    top_buseta_value = None
    top_buseta_ids = []
    if revenue_by_vehicle_intermunicipal:
        top_buseta_value = max(revenue_by_vehicle_intermunicipal.values())
        top_buseta_ids = sorted([vid for vid, val in revenue_by_vehicle_intermunicipal.items() if val == top_buseta_value])

    lowest_route_value = None
    lowest_route_ids = []
    if revenue_by_route:
        lowest_route_value = min(revenue_by_route.values())
        lowest_route_ids = sorted([rid for rid, val in revenue_by_route.items() if val == lowest_route_value])

    better_transport = None
    if revenue_by_transport:
        a = revenue_by_transport.get("interveredal", 0.0)
        b = revenue_by_transport.get("intermunicipal", 0.0)
        if a > b:
            better_transport = "interveredal"
        elif b > a:
            better_transport = "intermunicipal"

    return {
        "total_revenue": round(total_revenue, 2),
        "top_intermunicipal_busetas": {
            "vehicle_ids": top_buseta_ids,
            "revenue": round(top_buseta_value, 2) if top_buseta_value is not None else None,
        },
        "lowest_routes": {
            "route_ids": lowest_route_ids,
            "revenue": round(lowest_route_value, 2) if lowest_route_value is not None else None,
        },
        "better_transport": better_transport,
        "revenue_by_transport": {k: round(v, 2) for k, v in revenue_by_transport.items()},
        "total_discounts": round(total_discount, 2),
        "total_discounts_female_minors": round(total_discount_female_minors, 2),
    }