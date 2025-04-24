import streamlit as st
from firebase_utils import validate_login, get_power_status
import importlib

PAGES = {
    "LED Control": "2_Manual_Control",
    "WiFi & Credentials": "1_Change_Credentials",
    "Deep Sleep": "3_DeepSleep_and_Restart",
    "Upload Timetable": "4_Upload_Timetable"
}

def login():
    st.title("Device Login")
    device_name = st.text_input("Enter Device Name")
    password = st.text_input("Enter Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        if validate_login(device_name, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

def show_power_status():
    power_on = get_power_status()
    if power_on:
        st.info("🔌 Power Status: ON")
    else:
        st.warning("⚡ Power Status: OFF")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()
        st.stop()

    st.sidebar.title("ESP32 Firebase Dashboard")

    # Add a unique key to the radio button to prevent ID conflict
    selection = st.sidebar.radio("Select Page", list(PAGES.keys()), key="page_selection_radio")

    # Display power status
    show_power_status()

    # Dynamically load and run the selected module
    module_name = PAGES[selection]
    module = importlib.import_module(module_name)
    module.run()

if __name__ == "__main__":
    main()
