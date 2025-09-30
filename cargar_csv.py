from csv import DictReader
from recaudo import compute_stats

def cargar_csv(path):
    r = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in DictReader(f):
            r.append(
                {
                    "transport_type": row["transport_type"],
                    "vehicle_id": row["vehicle_id"],
                    "route_id": row["route_id"],
                    "passenger_age": int(row["passenger_age"]),
                    "passenger_gender": row["passenger_gender"],
                    "base_fare": float(row["base_fare"]),
                }
            )
    return r

if __name__ == "__main__":
    data = cargar_csv("tickets.csv")
    stats = compute_stats(data)

    print("\n Resultados del Proyecto de Recaudo\n")
    print(f"1. Total recaudado: ${stats['total_revenue']:,}")

    print("\n2. Buseta(s) intermunicipal(es) con más recaudo:")
    if stats['top_intermunicipal_busetas']['vehicle_ids']:
        print(f"   ID(s): {', '.join(stats['top_intermunicipal_busetas']['vehicle_ids'])}")
        print(f"   Valor: ${stats['top_intermunicipal_busetas']['revenue']:,}")
    else:
        print("   No hay datos de busetas intermunicipales")

    print("\n3. Ruta(s) con menor recaudo:")
    if stats['lowest_routes']['route_ids']:
        print(f"   ID(s): {', '.join(stats['lowest_routes']['route_ids'])}")
        print(f"   Valor: ${stats['lowest_routes']['revenue']:,}")
    else:
        print("   No hay datos de rutas")

    print("\n4. Tipo de transporte que deja más dinero:")
    if stats['better_transport']:
        print(f"   {stats['better_transport']} con ${stats['revenue_by_transport'][stats['better_transport']]:,}")
    else:
        print("   Ambos transportes recaudan lo mismo")

    print("\n5. Descuentos:")
    print(f"   Total descuentos otorgados: ${stats['total_discounts']:,}")
    print(f"   Descuentos a pasajeras menores: ${stats['total_discounts_female_minors']:,}\n")
