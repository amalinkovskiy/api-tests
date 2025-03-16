import json

DB_FILE = "users.json"

def clear_users():
    with open(DB_FILE, "w") as f:
        json.dump([], f, indent=4)
    print("All users have been removed from the collection.")

if __name__ == "__main__":
    clear_users()