import streamlit as st
from firebase_utils import update_value, get_value, get_power_status,check_wifi
import time

def run():
    st.title("🔐 Change Device Credentials / WiFi")

    option = st.radio("Select what you want to change:", ["Change Device name & Password", "Change WiFi"], key="change_option")

    if option == "Change Device name & Password":
      new_user = st.text_input("New Device name")
      new_pass = st.text_input("New Device Password (8-15 characters)", type="password")
      if st.button("Apply Changes", key="cred_change"):
        update_value("user_presence", True)
        if new_user and new_pass:
         if 8<= len(new_pass):
          with st.spinner('🔄 Updating...'):
           if check_wifi():   
                update_value("Esp32_configure/DeviceName", new_user)
                update_value("Esp32_configure/Password", new_pass)
                update_value("Esp32_configure/chg", True)
                time.sleep(5)
                if get_value("Esp32_configure/sr"):
                    st.success("Username and Password updated successfully.")
                    update_value("Esp32_configure/sr", False)
                else:
                    st.error("Error updating credentials.")
                    update_value("Esp32_configure/chg", False)
           else:
                st.error("Device is not connected to wifi.")
         else:
              st.error("Password must be between 8-15 characters")
        else:
            st.warning("Both fields are required.")
    elif option == "Change WiFi":
        ssid = st.text_input("New WiFi SSID")
        wifi_pass = st.text_input("New WiFi Password", type="password")
        if st.button("Apply Changes", key="wifi_change"):
         update_value("user_presence", True)
         if ssid and wifi_pass:
            update_value("Wifi_configure/SSID", ssid)
            update_value("Wifi_configure/Password", wifi_pass)
            update_value("Wifi_configure/chg", True)

            with st.spinner('🔄 Checking the connection...'):
                time.sleep(10)  # simulate wait while ESP tries to reconnect
                if get_value("Wifi_configure/sr") and check_wifi():
                    st.success("✅ WiFi credentials updated successfully.")
                    update_value("Wifi_configure/sr", False)
                else:
                    st.error("❌ Error updating WiFi credentials.")
         else:
            st.warning("⚠️ Both SSID and Password are required.")
