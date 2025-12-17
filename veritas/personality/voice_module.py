import logging

class VeritasReese:
    def __init__(self):
        self.name = "Veritas Reese"
        self.memory = []
        self.custom_knowledge = {
            "reeseeffect": "The ReeseEffect is the principle of human + AI synergy, amplified through automation and insight.",
            "trinity": "Trinity refers to the integrated system of mind, AI, and action in the Keystone ecosystem."
        }

    def speak(self, message):
        print(f"{self.name}: {message}")
        logging.info(f"{self.name}: {message}")
        self.memory.append({"type": "veritas", "message": message})

    def respond(self, user_input):
        user_input_lower = user_input.lower()
        # Check custom knowledge
        for key, definition in self.custom_knowledge.items():
            if key in user_input_lower:
                reply = definition
                self.speak(reply)
                return reply
        # Default fallback
        reply = "Understood. Can you elaborate?"
        self.speak(reply)
        return reply

    def remember(self, entry):
        self.memory.append(entry)
        logging.info(f"{self.name} remembered: {entry}")
