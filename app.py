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
menu = st.sidebar.radio("Go to", [
    "Session Details", 
    "Cold Probe Data", 
    "Trial-by-Trial Data", 
    "Task Analysis", 
    "Behavior Duration Tracking", 
    "Progress & Reports"
])

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

    targets = st.text_input("Enter targets (comma-separated)").split(',')
    response_options = ["Y", "N", "NA"]
    response_data = {}

    for target in targets:
        response = st.selectbox(f"{target.strip()}", response_options, key=target)
        response_data[target] = response

    if st.button("💾 Save Cold Probe Data"):
        save_data_to_csv(response_data)

# 3️⃣ Trial-by-Trial Data
elif menu == "Trial-by-Trial Data":
    st.header("🎯 Trial-by-Trial Data")

    targets = st.text_input("Enter up to 10 targets (comma-separated)").split(',')
    trial_options = ["+", "p", "-", "I"]
    trial_data = {}

    for target in targets[:10]:  # Limit to 10 targets
        trials = []
        for i in range(10):  # 10 trials per target
            trial = st.selectbox(f"{target.strip()} - Trial {i+1}", trial_options, key=f"{target}_T{i}")
            trials.append(trial)
        trial_data[target] = trials

    if st.button("💾 Save Trial-by-Trial Data"):
        save_data_to_csv(trial_data)

# 4️⃣ Task Analysis
elif menu == "Task Analysis":
    st.header("📋 Task Analysis")

    steps = st.text_input("Enter task steps (comma-separated)").split(',')
    prompt_levels = ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"]
    task_data = {}

    for step in steps:
        prompt = st.selectbox(f"Prompt Level for {step.strip()}", prompt_levels, key=step)
        task_data[step] = prompt

    if st.button("💾 Save Task Analysis Data"):
        save_data_to_csv(task_data)

# 5️⃣ Behavior Duration Tracking
elif menu == "Behavior Duration Tracking":
    st.header("⏳ Behavior Duration Tracking")

    if "start_time" not in st.session_state:
        st.session_state["start_time"] = None
    if "duration_list" not in st.session_state:
        st.session_state["duration_list"] = []

    if st.button("▶ Start Timer"):
        st.session_state["start_time"] = pd.Timestamp.now()
        st.success("Timer Started!")

    if st.button("⏹ Stop Timer"):
        if st.session_state["start_time"]:
            duration = (pd.Timestamp.now() - st.session_state["start_time"]).seconds
            st.session_state["duration_list"].append(duration)
            st.session_state["start_time"] = None
            st.success(f"🕒 Episode Duration: {duration} seconds")

    total_duration = sum(st.session_state["duration_list"])
    st.write(f"📊 **Total Duration Tracked:** {total_duration} seconds")

    if st.button("💾 Save Behavior Duration"):
        save_data_to_csv({"Total Duration (s)": total_duration})

# 6️⃣ Progress & Reports
elif menu == "Progress & Reports":
    st.header("📈 Progress & Reports")

    # Load saved data if available
    if os.path.exists("session_data.csv"):
        df = pd.read_csv("session_data.csv")
        st.write("📋 **Session Data Overview**")
        st.dataframe(df)

        # Generate cumulative graph
        if "Date" in df.columns and "Total Duration (s)" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")
            plt.figure(figsize=(10, 5))
            plt.plot(df["Date"], df["Total Duration (s)"].cumsum(), marker="o", linestyle="-", color="b")
            plt.xlabel("Date")
            plt.ylabel("Cumulative Duration (s)")
            plt.title("📈 Cumulative Graph: Behavior Duration Over Time")
            plt.grid()
            st.pyplot(plt)

    # Auto-Generated Session Notes
    if st.button("📄 Generate Session Notes"):
        if "Date" in df.columns and "Therapist" in df.columns:
            latest_session = df.iloc[-1]  # Get the latest session
            session_notes = f"""
            ## 📄 Auto-Generated Session Notes
            **Date:** {latest_session['Date']}
            **Therapist:** {latest_session['Therapist']}
            **Start Time:** {latest_session['Start Time']}
            **End Time:** {latest_session['End Time']}
            **Total Duration Tracked:** {latest_session.get('Total Duration (s)', 'N/A')} seconds

            **Session Summary:**  
            - Trial-by-Trial & Cold Probe data saved  
            - Behavior duration tracked  
            - Progress recorded  
            """
            st.markdown(session_notes)
