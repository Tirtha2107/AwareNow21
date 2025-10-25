

import streamlit as st
import pandas as pd
import base64
import random
from datetime import datetime
from pathlib import Path
import time


start_time = time.time()


USER_LOGINS_FILE_CSV = 'user_logins_awarenow.csv'
USER_LOGINS_FILE_EXCEL = 'user_logins_awarenow.xlsx'
ADMIN_ID = "AwareNow"
ADMIN_PASSWORD = "2107"
IMG_PATH = "background_img.png"  # Move your image here from OneDrive!


@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning("⚠️ Background image not found.")
        return ""

@st.cache_data
def read_user_logins():
    try:
        return pd.read_csv(USER_LOGINS_FILE_CSV)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            'user_id', 'first_name', 'last_name', 'age', 'location', 
            'email', 'password', 'login_time', 'logout_time', 'feedback'
        ])


def append_new_user(first_name, last_name, email, password):
    df = read_user_logins()
    new_user_id = df['user_id'].max() + 1 if not df.empty else 1001
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

    new_user_data = {
        'user_id': new_user_id,
        'first_name': first_name,
        'last_name': last_name,
        'age': '',
        'location': '',
        'email': email,
        'password': password,
        'login_time': current_time,
        'logout_time': '',
        'feedback': ''
    }

    df = pd.concat([df, pd.DataFrame([new_user_data])], ignore_index=True)

    try:
        df.to_csv(USER_LOGINS_FILE_CSV, index=False)
        df.to_excel(USER_LOGINS_FILE_EXCEL, index=False)
        st.success(f"✅ Registration successful for {first_name} {last_name}! You can now log in.")
        return True
    except Exception as e:
        st.error(f"❌ Error saving user data: {e}")
        return False


img_base64 = get_base64_image(IMG_PATH)

def set_background():
    if not st.session_state.get("logged_in", False):
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

        # Custom CSS
        custom_css = """
        <style>
        div[data-testid="stRadio"] > label {
            font-size: 22px;
            color: #25043B;
            font-weight: bold;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label[data-baseweb="radio"] {
            background-color: black;
            border-radius: 10px;
            padding: 8px 14px;
            margin: 5px 0;
            font-size: 18px;
            font-weight: 500;
            color: #25043B;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label[aria-checked="true"] {
            background-color: #FF6F61 !important;
            color: white !important;
            font-weight: bold;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_email = None
    st.session_state.language_selected = False
    st.session_state.user_name = ""

set_background()


if not st.session_state.language_selected:
    st.markdown("<h1 style='text-align: center; color: #25043B;'>AwareNow</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #25043B;'>Real-Time Local Alert and Safety Information System</h4>", unsafe_allow_html=True)

    if st.button("Get Started"):
        st.session_state.language_selected = True
        st.rerun()
    st.stop()

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #25043B;'>User/Admin Login Portal</h2>", unsafe_allow_html=True)
    choice = st.radio("Login as:", ['Admin', 'User'])

    # --- Admin Login ---
    if choice == 'Admin':
        with st.form("admin_form"):
            admin_id = st.text_input("Admin ID")
            admin_password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if admin_id == ADMIN_ID and admin_password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'Admin'
                    st.success("✅ Admin login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Admin ID or Password")

    # --- User Login/Register ---
    elif choice == 'User':
        user_action = st.radio("Select:", ['Login', 'Register'])

        # User Login
        if user_action == 'Login':
            with st.form("user_login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    df = read_user_logins()
                    user = df[(df['email'] == email) & (df['password'] == password)]
                    if not user.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_type = 'User'
                        st.session_state.user_email = email
                        st.session_state.user_name = user.iloc[0]['first_name'] + " " + user.iloc[0]['last_name']
                        st.success(f"🎉 Welcome back, {st.session_state.user_name}!")
                        st.rerun()
                    else:
                        st.error("❌ Incorrect email or password.")

        # User Register
        elif user_action == 'Register':
            with st.form("user_register_form"):
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Register"):
                    if not first_name or not last_name or not new_email or not new_password:
                        st.error("⚠️ All fields are required.")
                    elif len(new_password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long.")
                    else:
                        df = read_user_logins()
                        if new_email in df['email'].values:
                            st.error("⚠️ This email is already registered. Please log in.")
                        else:
                            append_new_user(first_name, last_name, new_email, new_password)


else:
    st.sidebar.header(f"Logged in as: {st.session_state.user_type}")
    if st.session_state.user_type == 'User':
        st.sidebar.markdown(f"{st.session_state.user_email}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.user_email = None
        st.session_state.language_selected = False
        st.session_state.user_name = ""
        st.success("👋 Logged out successfully.")
        st.rerun()

    if st.session_state.user_type == 'Admin':
        from admin import admiin
        st.header("🛠️ Admin Dashboard")
        admiin()

    elif st.session_state.user_type == 'User':
        from projectfront2 import show_dashboard
        st.write(f"Welcome, **{st.session_state.user_name}**! You are now logged in.")
        show_dashboard()


print("✅ login.py loaded in", round(time.time() - start_time, 2), "seconds")
