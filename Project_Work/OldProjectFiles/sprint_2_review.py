"""
ASSIGNMENT 9B: SPRINT 2 – FUNCTIONAL STUBS
Project: Welcome Basket Brew Co. – Welcome Brew Menu
Developer: Julie Gavas
"""

# GLOBAL CONSTANTS (Pantry Rules)
PRICING_FILE = "pricing.txt"
ORDER_HISTORY = "order_history.txt"


def get_customer_info():
    """Asks for delivery location (apartment, condo unit, office, etc.)."""
    # TODO: Ask user for delivery location
    return "Apt 3B – Lakeside Residences"


def take_order():
    """Collects drink name, size, milk type, and syrup pumps."""
    # TODO: Ask user for drink selection, size, milk, and pumps
    pass


def calculate_total(order_data):
    """Calculates price based on size and number of flavor boosts."""
    # TODO: Load pricing tiers from pricing.txt and compute total
    return 2.20


def save_order(order_data, total):
    """Saves raw order data to file for computer memory."""
    # TODO: Append order to ORDER_HISTORY
    pass


def print_label(order_data, total):
    """Prints the human‑readable cup label for the barista."""
    # TODO: Format and print the cup label
    pass


def main():
    # 1. THE IDENTITY PHASE
    # Function returns a string (location). main() catches it in a variable.
    customer_location = get_customer_info() 

    # 2. THE COLLECTION PHASE
    # Function returns a collection of data (the order). main() catches it.
    # This is the "bucket" that holds size, milk, and pumps.
    current_order = take_order() 

    # 3. THE CALCULATION PHASE (The first handoff)
    # main() passes the "order bucket" TO the math processor.
    # The processor returns the calculated price back to main().
    final_price = calculate_total(current_order)

    # 4. THE PERSISTENCE & OUTPUT PHASE (The final handoff)
    # main() passes BOTH buckets to the final processors.
    # This ensures the computer remembers the order and the barista gets the label.
    save_order(current_order, final_price)
    print_label(current_order, final_price, customer_location)

main()