# item.py
class Item:
    def __init__(self, name, description, readable=False, content=None,
                 playable=False, unlocks=False, inspect_text=None):
        self.name = name                      # item name shown to player
        self.description = description        # short description for inventory/listings
        self.readable = readable              # can be read via "read" command
        self.content = content                # text shown when read
        self.playable = playable              # usable via "play" command
        self.unlocks = unlocks                # used for "unlock" checks (e.g., keys)
        # fallback for inspect_text if not provided
        self.inspect_text = inspect_text if inspect_text is not None else description

    def __repr__(self):
        return f"Item({self.name})"
