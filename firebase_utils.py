import streamlit as st
import requests
import json

# Firebase configuration
FIREBASE_URL = "https://esp-os-project-74989-default-rtdb.firebaseio.com"
API_KEY = "AIzaSyCwkisRlf3qT2X2lSIezZ4IQSqsdI4-avo"  # Replace with your actual API key

# === Firebase REST API Helper Functions ===
def firebase_request(method, path, data=None, device_id="Device_001"):
    """Generic Firebase REST API request handler"""
    url = f"{FIREBASE_URL}/{device_id}/{path}.json?auth={API_KEY}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError("Invalid HTTP method")
        
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        st.error(f"Firebase API error: {str(e)}")
        return None

# === Transformed Functions ===

def get_device_credentials(device_id="Device_001"):
    """Get device credentials using REST API"""
    data = firebase_request("GET", f"{device_id}/Esp32_configure")
    if data:
        return data.get("DeviceName"), data.get("Password")
    return None, None

def validate_login(input_device_name, input_password, device_id="Device_001"):
    """Validate login credentials using REST API"""
    stored_name, stored_password = get_device_credentials(device_id)
    return input_device_name == stored_name and input_password == stored_password

def get_value(path, device_id="Device_001"):
    """Read a value from Firebase using REST API"""
    return firebase_request("GET", f"{device_id}/{path}")

def update_value(path, value, device_id="Device_001"):
    """Update a value in Firebase using REST API"""
    result = firebase_request("PUT", f"{device_id}/{path}", value)
    return result is not None

def get_power_status(device_id="Device_001"):
    """Get power status using REST API"""
    state = firebase_request("GET", f"{device_id}/led/state")
    return state == 1 if state is not None else False

# === Example Usage in Streamlit ===
st.title("Firebase REST API with Streamlit")

# Example: Read and display device credentials
device_name, password = get_device_credentials()
if device_name and password:
    st.write(f"Device Name: {device_name}")
    st.write(f"Password: {'*' * len(password)}")

# Example: Toggle power status
if st.button("Toggle Power"):
    current_status = get_power_status()
    success = update_value("led/state", 0 if current_status else 1)
    if success:
        st.success("Power status updated!")
    else:
        st.error("Failed to update power status")
