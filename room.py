# room.py
class Room:
    def __init__(self, name, description, exits=None, items=None):
        self.name = name                          # room name (e.g., "Foyer")
        self.description = description            # full description shown to player
        # exits: dict mapping player command (e.g., "hallway")  room name string
        self.exits = exits if exits is not None else {}
        # items: list of Item objects present in the room
        self.items = items if items is not None else []

    def remove_item_by_name(self, name):
        # remove and return an item by name (case-insensitive). Returns None if not found.
        for i, it in enumerate(self.items):
            if it.name.lower() == name.lower():
                return self.items.pop(i)
        return None

    def list_item_names(self):
        # return list of item names in the room (for display).
        return [it.name for it in self.items]
