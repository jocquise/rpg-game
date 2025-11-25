# inventory.py
class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, name):
        self.items = [i for i in self.items if i.name.lower() != name.lower()]

    def has(self, name):
        return any(i.name.lower() == name.lower() for i in self.items)

    def get(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return None

    def list_items(self):
        return [(i.name, i.description) for i in self.items]

    def get_by_index(self, idx):
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None

