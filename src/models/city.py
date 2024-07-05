from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class City(db.Model):
    """City representation"""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(3), db.ForeignKey('country.code'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    country = db.relationship("Country", backref=db.backref("cities", lazy=True))

    def __init__(self, name: str, country_code: str, **kwargs) -> None:
        """Initialize a City"""
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """String representation of the City"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.query.filter_by(code=data["country_code"]).first()

        if not country:
            raise ValueError("Country not found")

        new_city = City(name=data["name"], country_code=data["country_code"])

        db.session.add(new_city)
        db.session.commit()

        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.query.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        db.session.commit()

        return city
