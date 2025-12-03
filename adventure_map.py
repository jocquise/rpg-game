from room import Room
from item import Item   

# adventure_map.py
from room import Room
from item import Item

dead_owl = Item("Dead Owl", "A lifeless owl lies on the floor. Its eyes stare like voids.",
                readable=False, inspect_text="Its feathers are brittle, dark stains beneath a wing.")
bejewelled_earrings = Item("Bejeweled Earrings", "A pair of glassy earrings that catch dim light.",
                          inspect_text="The gems seem to reflect movements you didn't make.")
umbras_echo = Item("Umbra's Echo", "A mysterious talisman pulsing with dark energy.",
                   readable=True, content="You feel a flicker of clarity.",
                   inspect_text="The engraving feels oddly familiar.")
broken_ankh = Item("Broken Ankh", "Fragments of a sacred relic, needing restoration.",
                   inspect_text="The pieces almost fit together. Perhaps they could be repaired.")
retribution_light = Item("Retribution's Dying Light",
                         "A shard of fading radiance that hums with judgment.",
                         inspect_text="The shard hums with moral heat.")
ancient_tome = Item("Ancient Tome", "Its pages are brittle, filled with cryptic symbols.",
                    readable=True, content="Glyphs wriggle at the edge of vision.",
                    inspect_text="The ink seems to slip when you blink.")
skeleton_key = Item("Skeleton Key",
                    "Forged in silence. Its metal hums faintly like a heartbeat.\nLegends say it was carved from the spine of a forgotten king.\nIt unlocks not just doors—but endings.",
                    unlocks=True, inspect_text="Cold metal with careful teeth; it feels older than any lock.")
burning_light_dagger = Item("Burning Light Dagger", "A blade forged from pale fire. Warm to the touch.",
                           inspect_text="Despite its warmth, the edge draws no ordinary blood.")
perfect_steel_ball = Item("Perfect Rotating Steel Ball",
                         "A polished sphere humming with spiraling golden energy.",
                         content="The Golden Spin… a force that aligns intention.",
                         playable=True, inspect_text="Tiny glyphs hide beneath the smooth surface.")
phoenix_soul_fire = Item("Phoenix's Soul Fire",
                         "A jarred ember of a long-dead phoenix. Its heat licks like the Endsong Inferno.",
                         content="You feel a surge of violent warmth — rebirth with teeth.",
                         playable=True, inspect_text="The ember flares with its own hunger.")
necronomicon = Item("Necronomicon", "A flesh-bound tome inked in something too dark to be ink.",
                    readable=True, content="The pages writhe; something reads YOU in return.",
                    inspect_text="The binding pulses faintly; the smell is of old funerals.")
holy_ankh = Item("Holy Ankh", "A restored sacred relic. Light radiates from it, steadying your mind.",
                 readable=True, content="Clarity and strength fill you.", inspect_text="A perfect golden ankh.")

# --- Rooms ---
foyer = Room(
    name="Foyer",
    description="Foyer: Dust fills the air. Faded books cling to warped shelves; the floorboards groan.",
    exits={"hallway": "Hallway", "library": "Library"},
    items=[dead_owl, bejewelled_earrings, umbras_echo]
)

hallway = Room(
    name="Hallway",
    description="Hallway: A narrow corridor where candlelight fails to reach the far wall.",
    exits={"foyer": "Foyer", "bedroom": "Bedroom", "attic": "Attic", "basement": "Basement"},
    items=[broken_ankh, retribution_light, perfect_steel_ball]
)

library = Room(
    name="Library",
    description="Library: Tall shelves tower above you, filled with unreadable tomes.",
    exits={"foyer": "Foyer"},
    items=[ancient_tome]
)

bedroom = Room(
    name="Bedroom",
    description="Bedroom: The bed is tattered, and a cold wind drifts from the trap door beneath.",
    exits={"hallway": "Hallway"},
    items=[skeleton_key]
)

attic = Room(
    name="Attic",
    description="Attic: The roof sags, and a cold draft bites. Shadows dance unnaturally along the rafters.",
    exits={"hallway": "Hallway"},
    items=[burning_light_dagger, Item("Torn Portrait", "A a woman’s blade hovers over a bloodied man, much of the scene missing."),
           Item("Candle", "An unlit candle.")]
)

basement = Room(
    name="Basement",
    description="Basement: Damp walls and rusted chains. The darkness seems to breathe.",
    exits={"hallway": "Hallway"},
    items=[phoenix_soul_fire]
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
