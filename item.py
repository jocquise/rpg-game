# item.py
class Item:
    def __init__(self, name, description, readable=False, content=None, playable=False, unlocks=False, inspect_text=None):
        self.name = name
        self.description = description
        self.readable = readable
        self.content = content
        self.playable = playable
        self.unlocks = unlocks
        # fallback inspect text to description if none provided
        self.inspect_text = inspect_text if inspect_text is not None else description

    def __repr__(self):
        return f"Item({self.name})"
