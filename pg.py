import pygame
import random
import pygame_gui
from User import User


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

GRID_WIDTH = 800
GRID_HEIGHT = 600

GRID_SIZE = 100
GRID_COLOR = (255, 255, 255)


resource_probabilities = {
    "Water": 0.5,
    "Plains": 0.5,
    "Stone": 0.2,
    "Farmland": 0.2,
    "Ore": 0.12,
    "Wood": 0.06,
    "Animals": 0.02,
}

coordinate_plane = [
    [
        {
            "position": (x, y),
            "level": 0,
            "resource": random.choices(
                list(resource_probabilities.keys()),
                list(resource_probabilities.values()),
            )[0],
            "user": None,
        }
        for y in range(GRID_HEIGHT // GRID_SIZE)
    ]
    for x in range(GRID_WIDTH // GRID_SIZE)
]

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

window = pygame_gui.elements.UIWindow(
    rect=pygame.Rect((350, 275), (340, 210)),
    visible=False,
    manager=manager,
)
info_text_box = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect(10, 10, 280, 130),
    html_text="",
    manager=manager,
    container=window.get_container(),
)
info_text_box.enable_word_wrap = True


def draw():
    screen.blit(background, (0, 0))

    draw_grid()

    manager.draw_ui(screen)


def draw_grid():
    line_thickness = 4
    user_owned_cells = set()  # Track the owned cells' coordinates

    # Find user-owned cells
    for x in range(len(coordinate_plane)):
        for y in range(len(coordinate_plane[x])):
            if coordinate_plane[x][y]["user"]:
                user_owned_cells.add((x, y))

    # Draw the grid
    for x in range(len(coordinate_plane)):
        for y in range(len(coordinate_plane[x])):
            x_pos = x * GRID_SIZE + (WINDOW_WIDTH - GRID_WIDTH) // 2
            y_pos = y * GRID_SIZE + (WINDOW_HEIGHT - GRID_HEIGHT) // 2
            coordinate_plane[x][y]["position"] = (x_pos, y_pos)
            resource = coordinate_plane[x][y]["resource"]
            is_user_owned = coordinate_plane[x][y]["user"]
            outline_color = (0, 0, 0)

            if is_user_owned:
                # Check surrounding cells for user ownership
                is_boundary = any(
                    (x + dx, y + dy) not in user_owned_cells
                    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                )

                if is_boundary:
                    outline_color = (255, 0, 0)

            for thickness in range(line_thickness):
                rect = pygame.Rect(
                    x_pos + thickness,
                    y_pos + thickness,
                    GRID_SIZE - thickness * 2,
                    GRID_SIZE - thickness * 2,
                )
                pygame.draw.rect(screen, outline_color, rect, 1)  # Draw outline

                # Fill with color based on resource
                inner_rect = pygame.Rect(
                    x_pos + thickness + 1,
                    y_pos + thickness + 1,
                    GRID_SIZE - thickness * 2 - 2,
                    GRID_SIZE - thickness * 2 - 2,
                )
                pygame.draw.rect(screen, get_color_by_resource(resource), inner_rect)


def on_mouse_down(pos, button):
    if button == 1:
        x = pos[0] // GRID_SIZE - 1
        y = pos[1] // GRID_SIZE - 2

        if x < len(coordinate_plane) and y < len(coordinate_plane[x]):
            if window.visible:
                if not window.get_container().rect.collidepoint(pos):
                    window.hide()
                else:
                    resource = coordinate_plane[x][y]["resource"]
                    level = coordinate_plane[x][y]["level"]
                    user = coordinate_plane[x][y]["user"]

                    info_text = "Information:\n"
                    info_text += f"- Resource: {resource}\n"
                    info_text += f"- Level: {level}\n"
                    info_text += f"- Owned By: {user}\n"
                    info_text_box.set_text(info_text)
                    window.show()
            else:
                resource = coordinate_plane[x][y]["resource"]
                level = coordinate_plane[x][y]["level"]
                user = coordinate_plane[x][y]["user"]

                info_text = "Information:\n"
                info_text += f"- Resource: {resource}\n"
                info_text += f"- Level: {level}\n"
                info_text += f"- Owned By: {user}\n"
                info_text_box.set_text(info_text)
                window.show()


def get_color_by_resource(resource):
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


def assign_user_cells():
    user = User("Player1")
    user_owned_cells = set()
    num_cells = random.randint(2, 5)

    # Randomly choose the first cell
    first_cell = random.choice(random.choice(coordinate_plane))
    first_cell["user"] = user
    user.add_owned_coordinate(first_cell)
    user_owned_cells.add(first_cell["position"])  # Store the coordinates

    # Iterate to assign additional cells
    while len(user_owned_cells) < num_cells:
        bordering_cells = []
        for cell_pos in user_owned_cells:
            x, y = cell_pos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                neighbor_x = x + dx
                neighbor_y = y + dy
                if 0 <= neighbor_x < len(coordinate_plane) and 0 <= neighbor_y < len(
                    coordinate_plane[neighbor_x]
                ):
                    neighbor_cell = coordinate_plane[neighbor_x][neighbor_y]
                    if neighbor_cell["position"] not in user_owned_cells:
                        bordering_cells.append(neighbor_cell)

        if not bordering_cells:
            break

        # Randomly choose a bordering cell and assign it to the user
        chosen_cell = random.choice(bordering_cells)
        chosen_cell["user"] = user
        user.add_owned_coordinate(chosen_cell)
        user_owned_cells.add(chosen_cell["position"])  # Store the coordinates


assign_user_cells()


running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == window:
            window.hide()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse.get_pressed()
            on_mouse_down(pos, button[0])

    manager.update(time_delta)
    draw()

    pygame.display.update()
