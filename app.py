import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# App title
st.set_page_config(page_title="Therapist Data Collection Tool", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Session Details", "Cold Probe Data", "Trial-by-Trial Data",
                                     "Task Analysis", "Behavior Duration Tracking", "Progress & Reports"])

# Initialize session state variables if they don't exist
if "session_data" not in st.session_state:
    st.session_state.session_data = {}

# ----------------------------- 1️⃣ SESSION DETAILS -----------------------------
if section == "Session Details":
    st.title("📌 Session Details")

    # Input fields
    date = st.date_input("Session Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    day_of_session = st.selectbox("Day of Session", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    therapist_name = st.text_input("Therapist Name", placeholder="Enter your name")

    if st.button("Save Session Details"):
        st.session_state.session_data["session_details"] = {
            "Date": date,
            "Time": f"{start_time} - {end_time}",
            "Day": day_of_session,
            "Therapist": therapist_name
        }
        st.success("Session details saved!")

# ----------------------------- 2️⃣ COLD PROBE DATA -----------------------------
elif section == "Cold Probe Data":
    st.title("📌 Cold Probe Data")

    target_input = st.text_input("Enter Targets (comma-separated)", placeholder="E.g., Target 1, Target 2, Target 3")
    targets = [t.strip() for t in target_input.split(",") if t.strip()]

    response_data = {}
    if targets:
        for target in targets:
            response = st.selectbox(f"{target}", ["Y", "N", "NA"])
            response_data[target] = response

    if st.button("Save Cold Probe Data"):
        st.session_state.session_data["cold_probe"] = response_data
        st.success("Cold probe data saved!")

# ----------------------------- 3️⃣ TRIAL-BY-TRIAL DATA -----------------------------
elif section == "Trial-by-Trial Data":
    st.title("📌 Trial-by-Trial Data")

    # Enter targets (max 10)
    target_input = st.text_input("Enter up to 10 Targets (comma-separated)", placeholder="E.g., Target 1, Target 2, Target 3")
    targets = [t.strip() for t in target_input.split(",") if t.strip()][:10]  # Limit to 10 targets

    trial_data = {}

    if targets:
        for target in targets:
            st.subheader(f"🎯 {target}")
            
            responses = []
            col1, col2 = st.columns(2)

            with col1:
                for i in range(1, 6):  # First 5 trials
                    response = st.selectbox(f"Trial {i}", ["+", "p", "-", "I"], key=f"{target}_t{i}")
                    responses.append(response)

            with col2:
                for i in range(6, 11):  # Next 5 trials
                    response = st.selectbox(f"Trial {i}", ["+", "p", "-", "I"], key=f"{target}_t{i}")
                    responses.append(response)

            # Calculate accuracy
            correct_trials = responses.count("+") + responses.count("I")
            accuracy_percentage = (correct_trials / len(responses)) * 100 if responses else 0

            trial_data[target] = {
                "Responses": responses,
                "Accuracy": f"{accuracy_percentage:.2f}%"
            }

            st.write(f"✅ **Accuracy:** {accuracy_percentage:.2f}%")

    if st.button("Save Trial Data"):
        st.session_state.session_data["trial_data"] = trial_data
        st.success("Trial-by-Trial Data Saved!")

# ----------------------------- 4️⃣ TASK ANALYSIS -----------------------------
elif section == "Task Analysis":
    st.title("📌 Task Analysis")

    step_input = st.text_input("Enter Steps (comma-separated)", placeholder="E.g., Step 1, Step 2, Step 3")
    steps = [s.strip() for s in step_input.split(",") if s.strip()]

    step_data = {}
    if steps:
        for step in steps:
            prompt_level = st.selectbox(f"{step}", ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"])
            step_data[step] = prompt_level

    if st.button("Save Task Analysis"):
        st.session_state.session_data["task_analysis"] = step_data
        st.success("Task analysis data saved!")

# ----------------------------- 5️⃣ BEHAVIOR DURATION TRACKING -----------------------------
elif section == "Behavior Duration Tracking":
    st.title("📌 Behavior Duration Tracking")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
        st.session_state.total_duration = 0

    if st.button("Start Timer"):
        st.session_state.start_time = time.time()

    if st.button("Stop Timer"):
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            st.session_state.total_duration += elapsed_time
            st.session_state.start_time = None

    st.write(f"⏳ **Total Behavior Duration:** {st.session_state.total_duration:.2f} seconds")

    if st.button("Save Behavior Duration"):
        st.session_state.session_data["behavior_duration"] = st.session_state.total_duration
        st.success("Behavior duration saved!")

# ----------------------------- 6️⃣ PROGRESS & REPORTS -----------------------------
elif section == "Progress & Reports":
    st.title("📌 Progress & Reports")

    # Cumulative graph data (Placeholder)
    dates = pd.date_range(start="2024-01-01", periods=10, freq='D')
    scores = [50, 55, 60, 65, 70, 75, 78, 80, 85, 90]

    fig, ax = plt.subplots()
    ax.plot(dates, scores, marker="o", linestyle="-", color="b")
    ax.set_title("Cumulative Progress Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score (%)")
    ax.grid(True)


