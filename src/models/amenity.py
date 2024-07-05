from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Amenity(db.Model):
    """Amenity representation"""

    __tablename__ = 'amenity'

    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name: str, **kwargs) -> None:
        """Initialize an Amenity"""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self) -> str:
        """String representation of the Amenity"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        new_amenity = Amenity(name=data["name"])

        db.session.add(new_amenity)
        db.session.commit()

        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity = Amenity.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        db.session.commit()

        return amenity

class PlaceAmenity(db.Model):
    """PlaceAmenity representation"""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = db.Column(UUID(as_uuid=True), db.ForeignKey('place.id'), nullable=False)
    amenity_id = db.Column(UUID(as_uuid=True), db.ForeignKey('amenity.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    place = db.relationship("Place", backref=db.backref("place_amenities", lazy=True))
    amenity = db.relationship("Amenity", backref=db.backref("place_amenities", lazy=True))

    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        """Initialize a PlaceAmenity"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """String representation of the PlaceAmenity"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        return PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(place_id=data["place_id"], amenity_id=data["amenity_id"])

        db.session.add(new_place_amenity)
        db.session.commit()

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        db.session.delete(place_amenity)
        db.session.commit()

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError("This method is defined only because of the Base class")