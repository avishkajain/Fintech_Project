def check_permission(role, action):
    permissions = {
        "admin": ["create", "read", "update", "delete"],
        "analyst": ["read"],
        "viewer": ["read"]
    }
    return action in permissions.get(role, [])

def apply_filters(data, category=None, type=None):
    if category:
        data = [d for d in data if d["category"] == category]
    if type:
        data = [d for d in data if d["type"] == type]
    return data