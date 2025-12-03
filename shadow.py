import random

class Shadow:  # Represents the mysterious shadow entity
    def __init__(self, typewriter_func):
        self.typewriter = typewriter_func
        self.lines = [
            "An absolute fool you are.",
            "Futile… What do you hope to achieve?",
            "You shouldn’t be here… each step stains your mind.",
            "You’ve played these games before, yet learned nothing.",
            "You won’t stop… will you?",
            "The shadows remember… and they are patient.",
            "Every decision leaves an echo; your thoughts betray you.",
            "Some doors should never be opened, but you insist.",
            "You can feel them watching, though you are alone.",
            "Time is not kind here; it fractures and deceives.",
            "Even clarity is a lie when fear guides your hand.",
            "The walls whisper truths you are not ready to hear.",
            "You touched the forbidden text… foolish child of light.",
            "The book whispers your name now. It will not forget.",
            "You read what was meant to stay silent. Consequences follow."
        ]

    def speak(self, idx=None):
        if idx is None:
            idx = random.randint(0, len(self.lines) - 1)
        if 0 <= idx < len(self.lines):
            
            self.typewriter(f"???: \"{self.lines[idx]}\"", speed=0.03)

