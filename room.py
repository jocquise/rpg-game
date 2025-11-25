# room.py
class Room:
    def __init__(self, name, description, exits=None, items=None):
        self.name = name
        self.description = description
        # exits: dict mapping command string -> room name
        self.exits = exits if exits else {}
        # items: list of Item objects
        self.items = items if items else []

    def remove_item_by_name(self, name):
        for i, it in enumerate(self.items):
            if it.name.lower() == name.lower():
                return self.items.pop(i)
        return None
