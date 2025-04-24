import streamlit as st
import time
import threading
from firebase_utils import get_value, get_power_status

def show_power_status():
    if "show_power" not in st.session_state:
        st.session_state.show_power = False
        st.session_state.power_checked_at = None
        st.session_state.power_result = ""

    if st.button("🔍 View Current Power Status"):
        power_on = get_power_status()
        st.session_state.power_result = "🔌 Power Status: ON" if power_on else "⚡ Power Status: OFF"
        st.session_state.show_power = True
        st.session_state.power_checked_at = time.time()

    # Show the result for 3 seconds after button press
    if st.session_state.show_power:
        elapsed = time.time() - st.session_state.power_checked_at
        if elapsed < 3:
            if "ON" in st.session_state.power_result:
                st.info(st.session_state.power_result)
            else:
                st.warning(st.session_state.power_result)
        else:
            st.session_state.show_power = False  # auto-hide
