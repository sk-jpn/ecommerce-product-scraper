from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class Product:
    """Store-independent product data."""

    name: str
    price: Decimal
    url: str
    sku: str | None = None
    image_url: str | None = None
    description: str | None = None
