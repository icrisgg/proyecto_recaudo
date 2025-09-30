from csv import DictReader
from recaudo import compute_stats

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(DictReader(f))

def build_tickets(transports, routes, trips, passengers):
    trips_by_id = {t["trip_id"]: t for t in trips}
    fare_by_route = {r["route_id"]: float(r["base_fare"]) for r in routes}
    cat_by_vehicle = {t["vehicle_id"]: t["category"] for t in transports}
    tickets = []
    for p in passengers:
        tr = trips_by_id[p["trip_id"]]
        vehicle_id = tr["vehicle_id"]
        route_id = tr["route_id"]
        category = cat_by_vehicle[vehicle_id]
        transport_type = "intermunicipal" if category == "buseta_intermunicipal" else "interveredal"
        tickets.append({
            "transport_type": transport_type,
            "vehicle_id": vehicle_id,
            "route_id": route_id,
            "passenger_age": int(p["passenger_age"]),
            "passenger_gender": p["passenger_gender"],
            "base_fare": fare_by_route[route_id],
        })
    return tickets

if __name__ == "__main__":
    transports = read_csv("transports.csv")
    routes = read_csv("routes.csv")
    trips = read_csv("trips.csv")
    passengers = read_csv("passengers.csv")
    tickets = build_tickets(transports, routes, trips, passengers)
    stats = compute_stats(tickets)

    print("\n Resultados del Proyecto de Recaudo\n")
    print(f"1. Total recaudado: ${stats['total_revenue']:,}")

    print("\n2. Buseta(s) intermunicipal(es) con más recaudo:")
    if stats["top_intermunicipal_busetas"]["vehicle_ids"]:
        print(f"   ID(s): {', '.join(stats['top_intermunicipal_busetas']['vehicle_ids'])}")
        print(f"   Valor: ${stats['top_intermunicipal_busetas']['revenue']:,}")
    else:
        print("   No hay datos de busetas intermunicipales")

    print("\n3. Ruta(s) con menor recaudo:")
    if stats["lowest_routes"]["route_ids"]:
        print(f"   ID(s): {', '.join(stats['lowest_routes']['route_ids'])}")
        print(f"   Valor: ${stats['lowest_routes']['revenue']:,}")
    else:
        print("   No hay datos de rutas")

    print("\n4. Tipo de transporte que deja más dinero:")
    if stats["better_transport"]:
        print(f"   {stats['better_transport']} con ${stats['revenue_by_transport'][stats['better_transport']]:,}")
    else:
        print("   Ambos transportes recaudan lo mismo")

    print("\n5. Descuentos:")
    print(f"   Total descuentos otorgados: ${stats['total_discounts']:,}")
    print(f"   Descuentos a pasajeras menores: ${stats['total_discounts_female_minors']:,}\n")