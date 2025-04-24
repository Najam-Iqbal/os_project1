import streamlit as st
import os
import time
from firebase_utils import update_value, get_value, get_power_status
from timetable_parser import csv_to_timetable_string

def run():
    st.title("📅 Upload Timetable")

    # Power status
    try:
        if get_power_status():
            st.info("🔌 Power Status: ON")
        else:
            st.warning("⚡ Power Status: OFF")
    except:
        st.error("Unable to fetch power status due to WiFi issue.")

    st.info("⚠️ Strictly follow the given format before uploading timetable.")

    # Sample CSV download link
    sample_link = "https://drive.google.com/uc?export=download&id=1WD7XPlYo72T7pkhoZ1mkOyznk2iOWolwcIPRkqVTNN4"
    st.markdown(f"[⬇️ Download Sample Timetable CSV]({sample_link})", unsafe_allow_html=True)

    # Show sample image (if available)
    image_path = "timetable_sample.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="Sample Timetable Format")

    # File uploader
    uploaded = st.file_uploader("📤 Upload your Timetable CSV file", type=["csv"])
    if uploaded:
        csv_path = "temp_uploaded.csv"
        with open(csv_path, "wb") as f:
            f.write(uploaded.read())

        # Parse and validate timetable string
        output = csv_to_timetable_string(csv_path)
        required_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if "Error" not in output and all(day in output for day in required_days):
            if update_value("schedule_string", output):
                st.success("✅ Timetable uploaded successfully!")
            else:
                st.error("❌ Failed to upload timetable to Firebase.")
        else:
            st.error("❌ Incorrect timetable format. Make sure all days are included.")
