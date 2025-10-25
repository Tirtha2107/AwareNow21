

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def admiin():
    st.set_page_config(page_title="Admin - Incident Review", layout="centered")
    st.title("Admin Panel: Incident Review")
    csv_path = "feedback_responses.csv"
    try:
        df = pd.read_csv(csv_path)
        st.subheader("Feedback Response")
        st.dataframe(df.head(6))  
    except FileNotFoundError:
        st.warning("CSV file not found.")

    CSV_FILE = "reports.csv"

    csv_path = "user_logins_awarenow.csv"
    try:
        df = pd.read_csv(csv_path)
        st.subheader("User Register")
        st.dataframe(df.head(10))  
    except FileNotFoundError:
        st.warning("CSV file not found.")

    CSV_FILE = "reports.csv"

    # Load or initialize data
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        st.warning("No reports found.")
        st.stop()

    # Ensure status column exists
    if "status" not in df.columns:
        df["status"] = "Pending"

    # Show only pending reports
    pending_df = df[df["status"] == "Pending"]

    if pending_df.empty:
        st.success("All incidents have been reviewed.")
    else:
        for index, row in pending_df.iterrows():
            with st.expander(f" {row['title']} ({row['category']})"):
                st.markdown(f"Description: {row['description']}")
                st.markdown(f" Location:{row['location']}")
                st.markdown(f" Date: {row['date']}")

                # Show uploaded file if exists
                if "file" in row and isinstance(row["file"], str) and os.path.exists(row["file"]):
                    file_ext = row["file"].split('.')[-1].lower()
                    st.markdown(" Uploaded File:")

                    if file_ext in ["jpg", "jpeg", "png"]:
                        st.image(row["file"], use_column_width=True)
                    elif file_ext in ["mp4", "mov", "avi"]:
                        st.video(row["file"])
                    else:
                        st.write(f" File: {os.path.basename(row['file'])}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(" Mark as Reviewed", key=f"review_{index}"):
                        df.at[index, "status"] = "Reviewed"
                        df.to_csv(CSV_FILE, index=False)
                        st.success("Marked as Reviewed.")
                        st.rerun()

                with col2:
                    if st.button(" Reject", key=f"reject_{index}"):
                        df.at[index, "status"] = "Rejected"
                        df.to_csv(CSV_FILE, index=False)
                        st.error("Report Rejected.")
                        st.rerun()


# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime

# def admiin():
#     st.set_page_config(page_title="Admin - Incident Review", layout="centered")
#     st.title("Admin Panel: Incident Review")

#     CSV_FILE = "reports.csv"

#     # Load or initialize data
#     if os.path.exists(CSV_FILE):
#         df = pd.read_csv(CSV_FILE)
#     else:
#         st.warning("No reports found.")
#         st.stop()

#     # Ensure status column exists
#     if "status" not in df.columns:
#         df["status"] = "Pending"

#     # Show only pending reports
#     pending_df = df[df["status"] == "Pending"]

#     if pending_df.empty:
#         st.success("All incidents have been reviewed.")
#     else:
#         for index, row in pending_df.iterrows():
#             with st.expander(f" {row['title']} ({row['category']})"):
#                 st.markdown(f"Description: {row['description']}")
#                 st.markdown(f" Location:{row['location']}")
#                 st.markdown(f" Date: {row['date']}")

#                 # Show uploaded file if exists
#                 if "file" in row and isinstance(row["file"], str) and os.path.exists(row["file"]):
#                     file_ext = row["file"].split('.')[-1].lower()
#                     st.markdown(" Uploaded File:")

#                     if file_ext in ["jpg", "jpeg", "png"]:
#                         st.image(row["file"], use_column_width=True)
#                     elif file_ext in ["mp4", "mov", "avi"]:
#                         st.video(row["file"])
#                     else:
#                         st.write(f" File: {os.path.basename(row['file'])}")

#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button(" Mark as Reviewed", key=f"review_{index}"):
#                         df.at[index, "status"] = "Reviewed"
#                         df.to_csv(CSV_FILE, index=False)
#                         st.success("Marked as Reviewed.")
#                         st.rerun()

#                 with col2:
#                     if st.button(" Reject", key=f"reject_{index}"):
#                         df.at[index, "status"] = "Rejected"
#                         df.to_csv(CSV_FILE, index=False)
#                         st.error("Report Rejected.")
#                         st.rerun()


