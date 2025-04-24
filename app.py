import streamlit as st
from firebase_utils import validate_login, get_power_status
from status_monitor import show_status_in_app
import importlib
import threading
import time

# Pages to navigate to
PAGES = {
    "LED Control": "2_Manual_Control",
    "WiFi & Credentials": "1_Change_Credentials",
    "Deep Sleep": "3_DeepSleep_and_Restart",
    "Upload Timetable": "4_Upload_Timetable"
}

# Initialize the power status in session state
if 'power_status' not in st.session_state:
    st.session_state.power_status = False

# Function to update the power status
def update_power_status():
    while True:
        st.session_state.power_status = get_power_status()  # Fetch the latest power status
        time.sleep(5)  # Update every 5 seconds (or adjust as needed)

# Start the power status update thread when the app starts
if 'power_status_thread' not in st.session_state:
    st.session_state.power_status_thread = threading.Thread(target=update_power_status, daemon=True)
    st.session_state.power_status_thread.start()

# Login function to authenticate the user
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

# Function to show power status dynamically
def show_power_status():
    if st.session_state.power_status:
        st.markdown("### Power Status: LED is ON")
    else:
        st.markdown("### Power Status: LED is OFF")

# Main function to display the app content
def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()
        st.stop()

    st.sidebar.title("ESP32 Firebase Dashboard")

    # Add a unique key to the radio button to prevent ID conflict
    selection = st.sidebar.radio("Select Page", list(PAGES.keys()), key="page_selection_radio")

    # Display power status dynamically
    show_power_status()

    # Dynamically load and run the selected module
    module_name = PAGES[selection]
    module = importlib.import_module(module_name)
    module.run()

# Run the app
if __name__ == "__main__":
    main()
