# sprint4.1.py
# -----------------------------------------------------------------------
# ASSIGNMENT 11B: SPRINT 4 - WRITING TO FILES
# Project: Welcome Basket Supply Co. – Welcome Kit System (V4.0)
# Developer: Julie Gavas
# -----------------------------------------------------------------------

import datetime

# -----------------------------
# GLOBAL CONSTANTS
# -----------------------------
ORDER_HISTORY = "kit_order_history.txt"

VALID_KIT_TYPES = ("New_Employee", "Office", "Pet", "Baby", "Birthday")
DEFAULT_KIT = "New_Employee"
DEFAULT_QUANTITY = 1
DEFAULT_PRICE = 15.00

# -----------------------------
# IDENTITY PHASE
# -----------------------------
def get_identity_info():
    """
    Collects customer and business identity details.
    """
    name = input("Contact Name: ").strip()
    business = input("Business Name: ").strip()
    address = input("Street Address: ").strip()
    unit = input("Unit / Suite Number: ").strip()
    city = input("City: ").strip()
    phone = input("Phone Number: ").strip()

    return {
        "name": name,
        "business": business,
        "address": address,
        "unit": unit,
        "city": city,
        "phone": phone
    }

# -----------------------------
# COLLECTION PHASE
# -----------------------------
def collect_kit_order():
    """
    Collects welcome kit type and quantity.
    Uses validation to prevent system crashes.
    """
    while True:
        print(f"Available Kit Types: {VALID_KIT_TYPES}")
        kit = input("Select Kit Type: ").title()

        if kit in VALID_KIT_TYPES:
            break
        else:
            print("Invalid kit type. Please try again.\n")

    qty_input = input("Quantity Requested: ")
    quantity = int(qty_input) if qty_input.isdigit() else DEFAULT_QUANTITY

    return {
        "kit": kit,
        "quantity": quantity
    }

# -----------------------------
# CALCULATION PHASE
# -----------------------------
def calculate_total(order_data):
    """
    Calculates total cost based on quantity.
    """
    return DEFAULT_PRICE * order_data["quantity"]

# -----------------------------
# PERSISTENCE PHASE
# -----------------------------
def save_order(identity, order_data, total):
    """
    Appends order data to file with timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ORDER_HISTORY, "a") as file:
        file.write(f"\n[{timestamp}]\n")

        identity_labels = ["Name", "Business", "Address", "Unit", "City", "Phone"]
        identity_values = identity.values()

        for label, value in zip(identity_labels, identity_values):
            file.write(f"{label}: {value}\n")

        for key, value in order_data.items():
            file.write(f"{key.title()}: {value}\n")

        file.write(f"Total: ${total:.2f}\n")
        file.write("--------------------------------------------------\n")

# -----------------------------
# OUTPUT PHASE
# -----------------------------
def print_packing_slip(identity, order_data, total):
    """
    Displays human-readable packing slip.
    """
    print("\n--- PACKING SLIP ---")
    print(f"Contact: {identity['name']}")
    print(f"Business: {identity['business']}")
    print(f"Address: {identity['address']} {identity['unit']}, {identity['city']}")
    print(f"Phone: {identity['phone']}")
    print(f"Kit Type: {order_data['kit']}")
    print(f"Quantity: {order_data['quantity']}")
    print(f"TOTAL: ${total:.2f}")
    print("--------------------\n")

# -----------------------------
# MAIN FUNCTION (SYSTEM CONDUCTOR)
# -----------------------------
def main():
    identity = get_identity_info()
    order = collect_kit_order()
    total = calculate_total(order)
    save_order(identity, order, total)
    print_packing_slip(identity, order, total)

main()

