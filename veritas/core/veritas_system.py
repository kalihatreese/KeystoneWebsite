"""
VeritasSystem — integrates AIModel + SemanticMemory + VeritasPersona
for fully mission-aligned, self-reflective assistant behavior.
"""
from core.model import load_model
from core.veritas_persona import VeritasPersona

# Attempt to import semantic memory utilities
try:
    from core.memory_shaper import ingest_and_chunk, search_memory
except ImportError:
    # Fallback stubs
    def ingest_and_chunk(text):
        return []

    def search_memory(query):
        return "Semantic memory unavailable."

class SemanticMemory:
    """Simple wrapper for semantic memory."""
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.chunks = []

    def ingest(self, text):
        new_chunks = ingest_and_chunk(text)
        self.chunks.extend(new_chunks)
        return new_chunks

    def search(self, query):
        return search_memory(query)

class VeritasSystem:
    """Full Veritas integration."""
    def __init__(self, model_path=None, memory_db=None):
        self.model = load_model(model_path)
        self.memory = SemanticMemory(memory_db)
        self.persona = VeritasPersona(memory_system=self.memory)

    def ingest_text(self, text):
        """Add text to semantic memory."""
        return self.memory.ingest(text)

    def ask(self, prompt):
        """Return combined semantic recall, AIModel output, and persona reflection."""
        semantic_results = self.memory.search(prompt)
        ai_response = self.model.generate(prompt)
        reflection = self.persona.reflect(prompt)
        combined_response = (
            f"{reflection}\n"
            f"Semantic recall:\n{semantic_results}\n"
            f"AIModel response:\n{ai_response}"
        )
        return combined_response

    def act(self, prompt):
        """Generate persona-aligned action advice."""
        return self.persona.generate_action(prompt)
