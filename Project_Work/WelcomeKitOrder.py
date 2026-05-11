"""
Welcome Basket Supply Co. — OOP Blueprint

[x] 1. Streamlit Migration: Logic is successfully ported to a web UI.
[x] 2. UI/UX Design: Layout is organized, intuitive, and easy to navigate.
[x] 3. GitHub Integration: Full source code is pushed to a public repo.
[x] 4. Live Deployment: The app is accessible via a Streamlit Cloud URL.
[x] 5. System Resilience: UI elements handle invalid inputs gracefully.
[x] 6. OOP Backend: The app still uses Classes/Objects to manage data.
[x] 7. Data Persistence: System reads/writes to a .txt or .csv file.

Deployment-ready WelcomeKitOrder class:
- Encapsulation via private attributes
- Getter/Setter methods for granular updates
- Business logic: calculate_total()
- Persistence helpers: to_row(), from_dict()
"""

from __future__ import annotations


class WelcomeKitOrder:
    """One welcome-kit order stored as an object."""

    def __init__(
        self,
        contact_name: str = "",
        business_name: str = "",
        address: str = "",
        unit: str = "",
        city: str = "",
        phone: str = "",
        kit_name: str = "",
        unit_price: float = 0.0,
        quantity: int = 1,
        timestamp: str = "",
    ) -> None:
        self.__timestamp = str(timestamp)
        self.__contact_name = str(contact_name)
        self.__business_name = str(business_name)
        self.__address = str(address)
        self.__unit = str(unit)
        self.__city = str(city)
        self.__phone = str(phone)
        self.__kit_name = str(kit_name)
        self.__unit_price = float(unit_price)
        self.__quantity = int(quantity) if int(quantity) > 0 else 1

    # -----------------
    # Getters
    # -----------------
    def get_timestamp(self) -> str:
        return self.__timestamp

    def get_contact_name(self) -> str:
        return self.__contact_name

    def get_business_name(self) -> str:
        return self.__business_name

    def get_address(self) -> str:
        return self.__address

    def get_unit(self) -> str:
        return self.__unit

    def get_city(self) -> str:
        return self.__city

    def get_phone(self) -> str:
        return self.__phone

    def get_kit_name(self) -> str:
        return self.__kit_name

    def get_unit_price(self) -> float:
        return self.__unit_price

    def get_quantity(self) -> int:
        return self.__quantity

    # -----------------
    # Setters
    # -----------------
    def set_timestamp(self, value: str) -> None:
        self.__timestamp = str(value).strip()

    def set_contact_name(self, value: str) -> None:
        self.__contact_name = str(value).strip()

    def set_business_name(self, value: str) -> None:
        self.__business_name = str(value).strip()

    def set_address(self, value: str) -> None:
        self.__address = str(value).strip()

    def set_unit(self, value: str) -> None:
        self.__unit = str(value).strip()

    def set_city(self, value: str) -> None:
        self.__city = str(value).strip()

    def set_phone(self, value: str) -> None:
        self.__phone = str(value).strip()

    def set_kit_name(self, value: str) -> None:
        self.__kit_name = str(value).strip()

    def set_unit_price(self, value: float) -> None:
        self.__unit_price = float(value)

    def set_quantity(self, value: int) -> None:
        value = int(value)
        self.__quantity = value if value > 0 else 1

    # -----------------
    # Business Logic
    # -----------------
    def calculate_total(self) -> float:
        return float(self.__unit_price) * int(self.__quantity)

    # -----------------
    # Persistence Helpers
    # -----------------
    def to_row(self) -> list:
        """CSV row aligned to app.py header."""
        return [
            self.__timestamp,
            self.__contact_name,
            self.__business_name,
            self.__address,
            self.__unit,
            self.__city,
            self.__phone,
            self.__kit_name,
            f"{self.__unit_price:.2f}",
            self.__quantity,
            f"{self.calculate_total():.2f}",
        ]

    @staticmethod
    def from_dict(row: dict) -> "WelcomeKitOrder":
        """
        Create object from a DictReader row.
        Expected keys (from app.py history header):
        timestamp, contact, business, address, unit, city, phone, kit, unit_price, quantity, total
        """
        return WelcomeKitOrder(
            timestamp=str(row.get("timestamp", "")).strip(),
            contact_name=str(row.get("contact", "")).strip(),
            business_name=str(row.get("business", "")).strip(),
            address=str(row.get("address", "")).strip(),
            unit=str(row.get("unit", "")).strip(),
            city=str(row.get("city", "")).strip(),
            phone=str(row.get("phone", "")).strip(),
            kit_name=str(row.get("kit", "")).strip(),
            unit_price=float(row.get("unit_price", 0) or 0),
            quantity=int(float(row.get("quantity", 1) or 1)),
        )

    def __str__(self) -> str:
        return (
            f"{self.__contact_name} | {self.__business_name} | "
            f"{self.__quantity} x {self.__kit_name} @ ${self.__unit_price:.2f} "
            f"= ${self.calculate_total():.2f}"
        )
