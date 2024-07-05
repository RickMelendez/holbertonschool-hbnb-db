"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""
from src import db
from src.models.base import Base
from src.persistence.repository import Repository
from sqlalchemy.orm import Session

class DBRepository(Repository):
    """Repository class for interacting with SQLAlchemy models."""

    def __init__(self, session: Session = None) -> None:
        """Initialize with an optional SQLAlchemy session."""
        self.session = session or db.session

    def get_all(self, model_name: str) -> list:
        """Retrieve all instances of a model."""
        model_class = getattr(Base, model_name)
        return self.session.query(model_class).all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Retrieve a single instance of a model by ID."""
        model_class = getattr(Base, model_name)
        return self.session.query(model_class).filter_by(id=obj_id).first()

    def save(self, obj: Base) -> None:
        """Save a new instance of a model."""
        self.session.add(obj)
        self.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an existing instance of a model."""
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Delete an instance of a model."""
        self.session.delete(obj)
        self.session.commit()
        return True

    def reload(self) -> None:
        """Optional method for reloading data."""
        pass

