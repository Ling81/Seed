import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Function to save data to CSV
def save_data_to_csv(data, filename="session_data.csv"):
    df = pd.DataFrame([data])  # Convert dictionary to DataFrame
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Append data
    else:
        df.to_csv(filename, mode='w', header=True, index=False)  # Create new file
    st.success("✅ Data saved successfully!")

# Sidebar navigation
st.sidebar.title("📊 Data Collection Tool")
menu = st.sidebar.radio("Go to", ["Session Details", "Cold Probe Data", "Trial-by-Trial Data", "Task Analysis", "Behavior Duration Tracking", "Progress & Reports"])

# 1️⃣ Session Details
if menu == "Session Details":
    st.header("📝 Session Details")

    date = st.date_input("Date", value=pd.Timestamp.today().date())
    therapist_name = st.text_input("Therapist’s Name")

    # Define available time slots from 9:00 AM to 5:30 PM
    time_slots = [
        "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
        "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM",
        "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"
    ]

    start_time = st.selectbox("Start Time", time_slots, index=0)
    end_time = st.selectbox("End Time", time_slots, index=len(time_slots) - 1)

    if st.button("💾 Save Session Details"):
        session_data = {
            "Date": date,
            "Start Time": start_time,
            "End Time": end_time,
            "Therapist": therapist_name
        }
        save_data_to_csv(session_data)

# 2️⃣ Cold Probe Data
elif menu == "Cold Probe Data":
    st.header("🧊 Cold Probe Data")

    domains = st.text_input("Enter domains (comma-separated)").split(',')
    targets = st.text_input("Enter targets (comma-separated)").split(',')

    response_options = ["Y", "N", "NA"]
    response_data = {}

    for domain in domains:
        st.subheader(f"📂 {domain.strip()}")
        for target in targets:
            response = st.selectbox(f"{target.strip()}", response_options, key=f"{domain}_{target}")
            response_data[target] = response

    if st.button("💾 Save Cold Probe Data"):
        save_data_to_csv(response_data)

# 3️⃣ Trial-by-Trial Data
elif menu == "Trial-by-Trial Data":
    st.header("🎯 Trial-by-Trial Data

              
