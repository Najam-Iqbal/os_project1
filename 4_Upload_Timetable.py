import streamlit as st
import os
import time
import pandas as pd
from firebase_utils import update_value, get_value, get_power_status,check_wifi
from timetable_parser import excel_to_timetable_string  # Renamed from csv_to_timetable_string

def run():
    st.title("📅 Upload Timetable")

    st.info("⚠️ Strictly follow the given format before uploading timetable.")

    # Sample XLSX download link (update this with your actual sample file)
    sample_link = "https://drive.google.com/uc?export=download&id=YOUR_XLSX_FILE_ID"
    st.markdown(f"[⬇️ Download Sample Timetable XLSX]({sample_link})", unsafe_allow_html=True)

    # Show sample image (if available)
    image_path = "timetable_sample.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="Sample Timetable Format")

    # File uploader - changed to accept xlsx
    uploaded = st.file_uploader("📤 Upload your Timetable Excel file", type=["xlsx"])
    
    if uploaded:
        # Save the uploaded file temporarily
        excel_path = "temp_uploaded.xlsx"
        with open(excel_path, "wb") as f:
            f.write(uploaded.read())

        # Parse and validate timetable string
        output = excel_to_timetable_string(excel_path)  # Changed function name
        st.success(output)
        required_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        if "Error" not in output and all(day in output for day in required_days):
            if update_value("schedule_string", output):
                st.success("✅ Timetable uploaded successfully!")
                # Remove temporary file
                if os.path.exists(excel_path):
                    os.remove(excel_path)
            else:
                st.error("❌ Failed to upload timetable to Firebase.")
        else:
            st.error("❌ Incorrect timetable format. Make sure all days are included.")
        
        # Clean up temporary file
        if os.path.exists(excel_path):
            os.remove(excel_path)
