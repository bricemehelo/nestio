from decimal import Decimal

from app.database import SessionLocal
from app.models.property import Property


PROPERTIES = [
    {
        "title": "Modern 3 Bedroom Apartment in Lekki Phase 1",
        "description": "Beautifully finished three-bedroom apartment with modern fittings, spacious living room and dedicated parking.",
        "price": Decimal("85000000.00"),
        "address": "12 Admiralty Way, Lekki Phase 1",
        "city": "Lagos",
        "latitude": 6.4474,
        "longitude": 3.4722,
        "property_type": "apartment",
        "status": "for_sale",
        "source": "manual",
        "verified": True,
        "verification_count": 4,
        "outdated_count": 0,
    },
    {
        "title": "Luxury 4 Bedroom Duplex in Ikoyi",
        "description": "Spacious luxury duplex in a secure residential neighbourhood close to major business and leisure destinations.",
        "price": Decimal("180000000.00"),
        "address": "8 Bourdillon Road, Ikoyi",
        "city": "Lagos",
        "latitude": 6.4549,
        "longitude": 3.4316,
        "property_type": "house",
        "status": "for_sale",
        "source": "manual",
        "verified": True,
        "verification_count": 7,
        "outdated_count": 0,
    },
    {
        "title": "2 Bedroom Apartment for Rent in Yaba",
        "description": "Affordable two-bedroom apartment suitable for young professionals and small families.",
        "price": Decimal("3500000.00"),
        "address": "15 Herbert Macaulay Way, Yaba",
        "city": "Lagos",
        "latitude": 6.5095,
        "longitude": 3.3782,
        "property_type": "apartment",
        "status": "for_rent",
        "source": "manual",
        "verified": True,
        "verification_count": 3,
        "outdated_count": 0,
    },
    {
        "title": "Residential Land in Ajah",
        "description": "Serviced residential land suitable for building a family home or investment property.",
        "price": Decimal("45000000.00"),
        "address": "Sangotedo, Ajah",
        "city": "Lagos",
        "latitude": 6.4698,
        "longitude": 3.6157,
        "property_type": "land",
        "status": "for_sale",
        "source": "agent",
        "verified": False,
        "verification_count": 0,
        "outdated_count": 0,
    },
    {
        "title": "3 Bedroom Terrace Duplex in Wuse 2",
        "description": "Well-maintained terrace duplex in one of Abuja's established residential districts.",
        "price": Decimal("95000000.00"),
        "address": "24 Aminu Kano Crescent, Wuse 2",
        "city": "Abuja",
        "latitude": 9.0765,
        "longitude": 7.4898,
        "property_type": "house",
        "status": "for_sale",
        "source": "manual",
        "verified": True,
        "verification_count": 5,
        "outdated_count": 0,
    },
    {
        "title": "Luxury 2 Bedroom Apartment in Maitama",
        "description": "Premium two-bedroom apartment with modern finishes, security and dedicated parking.",
        "price": Decimal("6500000.00"),
        "address": "15 Agadez Street, Maitama",
        "city": "Abuja",
        "latitude": 9.0836,
        "longitude": 7.5019,
        "property_type": "apartment",
        "status": "for_rent",
        "source": "agent",
        "verified": True,
        "verification_count": 6,
        "outdated_count": 0,
    },
    {
        "title": "Commercial Property in Garki",
        "description": "Commercial building suitable for offices, retail operations or professional services.",
        "price": Decimal("120000000.00"),
        "address": "12 Garki Area 11",
        "city": "Abuja",
        "latitude": 9.0227,
        "longitude": 7.4856,
        "property_type": "commercial",
        "status": "for_sale",
        "source": "web_search",
        "verified": False,
        "verification_count": 1,
        "outdated_count": 0,
    },
    {
        "title": "4 Bedroom Detached House in GRA",
        "description": "Spacious detached family home in a quiet and secure part of Port Harcourt GRA.",
        "price": Decimal("110000000.00"),
        "address": "21 Forces Avenue, Old GRA",
        "city": "Port Harcourt",
        "latitude": 4.8156,
        "longitude": 7.0498,
        "property_type": "house",
        "status": "for_sale",
        "source": "manual",
        "verified": True,
        "verification_count": 8,
        "outdated_count": 0,
    },
    {
        "title": "3 Bedroom Apartment in New GRA",
        "description": "Comfortable three-bedroom apartment in a well-developed residential area.",
        "price": Decimal("4500000.00"),
        "address": "14 Stadium Road, New GRA",
        "city": "Port Harcourt",
        "latitude": 4.8242,
        "longitude": 7.0125,
        "property_type": "apartment",
        "status": "for_rent",
        "source": "manual",
        "verified": True,
        "verification_count": 2,
        "outdated_count": 0,
    },
    {
        "title": "Residential Land in Rumuodara",
        "description": "Residential plot suitable for a family home or small residential development.",
        "price": Decimal("18000000.00"),
        "address": "Rumuodara, Port Harcourt",
        "city": "Port Harcourt",
        "latitude": 4.8711,
        "longitude": 7.0023,
        "property_type": "land",
        "status": "for_sale",
        "source": "agent",
        "verified": False,
        "verification_count": 0,
        "outdated_count": 0,
    },
]


def seed():
    db = SessionLocal()

    try:
        existing_count = db.query(Property).count()

        if existing_count > 0:
            print(
                f"Database already contains {existing_count} properties. "
                "Skipping seed."
            )
            return

        properties = [
            Property(**property_data)
            for property_data in PROPERTIES
        ]

        db.add_all(properties)
        db.commit()

        print(f"Successfully seeded {len(properties)} properties.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()