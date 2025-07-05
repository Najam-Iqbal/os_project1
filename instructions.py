import streamlit as stl

stl.header("📶 How to Input WiFi Credentials to Your Device (Offline Mode)")

stl.markdown("""
Follow these steps to connect your device to WiFi when it is offline:

1. **Be near the device** (within approximately **15 meters**).
2. **Scan for available WiFi networks** on your phone or computer. You will see a network with the **same name as your device**.
3. **Connect to that network** using your device's default password.
4. Once connected, **[click here](http://192.168.4.1/)** to open the configuration page.
5. **Enter your WiFi credentials** (SSID and password) and submit.
""")

stl.warning("""
⚠️ Please double-check your WiFi credentials before submitting.  
If incorrect credentials are saved, the device will not be able to connect to WiFi in the future unless correct Credentials are provided again.
""")
