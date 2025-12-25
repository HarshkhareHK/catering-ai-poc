import streamlit as st
from datetime import time
from app.ai.calculator import calculate_ingredients

st.set_page_config(
    page_title="Little Naples AI Catering Calculator",
    layout="wide"
)

st.title("🍕 Little Naples – AI Catering Ingredient Calculator")

st.markdown("Fill in the event details and let the AI calculate exact ingredient quantities.")

# -------------------------
# EVENT DETAILS
# -------------------------

st.header("📋 Event Details")

name = st.text_input("Customer Name")
phone = st.text_input("Phone Number")
location = st.text_area("Event Location")

col1, col2 = st.columns(2)
with col1:
    event_name = st.text_input("Event Name (Birthday, Wedding, etc.)")
with col2:
    serving_time = st.time_input("Serving Start Time", value=time(18, 0))

# -------------------------
# PEOPLE COUNT
# -------------------------

st.header("👥 Guests")

col3, col4 = st.columns(2)
with col3:
    adults = st.number_input("Number of Adults", min_value=0, value=30)
with col4:
    kids = st.number_input("Number of Kids", min_value=0, value=10)

# -------------------------
# FOOD SELECTION
# -------------------------

st.header("🍽 Food Selection")

food_choices = st.multiselect(
    "Select Food Items",
    ["Antipasto", "Veggie Pizza", "Margherita Pizza", "Pasta Arrabiata", "Cannoli"]
)

package = st.selectbox("Catering Package", ["Option 2"])

event_type = st.selectbox(
    "Event Type",
    ["birthday", "party", "wedding", "corporate", "kids_party"]
)

buffer_percent = st.slider(
    "Chef Safety Buffer (%)",
    min_value=0,
    max_value=20,
    value=5
) / 100

# -------------------------
# CALCULATE
# -------------------------

if st.button("🤖 Calculate Ingredients"):
    if adults + kids == 0:
        st.error("Please enter at least one guest.")
    else:
        dishes, reasoning = calculate_ingredients(
            package=package,
            adults=adults,
            kids=kids,
            event_type=event_type,
            buffer_percent=buffer_percent
        )

        st.success("Ingredient calculation completed!")

        st.header("🧾 Ingredient Breakdown")

        for dish in dishes:
            if food_choices and dish["dish"] not in food_choices:
                continue

            st.subheader(f"{dish['dish']} (Confidence: {dish['confidence_score']}%)")
            for ing in dish["ingredients"]:
                st.write(f"- {ing['name']}: {ing['quantity']} {ing['unit']}")

        st.header("🧠 AI Reasoning")
        st.info(reasoning["explanation"])
