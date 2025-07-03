import streamlit as st
import os
import time
import pandas as pd
from firebase_utils import update_value, get_value, get_power_status, check_wifi
from timetable_parser import excel_to_timetable_string

def run():
    st.title("📅 Upload Timetable")

    st.info("⚠️ Strictly follow the given format before uploading timetable. USE 24 HOURS FORMAT")

    # Sample XLSX download link
    sample_link = "https://docs.google.com/spreadsheets/d/1vK3Z0bKfTKKu9eT_yo6MBXcmpr-YEQ2N/export?format=xlsx"
    st.markdown(f"[⬇️ Download Sample Timetable XLSX]({sample_link})", unsafe_allow_html=True)

    # Show sample image
    image_path = "timetable_sample.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="Sample Timetable Format")

    # Upload
    uploaded = st.file_uploader("📤 Upload your Timetable Excel file", type=["xlsx"])
    
    if uploaded:
        excel_path = "temp_uploaded.xlsx"
        with open(excel_path, "wb") as f:
            f.write(uploaded.read())

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
                    else:
                        st.error("❌ Failed to upload timetable to Firebase.")
                        update_value("sch_update", False)
            else:
                st.error("Device is not connected to Wi-Fi.")
                update_value("sch_update", False)
        else:
            st.error("❌ Incorrect timetable format. Make sure all days are included.")
            update_value("sch_update", False)

        if os.path.exists(excel_path):
            os.remove(excel_path)

    # ----------------------------
    # 🗑️ Delete Timetable Section
    # ----------------------------

    st.markdown("---")
    st.subheader("🗑️ Delete Timetable")

    if st.checkbox("⚠️ I confirm I want to delete the current timetable."):
        if st.button("Delete Timetable"):
            with st.spinner("Deleting timetable..."):
                update_value("sch_del", True)
                time.sleep(5)
                if get_value("sch_del") == False:
                    st.success("✅ Timetable deleted successfully!")
                else:
                    st.error("❌ Failed to delete timetable.")
                    update_value("sch_del", False)

    # ----------------------------
    # 📄 View Current Timetable Section
    # ----------------------------

    st.markdown("---")
    st.subheader("📄 View Current Timetable")

    if st.button("📖 Show Current Timetable"):
        with st.spinner("Loading current timetable..."):
            try:
                timetable = get_value("schedule_string")
                if timetable and len(timetable.strip()) > 0:
                    st.success("✅ Current Timetable:")
                    st.text_area("🕒 Timetable Contents", timetable, height=300)
                else:
                    st.warning("⚠️ No timetable currently stored.")
            except Exception as e:
                st.error(f"❌ Failed to fetch timetable: {str(e)}")
