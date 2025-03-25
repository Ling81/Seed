import pandas as pd
import os
import streamlit as st

# Function to save session data to a CSV file
def save_data_to_csv(data, filename="session_data.csv"):
    df = pd.DataFrame([data])  # Convert dictionary to DataFrame
    
    # Check if file exists, if yes, append data, else create new file
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Append data
    else:
        df.to_csv(filename, mode='w', header=True, index=False)  # Create new file

    st.success("✅ Data saved successfully!")

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

if st.button("💾 Save Session Details"):
    session_data = {
        "Date": date,
        "Time Start": start_time,
        "Time End": end_time,
        "Therapist": therapist_name,
    }
    save_data_to_csv(session_data)

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

if st.button("💾 Save Cold Probe Data"):
    cold_probe_data = {"Date": date}  # Store session date
    for domain in domains:
        for target in cold_probe_targets[domain]:
            key = f"{domain} - {target}"  # Create a unique key
            cold_probe_data[key] = cold_probe_responses[domain][target]

    save_data_to_csv(cold_probe_data)

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

if st.button("💾 Save Trial Data"):
    trial_data = {"Date": date}  # Store session date
    for domain in trial_domains:
        for target in trial_targets[domain]:
            key = f"{domain} - {target}"  # Unique key for target
            trial_data[key] = trial_responses[domain][target]  # Store percentage

    save_data_to_csv(trial_data)
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

import pandas as pd
import io

# Function to convert session data to a downloadable Excel file
def export_to_excel(data):
    output = io.BytesIO()  # Create a buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for key, value in data.items():
            if isinstance(value, dict):  # Convert dictionaries into DataFrame
                df = pd.DataFrame.from_dict(value, orient="index")
            else:
                df = pd.DataFrame([value])  # Convert other data into DataFrame
            
            df.to_excel(writer, sheet_name=key[:31])  # Sheet name max length = 31

    output.seek(0)
    return output

# Button to trigger export
if st.button("📤 Export Data to Excel"):
    if "session_data" in st.session_state and st.session_state.session_data:
        excel_data = export_to_excel(st.session_state.session_data)
        st.download_button(label="📥 Download Excel File",
                           data=excel_data,
                           file_name="session_data.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("No data available to export.")

