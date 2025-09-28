from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Tuple, List, Literal, Optional
from collections import defaultdict

Transport = Literal["interveredal", "intermunicipal"]

@dataclass(frozen=True)
class Ticket:
    transport_type: Transport
    vehicle_id: str
    route_id: str
    passenger_age: int
    passenger_gender: Literal["F", "M"]
    base_fare: float

DISCOUNT_RATE = 0.20

def is_minor(age: int) -> bool:
    return age < 18

def net_amount(base_fare: float, age: int) -> Tuple[float, float]:
    d = base_fare * DISCOUNT_RATE if is_minor(age) else 0.0
    return base_fare - d, d

def compute_stats(tickets: Iterable[Ticket]) -> Dict[str, object]:
    total_revenue = 0.0
    total_discount = 0.0
    total_discount_female_minors = 0.0

    revenue_by_vehicle_intermunicipal: Dict[str, float] = defaultdict(float)
    revenue_by_route: Dict[str, float] = defaultdict(float)
    revenue_by_transport: Dict[Transport, float] = defaultdict(float)

    for t in tickets:
        paid, disc = net_amount(t.base_fare, t.passenger_age)
        total_revenue += paid
        total_discount += disc
        if t.passenger_gender == "F" and is_minor(t.passenger_age):
            total_discount_female_minors += disc
        if t.transport_type == "intermunicipal":
            revenue_by_vehicle_intermunicipal[t.vehicle_id] += paid
        revenue_by_route[t.route_id] += paid
        revenue_by_transport[t.transport_type] += paid

    top_buseta_value = None
    top_buseta_ids: List[str] = []
    if revenue_by_vehicle_intermunicipal:
        top_buseta_value = max(revenue_by_vehicle_intermunicipal.values())
        top_buseta_ids = [vid for vid, val in revenue_by_vehicle_intermunicipal.items() if val == top_buseta_value]

    lowest_route_value = None
    lowest_route_ids: List[str] = []
    if revenue_by_route:
        lowest_route_value = min(revenue_by_route.values())
        lowest_route_ids = [rid for rid, val in revenue_by_route.items() if val == lowest_route_value]

    better_transport: Optional[Transport] = None
    if revenue_by_transport:
        a = revenue_by_transport.get("interveredal", 0.0)
        b = revenue_by_transport.get("intermunicipal", 0.0)
        if a > b:
            better_transport = "interveredal"
        elif a < b:
            better_transport = "intermunicipal"
        else:
            better_transport = None

    return {
        "total_revenue": round(total_revenue, 2),
        "top_intermunicipal_busetas": {
            "vehicle_ids": sorted(top_buseta_ids),
            "revenue": round(top_buseta_value, 2) if top_buseta_value is not None else None,
        },
        "lowest_routes": {
            "route_ids": sorted(lowest_route_ids),
            "revenue": round(lowest_route_value, 2) if lowest_route_value is not None else None,
        },
        "better_transport": better_transport,
        "revenue_by_transport": {k: round(v, 2) for k, v in revenue_by_transport.items()},
        "total_discounts": round(total_discount, 2),
        "total_discounts_female_minors": round(total_discount_female_minors, 2),
    }