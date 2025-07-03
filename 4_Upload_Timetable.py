import streamlit as st
import os
import time
import pandas as pd
from firebase_utils import update_value, get_value, get_power_status, check_wifi
from timetable_parser import excel_to_timetable_string  # Renamed from csv_to_timetable_string

def run():
    st.title("📅 Upload Timetable")

    st.info("⚠️ Strictly follow the given format before uploading timetable. USE 2 HOURS FORMAT")

    # Sample XLSX download link
    sample_link = "https://docs.google.com/spreadsheets/d/1vK3Z0bKfTKKu9eT_yo6MBXcmpr-YEQ2N/export?format=xlsx"
    st.markdown(f"[⬇️ Download Sample Timetable XLSX]({sample_link})", unsafe_allow_html=True)

    # Show sample image (if available)
    image_path = "timetable_sample.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="Sample Timetable Format")

    # File uploader
    uploaded = st.file_uploader("📤 Upload your Timetable Excel file", type=["xlsx"])
    
    if uploaded:
        # Save the uploaded file temporarily
        excel_path = "temp_uploaded.xlsx"
        with open(excel_path, "wb") as f:
            f.write(uploaded.read())
        
        # Parse and validate timetable string
        output = excel_to_timetable_string(excel_path)
        required_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        if "Error" not in output and all(day in output for day in required_days):
            if check_wifi():
                with st.spinner('Processing...'):   
                    update_value("schedule_string", output)
                    update_value("sch_update", True)
                    time.sleep(5)
                    if get_value("sch_update") == False:
                        st.success("✅ Timetable uploaded successfully!")
                        if os.path.exists(excel_path):
                            os.remove(excel_path)
                    else:
                        st.error("❌ Failed to upload timetable to Firebase.")
                        update_value("sch_update", False)
            else:
                st.error("Device is not connected to Wi-Fi.")
                update_value("sch_update", False)
        else:
            st.error("❌ Incorrect timetable format. Make sure all days are included.")
            update_value("sch_update", False)
        
        # Clean up temporary file
        if os.path.exists(excel_path):
            os.remove(excel_path)

    # ----------------------------
    # 🗑️ Delete Timetable Section
    # ----------------------------

    st.markdown("---")  # Visual separator

    st.subheader("🗑️ Delete Timetable")

    if st.checkbox("⚠️ I confirm I want to delete the current timetable."):
        if st.button("Delete Timetable"):
            with st.spinner("Deleting timetable..."):
                    update_value("sch_del", True)
                    time.sleep(5)
                    if get_value("sch_del") == False:
                        st.success("✅ Timetable Deleted successfully!")
                    else:
                        st.error("❌ Failed to Delete timetable")
                        update_value("sch_del", False)
