from streamlit_autorefresh import st_autorefresh
import streamlit as st
import time
from firebase_utils import get_power_status, check_wifi, get_value

def show_power_status():
    # Auto-refresh every second if needed
    if "show_power" in st.session_state and st.session_state.show_power:
        st_autorefresh(interval=1000, key="power_refresh")

    if "show_power" not in st.session_state:
        st.session_state.show_power = False
        st.session_state.power_checked_at = None
        st.session_state.power_result = ""

    if st.button("🔍 View Current Power Status"):
       if check_wifi(): 
        power_on = get_power_status()
        st.session_state.power_result = "🔌 Power Status: ON (Click again to get current status)" if power_on else "⚡ Power Status: OFF (Click again to get current status)"
        st.session_state.show_power = True
        st.session_state.power_checked_at = time.time()
       else:
        st.error("Device is not connected to Wi-Fi")

    # Show the result and auto-hide after 3 seconds
    if st.session_state.show_power:
        elapsed = time.time() - st.session_state.power_checked_at
        if elapsed < 3:
            if "ON" in st.session_state.power_result:
               if get_value("led/manualcontrol"): 
                st.info(f"{st.session_state.power_result}_ Manual Control Till {get_value("fr_end/noted_time")}")
               elif get_value(schedule_string) != "":
                st.info(f"{st.session_state.power_result}_ Following Timetable")
               else:
                st.info(st.session_state.power_result)
            else:
               if get_value("led/manualcontrol"): 
                st.Warning(f"{st.session_state.power_result}_ Manual Control Till {get_value("fr_end/noted_time")}")
               elif get_value(schedule_string) != "":
                st.Warning(f"{st.session_state.power_result}_ Following Timetable")
               else:
                st.Warning(st.session_state.power_result)
        else:
            st.session_state.show_power = False  # Hide after 3 seconds
