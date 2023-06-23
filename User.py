class User:
    def __init__(self, name):
        self.name = name
        self.owned_coordinates = []
        self.resource_bank = {}

    def add_owned_coordinate(self, coordinate):
        self.owned_coordinates.append(coordinate)

    def remove_owned_coordinate(self, coordinate):
        self.owned_coordinates.remove(coordinate)

    def add_resource(self, resource, amount=1):
        if resource in self.resource_bank:
            self.resource_bank[resource] += amount
        else:
            self.resource_bank[resource] = amount

    def remove_resource(self, resource, amount=1):
        if resource in self.resource_bank:
            self.resource_bank[resource] -= amount
            if self.resource_bank[resource] <= 0:
                del self.resource_bank[resource]

    def get_owned_coordinates(self):
        return self.owned_coordinates

    def get_resource_bank(self):
        return self.resource_bank

    def __str__(self):
        return f"{self.name}"
