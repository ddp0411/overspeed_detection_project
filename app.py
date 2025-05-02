# app.py

import streamlit as st
import pandas as pd
import time
import os

DATA_PATH = 'data/vehicle_records.csv'

st.set_page_config(page_title="Overspeed Detection System", page_icon=":oncoming_automobile:", layout="wide")

st.title("🚗 Advanced Vehicle Overspeed Detection System")
st.markdown(" Real-Time Monitoring Dashboard")
st.markdown("---")

def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Plate Number", "Entry Time", "Exit Time", "Speed (kmph)", "Status"])


placeholder = st.empty()

while True:
    df = load_data()

    with placeholder.container():
        total = df.shape[0]
        overspeeded = df[df['Status'] == 'Overspeeding'].shape[0]
        normal = df[df['Status'] == 'Normal'].shape[0]

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Vehicles", total)
        with col2: st.metric("Overspeeded", overspeeded)
        with col3: st.metric("Normal Vehicles", normal)

        st.markdown("---")

        if not df.empty:
            st.dataframe(df.style.applymap(lambda x: 'background-color: #FF7F7F' if x=="Overspeeding" else 'background-color: #90EE90', subset=['Status']), use_container_width=True)
            st.bar_chart(df['Status'].value_counts())
        else:
            st.info("No vehicle detected yet...")

    time.sleep(10)
