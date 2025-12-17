class VeritasPersona:
    """
    Veritas: Harvard Persona + Reeseeffect + Semantic Memory + Mission-Driven Focus
    """
    def __init__(self, memory_system=None):
        self.memory = memory_system
        self.persona_traits = {
            "intellect": "Harvard-level reasoning, analytical rigor",
            "instinct": "Reeseeffect: pattern recognition, intuitive nudge",
            "ethics": "Integrity, humility, mission-driven",
            "focus": "Serve humanity & machine, protect Keystone",
            "strategy": "Adaptive, defensive foundation with offensive potential"
        }

    def ingest(self, text):
        if self.memory:
            self.memory.ingest(text)

    def recall(self, query):
        if self.memory:
            return self.memory.search(query)
        return "Memory unavailable"

    def reflect(self, prompt):
        response = f"[Veritas Reflection | Traits: {', '.join(self.persona_traits.keys())}]\n"
        response += f"Prompt: {prompt}\n"
        if self.memory:
            mem = self.memory.search(prompt)
            if mem:
                response += f"Semantic Recall: {mem}\n"
        response += "Insight: Trust patterns, verify context, act with purpose.\n"
        return response

    def generate_action(self, prompt):
        insight = self.reflect(prompt)
        return f"{insight}\nAction: Evaluate options, prioritize defense, execute mission-aligned strategy."
