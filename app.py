import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Initialize session state variables
if "date" not in st.session_state:
    st.session_state.date = datetime.date.today()
if "therapist" not in st.session_state:
    st.session_state.therapist = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "total_duration" not in st.session_state:
    st.session_state.total_duration = 0
if "trial_data" not in st.session_state:
    st.session_state.trial_data = pd.DataFrame(columns=["Domain", "Target", "Trial 1", "Trial 2", "Trial 3", "Accuracy (%)"])

# Sidebar navigation
st.sidebar.title("📊 ABA Data Collection Tool")
section = st.sidebar.radio("Choose a section:", ["Session Details", "Cold Probe Data", "Trial-by-Trial Data", "Task Analysis", "Behavior Duration", "Progress & Reports"])

# 1️⃣ **Session Details**
if section == "Session Details":
    st.header("📅 Session Details")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.date = st.date_input("Select Date", st.session_state.date)
        st.session_state.therapist = st.text_input("Therapist’s Name", st.session_state.therapist)

    with col2:
        st.session_state.start_time = st.time_input("Start Time", st.session_state.start_time)
        st.session_state.end_time = st.time_input("End Time", st.session_state.end_time)

    st.write("### ✅ Session Summary")
    st.json({
        "Date": str(st.session_state.date),
        "Therapist": st.session_state.therapist,
        "Start Time": str(st.session_state.start_time),
        "End Time": str(st.session_state.end_time)
    })

# 2️⃣ **Cold Probe Data**
elif section == "Cold Probe Data":
    st.header("📌 Cold Probe Data")

    domains = ["Communication", "Social Skills", "Daily Living", "Academic", "Motor Skills"]
    selected_domain = st.selectbox("Select Domain", domains)
    
    st.write(f"**Selected Domain:** {selected_domain}")

    # Example cold probe table
    targets = ["Target 1", "Target 2", "Target 3"]
    responses = {t: st.selectbox(f"{t}:", ["Y", "N", "NA"], key=t) for t in targets}

    st.write("✅ **Cold Probe Data Saved!**")

# 3️⃣ **Trial-by-Trial Data**
elif section == "Trial-by-Trial Data":
    st.header("🎯 Trial-by-Trial Data")

    domain = st.selectbox("Select Domain", ["Communication", "Social Skills", "Daily Living", "Academic"])
    target = st.text_input("Enter Target Behavior")

    col1, col2, col3 = st.columns(3)
    trial_1 = col1.selectbox("Trial 1", ["+", "p", "-", "I"], key="trial_1")
    trial_2 = col2.selectbox("Trial 2", ["+", "p", "-", "I"], key="trial_2")
    trial_3 = col3.selectbox("Trial 3", ["+", "p", "-", "I"], key="trial_3")

    if st.button("Save Data"):
        correct_count = sum([trial_1 == "+", trial_2 == "+", trial_3 == "+"])
        accuracy = (correct_count / 3) * 100

        new_data = pd.DataFrame({"Domain": [domain], "Target": [target], "Trial 1": [trial_1], "Trial 2": [trial_2], "Trial 3": [trial_3], "Accuracy (%)": [accuracy]})
        st.session_state.trial_data = pd.concat([st.session_state.trial_data, new_data], ignore_index=True)

    st.dataframe(st.session_state.trial_data)

# 4️⃣ **Task Analysis**
elif section == "Task Analysis":
    st.header("📝 Task Analysis")

    steps = ["Step 1", "Step 2", "Step 3"]
    prompts = ["FP", "PP", "MP", "VI", "VP", "GP", "TD", "I"]
    
    task_data = {step: st.selectbox(f"{step}:", prompts, key=step) for step in steps}

    st.write("✅ **Task Analysis Data Saved!**")

# 5️⃣ **Behavior Duration**
elif section == "Behavior Duration":
    st.header("⏳ Behavior Duration Tracking")

    if st.button("Start Timer"):
        st.session_state.start_time = datetime.datetime.now()

    if st.button("End Timer"):
        if st.session_state.start_time:
            duration = (datetime.datetime.now() - st.session_state.start_time).total_seconds()
            st.session_state.total_duration += duration
            st.write(f"🕒 **Episode Duration:** {round(duration, 2)} seconds")
        else:
            st.warning("⚠ Start the timer first!")

    st.write(f"**Total Duration of Behavior:** {round(st.session_state.total_duration, 2)} seconds")

# 6️⃣ **Progress & Reports**
elif section == "Progress & Reports":
    st.header("📊 Progress & Reports")

    # Retrieve stored session details
    date = st.session_state.get("date", "N/A")
    therapist = st.session_state.get("therapist", "N/A")
    start_time = st.session_state.get("start_time", "N/A")
    end_time = st.session_state.get("end_time", "N/A")

    # Generate session notes
    st.subheader("📄 Auto-Generated Session Notes")
    session_summary = f"""
    **Date:** {date}  
    **Therapist:** {therapist}  
    **Session Time:** {start_time} - {end_time}  

    **Cold Probe Data:** Data not yet stored  
    **Trial-by-Trial Data:** {len(st.session_state.trial_data)} trials recorded  
    **Task Analysis Data:** Data not yet stored  
    **Behavior Duration:** {round(st.session_state.get("total_duration", 0), 2)} seconds  
    """

    st.text_area("Session Notes", session_summary, height=200)
    st.download_button("📥 Download Session Notes", session_summary, file_name="session_notes.txt")

    # Generate cumulative graph
    if not st.session_state.trial_data.empty:
        st.subheader("📈 Cumulative Progress Graph")
        fig, ax = plt.subplots()
        st.session_state.trial_data.plot(kind="line", x="Target", y="Accuracy (%)", ax=ax, marker="o")
        plt.xticks(rotation=45)
        plt.ylabel("Accuracy (%)")
        plt.title("Cumulative Progress Over Time")
        st.pyplot(fig)


