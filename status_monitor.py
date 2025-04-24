import streamlit as st
import time
import threading
from firebase_utils import get_value, get_power_status


def show_power_status():
    if "show_power" not in st.session_state:
        st.session_state.show_power = False
        st.session_state.power_checked_at = None

    if st.button("🔍 View Current Power Status"):
        st.session_state.show_power = True
        st.session_state.power_checked_at = time.time()

    # Display power status if flag is True
    if st.session_state.show_power:
        power_on = get_power_status()
        if power_on:
            st.info("🔌 Power Status: ON")
        else:
            st.warning("⚡ Power Status: OFF")

        # Auto-hide after 3 seconds
        if time.time() - st.session_state.power_checked_at > 3:
            st.session_state.show_power = False
            st.experimental_rerun()
