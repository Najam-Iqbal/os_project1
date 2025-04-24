# status_monitor.py

import streamlit as st
import time
import threading
from firebase_utils import get_value, get_power_status

# Function to monitor WiFi status from Firebase every 6 seconds
def monitor_wifi_status():
    previous_status = None
    
    while True:
        try:
            # Get the current WiFi status from Firebase
            current_status = get_value("Device_001/wifi_status")  # Adjust the path as needed
            
            # Check if the status has changed
            if current_status != previous_status:
                if current_status == 1:
                    st.session_state.wifi_connected = True
                    st.session_state.last_wifi_status = current_status
                else:
                    st.session_state.wifi_connected = False
                    st.session_state.last_wifi_status = current_status
            # If the status has not changed, keep the last status
            previous_status = current_status
        except Exception as e:
            # If there's an error, mark the device as offline
            st.session_state.wifi_connected = False
            st.session_state.last_wifi_status = None
            print(f"Error fetching WiFi status: {e}")

        # Wait for 6 seconds before checking again
        time.sleep(6)

# Function to start the Wi-Fi status monitoring thread
def start_status_threads():
    if "wifi_thread_started" not in st.session_state:
        st.session_state.last_wifi_status = None
        st.session_state.wifi_connected = False
        threading.Thread(target=monitor_wifi_status, daemon=True).start()
        st.session_state.wifi_thread_started = True

# Function to check if the WiFi is connected
def is_wifi_connected():
    return st.session_state.get("wifi_connected", False)

# Function to display the Wi-Fi and Power status
def show_status_bar():
    cols = st.columns(2)

    # WiFi Status
    if is_wifi_connected():
        cols[0].success("✅ WiFi Connected")
    else:
        cols[0].error("❌ WiFi Disconnected")

    # Power Status (only shown if Wi-Fi is connected)
    if is_wifi_connected():
        try:
            power_on = get_power_status()
            if power_on:
                cols[1].info("🔌 Power: ON")
            else:
                cols[1].warning("⚡ Power: OFF")
        except Exception as e:
            cols[1].error(f"⚠️ Error fetching power status: {e}")
    else:
        cols[1].error("⚠️ Cannot fetch power status. Device is offline.")

# Initialize the monitoring thread when the app starts
if __name__ == "__main__":
    st.title("Device Status Monitor")
    start_status_threads()
    show_status_bar()
