#sprint 3
"""
-----------------------------------------------------------------------
ASSIGNMENT 10B: SPRINT 3 - REFACTORING & DATA ACCOUNTABILITY
Project: Welcome Basket Brew Co. – Welcome Brew Menu (V3.0)
Developer: Julie Gavas
-----------------------------------------------------------------------
"""

# -----------------------------
# GLOBAL CONSTANTS (Pantry Rules)
# -----------------------------
PRICING_FILE = "pricing.txt"
ORDER_HISTORY = "order_history.txt"

# Business Rules
VALID_SIZES = ("Small", "Medium", "Large")
VALID_MILKS = ("Dairy", "Oat", "Almond", "Soy", "Coconut")
DEFAULT_PRICE = 2.20   # fallback if pricing file missing
DEFAULT_PUMPS = 0       # fallback for missing data


# -----------------------------
# IDENTITY PHASE
# -----------------------------
def get_customer_info(default_location="Unknown Location"):
    """
    Asks for delivery location (apartment, condo unit, office, etc.).
    Default ensures system never crashes if user leaves it blank.
    """
    location = input("Delivery Location: ").strip()
    return location or default_location


# -----------------------------
# COLLECTION PHASE
# -----------------------------
def take_order(
    default_drink="House Brew",
    default_size="Medium",
    default_milk="Dairy",
    default_pumps=DEFAULT_PUMPS
):
    """
    Collects drink name, size, milk type, and syrup pumps.
    Uses defaults to prevent system crashes.
    """

    drink = input("Drink Name: ").title() or default_drink

    size = input("Size (Small/Medium/Large): ").title()
    if size not in VALID_SIZES:
        size = default_size

    print(f"Available Milks: {VALID_MILKS}")
    milk = input("Milk Choice: ").title()
    if milk not in VALID_MILKS:
        milk = default_milk

    pumps_input = input("Flavor Boost Pumps: ")
    pumps = int(pumps_input) if pumps_input.isdigit() else default_pumps

    return {
        "drink": drink,
        "size": size,
        "milk": milk,
        "pumps": pumps
    }


# -----------------------------
# CALCULATION PHASE
# -----------------------------
def calculate_total(order_data, base_price=DEFAULT_PRICE):
    """
    Calculates price based on size and number of flavor boosts.
    Uses default base price if pricing file is missing.
    """
    syrup_cost = order_data["pumps"] * 0.10
    return base_price + syrup_cost


# -----------------------------
# PERSISTENCE PHASE
# -----------------------------
def save_order(order_data, total, filename=ORDER_HISTORY):
    """
    Saves raw order data to file for computer memory.
    Uses ORDER_HISTORY constant for file name.
    """
    with open(filename, "a") as file:
        file.write(f"{order_data} | Total: {total:.2f}\n")


# -----------------------------
# OUTPUT PHASE
# -----------------------------
def print_label(order_data, total, location="Unknown"):
    """
    Prints the human‑readable cup label for the barista.
    Default location ensures resilience.
    """
    print("\n--- BARISTA LABEL ---")
    print(f"Deliver To: {location}")
    print(f"Drink: {order_data['drink']}")
    print(f"Size: {order_data['size']}")
    print(f"Milk: {order_data['milk']}")
    print(f"Pumps: {order_data['pumps']}")
    print(f"TOTAL: ${total:.2f}")
    print("----------------------\n")


# -----------------------------
# MAIN FUNCTION (THE CONDUCTOR)
# -----------------------------
def main():
    # 1. Identity Phase
    customer_location = get_customer_info()

    # 2. Collection Phase
    current_order = take_order()

    # 3. Calculation Phase
    final_price = calculate_total(order_data=current_order)

    # 4. Persistence & Output Phase
    save_order(order_data=current_order, total=final_price)
    print_label(order_data=current_order, total=final_price, location=customer_location)


# -----------------------------
# CALL MAIN
# -----------------------------
main()