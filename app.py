import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

# App Title
st.set_page_config(page_title="ABA Data Collection", layout="wide")
st.title("📊 ABA Data Collection Tool")

# Sidebar Navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Select a Section:", [
    "Session Details", "Cold Probe Data", "Trial-by-Trial Data",
    "Task Analysis", "Behavior Duration", "Progress & Reports"
])

# ================== 1️⃣ SESSION DETAILS ==================
if section == "Session Details":
    st.header("📅 Session Details")

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Select Date", datetime.date.today())
        therapist = st.text_input("Therapist’s Name", "")

    with col2:
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")

    session_info = {
        "Date": date,
        "Start Time": start_time,
        "End Time": end_time,
        "Therapist": therapist
    }
    st.write("### ✅ Session Information")
    st.json(session_info)

# ================== 2️⃣ COLD PROBE DATA ==================
elif section == "Cold Probe Data":
    st.header("🧪 Cold Probe Data")

    # Define domains
    domains = ["Communication", "Social Skills", "Motor Skills"]
    selected_domain = st.selectbox("Select Domain", domains)

    # Enter targets
    targets = st.text_area("Enter Targets (comma-separated)").split(',')

    st.subheader("📋 Data Entry")
    cold_probe_data = []
    for target in targets:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{target.strip()}**")
        with col2:
            response = st.selectbox(f"{target.strip()}", ["Y", "N", "NA"], key=target.strip())
        cold_probe_data.append({"Target": target.strip(), "Response": response})

    st.write("### ✅ Collected Data")
    st.dataframe(pd.DataFrame(cold_probe_data))

# ================== 3️⃣ TRIAL-BY-TRIAL DATA ==================
elif section == "Trial-by-Trial Data":
    st.header("🎯 Trial-by-Trial Data")

    selected_domain = st.selectbox("Select Domain", domains)
    targets = st.text_area("Enter Targets (comma-separated)").split(',')

    st.subheader("📋 Trial Data Entry")
    trial_data = []
    for target in targets:
        responses = st.text_input(f"Enter trial responses for {target.strip()} (+, p, -, I, comma-separated)")
        response_list = responses.split(',')
        correct_responses = sum(1 for r in response_list if r.strip() in ["+", "I"])
        percentage = round((correct_responses / len(response_list)) * 100, 2) if response_list else 0
        trial_data.append({"Target": target.strip(), "Responses": response_list, "Correct %": percentage})

    st.write("### ✅ Trial Data Summary")
    st.dataframe(pd.DataFrame(trial_data))

# ================== 4️⃣ TASK ANALYSIS ==================
elif section == "Task Analysis":
    st.header("📋 Task Analysis")

    steps = st.text_area("Enter Steps (comma-separated)").split(',')
    prompt_levels = ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"]

    st.subheader("📋 Data Entry")
    task_data = []
    for step in steps:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{step.strip()}**")
        with col2:
            prompt = st.selectbox(f"Prompt for {step.strip()}", prompt_levels, key=step.strip())
        task_data.append({"Step": step.strip(), "Prompt": prompt})

    st.write("### ✅ Task Analysis Data")
    st.dataframe(pd.DataFrame(task_data))

# ================== 5️⃣ BEHAVIOR DURATION TRACKING ==================
elif section == "Behavior Duration":
    st.header("⏳ Behavior Duration Tracking")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "total_duration" not in st.session_state:
        st.session_state.total_duration = 0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 Start Timer"):
            st.session_state.start_time = time.time()

    with col2:
        if st.button("🔴 Stop Timer") and st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            st.session_state.total_duration += elapsed_time
            st.session_state.start_time = None

    st.write(f"### ⏱ Total Duration: **{round(st.session_state.total_duration, 2)} seconds**")

# ================== 6️⃣ PROGRESS & REPORTS ==================
elif section == "Progress & Reports":
    st.header("📊 Progress & Reports")

    # Sample cumulative data
    progress_data = {"Dates": ["2025-03-01", "2025-03-10", "2025-03-20"], "Cumulative Trials": [5, 15, 25]}
    df = pd.DataFrame(progress_data)

    # Plot cumulative graph
    st.subheader("📈 Cumulative Graph")
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

    **Cold Probe Data:** {cold_probe_data}  
    **Trial-by-Trial Data:** {trial_data}  
    **Task Analysis Data:** {task_data}  
    **Behavior Duration:** {round(st.session_state.total_duration, 2)} seconds  
    """
    st.text_area("Session Notes", session_summary, height=200)

    # Option to download session notes
    st.download_button("📥 Download Session Notes", session_summary, file_name="session_notes.txt")
