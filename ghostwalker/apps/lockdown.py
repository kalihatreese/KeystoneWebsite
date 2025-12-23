import hashlib

def generate_deployment_key(user_id):
    # Creates a unique key based on User ID + GhostWalker Salt
    salt = "GHOST_WALKER_2025_SECRET"
    key = hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()[:16].upper()
    print(f"--- DEPLOYMENT KEY GENERATED ---")
    print(f"User: {user_id}")
    print(f"Key: {key}")
    return key

if __name__ == "__main__":
    generate_deployment_key("ReeseDroid_Admin")
