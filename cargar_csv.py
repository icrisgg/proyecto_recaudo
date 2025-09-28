from csv import DictReader
from recaudo import Ticket, compute_stats

def cargar_csv(path: str):
    r = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in DictReader(f):
            r.append(
                Ticket(
                    transport_type=row["transport_type"],
                    vehicle_id=row["vehicle_id"],
                    route_id=row["route_id"],
                    passenger_age=int(row["passenger_age"]),
                    passenger_gender=row["passenger_gender"],
                    base_fare=float(row["base_fare"]),
                )
            )
    return r

if __name__ == "__main__":
    data = cargar_csv("tickets.csv")
    stats = compute_stats(data)
    print(stats)