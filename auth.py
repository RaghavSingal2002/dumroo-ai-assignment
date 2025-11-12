# This file simulates a user authentication system.
# In a real app, this would come from a database query based on a logged-in user.

MOCK_USERS = {
    "Ms. Davis (Grade 8 Admin)": {
        "user_id": "u001",
        "role": "admin",
        "scope_type": "grade",
        "scope_value": 8
    },
    "Mr. Chen (Grade 9 Admin)": {
        "user_id": "u002",
        "role": "admin",
        "scope_type": "grade",
        "scope_value": 9
    },
    "Mrs. Iqbal (North Region)": {
        "user_id": "u003",
        "role": "admin",
        "scope_type": "region",
        "scope_value": "North"
    },
    "Mr. Frank (Grade 10 Admin)": {
        "user_id": "u004",
        "role": "admin",
        "scope_type": "grade",
        "scope_value": 10
    }
}

def get_user_details(user_name):
    """Fetches the details for a simulated user."""
    return MOCK_USERS.get(user_name)

def get_available_users():
    """Returns a list of all available mock users for the login dropdown."""
    return list(MOCK_USERS.keys())