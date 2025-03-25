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

# ----------------------------- 1️⃣ SESSION DETAILS -----------------------------
if section == "Session Details":
    st.title("📌 Session Details")

    # Input fields
    date = st.date_input("Session Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    day_of_session = st.selectbox("Day of Session", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    therapist_name = st.text_input("Therapist Name", placeholder="Enter your name")

    # Display summary
    st.write(f"📅 **Date:** {date}, 🕒 **Time:** {start_time} - {end_time}, 📌 **Day:** {day_of_session}, 👩‍⚕️ **Therapist:** {therapist_name}")

# ----------------------------- 2️⃣ COLD PROBE DATA -----------------------------
elif section == "Cold Probe Data":
    st.title("📌 Cold Probe Data")

    # Define domains
    domains = ["Language", "Social Skills", "Motor Skills"]
    selected_domain = st.selectbox("Select Domain", domains)

    # Target list for domain
    targets = ["Target 1", "Target 2", "Target 3"]
    
    # Response selection for each target
    response_data = {}
    for target in targets:
        response = st.selectbox(f"{target}", ["Y", "N", "NA"])
        response_data[target] = response
    
    # Display recorded responses
    st.write("📋 **Recorded Responses:**", response_data)

# ----------------------------- 3️⃣ TRIAL-BY-TRIAL DATA -----------------------------
elif section == "Trial-by-Trial Data":
    st.title("📌 Trial-by-Trial Data")

    # Select domain
    selected_domain = st.selectbox("Select Domain", domains)
    
    # Target selection
    targets = ["Target 1", "Target 2", "Target 3"]
    selected_target = st.selectbox("Select Target", targets)

    # Trial entry and percentage calculation
    trial_data = []
    for trial in range(1, 6):
        response = st.selectbox(f"Trial {trial}", ["+", "p", "-", "I"])
        trial_data.append(response)
    
    # Calculate percentage of correct responses
    correct_trials = trial_data.count("+") + trial_data.count("I")
    accuracy_percentage = (correct_trials / len(trial_data)) * 100

    # Display results
    st.write(f"🎯 **Accuracy for {selected_target}:** {accuracy_percentage:.2f}%")

# ----------------------------- 4️⃣ TASK ANALYSIS -----------------------------
elif section == "Task Analysis":
    st.title("📌 Task Analysis")

    # Define steps
    steps = ["Step 1", "Step 2", "Step 3"]
    step_data = {}

    for step in steps:
        prompt_level = st.selectbox(f"{step}", ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"])
        step_data[step] = prompt_level

    # Display recorded steps
    st.write("📋 **Prompt Levels:**", step_data)

# ----------------------------- 5️⃣ BEHAVIOR DURATION TRACKING -----------------------------
elif section == "Behavior Duration Tracking":
    st.title("📌 Behavior Duration Tracking")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
        st.session_state.total_duration = 0

    # Timer controls
    if st.button("Start Timer"):
        st.session_state.start_time = time.time()

    if st.button("Stop Timer"):
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            st.session_state.total_duration += elapsed_time
            st.session_state.start_time = None

    # Display total duration
    st.write(f"⏳ **Total Behavior Duration:** {st.session_state.total_duration:.2f} seconds")

# ----------------------------- 6️⃣ PROGRESS & REPORTS -----------------------------
elif section == "Progress & Reports":
    st.title("📌 Progress & Reports")

    # Placeholder data for cumulative graph
    dates = pd.date_range(start="2024-01-01", periods=10, freq='D')
    scores = [50, 55, 60, 65, 70, 75, 78, 80, 85, 90]

    # Plot cumulative graph
    fig, ax = plt.subplots()
    ax.plot(dates, scores, marker="o", linestyle="-", color="b")
    ax.set_title("Cumulative Progress Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score (%)")
    ax.grid(True)
    st.pyplot(fig)

    # Auto-generated session notes
    session_notes = f"""
    📅 **Date:** {date}  
    🕒 **Time:** {start_time} - {end_time}  
    📌 **Day:** {day_of_session}  
    👩‍⚕️ **Therapist:** {therapist_name}  

    🎯 **Cold Probe Summary:** {response_data}  
    🔄 **Trial-by-Trial Summary:** Accuracy for {selected_target} = {accuracy_percentage:.2f}%  
    🛠 **Task Analysis Steps:** {step_data}  
    ⏳ **Total Behavior Duration:** {st.session_state.total_duration:.2f} sec  
    """
    st.markdown("### 📄 Auto-Generated Session Notes")
    st.text_area("Session Notes", session_notes, height=150)

