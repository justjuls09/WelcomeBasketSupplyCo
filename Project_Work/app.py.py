import csv
import io
import os
from datetime import datetime

import streamlit as st
from WelcomeKitOrder import WelcomeKitOrder


# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Welcome Basket Supply Co.",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATALOG_FILE = "kit_catalog.txt"
DATA_FILE = "kit_order_history.csv"


# -----------------------------
# Data Loaders / Persistence
# -----------------------------
@st.cache_data
def load_catalog(path: str = CATALOG_FILE) -> dict:
    """
    Robust loader for kit_catalog.txt.
    Supports:
      - one-per-line:  Kit,12.00\nKit2,15.00
      - one-line tokens separated by spaces
    """
    catalog = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        tokens = [t for t in raw.replace("\n", " ").split(" ") if t.strip()]
        for token in tokens:
            if "," not in token:
                continue
            kit, price = token.split(",", 1)
            kit = kit.strip()
            price = float(price.strip())
            catalog[kit] = price

    except FileNotFoundError:
        # Fallback prevents “red screen” if file missing
        catalog = {
            "New_Employee": 15.00,
            "VIP": 25.00,
            "Remote_Worker": 20.00,
            "Office": 18.00,
            "Pet": 12.00,
            "Baby": 16.00,
            "Birthday": 17.00,
        }
    except Exception:
        # Any parsing issues -> fallback
        catalog = {
            "New_Employee": 15.00,
            "VIP": 25.00,
            "Remote_Worker": 20.00,
        }

    return catalog


def ensure_history_file(path: str = DATA_FILE) -> None:
    """Create CSV with header if it doesn't exist."""
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "contact",
                "business",
                "address",
                "unit",
                "city",
                "phone",
                "kit",
                "unit_price",
                "quantity",
                "total",
            ])


def load_order_history(path: str = DATA_FILE) -> list[WelcomeKitOrder]:
    """Load existing orders from CSV into objects."""
    ensure_history_file(path)
    orders: list[WelcomeKitOrder] = []

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                orders.append(WelcomeKitOrder.from_dict(row))
            except Exception:
                # Skip malformed rows safely (resilience)
                continue
    return orders


def append_order_history(order_obj: WelcomeKitOrder, path: str = DATA_FILE) -> None:
    """Append a single order to CSV history."""
    ensure_history_file(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(order_obj.to_row())


def rewrite_order_history(order_list: list[WelcomeKitOrder], path: str = DATA_FILE) -> None:
    """Rewrite the entire history file (used for edit/delete/clear)."""
    ensure_history_file(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "contact",
            "business",
            "address",
            "unit",
            "city",
            "phone",
            "kit",
            "unit_price",
            "quantity",
            "total",
        ])
        for o in order_list:
            writer.writerow(o.to_row())


def orders_to_csv_bytes(order_list: list[WelcomeKitOrder]) -> bytes:
    """Export current session orders as CSV bytes for st.download_button."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "timestamp",
        "contact",
        "business",
        "address",
        "unit",
        "city",
        "phone",
        "kit",
        "unit_price",
        "quantity",
        "total",
    ])
    for o in order_list:
        writer.writerow(o.to_row())
    return buffer.getvalue().encode("utf-8")


def packing_slip_text(order_obj: WelcomeKitOrder) -> str:
    """Human-friendly packing slip (downloadable)."""
    return f"""WELCOME BASKET SUPPLY CO. — PACKING SLIP
----------------------------------------
Timestamp: {order_obj.get_timestamp()}
Contact:   {order_obj.get_contact_name()}
Business:  {order_obj.get_business_name()}
Address:   {order_obj.get_address()} {order_obj.get_unit()}
City:      {order_obj.get_city()}
Phone:     {order_obj.get_phone()}

Kit:       {order_obj.get_kit_name()}
Unit $:    ${order_obj.get_unit_price():.2f}
Qty:       {order_obj.get_quantity()}
----------------------------------------
TOTAL:     ${order_obj.calculate_total():.2f}
----------------------------------------
"""


# -----------------------------
# Initialize Session State
# -----------------------------
catalog = load_catalog()
kit_names = sorted(catalog.keys())

if "orders" not in st.session_state:
    # Load persisted history on first run
    st.session_state.orders = load_order_history()

if "flash" not in st.session_state:
    st.session_state.flash = None


# -----------------------------
# Sidebar (Controls)
# -----------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    st.caption("These tools help demonstrate resilience + usability.")

    if st.button("🔄 Reload from file"):
        st.session_state.orders = load_order_history()
        st.session_state.flash = ("info", "Reloaded orders from CSV history.")
        st.rerun()

    if st.button("🗑 Clear ALL orders (session + file)"):
        st.session_state.orders = []
        rewrite_order_history(st.session_state.orders)
        st.session_state.flash = ("warning", "All orders cleared.")
        st.rerun()

    st.divider()
    st.caption("Download your full order history:")

    history_bytes = orders_to_csv_bytes(st.session_state.orders)
    st.download_button(
        "⬇️ Download History CSV",
        data=history_bytes,
        file_name="kit_order_history.csv",
        mime="text/csv",
        use_container_width=True,
    )


# -----------------------------
# Header + Metrics (Professional Feel)
# -----------------------------
st.title("🎁 Welcome Basket Supply Co.")
st.caption("Streamlit Cloud Delivery — OOP + Persistence + Resilient UX")
st.divider()

total_orders = len(st.session_state.orders)
total_revenue = sum(o.calculate_total() for o in st.session_state.orders) if total_orders else 0.0
avg_order = (total_revenue / total_orders) if total_orders else 0.0

m1, m2, m3 = st.columns(3)
m1.metric("📦 Orders", total_orders)
m2.metric("💰 Revenue", f"${total_revenue:,.2f}")
m3.metric("📈 Avg Order", f"${avg_order:,.2f}")

# Flash messaging area
if st.session_state.flash:
    level, msg = st.session_state.flash
    if level == "success":
        st.success(msg, icon="✅")
    elif level == "warning":
        st.warning(msg, icon="⚠️")
    else:
        st.info(msg, icon="ℹ️")
    st.session_state.flash = None


# -----------------------------
# Main Layout
# -----------------------------
left, right = st.columns([1, 1.35], gap="large")

# -----------------------------
# LEFT: New Order Form (with placeholders + validation)
# -----------------------------
with left:
    st.subheader("🧾 Place a New Order")

    with st.form("order_form", clear_on_submit=True):
        contact_name = st.text_input("Contact Name*", placeholder="e.g. John Smith")
        business_name = st.text_input("Business Name", placeholder="e.g. ABC Corporation")
        address = st.text_input("Street Address*", placeholder="e.g. 123 Main St")
        unit = st.text_input("Unit / Suite", placeholder="e.g. Apt 4B (optional)")
        city = st.text_input("City*", placeholder="e.g. Chicago")
        phone = st.text_input("Phone", placeholder="e.g. 555-123-4567")

        kit_name = st.selectbox("Kit*", kit_names)
        quantity = st.number_input("Quantity*", min_value=1, step=1, value=1)

        submitted = st.form_submit_button("➕ Add Order", use_container_width=True)

    if submitted:
        # Resilience: validate required fields
        errors = []
        if not contact_name.strip():
            errors.append("Contact Name is required.")
        if not address.strip():
            errors.append("Street Address is required.")
        if not city.strip():
            errors.append("City is required.")
        if kit_name not in catalog:
            errors.append("Selected kit is invalid (catalog mismatch).")

        if errors:
            for e in errors:
                st.warning(f"⚠️ {e}")
        else:
            unit_price = float(catalog[kit_name])

            new_order = WelcomeKitOrder(
                contact_name=contact_name.strip(),
                business_name=business_name.strip(),
                address=address.strip(),
                unit=unit.strip(),
                city=city.strip(),
                phone=phone.strip(),
                kit_name=kit_name,
                unit_price=unit_price,
                quantity=int(quantity),
                timestamp=datetime.now().isoformat(timespec="seconds"),
            )

            st.session_state.orders.append(new_order)
            append_order_history(new_order)

            st.session_state.flash = ("success", "Order added successfully!")
            st.balloons()
            st.rerun()

    st.caption("* Required fields")


# -----------------------------
# RIGHT: Order Manager (Cards + Edit/Delete + Downloads)
# -----------------------------
with right:
    st.subheader("🧺 Order Manager")

    if not st.session_state.orders:
        st.info("No orders yet. Place your first order on the left.")
    else:
        for i, order in enumerate(st.session_state.orders):
            # Card container (border=True looks like a “card”)
            with st.container(border=True):
                top = st.columns([3, 1])

                with top[0]:
                    st.markdown(
                        f"**{order.get_contact_name()}** "
                        f"— {order.get_quantity()} × `{order.get_kit_name()}` "
                        f"= **${order.calculate_total():.2f}**"
                    )
                    st.caption(
                        f"{order.get_business_name()} • {order.get_address()} {order.get_unit()} • "
                        f"{order.get_city()} • {order.get_phone()} • {order.get_timestamp()}"
                    )

                with top[1]:
                    if st.button("❌ Delete", key=f"del_{i}", use_container_width=True):
                        st.session_state.orders.pop(i)
                        rewrite_order_history(st.session_state.orders)
                        st.session_state.flash = ("warning", "Order deleted.")
                        st.rerun()

                # Actions row: Edit + Packing slip
                a1, a2 = st.columns([1.2, 1])

                with a1:
                    with st.expander("✏️ Edit this order"):
                        new_kit = st.selectbox(
                            "Kit",
                            kit_names,
                            index=kit_names.index(order.get_kit_name())
                            if order.get_kit_name() in kit_names else 0,
                            key=f"kit_{i}"
                        )
                        new_qty = st.number_input(
                            "Quantity",
                            min_value=1,
                            step=1,
                            value=int(order.get_quantity()),
                            key=f"qty_{i}"
                        )

                        if st.button("✅ Save Changes", key=f"save_{i}"):
                            # Update object safely
                            order.set_kit_name(new_kit)
                            order.set_unit_price(float(catalog[new_kit]))
                            order.set_quantity(int(new_qty))

                            rewrite_order_history(st.session_state.orders)
                            st.session_state.flash = ("success", "Order updated.")
                            st.rerun()

                with a2:
                    slip = packing_slip_text(order)
                    st.download_button(
                        "📄 Packing Slip",
                        data=slip.encode("utf-8"),
                        file_name=f"packing_slip_{i+1}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

        st.divider()

        # Download session CSV (current run)
        session_bytes = orders_to_csv_bytes(st.session_state.orders)
        st.download_button(
            "📥 Download Session CSV",
            data=session_bytes,
            file_name="session_orders.csv",
            mime="text/csv",
            use_container_width=True,
        )