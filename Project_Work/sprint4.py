
# -----------------------------------------------------------------------
# ASSIGNMENT 10B: SPRINT 3 - REFACTORING & DATA ACCOUNTABILITY
# Project: Welcome Basket Supply Co. – Welcome Kit System (V3.0)
# Developer: Julie Gavas
# -----------------------------------------------------------------------

# -----------------------------
# GLOBAL CONSTANTS (Business Rules)
# -----------------------------
PRICING_FILE = "kit_pricing.txt"
ORDER_HISTORY = "kit_order_history.txt"

VALID_KIT_TYPES = ("New_Employee", "New Doctor", "Pet", "Baby", "Birthday")
DEFAULT_KIT = "New_Employee"
DEFAULT_QUANTITY = 1
DEFAULT_PRICE = 15.00

# -----------------------------
# IDENTITY PHASE
# -----------------------------
def get_identity_info():
    """
    Collects customer and business identity information.
    Returns a dictionary of identity details.
    """

    name = input("Contact Name: ").strip()
    business = input("Business Name: ").strip()
    address = input("Business Address (Street): ").strip()
    unit = input("Unit / Suite Number: ").strip()
    city = input("City: ").strip()
    phone = input("Phone Number: ").strip()

    identity = {
        "name": name,
        "business": business,
        "address": address,
        "unit": unit,
        "city": city,
        "phone": phone
    }

    return identity

# -----------------------------
# COLLECTION PHASE
# -----------------------------
def collect_kit_order(
    default_kit=DEFAULT_KIT,
    default_quantity=DEFAULT_QUANTITY
):
    """
    Collects welcome kit type and quantity.
    Applies validation and defaults to prevent crashes.
    """
    print(f"Available Kit Types: {VALID_KIT_TYPES}")

    kit = input("Select Kit Type: ").title()
    if kit not in VALID_KIT_TYPES:
        kit = default_kit

    qty_input = input("Quantity Requested: ")
    quantity = int(qty_input) if qty_input.isdigit() else default_quantity

    return {
        "kit": kit,
        "quantity": quantity
    }

# -----------------------------
# CALCULATION PHASE
# -----------------------------
def calculate_total(order_data, base_price=DEFAULT_PRICE):
    """
    Calculates total cost based on kit quantity.
    Uses default pricing if pricing file is unavailable.
    """
    return base_price * order_data["quantity"]

# -----------------------------
# PERSISTENCE PHASE
# -----------------------------
def save_order(identity, order_data, total, filename=ORDER_HISTORY):
    """
    Writes order data to file for persistent system memory.
    """
    with open(filename, "a") as file:
        file.write(
            f"{identity} | {order_data} | Total: ${total:.2f}\n"
        )

# -----------------------------
# OUTPUT PHASE
# -----------------------------
def print_packing_slip(identity, order_data, total):
    """
    Outputs a human-readable packing slip for fulfillment staff.
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
    # 1. Identity Phase
    identity = get_identity_info()

    # 2. Collection Phase
    current_order = collect_kit_order()

    # 3. Calculation Phase
    final_price = calculate_total(order_data=current_order)

    # 4. Persistence & Output Phase
    save_order(identity=identity, order_data=current_order, total=final_price)
    print_packing_slip(
        identity=identity,
        order_data=current_order,
        total=final_price
    )

main()
