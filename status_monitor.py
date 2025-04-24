import streamlit as st
import time
import threading
from firebase_utils import get_value, get_power_status

# Monitor WiFi status
def monitor_wifi_status():
    previous_status = None
    while True:
        try:
            current_status = get_value("Device_001/wifi_status")
            if current_status != previous_status:
                st.session_state.wifi_connected = current_status == 1
                st.session_state.last_wifi_status = current_status
                previous_status = current_status
        except Exception as e:
            st.session_state.wifi_connected = False
            st.session_state.last_wifi_status = None
            print(f"Error fetching WiFi status: {e}")
        time.sleep(6)

# Monitor power status
def monitor_power_status():
    while True:
        try:
            st.session_state.power_on = get_power_status()
        except Exception as e:
            st.session_state.power_on = None
            print(f"Error fetching power status: {e}")
        time.sleep(6)

# Start monitoring threads
def start_status_threads():
    if "wifi_thread_started" not in st.session_state:
        st.session_state.last_wifi_status = None
        st.session_state.wifi_connected = False
        threading.Thread(target=monitor_wifi_status, daemon=True).start()
        st.session_state.wifi_thread_started = True

    if "power_thread_started" not in st.session_state:
        st.session_state.power_on = None
        threading.Thread(target=monitor_power_status, daemon=True).start()
        st.session_state.power_thread_started = True

# Check WiFi connection
def is_wifi_connected():
    return st.session_state.get("wifi_connected", False)

# Display status
def show_status_bar():
    cols = st.columns(2)

    if is_wifi_connected():
        cols[0].success("✅ WiFi Connected")
    else:
        cols[0].error("❌ WiFi Disconnected")

    power_status = st.session_state.get("power_on", None)

    if is_wifi_connected():
        if power_status is True:
            cols[1].info("🔌 Power: ON")
        elif power_status is False:
            cols[1].warning("⚡ Power: OFF")
        else:
            cols[1].error("⚠️ Error fetching power status")
    else:
        cols[1].error("⚠️ Cannot fetch power status. Device is offline.")

def show_status_in_app():
        start_status_threads()
        show_status_bar()
# Run the app
if __name__ == "__main__":
    st.title("Device Status Monitor")
    start_status_threads()
    show_status_bar()
