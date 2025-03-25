import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

# Title
st.title("ABA Data Collection Tool")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", [
    "Session Details", "Cold Probe Data", "Trial-by-Trial Data",
    "Task Analysis", "Behavior Duration", "Progress & Reports"
])

# ================== 1️⃣ SESSION DETAILS ==================
if section == "Session Details":
    st.header("📅 Session Details")
    
    # Date, Time, Therapist's Name
    date = st.date_input("Select Date", datetime.date.today())
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    therapist = st.text_input("Therapist’s Name", "")

    session_info = {
        "Date": date,
        "Start Time": start_time,
        "End Time": end_time,
        "Therapist": therapist
    }
    st.write("Session Info:", session_info)

# ================== 2️⃣ COLD PROBE DATA ==================
if section == "Cold Probe Data":
    st.header("🧪 Cold Probe Data")
    
    # Define domains
    domains = ["Communication", "Social Skills", "Motor Skills"]
    selected_domain = st.selectbox("Select Domain", domains)
    
    # Define Targets
    targets = st.text_area("Enter Targets (comma-separated)").split(',')
    
    # Response selection
    data = {}
    for target in targets:
        response = st.radio(f"{target.strip()}", ["Y", "N", "NA"], index=2, horizontal=True)
        data[target.strip()] = response
    
    st.write("Collected Data:", data)

# ================== 3️⃣ TRIAL-BY-TRIAL DATA ==================
if section == "Trial-by-Trial Data":
    st.header("🎯 Trial-by-Trial Data")
    
    # Select domain
    domains = ["Communication", "Social Skills", "Motor Skills"]
    selected_domain = st.selectbox("Select Domain", domains)
    
    # Enter targets
    targets = st.text_area("Enter Targets (comma-separated)").split(',')
    
    trial_data = {}
    for target in targets:
        responses = st.text_input(f"Enter trial responses for {target.strip()} (+, p, -, I, comma-separated)")
        response_list = responses.split(',')
        correct_responses = sum(1 for r in response_list if r.strip() in ["+", "I"])
        percentage = round((correct_responses / len(response_list)) * 100, 2) if response_list else 0
        trial_data[target.strip()] = {"Responses": response_list, "Correct %": percentage}
    
    st.write("Trial Data:", trial_data)

# ================== 4️⃣ TASK ANALYSIS ==================
if section == "Task Analysis":
    st.header("📋 Task Analysis")

    steps = st.text_area("Enter Steps (comma-separated)").split(',')
    prompt_levels = ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"]
    
    task_data = {}
    for step in steps:
        prompt = st.selectbox(f"Prompt for {step.strip()}", prompt_levels)
        task_data[step.strip()] = prompt
    
    st.write("Task Analysis Data:", task_data)

# ================== 5️⃣ BEHAVIOR DURATION TRACKING ==================
if section == "Behavior Duration":
    st.header("⏳ Behavior Duration Tracking")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "total_duration" not in st.session_state:
        st.session_state.total_duration = 0

    if st.button("Start Timer"):
        st.session_state.start_time = time.time()

    if st.button("Stop Timer") and st.session_state.start_time:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.total_duration += elapsed_time
        st.session_state.start_time = None

    st.write("Total Duration:", round(st.session_state.total_duration, 2), "seconds")

# ================== 6️⃣ PROGRESS & REPORTS ==================
if section == "Progress & Reports":
    st.header("📊 Progress & Reports")

    # Sample cumulative data
    progress_data = {"Dates": ["2025-03-01", "2025-03-10", "2025-03-20"], "Cumulative Trials": [5, 15, 25]}
    df = pd.DataFrame(progress_data)
    
    # Plot cumulative graph
    fig, ax = plt.subplots()
    ax.plot(df["Dates"], df["Cumulative Trials"], marker='o', linestyle='-')
    ax.set_title("Cumulative Graph")
    ax.set_xlabel("Date")
    ax.set_ylabel("Trials Completed")
    st.pyplot(fig)

    # Generate session notes
    st.subheader("📄 Auto-Generated Session Notes")
    session_summary = f"""
    **Date:** {date}  
    **Therapist:** {therapist}  
    **Session Time:** {start_time} - {end_time}  

    **Cold Probe Data:** {data}  
    **Trial-by-Trial Data:** {trial_data}  
    **Task Analysis Data:** {task_data}  
    **Behavior Duration:** {round(st.session_state.total_duration, 2)} seconds  
    """
    st.text_area("Session Notes", session_summary, height=200)

    # Option to download session notes
    st.download_button("Download Session Notes", session_summary, file_name="session_notes.txt")

