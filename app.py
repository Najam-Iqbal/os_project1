import streamlit as st
from firebase_utils import validate_login, get_power_status, check_wifi_status
from status_monitor import show_power_status
import importlib

PAGES = {
    "LED Control": "2_Manual_Control",
    "WiFi & Credentials": "1_Change_Credentials",
    "Deep Sleep": "3_DeepSleep_and_Restart",
    "Upload Timetable": "4_Upload_Timetable"
}

def login_page():
    st.title("Device Login")
    
    # Store credentials in session state for callback access
    if 'login_device_name' not in st.session_state:
        st.session_state.login_device_name = ""
    if 'login_password' not in st.session_state:
        st.session_state.login_password = ""
    
    # Form inputs that update session state
    st.text_input(
        "Enter Device Name",
        key="login_device_name",
        on_change=lambda: None  # Forces update
    )
    st.text_input(
        "Enter Password",
        type="password",
        key="login_password",
        on_change=lambda: None  # Forces update
    )
    
    # Login button with callback
    st.button(
        "Login",
        key="login_button",
        on_click=on_login_click
    )

def on_login_click():
    """Callback function for login button"""
    if validate_login(
        st.session_state.login_device_name,
        st.session_state.login_password
    ):
        st.session_state.logged_in = True
        st.session_state.device_name = st.session_state.login_device_name
        st.rerun()  # Immediately refresh to show main app
    else:
        st.error("Invalid credentials")

def main_app():
    st.sidebar.title("ESP32 Firebase Dashboard")
    selection = st.sidebar.radio(
        "Select Page",
        list(PAGES.keys()),
        key="page_selection_radio"
    )

    # Display status
    show_power_status()
    check_wifi_status()
    
    # Load selected module
    module = importlib.import_module(PAGES[selection])
    module.run()

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()
