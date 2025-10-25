




# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import os

# st.set_page_config(page_title="Incident Reporter", layout="centered")
# st.title("📝 Report an Incident")

# # CSV file path
# CSV_FILE = "reports.csv"

# # --- Incident Report Form ---
# with st.form("incident_report_form"):
#     category = st.selectbox("Select Incident Category", ["Crime", "Disaster", "Traffic", "Weather"])
#     report_title = st.text_input("Incident Title")
#     report_description = st.text_area("Description of the Incident")
#     report_location = st.text_input("Location (e.g., Street, City, Pincode)")
#     submitted = st.form_submit_button("Submit Report")

#     if submitted:
#         if report_title and report_description and report_location:
#             report_data = {
#                 "id": datetime.now().strftime("%Y%m%d%H%M%S"),
#                 "category": category,
#                 "title": report_title,
#                 "description": report_description,
#                 "location": report_location,
#                 "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             }

#             # Save to CSV
#             if os.path.exists(CSV_FILE):
#                 df = pd.read_csv(CSV_FILE)
#                 df = pd.concat([df, pd.DataFrame([report_data])], ignore_index=True)
#             else:
#                 df = pd.DataFrame([report_data])
#             df.to_csv(CSV_FILE, index=False)

#             st.success("✅ Your report has been submitted successfully!")
#         else:
#             st.error("❌ Please fill in all the fields.")



import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Incident Reporter", layout="centered")
st.title("Report an Incident")

# CSV file path
CSV_FILE = "reports.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create upload folder if not exists

# --- Incident Report Form ---
with st.form("incident_report_form"):
    category = st.selectbox("Select Incident Category", ["Crime", "Disaster", "Traffic", "Weather"])
    report_title = st.text_input("Incident Title")
    report_description = st.text_area("Description of the Incident")
    report_location = st.text_input("Location (e.g., Street, City, Pincode)")
    uploaded_file = st.file_uploader("Upload Image or Video (Optional)", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        if report_title and report_description and report_location:
            file_path = ""

            # Save uploaded file if exists
            if uploaded_file is not None:
                # Create a unique file name with timestamp
                file_extension = uploaded_file.name.split(".")[-1]
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                file_path = os.path.join(UPLOAD_DIR, unique_filename)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

            # Prepare report data
            report_data = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "category": category,
                "title": report_title,
                "description": report_description,
                "location": report_location,
                "file": file_path,  # Save file path in CSV
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Pending"
            }

            # Save to CSV
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE)
                df = pd.concat([df, pd.DataFrame([report_data])], ignore_index=True)
            else:
                df = pd.DataFrame([report_data])
            df.to_csv(CSV_FILE, index=False)

            st.success("Your report has been submitted successfully!")
        else:
            st.error("Please fill in all the fields.")
