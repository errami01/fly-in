from src.constants import ZoneType
from src.graph.graph import Graph
from src.simulation.drone import Drone
from typing import List
from src.simulation.planned_move import PlannedMove


class Simulation:
    def __init__(
        self,
        graph: Graph,
        drones: List[Drone],
        drone_paths: List[str],
    ) -> None:
        self.graph = graph
        self.drones = drones
        self.drone_paths = drone_paths
        self.stalled_turns = 0

        self.turn = 0
        self.path_indexes: dict[int, int] = {
            drone.drone_id: 0 for drone in self.drones
            }
        self.active_edge_occupancy: dict[
            tuple[str, str], int] = {}

    def _occupy_edge(self, edge_key: tuple[str, str],) -> None:
        self.active_edge_occupancy[edge_key] = (
            self.active_edge_occupancy.get(edge_key, 0) + 1
            )

    def _release_edge(self, edge_key: tuple[str, str]) -> None:
        if edge_key not in self.active_edge_occupancy:
            return

        self.active_edge_occupancy[edge_key] -= 1

        if (self.active_edge_occupancy[edge_key] <= 0):
            del self.active_edge_occupancy[edge_key]

    def run(self) -> None:
        print("\n=== SIMULATION START ===")

        while not self._all_delivered():
            self.turn += 1
            progress = self._execute_turn()
            if progress:
                self.stalled_turns = 0
            else:
                self.stalled_turns += 1

            if self.stalled_turns > 5:
                raise RuntimeError(
                    "Deadlock detected: "
                    "no progress for 5 turns"
                )

        print("\n=== SIMULATION END ===")

    def _all_delivered(self) -> bool:
        return all(
            drone.delivered
            for drone in self.drones
        )

    def _execute_turn(self) -> bool:
        movements: list[str] = []
        progress_made = False
        occupancy = self._current_occupancy()

        # PHASE 1
        planned_moves = self._plan_moves()

        # PHASE 2
        departures = self._compute_departures(
            planned_moves
        )

        # PHASE 3
        valid_moves = self._validate_moves(
            planned_moves,
            occupancy,
            departures,
        )

        # PHASE 4
        for move in valid_moves:
            movement = self._execute_move(move)

            if movement:
                movements.append(movement)
                progress_made = True

        if movements:
            print(
                f"Turn {self.turn}: "
                + " ".join(movements)
            )
        return progress_made

    def _plan_moves(self) -> list[PlannedMove]:
        planned_moves: list[PlannedMove] = []

        for drone in self.drones:
            if drone.delivered:
                continue

            move = self._plan_drone_move(drone)

            if move is not None:
                planned_moves.append(move)

        return planned_moves

    def _plan_drone_move(
        self,
        drone: Drone,
    ) -> PlannedMove | None:

        # Transit completion
        if drone.in_transit:
            destination = drone.transit_destination

            if destination is None:
                return None

            return PlannedMove(
                drone_id=drone.drone_id,
                from_zone=drone.current_zone,
                to_zone=destination,
                completes_transit=True,
            )

        path = self.drone_paths[drone.drone_id]
        path_index = self.path_indexes[drone.drone_id]

        if path_index >= len(path) - 1:
            return None

        current_zone = path[path_index]
        next_zone = path[path_index + 1]

        next_node = self.graph.nodes[next_zone]

        return PlannedMove(
            drone_id=drone.drone_id,
            from_zone=current_zone,
            to_zone=next_zone,
            is_restricted=(
                next_node.zone_type
                == ZoneType.RESTRICTED
            ),
        )

    def _compute_departures(
            self,
            planned_moves: list[PlannedMove]
            ) -> dict[str, int]:
        departures: dict[str, int] = {}

        for move in planned_moves:
            departures.setdefault(
                move.from_zone,
                0,
            )

            departures[move.from_zone] += 1

        return departures

    def _validate_moves(
            self,
            planned_moves: list[PlannedMove],
            occupancy: dict[str, int],
            departures: dict[str, int]
            ) -> list[PlannedMove]:
        valid_moves: list[PlannedMove] = []

        reservations: dict[str, int] = {}
        edge_reservations: dict[
            tuple[str, str], int] = {}

        for move in planned_moves:
            if move.completes_transit:
                valid_moves.append(move)
                continue
            # Check edge capacity
            edge = self.graph.get_edge(
                move.from_zone,
                move.to_zone,
            )
            edge_key = move.edge_key()
            persistent_usage = (
                self.active_edge_occupancy.get(edge_key, 0))
            current_edge_usage = (
                persistent_usage + edge_reservations.get(
                    edge_key, 0))

            if (
                current_edge_usage
                >= edge.max_link_capacity
            ):
                continue

            # Check destination capacity
            capacity = self._zone_capacity(move.to_zone)

            effective_occupancy = (
                occupancy.get(move.to_zone, 0)
                - departures.get(move.to_zone, 0)
                + reservations.get(move.to_zone, 0)
            )

            if effective_occupancy >= capacity:
                continue

            # Reserve edge
            edge_reservations.setdefault(edge_key, 0)
            edge_reservations[edge_key] += 1

            # Reserve destination
            reservations.setdefault(move.to_zone, 0)
            reservations[move.to_zone] += 1

            # Accept move
            valid_moves.append(move)

        return valid_moves

    def _execute_move(
            self,
            move: PlannedMove
            ) -> str | None:
        drone = self._get_drone(move.drone_id)

        if move.completes_transit:
            return self._complete_transit(
                drone,
                move,
            )

        if move.is_restricted:
            return self._start_restricted_transit(
                drone,
                move,
            )

        return self._execute_normal_move(
            drone,
            move,
        )

    def _get_drone(
            self,
            drone_id: int,
            ) -> Drone:
        for drone in self.drones:
            if drone.drone_id == drone_id:
                return drone

        raise ValueError(
            f"Drone not found: {drone_id}"
        )

    def _execute_normal_move(
            self,
            drone: Drone,
            move: PlannedMove
            ) -> str:
        drone.current_zone = move.to_zone

        self.path_indexes[drone.drone_id] += 1

        if move.to_zone == self.graph.end:
            drone.delivered = True

        return (
            f"D{drone.drone_id}-"
            f"{move.to_zone}"
        )

    def _start_restricted_transit(
            self,
            drone: Drone,
            move: PlannedMove
            ) -> str:
        drone.in_transit = True

        drone.transit_remaining = 1

        drone.transit_destination = move.to_zone

        drone.transit_connection = (
            move.from_zone,
            move.to_zone,
        )
        self._occupy_edge(move.edge_key())
        return (
            f"D{drone.drone_id}-"
            f"{move.from_zone}-"
            f"{move.to_zone}"
        )

    def _complete_transit(
            self,
            drone: Drone,
            move: PlannedMove
            ) -> str:
        drone.current_zone = move.to_zone

        drone.in_transit = False

        drone.transit_destination = None
        connection = drone.transit_connection
        if connection is not None:
            x, y = sorted(connection)
            self._release_edge((x, y))
        drone.transit_connection = None

        self.path_indexes[drone.drone_id] += 1

        if move.to_zone == self.graph.end:
            drone.delivered = True

        return (
            f"D{drone.drone_id}-"
            f"{move.to_zone}"
        )

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
