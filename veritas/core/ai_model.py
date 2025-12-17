"""
core/ai_model.py — main AIModel implementation for Veritas / Trinity integration.
Includes:
- Basic generate()
- Memory placeholder
- Semantic knowledge access hooks
"""

import os
import sqlite3

class AIModel:
    def __init__(self, memory_db_path='core/memory.db', semantic_index_path='core/semantic_knowledge.txt'):
        self.memory_db_path = memory_db_path
        self.semantic_index_path = semantic_index_path
        self.memory = self._load_memory()
        self.semantic_chunks = self._load_semantic_chunks()

    def _load_memory(self):
        if not os.path.exists(self.memory_db_path):
            return {}
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS memory(key TEXT PRIMARY KEY, value TEXT)")
            cursor.execute("SELECT key, value FROM memory")
            data = dict(cursor.fetchall())
            conn.close()
            return data
        except Exception as e:
            print(f"ERROR loading memory: {e}")
            return {}

    def save_memory(self):
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS memory(key TEXT PRIMARY KEY, value TEXT)")
            for k, v in self.memory.items():
                cursor.execute("INSERT OR REPLACE INTO memory(key, value) VALUES (?, ?)", (k, v))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"ERROR saving memory: {e}")

    def _load_semantic_chunks(self):
        if not os.path.exists(self.semantic_index_path):
            return []
        try:
            with open(self.semantic_index_path, 'r', encoding='utf-8') as f:
                data = f.read()
            # Simple chunking by double newlines
            chunks = [chunk.strip() for chunk in data.split('\n\n') if chunk.strip()]
            return chunks
        except Exception as e:
            print(f"ERROR loading semantic chunks: {e}")
            return []

    def generate(self, prompt):
        """
        Basic response function.
        Can be expanded to include retrieval-augmented generation (RAG) from semantic_chunks.
        """
        # Memory hook example
        if prompt in self.memory:
            return f"Memory recall: {self.memory[prompt]}"

        # Semantic search hook (naive keyword match for now)
        relevant = [chunk for chunk in self.semantic_chunks if prompt.lower() in chunk.lower()]
        if relevant:
            response = f"Semantic recall:\n{relevant[0]}"
        else:
            response = f"AIModel received: {prompt}"

        # Optionally store prompt/response in memory
        self.memory[prompt] = response
        self.save_memory()
        return response

