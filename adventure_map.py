# adventure_map.py
from room import Room
from item import Item

# Items definitions (placed into rooms below)
dead_owl = Item(
    name="Dead Owl",
    description="A lifeless owl lies on the floor. Its eyes stare like voids.",
    readable=False,
    inspect_text="Its feathers are brittle, and something dark stains the underside of one wing."
)

bejewelled_earrings = Item(
    name="Bejeweled Earrings",
    description="A pair of earrings set with glassy stones; they catch the light strangely.",
    inspect_text="Up close the gems seem to reflect movements that you didn't make."
)

# --- UPDATED Umbra's Echo per your text ---
umbras_echo = Item(
    name="Umbra's Echo",
    description="A mysterious talisman pulsing with dark energy.",
    readable=True,
    content="You feel a flicker of clarity.",
    inspect_text="The engraving is indecipherable but somehow familiar."
)

broken_ankh = Item(
    name="Broken Ankh",
    description="A fractured holy relic. It vibrates faintly with lost power.",
    inspect_text="The pieces almost fit together. Perhaps it could be repaired with the right items."
)

retribution_light = Item(
    name="Retribution's Dying Light",
    description="A shard of radiance fading from existence. Its glow flickers between agony and judgment.",
    inspect_text="The shard hums with moral heat—both comfort and condemnation."
)

ancient_tome = Item(
    name="Ancient Tome",
    description="Its pages are brittle, filled with cryptic symbols.",
    readable=True,
    content="The glyphs writhe like living serpents. Your vision swims as you read.",
    inspect_text="The ink seems to move when you blink."
)

skeleton_key = Item(
    name="Skeleton Key",
    description=(
        "Forged in silence. Its metal hums faintly like a heartbeat.\n"
        "Legends say it was carved from the spine of a forgotten king.\n"
        "It unlocks not just doors—but endings."
    ),
    unlocks=True,
    inspect_text="Cold metal with careful teeth; it feels older than any lock you know."
)

burning_light_dagger = Item(
    name="Burning Light Dagger",
    description="A blade forged from pale fire. Warm to the touch, yet weightless.",
    inspect_text="Despite its warmth, the edge draws no blood in ordinary ways."
)

perfect_steel_ball = Item(
    name="Perfect Rotating Steel Ball",
    description="A polished sphere humming with spiraling golden energy. It rotates with impossible precision.",
    content="The Golden Spin… a force that aligns intention, body, and soul.",
    inspect_text="Tiny glyphs run under the smooth surface; the spin is almost hypnotic.",
    playable=True
)

phoenix_soul_fire = Item(
    name="Phoenix's Soul Fire",
    description="A jarred ember of a long-dead phoenix. Its heat is unnatural and licks like the Endsong Inferno.",
    content="You feel a surge of violent warmth — rebirth with teeth.",
    inspect_text="The ember occasionally flares on its own, throwing small sparks.",
    playable=True
)

necronomicon = Item(
    name="Necronomicon",
    description="A flesh-bound tome inked in something too dark to be ink.",
    readable=True,
    content=(
        "The pages writhe under your fingers.\n"
        "Words rearrange themselves as if alive.\n"
        "Something ancient and starving reads YOU in return."
    ),
    inspect_text="The binding pulses faintly; the smell is of old funerals."
)

holy_ankh = Item(
    name="Holy Ankh",
    description="A restored sacred relic. Light radiates from it, steadying your mind.",
    readable=True,
    content="You feel clarity and strength as the Holy Ankh hums in your hands.",
    inspect_text="The Ankh's golden shape is perfect. Its power calms your fears."
)

# Rooms
foyer = Room(
    name="Foyer",
    description="Dust fills the air. Faded books cling to warped shelves; the floorboards groan.",
    exits={"hallway": "Hallway", "library": "Library"},
    items=[dead_owl, bejewelled_earrings, umbras_echo]
)

hallway = Room(
    name="Hallway",
    description="A narrow corridor where candlelight fails to reach the far wall.",
    exits={"foyer": "Foyer", "bedroom": "Bedroom", "attic": "Attic", "basement": "Basement"},
    items=[broken_ankh, retribution_light, perfect_steel_ball]
)

library = Room(
    name="Library",
    description="Tall shelves tower above you, filled with unreadable tomes.",
    exits={"foyer": "Foyer"},
    items=[ancient_tome]
)

bedroom = Room(
    name="Bedroom",
    description="The bed is tattered, and a cold wind drifts from the trap door beneath.",
    exits={"hallway": "Hallway"},
    items=[skeleton_key]
)

attic = Room(
    name="Attic",
    description="The roof sags, and a cold draft bites. Shadows dance unnaturally along the rafters.",
    exits={"hallway": "Hallway"},
    items=[burning_light_dagger, Item("Torn Portrait", "A torn portrait; something familiar is missing."), Item("Candle", "An unlit candle.")] 
)

basement = Room(
    name="Basement",
    description="Damp walls and rusted chains. The darkness seems to breathe.",
    exits={"hallway": "Hallway"},
    items=[phoenix_soul_fire]  # Necronomicon will be craftable; phoenix present here
)

# Map dictionary
adventure_map = {
    "Foyer": foyer,
    "Hallway": hallway,
    "Library": library,
    "Bedroom": bedroom,
    "Attic": attic,
    "Basement": basement
}
