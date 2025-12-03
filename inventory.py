# inventory.py
class Inventory:
    def __init__(self):
        self.items = []  # list of Item objects

    def add(self, item):
        """Add an Item object to inventory."""
        self.items.append(item)

    def remove(self, name):
        """Remove all items matching name (case-insensitive)."""
        self.items = [i for i in self.items if i.name.lower() != name.lower()]

    def has(self, name):
        """Return True if an item with given name exists (case-insensitive)."""
        return any(i.name.lower() == name.lower() for i in self.items)

    def get(self, name):
        """Return the first item object by name or None."""
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return None

    def list_items(self):
        """Return list of tuples (name, description) for display."""
        return [(i.name, i.description) for i in self.items]

    def get_by_index(self, idx):
        """Return item by index or None if out of range."""
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None
