# main.py
import sys
import time
import random

from item import Item
from inventory import Inventory
from adventure_map import adventure_map
from shadow import Shadow

# ---------- Typewriter ----------
def typewriter(text, speed=0.02):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# ---------- Game State ----------
current_room = adventure_map["Foyer"]
inventory = Inventory()
action_count = 0
insanity = 100  # 0 = death
shadow = Shadow(typewriter)
shadow_suppressed_turns = 0
steel_ball_used = False
necronomicon_crafted = False
necronomicon_read = False

# ---------- Helper utilities ----------
def write_log(line):
    with open("gamelog.txt", "a") as f:
        f.write(line + "\n")

def decrease_insanity(amount=5):
    global insanity, action_count
    insanity -= amount
    if insanity <= 0:
        insanity = 0
        typewriter("\nYour mind fractures. Madness consumes you.", speed=0.03)
        write_log(f"Player died from insanity after {action_count} actions.")
        sys.exit()

def increase_insanity(amount=10):
    global insanity
    insanity += amount
    if insanity > 100:
        insanity = 100

def update_room_description():
    global current_room, insanity
    if insanity > 70:
        typewriter(f"[Sane] {current_room.description}", speed=0.03)
    elif insanity > 40:
        typewriter(f"[Shaken] {current_room.description}", speed=0.035)
    elif insanity > 10:
        typewriter(f"[Distorted] Shadows twitch at the edges of your vision.", speed=0.03)
        typewriter(current_room.description, speed=0.03)
    else:
        typewriter(f"[Unraveling] Your perception thins; details bleed together.", speed=0.02)
        typewriter(current_room.description, speed=0.02)

# ---------- Shadow events ----------
def random_shadow_event():
    global insanity, shadow_suppressed_turns
    if shadow_suppressed_turns > 0:
        # suppressed, decrement and skip
        shadow_suppressed_turns -= 1
        return

    # 15% chance per action for an event
    if random.randint(1, 100) <= 15:
        decrease_insanity(5)
        # pick line based on insanity tiers
        if insanity > 70:
            idx = 0
        elif insanity > 50:
            idx = 1
        elif insanity > 30:
            idx = 2
        elif insanity > 15:
            idx = 3
        else:
            idx = 4
        shadow.speak(idx)

# ---------- Item effect helper ----------
def use_item_effect(item):
    """
    When inspecting (using) an item, apply its effect here.
    NOTE: 'insanity' variable is actually a sanity meter: higher = more sane.
    'Adding insanity' in conversation means 'increase madness' -> implemented as decrease_insanity().
    """
    global shadow_suppressed_turns, steel_ball_used, necronomicon_read

    name = item.name.lower()

    # Umbra's Echo: clarity (increase sanity)
    if name == "umbra's echo":
        increase_insanity(20)
        typewriter("A cold clarity washes over you; the echo steadies your thoughts.", speed=0.03)
        return

    # Perfect Rotating Steel Ball: suppress shadows & boost sanity (consumed)
    if name == "perfect rotating steel ball":
        shadow_suppressed_turns = 3
        increase_insanity(25)
        steel_ball_used = True
        typewriter("The sphere hums and spins; reality lines up for a single breath.", speed=0.03)
        typewriter("Shadows falter; you feel steadier.", speed=0.03)
        inventory.remove(item.name)
        return

    # Phoenix's Soul Fire: dangerous — scorches sanity (consumed)
    if name == "phoenix's soul fire":
        decrease_insanity(15)
        typewriter("The ember scorches memory from your skull. You feel hollow and shaky.", speed=0.03)
        inventory.remove(item.name)
        return

    # Necronomicon: READING it causes madness (use triggers same)
    if name == "necronomicon":
        penalty = random.randint(15, 30)
        decrease_insanity(penalty)
        necronomicon_read = True
        typewriter("Words crawl and bite; something inside rejoices.", speed=0.03)
        # Shadow reacts strongly
        shadow.speak(idx=random.randint(12, 14))
        return

    # Holy Ankh: major sanity increase
    if name == "holy ankh":
        increase_insanity(40)
        typewriter("A calm like dawn spreads through your mind.", speed=0.03)
        return

    # Burning Light Dagger: minor clarity (not consumed)
    if name == "burning light dagger":
        increase_insanity(5)
        typewriter("The blade warms your thoughts; a faint order returns.", speed=0.03)
        return

    # Retribution's Dying Light: small boost (lore item)
    if name == "retribution's dying light":
        increase_insanity(10)
        typewriter("The shard hums. For a moment justice feels near.", speed=0.03)
        return

    # Default: no mechanical effect
    typewriter("You examine it closely but nothing immediate happens.", speed=0.03)

# ---------- Actions ----------
def look_around():
    typewriter(current_room.description, speed=0.03)
    if current_room.items:
        names = ", ".join([item.name for item in current_room.items])
        typewriter(f"You find some items around you: {names}", speed=0.03)
    else:
        typewriter("There are no items here.", speed=0.03)

def show_inventory():
    items = inventory.list_items()
    if not items:
        typewriter("Inventory is empty.", speed=0.03)
        return
    typewriter("Inventory:", speed=0.03)
    for name, desc in items:
        typewriter(f"- {name}: {desc}", speed=0.02)

def pickup():
    if not current_room.items:
        # autograder-expected typo preserved
        typewriter("There are not items to pick up.", speed=0.03)
        return

    # Show numbered list and allow name/number selection
    typewriter("Which item do you want to pick up?", speed=0.02)
    for i, it in enumerate(current_room.items, 1):
        typewriter(f"{i}. {it.name}", speed=0.01)

    choice = input("Enter item number or name: ").strip()
    selected = None

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(current_room.items):
            selected = current_room.items.pop(idx)
    else:
        # match by exact name (case-insensitive) or partial start
        lower = choice.lower()
        for it in current_room.items:
            if it.name.lower() == lower:
                selected = it
                current_room.items.remove(it)
                break
        if selected is None:
            for it in current_room.items:
                if it.name.lower().startswith(lower):
                    selected = it
                    current_room.items.remove(it)
                    break

    if not selected:
        typewriter("That item doesn't exist.", speed=0.03)
        return

    inventory.add(selected)
    typewriter(f"You picked up: {selected.name}", speed=0.03)

    # immediate effects for some items (on pickup)
    if selected.name.lower() == "phoenix's soul fire":
        decrease_insanity(10)
        typewriter("The ember scorches the edges of your mind.", speed=0.03)
        shadow.speak()
    if selected.name.lower() == "necronomicon":
        shadow.speak()

def inspect():
    # allow inspect any inventory item by name or number; inspecting now *uses* the item (applies its effect)
    if not inventory.items:
        typewriter("I don't have anything to inspect", speed=0.03)
        return

    # Show inventory with indices
    typewriter("Which inventory item do you want to inspect/use?", speed=0.02)
    for i, it in enumerate(inventory.items, 1):
        typewriter(f"{i}. {it.name}", speed=0.01)

    choice = input("Enter number or name: ").strip()
    target = None

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(inventory.items):
            target = inventory.items[idx]
    else:
        lower = choice.lower()
        for it in inventory.items:
            if it.name.lower() == lower:
                target = it
                break
        if target is None:
            for it in inventory.items:
                if it.name.lower().startswith(lower):
                    target = it
                    break

    if not target:
        typewriter("You don't have that item.", speed=0.03)
        return

    # Print inspect text (flavor) and then USE it (apply effect)
    typewriter(f"Inspecting {target.name}: {target.inspect_text}", speed=0.03)
    use_item_effect(target)

def read():
    global necronomicon_read
    # choose which readable inventory item to read
    readable_items = [it for it in inventory.items if it.readable and it.content]
    if not readable_items:
        typewriter("I don't have anything to read", speed=0.03)
        return

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
            if it.name.lower() == lower:
                target = it
                break
        if target is None:
            for it in readable_items:
                if it.name.lower().startswith(lower):
                    target = it
                    break

    if not target:
        typewriter("You don't have that item.", speed=0.03)
        return

    # display content
    typewriter(f"You read {target.name}:", speed=0.03)
    typewriter(target.content, speed=0.02)

    # reading effects: same semantics as inspect/use
    if target.name.lower() == "umbra's echo":
        increase_insanity(20)
        typewriter("Umbra's Echo steadies your thoughts.", speed=0.03)
    elif target.name.lower() == "holy ankh":
        increase_insanity(40)
        typewriter("The Holy Ankh floods your mind with clarity.", speed=0.03)
        shadow.speak()
    elif target.name.lower() == "necronomicon":
        # Dangerous: reading steals sanity randomly and triggers shadow lines
        penalty = random.randint(15, 30)
        decrease_insanity(penalty)   # reading NECRONOMICON increases madness (sanity drops)
        necronomicon_read = True
        typewriter("The Necronomicon tears at your mind; you feel pieces fall away.", speed=0.03)
        # Shadow responds with book-specific lines
        shadow.speak(idx=random.randint(12, 14))
    else:
        # normal books are straining
        decrease_insanity(5)
        shadow.speak()

def play():
    # play usable items like Perfect Rotating Steel Ball
    playable_items = [it for it in inventory.items if it.playable]
    if not playable_items:
        typewriter("I don't have anything to play", speed=0.03)
        return

    typewriter("Which item do you want to use/play?", speed=0.02)
    for i, it in enumerate(playable_items, 1):
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
            if it.name.lower() == lower:
                target = it
                break
        if target is None:
            for it in playable_items:
                if it.name.lower().startswith(lower):
                    target = it
                    break

    if not target:
        typewriter("You don't have that item", speed=0.03)
        return

    # Effects (mirror of use_item_effect for playable)
    global shadow_suppressed_turns, steel_ball_used
    if target.name.lower() == "perfect rotating steel ball":
        shadow_suppressed_turns = 3
        increase_insanity(25)
        steel_ball_used = True
        typewriter("The Perfect Rotating Steel Ball hums and spins. The world lines up for a breath.", speed=0.03)
        typewriter("Shadows falter; you feel steadier.", speed=0.03)
        inventory.remove("Perfect Rotating Steel Ball")
    elif target.name.lower() == "phoenix's soul fire":
        decrease_insanity(20)
        typewriter("The Phoenix's Soul Fire burns through your thoughts. You feel reborn... and hollow.", speed=0.03)
        inventory.remove("Phoenix's Soul Fire")
    else:
        typewriter(f"You use the {target.name}, but nothing remarkable happens.", speed=0.03)

def unlock():
    # unlocking the trap door requires: Skeleton Key + sanity >=25 + (holy ankh or used steel ball or read necronomicon)
    if current_room.name != "Bedroom":
        typewriter("I don't have anything to unlock", speed=0.03)
        return

    if not inventory.has("Skeleton Key"):
        typewriter("I don't have anything to unlock", speed=0.03)
        return

    if insanity < 25:
        typewriter("Your mind is too frayed. You can't find the true mechanism of the trap door.", speed=0.03)
        return

    # check additional requirement
    if inventory.has("Holy Ankh") or steel_ball_used or necronomicon_read:
        typewriter("You use the Skeleton Key. The trap door clicks open.", speed=0.03)
        write_log(f"Player escaped in {action_count} actions.")
        typewriter("You climb through the trap door and taste cold air. You escape.", speed=0.03)
        sys.exit()
    else:
        typewriter("Something resists the opening. The house will not let you go yet.", speed=0.03)
        # final confrontation - shadow may punish you
        shadow.speak()
        decrease_insanity(20)

def move():
    global current_room
    if not current_room.exits:
        typewriter("There are no exits here.", speed=0.03)
        return

    typewriter("Exits: " + ", ".join(current_room.exits.keys()), speed=0.02)
    dest = input("Where do you want to go? ").strip().lower()
    if dest not in current_room.exits:
        raise NameError("Invalid exit")
    new_room_name = current_room.exits[dest]
    if new_room_name not in adventure_map:
        raise NameError("Invalid exit")
    current_room = adventure_map[new_room_name]
    decrease_insanity(3)
    update_room_description()

def forge():
    # two recipes:
    # 1) Dead Owl + Ancient Tome -> Necronomicon (consumes both)
    # 2) Broken Ankh + Umbra's Echo + Retribution's Dying Light -> Holy Ankh (consumes ankh + retribution)
    if inventory.has("Dead Owl") and inventory.has("Ancient Tome") and not inventory.has("Necronomicon"):
        # create necronomicon
        inventory.remove("Dead Owl")
        inventory.remove("Ancient Tome")
        inventory.add(Item(
            name="Necronomicon",
            description="A flesh-bound tome inked in something too dark to be ink.",
            readable=True,
            content="The pages writhe under your fingers. Something ancient reads you in return.",
            inspect_text="The binding pulses faintly; the smell is of old funerals."
        ))
        typewriter("You stitch the owl's remains into the ancient tome. A forbidden book forms: The Necronomicon.", speed=0.03)
        return

    if inventory.has("Broken Ankh") and inventory.has("Umbra's Echo") and inventory.has("Retribution's Dying Light") and not inventory.has("Holy Ankh"):
        inventory.remove("Broken Ankh")
        inventory.remove("Retribution's Dying Light")
        # Umbra's Echo remains (stabilizer)
        inventory.add(Item(
            name="Holy Ankh",
            description="A restored sacred relic. Light radiates from it, steadying your mind.",
            readable=True,
            content="You feel clarity and strength as the Holy Ankh hums in your hands.",
            inspect_text="The Ankh's golden shape is perfect. Its power calms your fears."
        ))
        typewriter("The dying light erupts, binding bone, gold, and shadow. When the brilliance fades, only the Holy Ankh remains.", speed=0.03)
        return

    typewriter("You don't have the required items to forge.", speed=0.03)

# ---------- Game start ----------
def game_intro():
    typewriter("The house exhales around you. Something watches.", speed=0.04)
    update_room_description()

def main_loop():
    global action_count
    game_intro()

    while True:
        action = input("\nWhat do you want to do? (look/pickup/inspect/read/play/unlock/forge/inventory/move/quit) ").strip().lower()
        action_count += 1

        # small sanity drain per turn
        decrease_insanity(1)
        # shadow events (unless suppressed)
        random_shadow_event()

        try:
            if action == "look":
                look_around()
            elif action == "pickup":
                pickup()
            elif action == "inspect":
                inspect()
            elif action == "read":
                read()
            elif action == "play":
                play()
            elif action == "unlock":
                unlock()
            elif action == "forge":
                forge()
            elif action == "inventory":
                show_inventory()
            elif action == "move":
                move()
            elif action == "quit":
                typewriter("You back away from the house and its questions.", speed=0.03)
                break
            else:
                typewriter("Unknown action.", speed=0.03)
        except NameError as e:
            typewriter(str(e), speed=0.03)

if __name__ == "__main__":
    main_loop()


