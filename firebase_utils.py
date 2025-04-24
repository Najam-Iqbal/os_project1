import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, db  # ✅ Added db here
import json
import tempfile
import time
# === Initialize Firebase ===
try:
    firebase_admin.get_app()
   # st.success("Firebase already initialized")
except ValueError:
    try:
        st.info("Initializing Firebase...")

        # Extract secrets from st.secrets and write to a temporary file
        firebase_secrets = dict(st.secrets["firebase"])

        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tmp:
            # Write the secrets as a proper JSON file
            json.dump(firebase_secrets, tmp)
            tmp.flush()  # Ensures data is written to disk
            cred = credentials.Certificate(tmp.name)

        # Initialize Firebase app with RTDB URL
        initialize_app(cred, {
            'databaseURL': 'https://esp-os-project-74989-default-rtdb.firebaseio.com/'
        })

        #st.success("✅ Firebase Initialized")

    except Exception as e:
        st.error(f"Firebase init error: {e}")

# === Firebase Read and Write Functions ===

def check_wifi_status():
    if "show_wifi_status" not in st.session_state:
        st.session_state.show_wifi_status = False
        st.session_state.wifi_checked_at = None
        st.session_state.wifi_prev_value = None
        st.session_state.wifi_result = ""

    if st.button("📶 Check WiFi Status"):
        st.session_state.show_wifi_status = True
        st.session_state.wifi_checked_at = time.time()

        # Get initial value
        prev = get_value("wifi_status")
        st.session_state.wifi_prev_value = prev

        with st.spinner("🔄 Checking WiFi connectivity... please wait 5 seconds"):
            time.sleep(5)
            new = get_value("wifi_status")

        if new != prev:
            st.session_state.wifi_result = "✅ Device connected to the internet."
        else:
            st.session_state.wifi_result = "❌ No internet connection."

    if st.session_state.show_wifi_status:
        st.info(st.session_state.wifi_result)

        if time.time() - st.session_state.wifi_checked_at > 3:
            st.session_state.show_wifi_status = False
            st.experimental_rerun()

def get_device_credentials(device_id="Device_001"):
    try:
        ref = db.reference(f"{device_id}/Esp32_configure")
        data = ref.get()
        if data:
            return data.get("DeviceName"), data.get("Password")
        else:
            return None, None
    except Exception as e:
        st.error(f"Error fetching device credentials: {e}")
        return None, None

def validate_login(input_device_name, input_password, device_id="Device_001"):
    stored_name, stored_password = get_device_credentials(device_id)
    return input_device_name == stored_name and input_password == stored_password

def get_value(path, device_id="Device_001"):
    try:
        ref = db.reference(f"{device_id}/{path}")
        return ref.get()
    except Exception as e:
        st.error(f"Failed to read from Firebase: {e}")
        return None

def update_value(path, value, device_id="Device_001"):
    try:
        ref = db.reference(f"{device_id}/{path}")
        ref.set(value)
        return True
    except Exception as e:
        st.error(f"Failed to update Firebase: {e}")
        return False


def get_power_status():
    try:
        ref = db.reference("Device_001/led/state")
        state = ref.get()
        return state == 1
    except Exception as e:
        print("Error reading power status:", e)
        return False


