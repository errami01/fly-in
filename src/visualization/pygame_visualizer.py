import os
import pygame
from typing import Tuple



os.environ["SDL_AUDIODRIVER"] = "dummy"

# COLOR_MAP = {
#     "red": (255,0,0),
#     "green": (0,255,0),
#     "blue": (0,0,255),
#     "yellow": (255,255,0),
#     "orange": (255,128,0),
#     "cyan": (0,255,255),
#     "purple": (128,0,128),
# }


class PygameVisualizer:

    def __init__(self, graph, replay_data) -> None:
        self.graph = graph
        self.replay_data = replay_data
        self.current_turn_index = 0
        self.playing = False
        self.turn_duration = 1000  # ms
        self.last_turn_time = pygame.time.get_ticks()
        self.drone_positions: dict[int, str] = {}
        self.window_width = 1200
        self.window_height = 800
        self.hud_height = 60
        xs = [node.x for node in graph.nodes.values()]
        self.padding = 100
        self.max_x = max(xs)
        self.scale = ((self.window_width - 200) / max(1, self.max_x))
        for drone_id in range(1, replay_data.drone_count + 1):
            self.drone_positions[drone_id] = replay_data.start_zone
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption("Fly-In Replay")
        self.clock = pygame.time.Clock()

    def world_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        return (self.padding + x * self.scale, 400 - y * 80)

    def apply_turn(self) -> bool:
        if (self.current_turn_index >= len(self.replay_data.turns)):
            return False
        turn = self.replay_data.turns[self.current_turn_index]
        for move in turn.moves:
            self.drone_positions[move.drone_id] = move.destination
        self.current_turn_index += 1
        return True

    def draw_hud_bar(self) -> None:
        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            (
                0,
                0,
                self.window_width,
                self.hud_height,
            ),
        )
        font = pygame.font.Font(None, 24)
        status = ("PLAYING" if self.playing else "PAUSED")
        hud_text = (
            f"Turn: {self.current_turn_index}"
            f"   |   {status}"
            f"   |   SPACE: Next Turn"
            f"   |   P: Play/Pause"
            f"   |   R: Reset"
        )
        label = font.render(hud_text, True, (255, 255, 255))
        self.screen.blit(label, (20, 25))

    def draw_edges(self) -> None:
        # For edge visualization
        # edge_usage = self.current_edge_usage()
        for edge in self.graph.edges.values():
            node_a = self.graph.nodes[edge.start]
            node_b = self.graph.nodes[edge.end]
            pygame.draw.line(
                self.screen,
                (150, 150, 150),
                self.world_to_screen(node_a.x, node_a.y),
                self.world_to_screen(node_b.x, node_b.y),
                3,
            )
        # Visualize edge occupancy-capacity
            # start_pos = self.world_to_screen(node_a.x, node_a.y)
            # end_pos = self.world_to_screen(node_b.x, node_b.y)
            # edge_key = edge.key()
            # occupancy = edge_usage.get(edge_key,0)
            # capacity = (edge.max_link_capacity)
            # mid_x = (start_pos[0] + end_pos[0]) / 2
            # mid_y = (start_pos[1] + end_pos[1]) / 2
            # font = pygame.font.Font(None,24)

            # label = font.render(
            #     f"{occupancy}/{capacity}",
            #     True,
            #     (255,255,255),
            # )
            # self.screen.blit(label,(mid_x,mid_y))

    def current_edge_usage(self) -> dict[tuple[str, str], int]:
        if (self.current_turn_index == 0):
            return {}
        turn = self.replay_data.turns[self.current_turn_index - 1]
        return turn.edge_usage

    def get_zone_capacity(self, zone_name: str) -> str:
        if zone_name == self.graph.start:
            return "inf"
        if zone_name == self.graph.end:
            return "inf"
        return str(self.graph.nodes[zone_name].max_drones)

    def draw_nodes(self) -> None:
        # font = pygame.font.Font(None, 24)
        # occupancy = self.calculate_occupancy()

        for node in self.graph.nodes.values():

            # color = COLOR_MAP.get(node.color,(200,200,200))
            position = self.world_to_screen(node.x, node.y)

            try:
                pygame.draw.circle(
                    self.screen,
                    node.color,
                    position,
                    20,
                )
            except Exception:
                pygame.draw.circle(
                    self.screen,
                    (200, 200, 200),
                    position,
                    20,
                )

        # Display node names
            # label = font.render(
            #     node.name,
            #     True,
            #     (255,255,255),
            # )
            # self.screen.blit(
            #     label,
            #     (
            #         position[0] + 25,
            #         position[1] - 10,
            #     ),
            # )
        # Display node occupancy-capacity
            # count = occupancy[node.name]
            # capacity = self.get_zone_capacity(node.name)
            # occupancy_text = font.render(
            #     f"{count}/{capacity}",
            #     True,
            #     (255,255,255),
            # )
            # self.screen.blit(
            #     occupancy_text,
            #     (
            #         position[0] - 15,
            #         position[1] + 25,
            #     ),
            # )

    def calculate_occupancy(self) -> dict[str, int]:
        occupancy: dict[str, int] = {}

        for zone_name in self.graph.nodes:
            occupancy[zone_name] = 0

        for zone_name in self.drone_positions.values():
            occupancy[zone_name] += 1

        return occupancy

    def render_static_map(self) -> None:
        self.screen.fill((30, 30, 30))
        self.draw_edges()
        self.draw_nodes()
        self.draw_drones()
        self.draw_hud_bar()
        pygame.display.flip()

    def draw_drones(self) -> None:
        font = pygame.font.Font(None, 20)
        for drone_id, zone_name in (self.drone_positions.items()):
            node = self.graph.nodes[zone_name]
            x, y = self.world_to_screen(node.x, node.y)
            # x += drone_id * 8
            # y -= 25
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 8)
            label = font.render(f"D{drone_id}", True, (255, 255, 255))

            self.screen.blit(label, (x + 10, y - 10))

    def update_playback(self) -> None:
        if not self.playing:
            return
        now = pygame.time.get_ticks()
        if (now - self.last_turn_time >= self.turn_duration):
            advanced = self.apply_turn()
            self.last_turn_time = now
            if not advanced:
                self.playing = False

    def draw_hud(self) -> None:
        font = pygame.font.Font(None, 36)
        label = font.render(
            f"Turn: {self.current_turn_index}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(label, (20, 20))
        status = (
            "PLAYING"
            if self.playing
            else "PAUSED"
        )
        status_label = font.render(status, True, (255, 255, 0))
        self.screen.blit(status_label, (20, 60))

    def reset(self) -> None:
        self.current_turn_index = 0
        self.playing = False
        self.drone_positions.clear()
        for drone_id in range(1, self.replay_data.drone_count + 1):
            self.drone_positions[drone_id] = self.replay_data.start_zone

    # def draw_controls(self):
    #     font = pygame.font.Font(
    #         None,
    #         28,
    #     )

    #     controls = [
    #         "SPACE : Next Turn",
    #         "P     : Play/Pause",
    #         "R     : Reset",
    #     ]

    #     start_x = 20
    #     start_y = 100

    #     for index, text in enumerate(controls):
    #         label = font.render(
    #             text,
    #             True,
    #             (220, 220, 220),
    #         )

    #         self.screen.blit(
    #             label,
    #             (
    #                 start_x,
    #                 start_y + index * 30,
    #             ),
    #         )
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        self.apply_turn()
                    elif event.key == pygame.K_p:
                        self.playing = not self.playing
                    elif event.key == pygame.K_r:
                        self.reset()
            self.update_playback()
            self.render_static_map()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
    # def run(self):
    #     print("Starting visualizer...")
    #     running = True

    #     # while running:
    #     #     print("Rendering frame...")
    #     #     for event in pygame.event.get():

    #     #         if (
    #     #             event.type
    #     #             == pygame.QUIT
    #     #         ):
    #     #             running = False

    #     self.render_static_map()
    #     pygame.image.save(
    #             self.screen,
    #             "graph.png",
    #         )

    #     print("Saved graph.png")
    #     pygame.display.flip()
    #     self.clock.tick(60)

    #     pygame.quit()
