import streamlit as st
from firebase_utils import validate_login, get_power_status, check_wifi_status
from status_monitor import show_power_status
import importlib
import time

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
            st.session_state.device_name = device_name  # Store device name for later use
            st.experimental_rerun()  # Force a rerun to immediately show the main app
        else:
            st.error("Invalid credentials")

def main():
    # Initialize session state variables if they don't exist
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login()
        st.stop()  # This will stop execution if not logged in
    
    # Only show the main app if logged in
    st.sidebar.title("ESP32 Firebase Dashboard")
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
