import asyncio
import platform
import pygame
import random

# Game constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 6
CELL_SIZE = 80
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = (HEIGHT - GRID_SIZE * CELL_SIZE) // 2
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Object types
CORE = "C"
NODE = "N"
CONNECTION = "L"

class AetherCircuit:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Aether Circuit")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.connections = []
        self.selected_node = None
        self.energy = 0
        self.max_energy = 100
        self.level = 1
        self.game_over = False
        self.setup_level()

    def setup_level(self):
        # Clear grid and connections
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.connections = []
        self.energy = 0
        self.max_energy = 100 + self.level * 10

        # Place core at center
        core_x, core_y = GRID_SIZE // 2, GRID_SIZE // 2
        self.grid[core_y][core_x] = CORE

        # Place nodes randomly
        num_nodes = self.level + 3
        for _ in range(num_nodes):
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if self.grid[y][x] is None:
                    self.grid[y][x] = NODE
                    break

    def is_valid_connection(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if (x1, y1) == (x2, y2):
            return False
        if abs(x1 - x2) + abs(y1 - y2) != 1:  # Must be adjacent
            return False
        if (x1, y1, x2, y2) in self.connections or (x2, y2, x1, y1) in self.connections:
            return False
        return True

    def add_connection(self, pos1, pos2):
        if self.is_valid_connection(pos1, pos2):
            self.connections.append((pos1[0], pos1[1], pos2[0], pos2[1]))
            self.energy += 20
            if self.energy > self.max_energy:
                self.game_over = True
            elif self.check_win_condition():
                self.level += 1
                self.setup_level()

    def check_win_condition(self):
        # Win if all nodes are connected to the core (simplified path check)
        connected_nodes = set()
        for x1, y1, x2, y2 in self.connections:
            connected_nodes.add((x1, y1))
            connected_nodes.add((x2, y2))
        
        core_pos = (GRID_SIZE // 2, GRID_SIZE // 2)
        if core_pos not in connected_nodes:
            return False
        
        node_count = sum(row.count(NODE) for row in self.grid)
        return len(connected_nodes) // 2 >= node_count

    def draw(self):
        self.screen.fill(BLACK)

        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    GRID_OFFSET_X + x * CELL_SIZE,
                    GRID_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE - 5,
                    CELL_SIZE - 5
                )
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                if self.grid[y][x] == CORE:
                    pygame.draw.circle(self.screen, GOLD, rect.center, CELL_SIZE // 3)
                elif self.grid[y][x] == NODE:
                    color = BLUE if (x, y) == self.selected_node else GREEN
                    pygame.draw.circle(self.screen, color, rect.center, CELL_SIZE // 4)

        # Draw connections
        for x1, y1, x2, y2 in self.connections:
            start_pos = (GRID_OFFSET_X + x1 * CELL_SIZE + CELL_SIZE // 2,
                         GRID_OFFSET_Y + y1 * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (GRID_OFFSET_X + x2 * CELL_SIZE + CELL_SIZE // 2,
                       GRID_OFFSET_Y + y2 * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(self.screen, BLUE, start_pos, end_pos, 3)

        # Draw energy and level
        energy_text = self.font.render(f"Energy: {self.energy}/{self.max_energy}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(energy_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

        if self.game_over:
            game_over_text = self.font.render("Overload! Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()

    def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                pos = pygame.mouse.get_pos()
                grid_x = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
                grid_y = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if self.grid[grid_y][grid_x] in [NODE, CORE]:
                        if self.selected_node is None:
                            self.selected_node = (grid_x, grid_y)
                        else:
                            self.add_connection(self.selected_node, (grid_x, grid_y))
                            self.selected_node = None
            elif event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.__init__()

        self.draw()

async def main():
    game = AetherCircuit()
    while not game.game_over:
        game.update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
