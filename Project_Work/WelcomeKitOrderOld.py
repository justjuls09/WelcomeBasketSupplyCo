""" 
Sprint 6 (13B)  Modular OOP Refactor of Sprint 5
Project: Welcome Basket Supply Co.  Welcome Kit System

This file is the "Blueprint" (Class Definition) required for Sprint 6.
- Encapsulation: private attributes using double underscores
- Modular Setters: individual setter methods for granular updates
- Display Logic: display_order() prints a numbered list for future editing

Use with: sprint6.py (main program)
"""

class WelcomeKitOrder:
    """One welcome-kit order (identity + kit selection) stored as an object."""

    def __init__(self):
        # --- Private Identity Attributes ---
        self.__contact_name = ""
        self.__business_name = ""
        self.__address = ""
        self.__unit = ""
        self.__city = ""
        self.__phone = ""

        # --- Private Order Attributes ---
        self.__kit_name = ""
        self.__unit_price = 0.0
        self.__quantity = 1

    # --------------------
    # Getters
    # --------------------
    def get_contact_name(self):
        return self.__contact_name

    def get_business_name(self):
        return self.__business_name

    def get_address(self):
        return self.__address

    def get_unit(self):
        return self.__unit

    def get_city(self):
        return self.__city

    def get_phone(self):
        return self.__phone

    def get_kit_name(self):
        return self.__kit_name

    def get_unit_price(self):
        return self.__unit_price

    def get_quantity(self):
        return self.__quantity

    # --------------------
    # Specialized Setters (Sprint 6)
    # --------------------
    def set_contact_name(self, value):
        if isinstance(value, str) and value.strip():
            self.__contact_name = value.strip()

    def set_business_name(self, value):
        if isinstance(value, str) and value.strip():
            self.__business_name = value.strip()

    def set_address(self, value):
        if isinstance(value, str) and value.strip():
            self.__address = value.strip()

    def set_unit(self, value):
        # unit can be blank
        if isinstance(value, str):
            self.__unit = value.strip()

    def set_city(self, value):
        if isinstance(value, str) and value.strip():
            self.__city = value.strip()

    def set_phone(self, value):
        if isinstance(value, str) and value.strip():
            self.__phone = value.strip()

    def set_kit_name(self, value):
        if isinstance(value, str) and value.strip():
            self.__kit_name = value.strip()

    def set_unit_price(self, value):
        try:
            price = float(value)
            if price >= 0:
                self.__unit_price = price
        except (TypeError, ValueError):
            pass

    def set_quantity(self, value):
        try:
            qty = int(value)
            if qty > 0:
                self.__quantity = qty
        except (TypeError, ValueError):
            pass

    # --------------------
    # Display
    # --------------------
    def calculate_total(self):
        return self.__unit_price * self.__quantity

    def display_order(self):
        """Numbered output."""
        lines = [
            f"Contact Name: {self.__contact_name}",
            f"Business Name: {self.__business_name}",
            f"Address: {self.__address}",
            f"Unit/Suite: {self.__unit}",
            f"City: {self.__city}",
            f"Phone: {self.__phone}",
            f"Kit: {self.__kit_name}",
            f"Unit Price: ${self.__unit_price:.2f}",
            f"Quantity: {self.__quantity}",
            f"Total: ${self.calculate_total():.2f}",
        ]
        print("\n--- ORDER DETAILS (Numbered) ---")
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line}")

    def __str__(self):
        return (
            f"{self.__contact_name} | {self.__business_name} | "
            f"{self.__quantity} x {self.__kit_name} @ ${self.__unit_price:.2f} "
            f"= ${self.calculate_total():.2f}"
        )

    # --------------------
    # Factory helpers (optional)
    # --------------------
    @classmethod
    def from_input(cls, catalog):
        """Create an order object by prompting the user."""
        order = cls()

        # Identity
        order.set_contact_name(input("Contact Name: "))
        order.set_business_name(input("Business Name: "))
        order.set_address(input("Street Address: "))
        order.set_unit(input("Unit / Suite Number (or blank): "))
        order.set_city(input("City: "))
        order.set_phone(input("Phone Number: "))

        # Order selection
        print("\n--- AVAILABLE KITS ---")
        for kit, price in catalog.items():
            print(f"- {kit}: ${price:.2f}")

        kit_choice = input("\nEnter kit name exactly as shown: ").strip()
        while kit_choice not in catalog:
            print("❌ Invalid kit. Please choose from the catalog.")
            kit_choice = input("Enter kit name: ").strip()

        qty_raw = input("Quantity: ").strip()
        while not qty_raw.isdigit() or int(qty_raw) <= 0:
            qty_raw = input("Quantity must be a positive whole number. Try again: ").strip()

        order.set_kit_name(kit_choice)
        order.set_unit_price(catalog[kit_choice])
        order.set_quantity(int(qty_raw))

        return order
