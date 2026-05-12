import csv
import io
import streamlit as st
from WelcomeKitOrder import WelcomeKitOrder

st.set_page_config(page_title="Welcome Basket Supply Co.", layout="wide")

st.title("🎁 Welcome Basket Supply Co.")
st.caption("Sprint 7 — Streamlit Modernization + OOP + Session Grand Total")

# ----------------------------
# Session State
# ----------------------------
if "orders" not in st.session_state:
    st.session_state.orders = []

# ----------------------------
# Catalog Loader (robust: one-line OR multi-line)
# ----------------------------
@st.cache_data
def load_catalog(path="kit_catalog.txt"):
    catalog = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        # supports either one-per-line or space-separated
        tokens = [t for t in raw.replace("\n", " ").split(" ") if t.strip()]
        for token in tokens:
            if "," not in token:
                continue
            kit, price = token.split(",", 1)
            kit = kit.strip()
            price = float(price.strip())
            catalog[kit] = price

    except FileNotFoundError:
        catalog = {
            "New_Employee": 15.00,
            "Office": 18.00,
            "Pet": 12.00,
            "Baby": 20.00,
            "Birthday": 17.00,
        }
    return catalog


catalog = load_catalog()
kit_names = sorted(catalog.keys())

# ----------------------------
# Helpers: exports (cloud-safe)
# ----------------------------
def orders_to_csv_bytes(order_list):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "contact", "business", "address", "unit", "city", "phone",
        "kit", "unit_price", "quantity", "total"
    ])
    for o in order_list:
        writer.writerow([
            o.get_contact_name(),
            o.get_business_name(),
            o.get_address(),
            o.get_unit(),
            o.get_city(),
            o.get_phone(),
            o.get_kit_name(),
            f"{o.get_unit_price():.2f}",
            o.get_quantity(),
            f"{o.calculate_total():.2f}",
        ])
    return buffer.getvalue().encode("utf-8")


def packing_slip_text(order_obj):
    return f"""WELCOME BASKET SUPPLY CO. PACKING SLIP

{order_obj}
"""


# ----------------------------
# UI Layout
# ----------------------------
left, right = st.columns([1.05, 1.25], gap="large")

with left:
    st.subheader("🧾 Place a New Order")

    with st.form("order_form"):
        contact = st.text_input("Contact Name")
        business = st.text_input("Business Name")
        address = st.text_input("Street Address")
        unit = st.text_input("Unit / Suite Number (optional)")
        city = st.text_input("City")
        phone = st.text_input("Phone Number")

        st.divider()

        kit_choice = st.selectbox("Kit Type", kit_names)
        quantity = st.number_input("Quantity", min_value=1, step=1, value=1)

        submitted = st.form_submit_button("➕ Add Order to Session")

    if submitted:
        # Create OOP object just like Sprint 6
        order = WelcomeKitOrder()
        order.set_contact_name(contact)
        order.set_business_name(business)
        order.set_address(address)
        order.set_unit(unit)
        order.set_city(city)
        order.set_phone(phone)

        order.set_kit_name(kit_choice)
        order.set_unit_price(catalog[kit_choice])
        order.set_quantity(quantity)

        st.session_state.orders.append(order)
        st.success("Order added to session view.")

        # Packing slip download for the most recent order
        st.download_button(
            "⬇️ Download Packing Slip (txt)",
            data=packing_slip_text(order),
            file_name="packing_slip.txt",
            mime="text/plain"
        )

    with st.expander("📦 View Catalog"):
        for k in kit_names:
            st.write(f"- `{k}` — ${catalog[k]:.2f}")

with right:
    st.subheader("🧺 Session Orders (This Run)")

    if not st.session_state.orders:
        st.info("No orders added yet.")
    else:
        grand_total = 0.0
        for i, o in enumerate(st.session_state.orders, start=1):
            line_total = o.calculate_total()
            grand_total += line_total
            st.write(
                f"**{i}.** {o.get_quantity()} × `{o.get_kit_name()}` "
                f"@ ${o.get_unit_price():.2f} = **${line_total:.2f}**"
            )

        st.divider()
        st.metric("💰 Grand Total (this session)", f"${grand_total:.2f}")

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "⬇️ Download Session History (CSV)",
                data=orders_to_csv_bytes(st.session_state.orders),
                file_name="kit_order_history.csv",
                mime="text/csv"
            )
        with c2:
            if st.button("🧹 Reset Session"):
                st.session_state.orders = []
                st.rerun()