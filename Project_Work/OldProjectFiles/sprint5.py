#sprint5.py
"""
-----------------------------------------------------------------------
ASSIGNMENT 12B: SPRINT 5 - DATA PERSISTENCE
Project: Welcome Basket Supply Co. – Welcome Kit System (V5.0)
Developer: Julie Gavas
-----------------------------------------------------------------------

"""

import datetime


# --------------------------------------------------------------------
# GLOBAL CONSTANTS
# --------------------------------------------------------------------
CATALOG_FILE = "kit_catalog.txt"
DATA_FILE = "kit_order_history.csv"
HUMAN_REPORT = "packing_slip.txt"

DEFAULT_KIT = "New_Employee"
DEFAULT_QUANTITY = 1


# --------------------------------------------------------------------
# CONFIG LOADER (Configuration Blocker FIX)
# --------------------------------------------------------------------
def load_catalog():
    """Reads kit names and prices from kit_catalog.txt into a dictionary."""
    catalog = {}

    try:
        with open(CATALOG_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue

                parts = line.split(",")
                if len(parts) != 2:
                    continue

                kit_name = parts[0].strip()
                try:
                    kit_price = float(parts[1].strip())
                except ValueError:
                    continue

                catalog[kit_name] = kit_price

    except FileNotFoundError:
        print("ERROR: kit_catalog.txt not found.")
        print("Example line: New_Employee,15.00\n")
        return None

    return catalog


# --------------------------------------------------------------------
# IDENTITY PHASE
# --------------------------------------------------------------------
def get_identity_info():
    """Collects customer identity information."""
    return {
        "name": input("Contact Name: ").strip(),
        "business": input("Business Name: ").strip(),
        "address": input("Street Address: ").strip(),
        "unit": input("Unit / Suite Number (or blank): ").strip(),
        "city": input("City: ").strip(),
        "phone": input("Phone Number: ").strip()
    }


# --------------------------------------------------------------------
# COLLECTION PHASE (Missing Interaction FIX)
# --------------------------------------------------------------------
def collect_kit_order(catalog):
    """Collects kit selection and quantity using validation loops."""
    print("\n--- AVAILABLE KITS ---")
    for kit, price in catalog.items():
        print(f"{kit} - ${price:.2f}")

    # Kit selection trap
    while True:
        kit = input(f"\nSelect Kit (default {DEFAULT_KIT}): ").strip()
        if kit == "":
            kit = DEFAULT_KIT
        if kit in catalog:
            break
        print("Invalid kit. Please choose from the list.")

    # Quantity trap
    while True:
        qty_input = input(f"Quantity (default {DEFAULT_QUANTITY}): ").strip()
        if qty_input == "":
            quantity = DEFAULT_QUANTITY
            break
        try:
            quantity = int(qty_input)
            if quantity < 1:
                print("Quantity must be 1 or more.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")

    return {
        "kit": kit,
        "quantity": quantity,
        "unit_price": catalog[kit]
    }


# --------------------------------------------------------------------
# CALCULATION PHASE
# --------------------------------------------------------------------
def calculate_total(order):
    """Calculates total cost."""
    return order["unit_price"] * order["quantity"]


# --------------------------------------------------------------------
# PERSISTENCE PHASE (Silent Vault FIX)
# --------------------------------------------------------------------
def save_files(identity, order, total):
    """Implements the Two-File Pattern."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Computer Log (append)
        with open(DATA_FILE, "a") as file:
            file.write(
                f"{timestamp},{identity['name']},{identity['business']},"
                f"{identity['address']},{identity['unit']},{identity['city']},"
                f"{identity['phone']},{order['kit']},{order['quantity']},"
                f"{order['unit_price']:.2f},{total:.2f}\n"
            )

        # Human Report (overwrite)
        with open(HUMAN_REPORT, "w") as file:
            file.write("WELCOME BASKET SUPPLY CO.\n")
            file.write("PACKING SLIP\n")
            file.write(f"DATE: {timestamp}\n")
            file.write("--------------------------------\n")
            file.write(f"CONTACT: {identity['name']}\n")
            file.write(f"BUSINESS: {identity['business']}\n")
            file.write(f"ADDRESS: {identity['address']} {identity['unit']}, {identity['city']}\n")
            file.write(f"PHONE: {identity['phone']}\n")
            file.write("--------------------------------\n")
            file.write(f"KIT: {order['kit']}\n")
            file.write(f"QTY: {order['quantity']}\n")
            file.write(f"UNIT PRICE: ${order['unit_price']:.2f}\n")
            file.write(f"TOTAL: ${total:.2f}\n")

        print("\nFiles saved successfully.\n")

    except Exception as e:
        print(f"System Error during save: {e}")


# --------------------------------------------------------------------
# REVIEW LOGIC (Persistence Loop FIX)
# --------------------------------------------------------------------
def review_history():
    """Displays saved orders using enumerate()."""
    rows = []

    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 11:
                    continue
                rows.append(parts)

    except FileNotFoundError:
        print("\nNo order history found.\n")
        return []

    print("\n--- ORDER HISTORY ---")
    for idx, r in enumerate(rows):
        print(f"[{idx}] {r[1]} | {r[7]} x{r[8]} | ${r[10]}")

    return rows


# --------------------------------------------------------------------
# GREAT REWRITE (Read-Modify-Overwrite)
# --------------------------------------------------------------------
def edit_order():
    rows = review_history()
    if not rows:
        return

    try:
        idx = int(input("Select order ID to edit: "))
        if idx < 0 or idx >= len(rows):
            print("Invalid ID.")
            return
    except ValueError:
        print("Invalid input.")
        return

    new_qty = int(input("Enter new quantity: "))
    rows[idx][8] = str(new_qty)
    unit_price = float(rows[idx][9])
    rows[idx][10] = f"{unit_price * new_qty:.2f}"

    try:
        with open(DATA_FILE, "w") as file:
            for r in rows:
                file.write(",".join(r) + "\n")
        print("Order updated successfully.\n")
    except Exception as e:
        print(f"Rewrite error: {e}")


# --------------------------------------------------------------------
# MAIN (Silent Conductor FIX)
# --------------------------------------------------------------------
def main():
    catalog = load_catalog()
    if not catalog:
        return

    identity = get_identity_info()
    order = collect_kit_order(catalog)
    total = calculate_total(order)
    save_files(identity, order, total)

    review_history()
    edit_choice = input("Edit an order? (y/n): ").lower()
    if edit_choice == "y":
        edit_order()


main()