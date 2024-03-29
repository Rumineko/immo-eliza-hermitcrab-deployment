import streamlit as st
import requests
import json

st.title("🏠 House Price Prediction")


st.write(
    "Please enter the following details to get the estimated price of the property:"
)

type = st.radio("Type of Property", ("Apartment", "House"))
kitchen_type = st.radio(
    "Type of Kitchen",
    ("Not Installed", "Semi Equipped", "Installed", "Hyper Equipped"),
)
epc = st.select_slider(
    "Energy Performance Certificate",
    options=["A++", "A+", "A", "B", "C", "D", "E", "F", "G"],
)
furnished = st.toggle("Is the Property Furnished?")
openfire = st.toggle("Does the Property have a Fireplace?")
state_of_building = st.radio(
    "State of Building", ("Good", "New", "To Renovate", "Just Renovated")
)
garden_surface = st.number_input(
    "Garden Surface (in m²)", min_value=0, max_value=1000, value=0
)
habitable_surface = st.number_input(
    "Habitable Surface (in m²)", min_value=0, max_value=1000, value=0
)
terrace_surface = st.number_input(
    "Terrace Surface (in m²)", min_value=0, max_value=1000, value=0
)
postal_code = st.number_input("Postal Code", min_value=1000, max_value=9999, value=1000)

if furnished:
    furnished = True
else:
    furnished = False

if openfire:
    openfire = True
else:
    openfire = False

if type == "Apartment":
    type = "APARTMENT"
else:
    type = "HOUSE"

if kitchen_type == "Not Installed":
    kitchen_type = "NOT_INSTALLED"
elif kitchen_type == "Semi Equipped":
    kitchen_type = "SEMI_EQUIPPED"
elif kitchen_type == "Installed":
    kitchen_type = "INSTALLED"
else:
    kitchen_type = "HYPER_EQUIPPED"

if state_of_building == "Good":
    state_of_building = "GOOD"
elif state_of_building == "New":
    state_of_building = "AS_NEW"
elif state_of_building == "To Renovate":
    state_of_building = "TO_RENOVATE"
elif state_of_building == "Just Renovated":
    state_of_building = "JUST_RENOVATED"

inputs = {
    "Habitable Surface": habitable_surface,
    "Kitchen Type": kitchen_type,
    "Terrace Surface": terrace_surface,
    "Garden Surface": garden_surface,
    "EPC": epc,
    "Type": type,
    "Postal Code": postal_code,
    "Furnished": furnished,
    "Openfire": openfire,
    "State of Building": state_of_building,
}


if "clicked" not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


st.header(
    "🦀 Charlie is awaiting your request. Whenever ready, click the button below! 🦀"
)
st.button("Click me to ask Charlie to Predict the Price!", on_click=click_button)


if st.session_state.clicked:
    response = requests.post(
        url="https://price-prediction-model-2.onrender.com/predict",
        data=json.dumps(inputs),
    )

    response = response.json()

    price = response["predicted_price"]
    rounded = round(price)
    value = int(rounded)
    st.subheader(f"🦀 Charlie says your property is worth: €{value:,d} 💶")
    st.session_state.clicked = False
