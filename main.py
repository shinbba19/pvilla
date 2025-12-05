import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="StayOps Prototype", layout="wide")

# ----------------- CONFIG -----------------
OWNER_SHARE = 0.65
OPERATOR_SHARE = 0.25
PLATFORM_SHARE = 0.10

# ----------------- INIT MOCK DATA -----------------
def init_mock():
    # Users
    st.session_state.users = [
        {"id": 1, "name": "Alice (Owner)", "role": "owner"},
        {"id": 2, "name": "Bob (Operator)", "role": "operator"},
        {"id": 3, "name": "Charlie (Guest)", "role": "guest"},
    ]

    # Properties – MORE MOCK LISTINGS
    st.session_state.properties = [
        {
            "id": 1,
            "name": "Khaoyai Sunset Villa",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 6000.0,
            "rating": 4.8,
            "reviews": 32,
            "bedrooms": 3,
            "baths": 3,
            "guests": 6,
            "image_url": "https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg",
            "description": "Private pool villa with mountain view, perfect for wellness & pet-friendly stays.",
        },
        {
            "id": 2,
            "name": "Forest Retreat Pool Villa",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 7500.0,
            "rating": 4.9,
            "reviews": 18,
            "bedrooms": 4,
            "baths": 4,
            "guests": 8,
            "image_url": "https://images.pexels.com/photos/32870/pexels-photo.jpg",
            "description": "Surrounded by trees, ideal for yoga retreats and quiet escapes from Bangkok.",
        },
        {
            "id": 3,
            "name": "Skyline Mountain View Villa",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 9000.0,
            "rating": 4.7,
            "reviews": 24,
            "bedrooms": 5,
            "baths": 5,
            "guests": 10,
            "image_url": "https://images.pexels.com/photos/258154/pexels-photo-258154.jpeg",
            "description": "Spacious villa with panoramic mountain views, great for large groups & events.",
        },
        {
            "id": 4,
            "name": "Minimal Zen Pool House",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 5500.0,
            "rating": 4.6,
            "reviews": 15,
            "bedrooms": 2,
            "baths": 2,
            "guests": 4,
            "image_url": "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg",
            "description": "Calm, minimal villa with private pool, ideal for couples and small families.",
        },
        {
            "id": 5,
            "name": "Family Garden Pool Villa",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 6800.0,
            "rating": 4.5,
            "reviews": 21,
            "bedrooms": 3,
            "baths": 3,
            "guests": 7,
            "image_url": "https://images.pexels.com/photos/261187/pexels-photo-261187.jpeg",
            "description": "Lush garden, BBQ area and kids-friendly pool – perfect for family trips.",
        },
        {
            "id": 6,
            "name": "Wellness Retreat Pool Villa",
            "location": "Khao Yai, Thailand",
            "owner_id": 1,
            "operator_id": 2,
            "nightly_rate": 8200.0,
            "rating": 5.0,
            "reviews": 11,
            "bedrooms": 4,
            "baths": 4,
            "guests": 8,
            "image_url": "https://images.pexels.com/photos/1458457/pexels-photo-1458457.jpeg",
            "description": "Designed for wellness: yoga deck, quiet surroundings and detox-friendly kitchen.",
        },
    ]

    # Bookings – still one initial booking as example
    st.session_state.bookings = [
        {
            "id": 1,
            "property_id": 1,
            "guest_name": "Charlie (Guest)",
            "check_in": date(2025, 1, 10),
            "check_out": date(2025, 1, 12),
            "nights": 2,
            "price_total": 12000.0,
            "status": "completed",
        }
    ]

    # Expenses
    st.session_state.expenses = [
        {"id": 1, "booking_id": 1, "description": "Cleaning", "amount": 500.0},
        {"id": 2, "booking_id": 1, "description": "Minor Repair", "amount": 300.0},
    ]

    # UI state
    st.session_state.selected_property_id = None

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    init_mock()

# ----------------- HELPERS -----------------
def get_new_id(items):
    if not items:
        return 1
    return max(i["id"] for i in items) + 1

def add_user(name: str, role: str):
    new_id = get_new_id(st.session_state.users)
    st.session_state.users.append({"id": new_id, "name": name, "role": role})
    return new_id

def add_property(name: str, location: str, owner_id: int, operator_id: int, nightly_rate: float):
    new_id = get_new_id(st.session_state.properties)
    st.session_state.properties.append(
        {
            "id": new_id,
            "name": name,
            "location": location,
            "owner_id": owner_id,
            "operator_id": operator_id,
            "nightly_rate": nightly_rate,
            "rating": 5.0,
            "reviews": 0,
            "bedrooms": 3,
            "baths": 3,
            "guests": 6,
            "image_url": "https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg",
            "description": "Newly added pool villa by owner.",
        }
    )
    return new_id

def add_booking(property_id: int, guest_name: str, check_in: date, check_out: date, nights: int) -> int:
    prop = next(p for p in st.session_state.properties if p["id"] == property_id)
    price_total = prop["nightly_rate"] * nights
    new_id = get_new_id(st.session_state.bookings)
    st.session_state.bookings.append(
        {
            "id": new_id,
            "property_id": property_id,
            "guest_name": guest_name,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "price_total": price_total,
            "status": "booked",
        }
    )
    return new_id

def add_expense(booking_id: int, desc: str, amount: float):
    new_id = get_new_id(st.session_state.expenses)
    st.session_state.expenses.append(
        {"id": new_id, "booking_id": booking_id, "description": desc, "amount": amount}
    )

def get_expenses_for_booking(booking_id: int) -> float:
    df = pd.DataFrame(st.session_state.expenses)
    if df.empty:
        return 0.0
    return float(df[df["booking_id"] == booking_id]["amount"].sum())

def compute_split(price_total: float, expenses: float):
    net = max(price_total - expenses, 0.0)
    owner_amt = net * OWNER_SHARE
    operator_amt = net * OPERATOR_SHARE
    platform_amt = net * PLATFORM_SHARE
    return net, owner_amt, operator_amt, platform_amt

def summarize_for_owner(owner_id: int):
    props = [p["id"] for p in st.session_state.properties if p["owner_id"] == owner_id]
    if not props:
        return 0, 0.0
    total_bookings = 0
    total_owner = 0.0
    for b in st.session_state.bookings:
        if b["property_id"] in props:
            expenses = get_expenses_for_booking(b["id"])
            _, owner_amt, _, _ = compute_split(b["price_total"], expenses)
            total_bookings += 1
            total_owner += owner_amt
    return total_bookings, total_owner

def summarize_for_operator(operator_id: int):
    props = [p["id"] for p in st.session_state.properties if p["operator_id"] == operator_id]
    if not props:
        return 0, 0.0
    total_bookings = 0
    total_op = 0.0
    for b in st.session_state.bookings:
        if b["property_id"] in props:
            expenses = get_expenses_for_booking(b["id"])
            _, _, op_amt, _ = compute_split(b["price_total"], expenses)
            total_bookings += 1
            total_op += op_amt
    return total_bookings, total_op

# ----------------- UI LAYOUT -----------------
st.title("StayOps – Pool Villa Platform Prototype")
st.caption("Owner ↔ Operator ↔ Guest with date-based booking & profit sharing (mock)")

tab_guest, tab_owner, tab_operator, tab_payout = st.tabs(
    ["🏡 Guest (Airbnb-style)", "👑 Owner", "🧑‍🔧 Operator", "💰 Payout Summary"]
)

# ---------- TAB 1: GUEST (AIRBNB-LIKE PAGE) ----------
with tab_guest:
    st.subheader("Find your wellness & pet-friendly pool villa in Khao Yai")

    # Top search bar (visual)
    with st.container():
        col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 1])
        with col_a:
            st.text_input("Location", value="Khao Yai")
        with col_b:
            st.date_input("Check in", value=date.today())
        with col_c:
            st.date_input("Check out", value=date.today())
        with col_d:
            st.number_input("Guests", min_value=1, max_value=16, value=4)

    st.markdown("---")
    st.markdown("### Stays in Khao Yai")

    props_df = pd.DataFrame(st.session_state.properties)

    # Property list as cards
    for _, row in props_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1.2, 2])
            with col1:
                st.image(row["image_url"], use_column_width=True)
            with col2:
                st.markdown(f"#### {row['name']}")
                st.write(f"📍 {row['location']}")
                st.write(
                    f"⭐ {row['rating']} · {row['reviews']} reviews · "
                    f"{int(row['guests'])} guests · {int(row['bedrooms'])} bedrooms · {int(row['baths'])} baths"
                )
                st.write(f"💰 **{row['nightly_rate']:.0f} THB / night**")
                if st.button("View details", key=f"view_{row['id']}"):
                    st.session_state.selected_property_id = int(row["id"])
        st.markdown("---")

    # Property details (Airbnb style) + booking box
    if st.session_state.selected_property_id is not None:
        prop = next(p for p in st.session_state.properties if p["id"] == st.session_state.selected_property_id)
        st.markdown("## Selected stay")
        left, right = st.columns([2, 1])

        with left:
            st.image(prop["image_url"], use_column_width=True)
            st.markdown(f"### {prop['name']}")
            st.write(f"📍 {prop['location']}")
            st.write(
                f"⭐ {prop['rating']} · {prop['reviews']} reviews · "
                f"{prop['guests']} guests · {prop['bedrooms']} bedrooms · {prop['baths']} baths"
            )
            st.markdown("#### About this place")
            st.write(prop["description"])

        with right:
            st.markdown("#### Reserve")
            check_in = st.date_input("Check-in date", value=date.today(), key="detail_check_in")
            check_out = st.date_input("Check-out date", value=date.today(), key="detail_check_out")
            guest_name = st.text_input("Guest name", value="Demo Guest", key="detail_guest_name")

            nights = (check_out - check_in).days
            if nights <= 0:
                st.error("Check-out must be after check-in.")
                est_price = 0
            else:
                est_price = prop["nightly_rate"] * nights

            st.markdown(f"**{prop['nightly_rate']:.0f} THB x {max(nights,0)} nights = {est_price:.0f} THB**")

            if st.button("Create booking", key="detail_create_booking"):
                if nights <= 0:
                    st.error("Cannot create booking: invalid dates.")
                else:
                    bid = add_booking(prop["id"], guest_name, check_in, check_out, nights)
                    st.success(f"✅ Booking created with ID: {bid}")

# ---------- TAB 2: OWNER ----------
with tab_owner:
    st.subheader("Owner: manage profile & add pool villas")

    users_df = pd.DataFrame(st.session_state.users)
    owners_df = users_df[users_df["role"] == "owner"]

    st.markdown("### Existing Owners")
    st.dataframe(owners_df)

    st.markdown("### Add new owner")
    new_owner_name = st.text_input("New owner name")
    if st.button("Create owner"):
        if new_owner_name.strip():
            oid = add_user(new_owner_name.strip(), "owner")
            st.success(f"Owner created with ID: {oid}")
        else:
            st.warning("Please enter a name.")

    st.markdown("---")
    st.markdown("### Add new pool villa")

    owners_df = pd.DataFrame(st.session_state.users)
    owners_df = owners_df[owners_df["role"] == "owner"]
    operators_df = pd.DataFrame(st.session_state.users)
    operators_df = operators_df[operators_df["role"] == "operator"]

    if owners_df.empty or operators_df.empty:
        st.info("Need at least 1 owner and 1 operator to add a property.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            pname = st.text_input("Property name", value="New Khao Yai Pool Villa")
            ploc = st.text_input("Location", value="Khao Yai, Thailand")
            nightly_rate = st.number_input("Nightly rate (THB)", min_value=1000.0, step=500.0, value=5000.0)
        with col2:
            owner_id = st.selectbox(
                "Owner",
                owners_df["id"],
                format_func=lambda i: owners_df[owners_df.id == i]["name"].iloc[0]
            )
            operator_id = st.selectbox(
                "Operator",
                operators_df["id"],
                format_func=lambda i: operators_df[operators_df.id == i]["name"].iloc[0]
            )

        if st.button("Add pool villa"):
            pid = add_property(pname, ploc, int(owner_id), int(operator_id), float(nightly_rate))
            st.success(f"🏡 New property created with ID: {pid}")

    st.markdown("### All properties")
    st.dataframe(pd.DataFrame(st.session_state.properties))

# ---------- TAB 3: OPERATOR ----------
with tab_operator:
    st.subheader("Operator: manage assigned properties & add expenses")

    users_df = pd.DataFrame(st.session_state.users)
    operators_df = users_df[users_df["role"] == "operator"]

    if operators_df.empty:
        st.warning("No operators found. Create one in Owner tab.")
    else:
        op_id = st.selectbox(
            "Select operator",
            operators_df["id"],
            format_func=lambda i: operators_df[operators_df.id == i]["name"].iloc[0]
        )

        props_df = pd.DataFrame(st.session_state.properties)
        assigned_props = props_df[props_df["operator_id"] == op_id]

        st.markdown("### Assigned properties")
        st.dataframe(assigned_props)

        bookings_df = pd.DataFrame(st.session_state.bookings)
        if assigned_props.empty:
            st.info("This operator has no assigned properties yet.")
        else:
            prop_ids = assigned_props["id"].tolist()
            op_bookings = bookings_df[bookings_df["property_id"].isin(prop_ids)]

            st.markdown("### Bookings for this operator's properties")
            st.dataframe(op_bookings)

            if not op_bookings.empty:
                st.markdown("### Add expenses to a booking")
                booking_id = st.selectbox(
                    "Booking",
                    op_bookings["id"],
                    format_func=lambda i: f"Booking #{i} (Property {int(op_bookings[op_bookings.id == i]['property_id'].iloc[0])})"
                )
                desc = st.text_input("Expense description", value="Cleaning")
                amount = st.number_input("Amount (THB)", min_value=0.0, step=100.0, value=500.0)
                if st.button("Add expense"):
                    add_expense(int(booking_id), desc, float(amount))
                    st.success("Expense added.")

                st.markdown("#### Current expenses for this booking")
                exp_df = pd.DataFrame(st.session_state.expenses)
                st.dataframe(exp_df[exp_df["booking_id"] == booking_id])

# ---------- TAB 4: PAYOUT SUMMARY ----------
with tab_payout:
    st.subheader("Per booking profit split")

    bookings_df = pd.DataFrame(st.session_state.bookings)
    if bookings_df.empty:
        st.warning("No bookings yet.")
    else:
        booking_id = st.selectbox("Select booking", bookings_df["id"], key="split_booking")
        b = bookings_df[bookings_df.id == booking_id].iloc[0]
        expenses_total = get_expenses_for_booking(int(booking_id))
        net, owner_amt, op_amt, platform_amt = compute_split(b["price_total"], expenses_total)

        st.write(f"🏡 Property ID: {b['property_id']}")
        st.write(f"👤 Guest: {b['guest_name']}")
        st.write(f"📅 {b['check_in']} → {b['check_out']} ({b['nights']} nights)")
        st.write(f"💰 Price Total: **{b['price_total']:.2f} THB**")
        st.write(f"🧾 Total Expenses: **{expenses_total:.2f} THB**")
        st.write(f"🏦 Net Profit: **{net:.2f} THB**")

        st.markdown("### Split")
        st.success(
            f"- 👑 Owner ({OWNER_SHARE*100:.0f}%): **{owner_amt:.2f} THB**\n"
            f"- 🧑‍🔧 Operator ({OPERATOR_SHARE*100:.0f}%): **{op_amt:.2f} THB**\n"
            f"- 🏢 Platform ({PLATFORM_SHARE*100:.0f}%): **{platform_amt:.2f} THB**"
        )

    st.markdown("---")
    st.subheader("Owner & Operator totals (mock)")

    owners = [u for u in st.session_state.users if u["role"] == "owner"]
    operators = [u for u in st.session_state.users if u["role"] == "operator"]

    if owners:
        owner = owners[0]
        ob, oe = summarize_for_owner(owner["id"])
        st.info(f"👑 {owner['name']} → Bookings: {ob}, Estimated Earnings: {oe:.2f} THB")

    if operators:
        op = operators[0]
        ob2, oe2 = summarize_for_operator(op["id"])
        st.info(f"🧑‍🔧 {op['name']} → Bookings: {ob2}, Estimated Earnings: {oe2:.2f} THB")
