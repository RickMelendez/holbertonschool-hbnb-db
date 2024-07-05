from src.models.base import Base
from src.persistence.repository import Repository
from src import db

class DBRepository(Repository):
    """Database repository implementation using SQLAlchemy"""

    def get_all(self, model_class: str) -> list:
        """Return all records of the given model class"""
        model_class = self._get_model_class(model_class)
        return model_class.query.all()

    def get(self, model_class: str, obj_id: str) -> Base | None:
        """Return a single record of the given model class by ID"""
        model_class = self._get_model_class(model_class)
        return model_class.query.get(obj_id)

    def reload(self) -> None:
        """Reload the database (if necessary)"""
        db.session.commit()

    def save(self, obj: Base) -> None:
        """Save a new record to the database"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> None:
        """Update an existing record in the database"""
        db.session.commit()

    def delete(self, obj: Base) -> bool:
        """Delete a record from the database"""
        db.session.delete(obj)
        db.session.commit()
        return True

    def _get_model_class(self, model_class: str):
        """Helper method to get the model class from the class name"""
        if model_class == "User":
            from src.models.user import User
            return User
        # Add other models here as needed
        raise ValueError(f"Model class '{model_class}' not found")
