import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Airport Runway Scheduling (FCFS)", layout="wide")

st.title("🛫 Airport Runway Scheduling - FCFS")
st.write("Simulating runway allocation using **First Come First Serve (FCFS)** scheduling.")

# Input: Number of planes
num_planes = st.number_input("Enter number of planes:", min_value=1, max_value=10, value=4, step=1)

planes = []
st.subheader("✈️ Enter Plane Details")
for i in range(num_planes):
    col1, col2, col3 = st.columns(3)
    with col1:
        pid = st.text_input(f"Plane {i+1} ID", f"A{i+1}")
    with col2:
        arrival = st.number_input(f"Arrival Time (Plane {i+1})", min_value=0, value=i, step=1)
    with col3:
        burst = st.number_input(f"Runway Time (Plane {i+1})", min_value=1, value=i+2, step=1)
    planes.append([pid, arrival, burst])

if st.button("Schedule Runway"):
    # Sort planes by arrival time
    planes.sort(key=lambda x: x[1])
    time = 0
    schedule_data = []
    waiting_times = []
    turnaround_times = []

    for plane in planes:
        pid, arrival, burst = plane
        if time < arrival:
            time = arrival
        start_time = time
        completion_time = start_time + burst
        waiting_time = start_time - arrival
        turnaround_time = completion_time - arrival

        waiting_times.append(waiting_time)
        turnaround_times.append(turnaround_time)

        schedule_data.append({
            "Plane": pid,
            "Arrival": arrival,
            "Runway Time": burst,
            "Start": start_time,
            "End": completion_time,
            "Waiting": waiting_time,
            "Turnaround": turnaround_time
        })

        time = completion_time

    df = pd.DataFrame(schedule_data)
    st.subheader("📋 Runway Allocation Table")
    st.dataframe(df, use_container_width=True)

    avg_wait = sum(waiting_times) / len(waiting_times)
    avg_turn = sum(turnaround_times) / len(turnaround_times)

    st.metric("Average Waiting Time", f"{avg_wait:.2f}")
    st.metric("Average Turnaround Time", f"{avg_turn:.2f}")

    # Gantt Chart Visualization
    st.subheader("📊 Runway Allocation Gantt Chart")
    fig, ax = plt.subplots(figsize=(8, 3))

    for idx, row in df.iterrows():
        ax.barh(y=row["Plane"], width=row["Runway Time"], left=row["Start"], edgecolor="black")
        ax.text(row["Start"] + row["Runway Time"]/2, idx, f'{row["Plane"]}', ha='center', va='center', color="white")

    ax.set_xlabel("Time")
    ax.set_ylabel("Planes")
    ax.set_title("FCFS Runway Scheduling")
    st.pyplot(fig)
