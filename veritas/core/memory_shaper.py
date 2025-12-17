class SemanticMemory:
    def __init__(self):
        self.chunks = []

    def ingest(self, filepath):
        with open(filepath, "r") as f:
            data = f.read()
        new_chunks = data.split("\n")
        self.chunks.extend(new_chunks)
        return len(new_chunks)

def search_memory(query, memory_instance):
    results = [chunk for chunk in memory_instance.chunks if query.lower() in chunk.lower()]
    return results
