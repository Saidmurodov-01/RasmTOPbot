import json

def log_user(user_id):
    try:
        with open("data/user_log.json", "r") as f:
            users = json.load(f)
    except:
        users = []
    if user_id not in users:
        users.append(user_id)
        with open("data/user_log.json", "w") as f:
            json.dump(users, f)
