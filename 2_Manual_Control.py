import streamlit as st
from firebase_utils import update_value, get_value, get_power_status,check_wifi
from datetime import datetime, timedelta
import time
import pytz

def run():
    st.title("🟢 Manual Power Control")

    # Manual mode control UI
    mode = st.radio("Select Manual Control Mode", ["Use Manual Control", "Exit Manual Control"], key="manual_mode")

    if mode == "Use Manual Control":
      if not get_value("led/manualcontrol"):
        delay_min = st.number_input("Enter time in minutes:", min_value=1, step=1)
        led_state = st.selectbox("Turn:", ["on", "off"], key="led_state_choice")
        if st.button("Submit Manual Command"):
         if check_wifi(): 
           with st.spinner('Sending command...'):
            update_value("led/delay", delay_min)
            update_value("led/manualcontrol", True)
            update_value("led/mn_st", 1 if led_state == "on" else 0)
            time.sleep(3)
            st.success("Manual control command sent.")
            tz=pytz.timezone('Asia/Karachi')
            now=datetime.now(tz)
            noted=now + timedelta(minutes=delay_min)
            update_value("fr_end/noted_time", noted.strftime("%H:%M"))
            time.sleep(2)
            st.rerun()
         else:
            st.error("Device is not connected to WiFi.")
      else:
         st.info("Manual control session is already running. If you want to enter new one, exit the manual control first.")
         
    elif mode == "Exit Manual Control":
        if st.button("Exit Manual Control", key="exit_manual"):
          if check_wifi():  
           with st.spinner('🔄 Exiting...'): 
            update_value("led/manualcontrol", False)
            time.sleep(3)
            st.success("Exited manual control.")
          else:
            st.error("Device is not connected to WiFi.")
       
