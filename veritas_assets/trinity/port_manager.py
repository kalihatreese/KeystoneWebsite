#!/usr/bin/env python3
import socket, json, os, threading

REGISTRY_PATH = os.path.expanduser("~/Keystones-Trinity-Core/port_registry.json")
LOCK = threading.Lock()

def find_open_port(base_port=5500, max_attempts=50):
    for port in range(base_port, base_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No open ports available in range.")

def register_service(name, base_port=5500):
    with LOCK:
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r") as f:
                registry = json.load(f)
        else:
            registry = {}
        if name in registry and check_port_available(registry[name]):
            return registry[name]
        new_port = find_open_port(base_port)
        registry[name] = new_port
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
        print(f"[PORT] {name} registered on tcp://127.0.0.1:{new_port}")
        return new_port

def get_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def check_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0

if __name__ == "__main__":
    for s in ["Ledger", "CyberCop", "Mesh", "Ashleyana", "EventLogger"]:
        register_service(s)
    print(json.dumps(get_registry(), indent=2))
