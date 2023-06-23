import random
import pygame

GRID_WIDTH = 800
GRID_HEIGHT = 600
GRID_SIZE = 100

resource_probabilities = {
    "Water": 0.5,
    "Plains": 0.5,
    "Stone": 0.2,
    "Farmland": 0.2,
    "Ore": 0.12,
    "Wood": 0.06,
    "Animals": 0.02,
}


class CoordinatePlane:
    def __init__(self):
        self.cells = []
        self.user_owned_cells = set()

        # Create the cells in the coordinate plane
        for x in range(GRID_WIDTH // GRID_SIZE):
            row = []
            for y in range(GRID_HEIGHT // GRID_SIZE):
                position = (
                    x * GRID_SIZE + (1000 - GRID_WIDTH) // 2,
                    y * GRID_SIZE + (1000 - GRID_HEIGHT) // 2,
                )
                resource = random.choices(
                    list(resource_probabilities.keys()),
                    list(resource_probabilities.values()),
                )[0]
                cell = Cell(position, resource)
                row.append(cell)
            self.cells.append(row)

    def draw(self, screen):
        # Draw the cells in the coordinate plane
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def update(self, time_delta):
        # Update the coordinate plane state
        pass

    def handle_mouse_down(self, pos, button, gui_manager, user):
        if button == 1:
            x = pos[0] // GRID_SIZE - 1
            y = pos[1] // GRID_SIZE - 2

            if 0 <= x < len(self.cells) and 0 <= y < len(self.cells[x]):
                cell = self.cells[x][y]
                cell.handle_click(gui_manager, user)

    def assign_user_cells(self, user):
        num_cells = random.randint(2, 5)

        # Randomly choose the first cell
        first_cell = random.choice(random.choice(self.cells))
        first_cell.set_user(user)
        self.user_owned_cells.add(first_cell)

        # Iterate to assign additional cells
        while len(self.user_owned_cells) < num_cells:
            bordering_cells = []
            for cell in self.user_owned_cells:
                x, y = cell.get_position()
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    neighbor_x = x + dx
                    neighbor_y = y + dy
                    if 0 <= neighbor_x < len(self.cells) and 0 <= neighbor_y < len(
                        self.cells[neighbor_x]
                    ):
                        neighbor_cell = self.cells[neighbor_x][neighbor_y]
                        if neighbor_cell not in self.user_owned_cells:
                            bordering_cells.append(neighbor_cell)

            if not bordering_cells:
                break

            # Randomly choose a bordering cell and assign it to the user
            chosen_cell = random.choice(bordering_cells)
            chosen_cell.set_user(user)
            self.user_owned_cells.add(chosen_cell)


class Cell:
    def __init__(self, position, resource):
        self.position = position
        self.resource = resource
        self.user = None

    def get_position(self):
        return self.position

    def set_user(self, user):
        self.user = user

    def draw(self, screen):
        x_pos, y_pos = self.position
        outline_color = (0, 0, 0)
        overlay_color = (0, 0, 0, 150)  # Darkened overlay color with transparency

        rect = pygame.Rect(x_pos, y_pos, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, outline_color, rect, 1)  # Draw outline

        inner_rect = pygame.Rect(x_pos + 1, y_pos + 1, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(screen, self.get_color_by_resource(self.resource), inner_rect)

        if not self.user:
            overlay_rect = pygame.Surface(
                (GRID_SIZE - 2, GRID_SIZE - 2), pygame.SRCALPHA
            )
            overlay_rect.fill(overlay_color)
            screen.blit(overlay_rect, (x_pos + 1, y_pos + 1))

    def handle_click(self, gui_manager, user):
        if self.user:
            info_text = (
                f"Information:\n- Resource: {self.resource}\n- Owned By: {self.user}"
            )
            gui_manager.show_info_window(info_text)
        else:
            self.user = user
            user.add_owned_coordinate(self)

    def is_boundary_cell(self):
        if not self.user:
            return False

        x_pos, y_pos = self.position

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor_x = x_pos + dx * GRID_SIZE
            neighbor_y = y_pos + dy * GRID_SIZE

            if (neighbor_x, neighbor_y) not in self.user.get_owned_coordinates():
                return True

        return False

    def get_color_by_resource(self, resource):
        if resource == "Water":
            return (0, 0, 255)  # Blue for 'Water'
        elif resource == "Farmland":
            return (0, 255, 0)  # Green for 'Farmland'
        elif resource == "Ore":
            return (128, 128, 128)  # Gray for 'Ore'
        elif resource == "Wood":
            return (139, 69, 19)  # Brown for 'Wood'
        elif resource == "Plains":
            return (210, 180, 140)  # Tan for 'Plains'
        elif resource == "Stone":
            return (192, 192, 192)  # Silver for 'Stone'
        elif resource == "Animals":
            return (255, 165, 0)  # Orange for 'Animals'
        else:
            return (255, 255, 255)  # Default color for unknown resource
