import streamlit as st
from firebase_utils import update_value, get_value, get_power_status
import time

def run():
    st.title("🌙 Deep Sleep and Restart")

    # Wi-Fi connection check
    """current_status = get_value("Device_001/wifi_status")
    time.sleep(6)
    updated_status = get_value("Device_001/wifi_status")

    if current_status == updated_status:
        st.error("Device is not connected to WiFi.")
        st.stop()"""

    # Power status
    try:
        if get_power_status():
            st.info("🔌 Power Status: ON")
        else:
            st.warning("⚡ Power Status: OFF")
    except:
        st.error("Unable to fetch power status due to WiFi issue.")

    # Deep sleep state tracking
    ds_time_key = "deep_sleep_minutes"
    if ds_time_key not in st.session_state:
        st.session_state[ds_time_key] = 0

    st.markdown("**Current deep sleep time (stored locally):**")
    st.info(f"{st.session_state[ds_time_key]} minutes")

    # Input for deep sleep duration
    ds_time = st.number_input("Enter deep sleep time (minutes)", min_value=1, step=1)

    # Warning and confirmation
    st.warning("⚠️ Once the ESP32 enters deep sleep, it cannot be controlled remotely until it wakes up.")
    confirm = st.checkbox("I understand and want to proceed")

    # Apply deep sleep
    if st.button("Apply Deep Sleep"):
        if confirm:
            update_value("Deepsleep", True)
            update_value("ds_time", ds_time)
            st.session_state[ds_time_key] = ds_time
            st.success(f"Deep sleep set for {ds_time} minutes. Please restart the device manually.")
        else:
            st.error("You must confirm the warning before applying deep sleep.")

    # Restart device
    if st.button("Restart ESP32"):
        update_value("restart", True)
        st.success("Restart signal sent to device.")
