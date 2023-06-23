# {position, level, resource}

import random
from User import User

game_on = True

width = 10
height = 10

resource_probabilities = {
    "Water": 0.5,
    "Plains": 0.5,
    "Stone": 0.2,
    "Farmland": 0.2,
    "Ore": 0.12,
    "Wood": 0.06,
    "Animals": 0.02,
}


def init_coord_plane():
    return [
        [
            {
                "position": (x, y),
                "level": 0,
                "resource": random.choices(
                    list(resource_probabilities.keys()),
                    list(resource_probabilities.values()),
                    k=random.randint(1, 3),
                ),
                "user": None,
            }
            for y in range(height)
        ]
        for x in range(width)
    ]


def search_coordinate(coordinate_plane, target_position):
    for row in coordinate_plane:
        for coordinate in row:
            if coordinate["position"] == target_position:
                return coordinate
    return None


def display_menu():
    print("\nMenu:")
    print("1. Display Owned Plots")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Quit \n")


def get_user_choice():
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return int(choice)
        else:
            print("Invalid input. Please enter a valid choice.")


while game_on:
    coordinate_plane = init_coord_plane()
    user = User("Player1")

    user_coordinate = random.choice(random.choice(coordinate_plane))
    user_coordinate["user"] = user
    user.add_owned_coordinate(user_coordinate)

    display_menu()
    user_choice = get_user_choice()

    if user_choice == 1:
        coords = user.get_owned_coordinates()
        for coord in coords:
            print(coord["resource"])

    if user_choice == 4:
        game_on = False

    pass
