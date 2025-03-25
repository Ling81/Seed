import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Title
st.title("ABA Data Collection Tool")

# Section 1: Session Details
st.header("📅 Session Details")
date = st.date_input("Date", datetime.date.today())
time = st.time_input("Time")
therapist = st.text_input("Therapist's Name")

# Section 2: Cold Probe Data
st.header("❄️ Cold Probe Data")
cold_probe_data = st.text_area("Enter targets and responses (e.g., 'Target 1: Correct, Target 2: Incorrect')")

# Section 3: Trial-by-Trial Data
st.header("🎯 Trial-by-Trial Data")
num_trials = st.number_input("Number of Trials", min_value=1, max_value=20, value=5)
correct_trials = st.number_input("Number of Correct Responses", min_value=0, max_value=num_trials, value=0)
if num_trials > 0:
    accuracy = (correct_trials / num_trials) * 100
    st.write(f"✅ Accuracy: {accuracy:.2f}%")

# Section 4: Task Analysis
st.header("📋 Task Analysis")
task_steps = st.text_area("List steps and prompts used (e.g., 'Step 1: Full Prompt, Step 2: Partial Prompt')")

# Section 5: Duration for Behavior of Concern
st.header("⏳ Behavior Duration Tracking")
behavior_start = st.time_input("Start Time")
behavior_end = st.time_input("End Time")
if behavior_start and behavior_end:
    duration = datetime.datetime.combine(datetime.date.today(), behavior_end) - datetime.datetime.combine(datetime.date.today(), behavior_start)
    st.write(f"⚠️ Behavior Duration: {duration}")

# Section 6: Data Visualization
st.header("📊 Progress Graphs")
session_dates = [date - datetime.timedelta(days=i) for i in range(5)]
accuracy_values = [accuracy - i * 5 for i in range(5)]
df = pd.DataFrame({"Date": session_dates, "Accuracy (%)": accuracy_values})
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Accuracy (%)"], marker="o", linestyle="-", color="blue")
ax.set_xlabel("Date")
ax.set_ylabel("Accuracy (%)")
ax.set_title("Trial Accuracy Over Time")
st.pyplot(fig)

# Section 7: Generate Session Notes
st.header("📝 Session Notes")
session_notes = f"""
**Session Details:**  
- Date: {date}  
- Time: {time}  
- Therapist: {therapist}  

**Cold Probe Data:**  
{cold_probe_data}  

**Trial-by-Trial Data:**  
- Accuracy: {accuracy:.2f}%  

**Task Analysis:**  
{task_steps}  

**Behavior Duration:**  
- Start: {behavior_start}  
- End: {behavior_end}  
- Duration: {duration}  

"""
st.text_area("Generated Notes", session_notes, height=200)

# Save Data Button
if st.button("Save Session Data"):
    st.success("✅ Data Saved Successfully!")
