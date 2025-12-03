#Jocquise Green
#November 23, 2025
#CPSC 1050
#A text-based adventure game with sanity mechanics and shadow interactions. This program is supposed to take place in a 
#haunted house where the player must manage their sanity while navigating rooms, collecting items, and avoiding the influence of a shadowy entity.

import sys
import time
import random

from item import Item
from inventory import Inventory
from adventure_map import adventure_map
from shadow import Shadow

# ---------- Typewriter ----------
def typewriter(text, speed=0.02):
    # print text char-by-char to simulate a typewriter effect.
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# ---------- Game State Class ----------
class GameState:
    def __init__(self):
        self.current_room = adventure_map["Foyer"]        # starting room
        self.inventory = Inventory()                     # player's inventory instance
        self.action_count = 0                             # counts actions until victory/death
        self.insanity = 100                               # sanity meter (100 sane -> 0 death)
        self.shadow = Shadow(typewriter)                  # shadow entity reacting to events
        self.shadow_suppressed_turns = 0                  # how many turns shadow is suppressed
        self.steel_ball_used = False                      # record of steel ball use
        self.necronomicon_read = False                    # track if read

# ---------- Helpers ----------
def write_log(line):
    """Append a single line to gamelog.txt"""
    with open("gamelog.txt", "a") as f:
        f.write(line + "\n")

def decrease_insanity(game_state, amount=5):
    """Decrease sanity; if reaches 0, the player dies."""
    game_state.insanity -= amount                              # reduce sanity
    if game_state.insanity <= 0:                               # check if insane
        game_state.insanity = 0
        typewriter("\nYour mind fractures. Madness consumes you.", speed=0.03)
        write_log(f"Player died from insanity after {game_state.action_count} actions.")
        sys.exit()                                             # end game

def increase_insanity(game_state, amount=10):
    """Increase sanity (cap at 100)."""
    game_state.insanity += amount
    if game_state.insanity > 100:
        game_state.insanity = 100                               # cap sanity

def update_room_description(game_state):
    """Show a room description modified by current sanity state."""
    if game_state.insanity > 70:
        typewriter(f"[Sane] {game_state.current_room.description}", speed=0.03)
    elif game_state.insanity > 40:
        typewriter(f"[Shaken] {game_state.current_room.description}", speed=0.035)
    elif game_state.insanity > 10:
        typewriter(f"[Distorted] Shadows twitch at the edges of your vision.", speed=0.03)
        typewriter(game_state.current_room.description, speed=0.03)
    else:
        typewriter(f"[Unraveling] Your perception thins; details bleed together.", speed=0.02)
        typewriter(game_state.current_room.description, speed=0.02)

# ---------- Shadow random events ----------
def random_shadow_event(game_state):
    # occasionally trigger a shadow whisper and decrease sanity unless suppressed.
    if game_state.shadow_suppressed_turns > 0:
        game_state.shadow_suppressed_turns -= 1                   # decrement suppression turns
        return
    if random.randint(1, 100) <= 15:                             # 15% chance per turn
        decrease_insanity(game_state, 5)                         # sanity loss
        # choose a line index based on current sanity tier for variety
        if game_state.insanity > 70:
            idx = 0
        elif game_state.insanity > 50:
            idx = 1
        elif game_state.insanity > 30:
            idx = 2
        elif game_state.insanity > 15:
            idx = 3
        else:
            idx = 4
        game_state.shadow.speak(idx)                             # shadow reacts

# ---------- Item usage effects ----------
def use_item_effect(game_state, item):
    
    # apply effects when an item is used/inspected/read/played.
    # (Higher 'insanity' value = more sane. decrease_insanity means losing sanity.)
   
    name = item.name.lower()

    if name == "umbra's echo":
        increase_insanity(game_state, 20)
        typewriter("A cold clarity washes over you; the echo steadies your thoughts.", speed=0.03)
        return

    if name == "perfect rotating steel ball":
        game_state.shadow_suppressed_turns = 5
        decrease_insanity(game_state, 40)
        game_state.steel_ball_used = True
        typewriter("The sphere hums and spins; reality lines up for a single breath.", speed=0.03)
        game_state.inventory.remove(item.name)
        return

    if name == "phoenix's soul fire":
        decrease_insanity(game_state, 15)
        typewriter("The ember scorches memory from your skull. You feel hollow and shaky.", speed=0.03)
        game_state.inventory.remove(item.name)
        return

    if name == "necronomicon":
        penalty = random.randint(20, 35)
        decrease_insanity(game_state, penalty)
        game_state.necronomicon_read = True
        typewriter("Words crawl and bite; something inside rejoices.", speed=0.03)
        game_state.shadow.speak(idx=random.randint(12, 14))
        return

    if name == "holy ankh":
        increase_insanity(game_state, 40)
        typewriter("A calm like dawn spreads through your mind.", speed=0.03)
        return

    if name == "burning light dagger":
        increase_insanity(game_state, 5)
        typewriter("The blade warms your thoughts; a faint order returns.", speed=0.03)
        return

    if name == "retribution's dying light":
        increase_insanity(game_state, 10)
        typewriter("The shard hums. For a moment justice feels near.", speed=0.03)
        return

    # default statement for items without specific effects
    typewriter("You examine it closely but nothing immediate happens.", speed=0.03)

# ---------- Player Actions ----------
def look_around(game_state):
    """Show the room description and list items (comma-separated if multiple)."""
    typewriter(game_state.current_room.description, speed=0.03)
    if game_state.current_room.items:
        names = ", ".join([it.name for it in game_state.current_room.items])
        typewriter(f"You find some items around you: {names}", speed=0.03)
    else:
        typewriter("There are no items here.", speed=0.03)

def show_inventory(game_state):
    """List items in inventory with descriptions."""
    items = game_state.inventory.list_items()
    if not items:
        typewriter("Inventory is empty.", speed=0.03)
        return
    typewriter("Inventory:", speed=0.03)
    for name, desc in items:
        typewriter(f"- {name}: {desc}", speed=0.02)

def pickup(game_state):

    if not game_state.current_room.items:
        typewriter("There are not items to pick up.", speed=0.03)  

    selected = game_state.current_room.items.pop(0)                 # pick first item
    game_state.inventory.add(selected)                              # add to inventory
    typewriter(f"You picked up: {selected.name}", speed=0.03)

    # immediate effect for some items
    if selected.name.lower() == "phoenix's soul fire":
        decrease_insanity(game_state, 10)
        typewriter("The ember scorches the edges of your mind.", speed=0.03)
        game_state.shadow.speak()
    if selected.name.lower() == "necronomicon":
        game_state.shadow.speak()

def inspect(game_state):
    """Inspect an item in inventory (player selects by number or name)."""
    if not game_state.inventory.items:
        typewriter("I don't have anything to inspect", speed=0.03)
        return

    typewriter("Which inventory item do you want to inspect?", speed=0.02)
    for i, it in enumerate(game_state.inventory.items, 1):
        typewriter(f"{i}. {it.name}", speed=0.01)

    choice = input("Enter number or name: ").strip()
    target = None

    if choice.isdigit():
        idx = int(choice) - 1
        target = game_state.inventory.get_by_index(idx)
    else:
        lower = choice.lower()
        for it in game_state.inventory.items:
            if it.name.lower() == lower or it.name.lower().startswith(lower):
                target = it
                break

    if not target:
        typewriter("You don't have that item.", speed=0.03)
        return

    typewriter(f"Inspecting {target.name}: {target.inspect_text}", speed=0.03)
    use_item_effect(game_state, target)                           # inspect applies item effect


def read(game_state):
    # read a readable item from inventory; apply effects.
    readable_items = [it for it in game_state.inventory.items if it.readable and it.content]
    if not readable_items:
        typewriter("I don't have anything to read", speed=0.03)
        return # exits the function early and prevents further code execution.

    typewriter("Which item do you want to read?", speed=0.02)
    for i, it in enumerate(readable_items, 1):
        typewriter(f"{i}. {it.name}", speed=0.01)

    choice = input("Enter number or name: ").strip()
    target = None

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(readable_items):
            target = readable_items[idx]
    else:
        lower = choice.lower()
        for it in readable_items:
            if it.name.lower() == lower or it.name.lower().startswith(lower):
                target = it
                break

    if not target:
        typewriter("You don't have that item.", speed=0.03)
        return

    typewriter(f"You read {target.name}:", speed=0.03)
    typewriter(target.content, speed=0.02)
    use_item_effect(game_state, target)                            # reading triggers effect


def play(game_state):
    # use/play a playable item from inventory; apply effects.
    playable_items = [it for it in game_state.inventory.items if it.playable]
    if not playable_items:
        typewriter("I don't have anything to play", speed=0.03)
        return

    typewriter("Which item do you want to use/play?", speed=0.02)
    for i, it in enumerate(playable_items, 1): # display playable items
        typewriter(f"{i}. {it.name}", speed=0.01)

    choice = input("Enter number or name: ").strip()
    target = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(playable_items):
            target = playable_items[idx]
    else:
        lower = choice.lower()
        for it in playable_items:
            if it.name.lower() == lower or it.name.lower().startswith(lower):
                target = it
                break

    if not target:
        typewriter("You don't have that item", speed=0.03)
        return

    use_item_effect(game_state, target)                            # playing triggers effect


def unlock(game_state):
    # unlock action (Bedroom + Skeleton Key = victory).
    if game_state.current_room.name != "Bedroom":
        typewriter("I don't have anything to unlock", speed=0.03)
        return

    if not game_state.inventory.has("Skeleton Key"):
        typewriter("I don't have anything to unlock", speed=0.03)
        return

    # player has the key in bedroom = escape success
    write_log(f"Player escaped in {game_state.action_count} actions.")
    typewriter("You use the Skeleton Key. The trap door clicks open.", speed=0.03)
    typewriter("You climb through the trap door and taste cold air. You escape.", speed=0.03)
    sys.exit()


def move(game_state):
    # move/exit command: allow player to choose an exit."""
    if not game_state.current_room.exits:
        typewriter("There are no exits here.", speed=0.03)
        return

    typewriter("Exits: " + ", ".join(game_state.current_room.exits.keys()), speed=0.02)
    dest = input("Where do you want to go? ").strip().lower()

    if dest not in game_state.current_room.exits:
        raise NameError("Invalid exit")                         

    new_room_name = game_state.current_room.exits[dest]
    if new_room_name not in adventure_map:
        raise NameError("Invalid exit")                         

    game_state.current_room = adventure_map[new_room_name]
    decrease_insanity(game_state, 3)                              # small sanity loss on movement
    update_room_description(game_state)

def forge(game_state):
    #Combine items to craft powerful items.
    if game_state.inventory.has("Dead Owl") and game_state.inventory.has("Ancient Tome") and not game_state.inventory.has("Necronomicon"):
        game_state.inventory.remove("Dead Owl")
        game_state.inventory.remove("Ancient Tome") 
        game_state.inventory.add(Item("Necronomicon",
                                      "A flesh-bound tome inked in something too dark to be ink.",
                                      readable=True,
                                      content="The pages writhe under your fingers. Something ancient reads you in return.",
                                      inspect_text="The binding pulses faintly; the smell is of old funerals."))
        typewriter("You stitch the owl's remains into the ancient tome. A forbidden book forms: The Necronomicon.", speed=0.03)
        return

    if game_state.inventory.has("Broken Ankh") and game_state.inventory.has("Umbra's Echo") and game_state.inventory.has("Retribution's Dying Light") and not game_state.inventory.has("Holy Ankh"):
        game_state.inventory.remove("Broken Ankh")
        game_state.inventory.remove("Retribution's Dying Light")
        
        game_state.inventory.add(Item("Holy Ankh",
                                      "A restored sacred relic. Light radiates from it, steadying your mind.",
                                      readable=True,
                                      content="You feel clarity and strength as the Holy Ankh hums in your hands.",
                                      inspect_text="The Ankh's golden shape is perfect. Its power calms your fears."))
        typewriter("The dying light erupts, binding bone, gold, and shadow. When the brilliance fades, only the Holy Ankh remains.", speed=0.03)
        return

    typewriter("You don't have the required items to forge.", speed=0.03)


def game_intro(game_state):
    # opening text and first room description.
    typewriter("The house exhales around you. Something watches.", speed=0.04)
    update_room_description(game_state)

def main():
    """Main game loop. Counts actions and runs until escape or death."""
    game_state = GameState()                                       # initialize all game state
    game_intro(game_state)
    playing = True
    while playing:
        action = input("\nWhat do you want to do? (look/pickup/inspect/read/play/unlock/forge/inventory/move/quit) ").strip().lower()
        game_state.action_count += 1                                # increment actions

        decrease_insanity(game_state, 1)                             # small sanity drain per turn
        try:
            random_shadow_event(game_state)                          # possible shadow event
        except Exception:
            pass

        try:
            if action == "look around" or action == "look":
                look_around(game_state)
            elif action == "pickup":
                pickup(game_state)
            elif action == "inspect":
                inspect(game_state)
            elif action == "read":
                read(game_state)
            elif action == "play":
                play(game_state)
            elif action == "unlock":
                unlock(game_state)
            elif action == "forge":
                forge(game_state)
            elif action == "inventory":
                show_inventory(game_state)
            elif action == "move" or action == "exit":
                move(game_state)
            elif action == "quit":
                typewriter("You back away from the house and its questions.", speed=0.03)
                break
            else:
                typewriter("Unknown action.", speed=0.03)
        except NameError as e:
            typewriter(str(e), speed=0.03)
        except Exception as e:
            typewriter(f"Error: {e}", speed=0.03)

if __name__ == "__main__":
    main()

'''Notes:
Any type of interaction with items (inspect, read, play) applies the item's effect immediately.

'''
