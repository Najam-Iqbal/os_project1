import streamlit as st
from firebase_utils import update_value, get_value, get_power_status
import time

def run():
    st.title("🟢 Manual LED Control")

    """# Check WiFi connection by polling /Device_001/wifi_status
    current_status = get_value("Device_001/wifi_status")
    time.sleep(6)
    updated_status = get_value("Device_001/wifi_status")

    if current_status == updated_status:
        st.error("Device is not connected to WiFi.")
        st.stop()"""

    # Show power status
    try:
        if get_power_status():
            st.info("🔌 Power Status: ON")
        else:
            st.warning("⚡ Power Status: OFF")
    except:
        st.error("Unable to fetch power status due to WiFi issue.")

    # Manual mode control UI
    mode = st.radio("Select Manual Control Mode", ["Use Manual Control", "Exit Manual Control"], key="manual_mode")

    if mode == "Use Manual Control":
        delay_min = st.number_input("Enter time in minutes:", min_value=1, step=1)
        led_state = st.selectbox("Turn:", ["on", "off"], key="led_state_choice")
        if st.button("Submit Manual Command"):
            update_value("led/manualcontrol", True)
            update_value("led/state", 1 if led_state == "on" else 0)
            update_value("led/delay", delay_min)
            st.success("Manual control command sent.")

    elif mode == "Exit Manual Control":
        if st.button("Exit Manual Control", key="exit_manual"):
            update_value("led/manualcontrol", False)
            st.info("Implementing......")
            time.sleep(3)
            st.success("Exited manual control.")
