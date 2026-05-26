from src.constants import ZoneType
from src.graph.graph import Graph
from src.simulation.drone import Drone
from typing import List

class Simulation:
    def __init__(
        self,
        graph: Graph,
        drones: List[Drone],
        path: List[str],
    ) -> None:
        self.graph = graph
        self.drones = drones
        self.path = path

        self.turn = 0
        self.path_indexes: dict[int, int] = {
        drone.drone_id: 0 for drone in self.drones
        }
    def run(self) -> None:
        print("\n=== SIMULATION START ===")

        while not self._all_delivered():
            self.turn += 1

            self._execute_turn()

        print("\n=== SIMULATION END ===")

    def _all_delivered(self) -> bool:
        return all(
            drone.delivered
            for drone in self.drones
        )

    def _execute_turn(self) -> None:
        movements: list[str] = []

        occupancy = self._current_occupancy()

        # Reservations for THIS turn
        reservations: dict[str, int] = {}

        for drone in self.drones:
            if drone.delivered:
                continue

            movement = self._move_drone(
                drone,
                occupancy,
                reservations,
            )

            if movement is not None:
                movements.append(movement)

        if movements:
            print(
                f"Turn {self.turn}: "
                + " ".join(movements)
            )

    def _move_drone(
        self,
        drone: Drone,
        occupancy: dict[str, int],
        reservations: dict[str, int],
    ) -> str | None:
        if drone.in_transit:
            return self._handle_transit(drone)

        path_index = self.path_indexes[drone.drone_id]

        if path_index >= len(self.path) - 1:
            drone.delivered = True
            return None

        current_zone = self.path[path_index]
        next_zone = self.path[path_index + 1]

        next_node = self.graph.nodes[next_zone]
        
        future_occupancy = (
            occupancy.get(next_zone, 0)
            + reservations.get(next_zone, 0)
        )

        capacity = self._zone_capacity(next_zone)

        # Current drone leaves current zone this turn
        if drone.current_zone == next_zone:
            future_occupancy -= 1

        if future_occupancy >= capacity:
            return None
        # Restricted movement
        if next_node.zone_type == ZoneType.RESTRICTED:
            reservations[next_zone] = (
                reservations.get(next_zone, 0) + 1)
            drone.in_transit = True

            drone.transit_remaining = 1

            drone.transit_destination = next_zone

            drone.transit_connection = (
                current_zone,
                next_zone,
            )

            return (
                f"D{drone.drone_id}-"
                f"{current_zone}-{next_zone}"
            )
        
        reservations[next_zone] = (reservations.get(next_zone, 0) + 1)
        # Normal movement
        drone.current_zone = next_zone

        self.path_indexes[drone.drone_id] += 1

        if next_zone == self.graph.end:
            drone.delivered = True

        return f"D{drone.drone_id}-{next_zone}"

    def _handle_transit(
            self,
            drone: Drone,
            ) -> str | None:
        drone.transit_remaining -= 1

        if drone.transit_remaining > 0:
            return None

        destination = drone.transit_destination

        if destination is None:
            raise ValueError(
                "Transit destination missing"
            )

        drone.current_zone = destination

        self.path_indexes[drone.drone_id] += 1

        drone.in_transit = False
        drone.transit_destination = None
        drone.transit_connection = None

        if destination == self.graph.end:
            drone.delivered = True

        return (
            f"D{drone.drone_id}-{destination}"
        )

    def _zone_capacity(self, zone_name: str) -> int:
        if zone_name == self.graph.start:
            return 999999

        if zone_name == self.graph.end:
            return 999999

        return self.graph.nodes[zone_name].max_drones
    
    def _current_occupancy(self) -> dict[str, int]:
        occupancy: dict[str, int] = {}

        for drone in self.drones:
            if drone.delivered:
                continue

            if drone.in_transit:
                continue

            occupancy.setdefault(
                drone.current_zone,
                0,
            )

            occupancy[drone.current_zone] += 1

        return occupancy