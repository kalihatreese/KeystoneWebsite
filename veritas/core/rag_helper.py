#!/usr/bin/env python3
"""
core/rag_helper.py
Simple Retrieval-Augmented-Generation helper that queries the
chunk store (core/reese_chunks.json) and returns a short context
string to prepend to prompts or feed into your model.
"""
import json
import os

CHUNKS_FILE = "core/reese_chunks.json"

def get_rag_context(query: str, top_k: int = 3) -> str:
    """
    Return a short context string built from the top_k chunks matching query.
    Uses the existing simple semantic_search scoring in memory_shaper (same logic).
    """
    if not os.path.exists(CHUNKS_FILE):
        return ""
    try:
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception:
        return ""
    q = query.lower().strip()
    scored = []
    q_tokens = set([w for w in q.split() if len(w) > 2])
    for c in chunks:
        text_low = c.get("text","").lower()
        score = 0
        if q in text_low:
            score += 100
        c_tokens = set([w for w in text_low.split() if len(w) > 2])
        overlap = q_tokens.intersection(c_tokens)
        score += len(overlap)
        if score > 0:
            scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for s,c in scored[:top_k]]
    # Build short context: join excerpts (trim to safe length)
    pieces = []
    for c in top:
        excerpt = c.get("text","").strip().replace("\n"," ")
        if len(excerpt) > 600:
            excerpt = excerpt[:600] + "..."
        pieces.append(f"Source: {c.get('source')} | Excerpt: {excerpt}")
    return "\n\n".join(pieces)
