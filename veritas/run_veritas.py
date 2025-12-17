from core.memory_shaper import SemanticMemory, search_memory

memory = SemanticMemory()

# Optionally ingest your semantic knowledge file
try:
    memory.ingest("/data/data/com.termux/files/home/shadowx_installed/core/semantic_knowledge.txt")
except FileNotFoundError:
    print("No semantic knowledge file found. Starting empty.")

print("=== ASK ===")
while True:
    try:
        user_input = input("\nYou: ")
        if not user_input.strip():
            continue
        results = search_memory(user_input, memory)
        if results:
            print("\n[Memory Recall]:", results)
        else:
            print("\n[Memory Recall]: Semantic memory unavailable.")
        print("\n[Veritas Reflection | Traits: intellect, instinct, ethics, focus, strategy]")
        print("Insight: Trust patterns, verify context, act with purpose.")
    except KeyboardInterrupt:
        print("\nExiting Veritas...")
        break
