import streamlit as st
from firebase_utils import validate_login, get_power_status, check_wifi_status
import importlib
import time

PAGES = {
    "LED Control": "2_Manual_Control",
    "WiFi & Credentials": "1_Change_Credentials",
    "Deep Sleep": "3_DeepSleep_and_Restart",
    "Upload Timetable": "4_Upload_Timetable"
}

def show_power_status():
    if "show_power" not in st.session_state:
        st.session_state.show_power = False
        st.session_state.power_checked_at = None

    if st.button("🔍 View Current Power Status"):
        st.session_state.show_power = True
        st.session_state.power_checked_at = time.time()

    # Display power status if flag is True
    if st.session_state.show_power:
        power_on = get_power_status()
        if power_on:
            st.info("🔌 Power Status: ON")
        else:
            st.warning("⚡ Power Status: OFF")

        # Auto-hide after 3 seconds
        if time.time() - st.session_state.power_checked_at > 3:
            st.session_state.show_power = False
            st.experimental_rerun()

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


def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()
        st.stop()
    st.sidebar.title("ESP32 Firebase Dashboard")
    # Add a unique key to the radio button to prevent ID conflict
    selection = st.sidebar.radio("Select Page", list(PAGES.keys()), key="page_selection_radio")

    # Display power status
    show_power_status()
    check_wifi_status()
    
    # Dynamically load and run the selected module
    module_name = PAGES[selection]
    module = importlib.import_module(module_name)
    module.run()

if __name__ == "__main__":
    main()
