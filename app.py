import streamlit as st
import pandas as pd
import json
from datetime import date

FILE = "data.json"

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

st.title("📊 Habit Tracker dashboard")

menu = st.sidebar.selectbox("Menu", ["Add Habit", "View Habits", "Analyze"])

data = load_data()

# ➤ Add Habit
if menu == "Add Habit":
    st.subheader("Add New Habit")

    habit = st.text_input("Habit Name")
    status = st.selectbox("Status", ["done", "missed"])

    if st.button("Save"):
        entry = {
            "date": str(date.today()),
            "habit": habit,
            "status": status
        }
        data.append(entry)
        save_data(data)
        st.success("Habit Saved ✅")

# ➤ View Habits
elif menu == "View Habits":
    st.subheader("Your Habits")

    if not data:
        st.warning("No habits yet")
    else:
        for d in data:
            st.write(f"{d['date']} - {d['habit']} - {d['status']}")

# ➤ Analyze
elif menu == "Analyze":
    st.subheader("Habit Analysis")

    done = {}
    missed = {}

    for d in data:
        if d["status"] == "done":
            done[d["habit"]] = done.get(d["habit"], 0) + 1
        else:
            missed[d["habit"]] = missed.get(d["habit"], 0) + 1

    st.subheader("✅ Completed Habits")
    st.json(done)

    st.subheader("❌ Missed Habits")
    st.json(missed)

    if missed:
        weakest = max(missed, key=missed.get)
        st.error(f"Weakest Habit: {weakest}")
    if done:

        df = pd.DataFrame({
            "Habit": list(done.keys()),
            "Completed": list(done.values()),
            "Missed": [missed.get(h, 0) for h in done.keys()]})
        st.subheader("📊 Habit Chart")
        st.bar_chart(df.set_index("Habit"))