import streamlit as st
from firebase_utils import validate_login, get_power_status, check_wifi_status, update_value
from status_monitor import show_power_status
import importlib
import time

PAGES = {
    "POWER Control": "2_Manual_Control",
    "WiFi & Credentials": "1_Change_Credentials",
    "Restart/Deep-Sleep": "3_DeepSleep_and_Restart",
    "Timetable Controls": "4_Upload_Timetable",
    "Device is Offline?": "offline_instructions"
}



def login():
    st.title("Device Login")
    device_name = st.text_input("Enter Device Name")
    password = st.text_input("Enter Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        if validate_login(device_name, password):
            st.session_state.logged_in = True
            update_value("user_presence", True)
            st.rerun()

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
