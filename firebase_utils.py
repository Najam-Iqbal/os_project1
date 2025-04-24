import streamlit as st
from streamlit.components.v1 import html
import json

# Firebase configuration (replace with your actual config)
firebase_config = {
    apiKey: "AIzaSyCwkisRlf3qT2X2lSIezZ4IQSqsdI4-avo",
    authDomain: "esp-os-project-74989.firebaseapp.com",
    databaseURL: "https://esp-os-project-74989-default-rtdb.firebaseio.com",
    projectId: "esp-os-project-74989",
    storageBucket: "esp-os-project-74989.firebasestorage.app",
    messagingSenderId: "24577304201",
    appId: "1:24577304201:web:0848f6aabe8e4940a40858"
}

# JavaScript code with Firebase initialization and functions
firebase_js = f"""
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-database-compat.js"></script>

<script>
  // Initialize Firebase
  const firebaseApp = firebase.initializeApp({json.dumps(firebase_config)});
  const database = firebase.database();

  // Store the last result for Streamlit to access
  let lastResult = null;

  // Function to get device credentials
  async function getDeviceCredentials(deviceId = "Device_001") {{
    try {{
      const snapshot = await database.ref(`${{deviceId}}/Esp32_configure`).once('value');
      const data = snapshot.val();
      lastResult = data ? {{name: data.DeviceName, password: data.Password}} : null;
      return lastResult;
    }} catch (error) {{
      console.error("Error fetching credentials:", error);
      lastResult = {{error: error.message}};
      return null;
    }}
  }}

  // Function to update values
  async function updateValue(path, value, deviceId = "Device_001") {{
    try {{
      await database.ref(`${{deviceId}}/${{path}}`).set(value);
      lastResult = {{success: true}};
      return true;
    }} catch (error) {{
      console.error("Update error:", error);
      lastResult = {{error: error.message}};
      return false;
    }}
  }}

  // Function to get power status
  async function getPowerStatus(deviceId = "Device_001") {{
    try {{
      const snapshot = await database.ref(`${{deviceId}}/led/state`).once('value');
      lastResult = {{status: snapshot.val() === 1}};
      return snapshot.val() === 1;
    }} catch (error) {{
      console.error("Error reading power status:", error);
      lastResult = {{error: error.message}};
      return false;
    }}
  }}

  // Make functions available to window for Streamlit access
  window.firebaseFunctions = {{
    getDeviceCredentials,
    updateValue,
    getPowerStatus,
    getLastResult: () => lastResult
  }};
</script>
"""

# Initialize Firebase (injects the JS code)
html(firebase_js, height=0)

# Function to call JS functions and get results
def call_js_function(function_name, *args):
    # Generate a unique ID for this call
    call_id = f"call_{hash((function_name, args))}"
    
    js_code = f"""
    <script>
        window.firebaseFunctions['{function_name}']({','.join(json.dumps(arg) for arg in args)})
            .then(result => {{
                // Store result with call ID
                window.resultStore = window.resultStore || {{}};
                window.resultStore['{call_id}'] = {{
                    status: 'completed',
                    result: window.firebaseFunctions.getLastResult()
                }};
            }})
            .catch(error => {{
                window.resultStore = window.resultStore || {{}};
                window.resultStore['{call_id}'] = {{
                    status: 'error',
                    error: error.message
                }};
            }});
    </script>
    """
    
    # Inject the JavaScript
    html(js_code)
    
    # Return the call ID for result retrieval
    return call_id

# Function to get JS function result
def get_js_result(call_id):
    result_js = f"""
    <script>
        const result = window.resultStore && window.resultStore['{call_id}'];
        if (result) {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: result,
                callId: '{call_id}'
            }}, '*');
        }}
    </script>
    """
    
    # Create a placeholder for the result
    result_placeholder = st.empty()
    result_placeholder.markdown(result_js, unsafe_allow_html=True)
    
    # Use Streamlit's session state to store results
    if 'js_results' not in st.session_state:
        st.session_state.js_results = {}
    
    # Check if we have a result
    return st.session_state.js_results.get(call_id)

# === Transformed Functions ===

def get_device_credentials(device_id="Device_001"):
    """Get device credentials using Firebase JS SDK"""
    call_id = call_js_function("getDeviceCredentials", device_id)
    result = get_js_result(call_id)
    if result and result.get('status') == 'completed':
        creds = result.get('result', {})
        return creds.get('name'), creds.get('password')
    return None, None

def validate_login(input_device_name, input_password, device_id="Device_001"):
    """Validate login credentials"""
    stored_name, stored_password = get_device_credentials(device_id)
    return input_device_name == stored_name and input_password == stored_password

def get_value(path, device_id="Device_001"):
    """Read a value from Firebase"""
    # This would need a separate JS function implementation
    # Similar pattern as get_device_credentials
    pass

def update_value(path, value, device_id="Device_001"):
    """Update a value in Firebase"""
    call_id = call_js_function("updateValue", path, value, device_id)
    result = get_js_result(call_id)
    return result and result.get('status') == 'completed'

def get_power_status(device_id="Device_001"):
    """Get power status"""
    call_id = call_js_function("getPowerStatus", device_id)
    result = get_js_result(call_id)
    if result and result.get('status') == 'completed':
        return result.get('result', {}).get('status', False)
    return False

# === Example Usage in Streamlit ===
st.title("Firebase JavaScript SDK with Streamlit")

# Example: Read and display device credentials
device_name, password = get_device_credentials()
if device_name and password:
    st.write(f"Device Name: {device_name}")
    st.write(f"Password: {'*' * len(password)}")

# Example: Toggle power status
if st.button("Toggle Power"):
    current_status = get_power_status()
    # Python ternary syntax: value_if_true if condition else value_if_false
    new_value = 0 if current_status else 1
    success = update_value("led/state", new_value)  # Fixed line
    if success:
        st.success("Power status updated!")
    else:
        st.error("Failed to update power status")

# JavaScript to handle results (inject once)
result_handler_js = """
<script>
    window.addEventListener('message', (event) => {
        if (event.data.type === 'streamlit:setComponentValue') {
            // Store result in Streamlit's session state
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                key: 'js_result_' + event.data.callId,
                value: event.data.value
            }, '*');
        }
    });
</script>
"""
html(result_handler_js)
