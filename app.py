# enhanced_app.py
import streamlit as st
import pandas as pd
import time
import os
import json
from datetime import datetime
import plotly.express as px

# File paths

DATA_PATH = r'C:\Users\HP\OneDrive\Desktop\overspeed_detection_project\demo_vehicle_records_10000_varied_time.csv'

USER_DB = 'data/users.json'

# Streamlit app config
st.set_page_config(
    page_title="Overspeed Detection System",
    page_icon=":oncoming_automobile:",
    layout="wide"
)

# Load vehicle data from CSV
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["Plate", "Entry_Time", "Exit_Time", "Time_Taken_sec", "Speed_kmph", "Status"])

# Load user credentials from JSON
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as f:
            return json.load(f)
    else:
        return {"admin": "admin123"}  # default user

# Optional user login with validation
def user_login():
    st.sidebar.title("🔐 User Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    users = load_users()
    if login_button:
        if username in users and users[username] == password:
            st.sidebar.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.sidebar.error("Invalid credentials")
            st.session_state.logged_in = False

# Main dashboard UI
def render_dashboard():
    st.markdown(f"""
        <h1 style='text-align: center; color: #ff4c4c;'>🚘 Advanced Vehicle Overspeed Detection System</h1>
        <h4 style='text-align: center;'>Logged in as: {st.session_state.username}</h4>
        <hr style='border-top: 3px solid #bbb;'>
    """, unsafe_allow_html=True)

    if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    placeholder = st.empty()

    while True:
        df = load_data()
        with placeholder.container():
            total = df.shape[0]
            overspeeded = df[df['Status'] == 'Overspeeding'].shape[0]
            normal = df[df['Status'] == 'Normal'].shape[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🚗 Total Vehicles", total)
            with col2:
                st.metric("⚠️ Overspeeded", overspeeded)
            with col3:
                st.metric("✅ Normal Vehicles", normal)

            st.markdown("---")

            if not df.empty:
                # Search and Filter Section
                st.subheader("🔍 Search & Filter")
                search_plate = st.text_input("Search by Plate Number")
                filter_status = st.selectbox("Filter by Status", ["All", "Overspeeding", "Normal"])

                filtered_df = df.copy()
                if search_plate:
                    filtered_df = filtered_df[filtered_df['Plate'].str.contains(search_plate, case=False)]
                if filter_status != "All":
                    filtered_df = filtered_df[filtered_df['Status'] == filter_status]

                # Data Table
                st.subheader("📋 Detected Vehicles Log")
                st.dataframe(
                    filtered_df.style.applymap(
                        lambda x: 'background-color: #FFCCCC' if x == "Overspeeding" else 'background-color: #CCFFCC',
                        subset=['Status']
                    ),
                    use_container_width=True
                )

                # CSV Download
                st.download_button(
                    label="📥 Download CSV",
                    data=filtered_df.to_csv(index=False),
                    file_name='vehicle_records.csv',
                    mime='text/csv'
                )

                st.markdown("---")
                st.subheader("📊 Speed Violation Analytics")

                colA, colB = st.columns(2)
                with colA:
                    fig1 = px.histogram(filtered_df, x="Speed_kmph", color="Status",
                                        nbins=20, title="Distribution of Vehicle Speeds",
                                        labels={"Speed_kmph": "Speed (km/h)"},
                                        template="plotly_dark")
                    st.plotly_chart(fig1, use_container_width=True)

                with colB:
                    fig2 = px.pie(filtered_df, names="Status", title="Speeding vs Normal Vehicles",
                                 color_discrete_sequence=["#FF7F7F", "#90EE90"])
                    st.plotly_chart(fig2, use_container_width=True)

                st.markdown("---")
                st.subheader("📈 Average Speed Over Time")
                filtered_df['Entry_Time'] = pd.to_datetime(filtered_df['Entry_Time'], errors='coerce')
                df_sorted = filtered_df.sort_values(by='Entry_Time')
                line_chart = px.line(df_sorted, x='Entry_Time', y='Speed_kmph', title='Average Speed Over Time', template='plotly_dark')
                st.plotly_chart(line_chart, use_container_width=True)

            else:
                st.info("No vehicle data detected yet...")

        time.sleep(10)

# --- APP START ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

if st.session_state.logged_in:
    render_dashboard()
else:
    user_login()
