from streamlit_autorefresh import st_autorefresh
import streamlit as st
import time
from firebase_utils import get_power_status

def show_power_status():
    # Auto-refresh every second if needed
    if "show_power" in st.session_state and st.session_state.show_power:
        st_autorefresh(interval=1000, key="power_refresh")

    if "show_power" not in st.session_state:
        st.session_state.show_power = False
        st.session_state.power_checked_at = None
        st.session_state.power_result = ""

    if st.button("🔍 View Current Power Status"):
        power_on = get_power_status()
        st.session_state.power_result = "🔌 Power Status: ON" if power_on else "⚡ Power Status: OFF"
        st.session_state.show_power = True
        st.session_state.power_checked_at = time.time()

    # Show the result and auto-hide after 3 seconds
    if st.session_state.show_power:
        elapsed = time.time() - st.session_state.power_checked_at
        if elapsed < 3:
            if "ON" in st.session_state.power_result:
                st.info(st.session_state.power_result)
            else:
                st.warning(st.session_state.power_result)
        else:
            st.session_state.show_power = False  # Hide after 3 seconds
