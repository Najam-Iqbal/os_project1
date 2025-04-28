import streamlit as st
import os
import time
import pandas as pd
from firebase_utils import update_value, get_value, get_power_status,check_wifi
from timetable_parser import excel_to_timetable_string  # Renamed from csv_to_timetable_string

def run():
    st.title("📅 Upload Timetable")

    st.info("⚠️ Strictly follow the given format before uploading timetable. USE 24 HOURS FORMAT")

    # Sample XLSX download link (update this with your actual sample file)
    sample_link = "https://1drv.ms/x/c/de99ff54dc50bb1a/EeSjj9GhO-BAk6Hf0Qu7hewBqoGlFljaquSCcuXm_2-KFA?e=ZDvR3C"
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
        required_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        if "Error" not in output and all(day in output for day in required_days):
          if check_wifi():
           with st.spinner('Processing...'):   
            update_value("schedule_string", output)
            update_value("sch_update", True)
            time.sleep(5)
            if get_value("sch_update")==False:
                st.success("✅ Timetable uploaded successfully!")
                # Remove temporary file
                if os.path.exists(excel_path):
                    os.remove(excel_path)
            else:
                st.error("❌ Failed to upload timetable to Firebase.")
                update_value("sch_update", False)
          else:
              st.error("Devic is not connected to Wi-Fi.")
              update_value("sch_update", False)
        else:
            st.error("❌ Incorrect timetable format. Make sure all days are included.")
            update_value("sch_update", False)
        
        # Clean up temporary file
        if os.path.exists(excel_path):
            os.remove(excel_path)
