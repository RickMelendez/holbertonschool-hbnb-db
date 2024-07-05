"""
Users controller module
"""

from flask import abort, request
from src.models.user import User

class User():

    def get_users():
        """Returns all users"""
        users: list[User] = User.get_all()
        return [user.to_dict() for user in users]


    def create_user():
        """Creates a new user"""
        data = request.get_json()

        try:
            user = User.create(data)
        except KeyError as e:
            abort(400, f"Missing field: {e}")
        except ValueError as e:
            abort(400, str(e))

        if user is None:
            abort(400, "User already exists")
        return user.to_dict(), 201


    def get_user_by_id(user_id: str):
        """Returns a user by ID"""
        user: User | None = User.get(user_id)

        if not user:
            abort(404, f"User with ID {user_id} not found")

        return user.to_dict(), 200


    def update_user(user_id: str):
        """Updates a user by ID"""
        data = request.get_json()

        try:
            user = User.update(user_id, data)
        except ValueError as e:
            abort(400, str(e))

        if user is None:
            abort(404, f"User with ID {user_id} not found")

        return user.to_dict(), 200


    def delete_user(user_id: str):
        """Deletes a user by ID"""
        if not User.delete(user_id):
            abort(404, f"User with ID {user_id} not found")

        return "", 204
    
