import streamlit as st
import json
import os
from datetime import datetime
from collections import Counter

# ================= LOGIN SYSTEM =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "thrusha" and password == "thrusha":
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

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

def add_habit():
    habit = input("Enter habit: ")
    status = input("Status (done/missed): ")

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "habit": habit,
        "status": status
    }

    data = load_data()
    data.append(entry)
    save_data(data)

    print("✅ Habit saved!")

def view_habits():
    data = load_data()
    if not data:
        print("No habits yet")
        return

    for d in data:
        print(f"{d['date']} - {d['habit']} - {d['status']}")

def analyze_habits():
    data = load_data()

    if not data:
        print("No data to analyze")
        return

    done = [d["habit"] for d in data if d["status"] == "done"]
    missed = [d["habit"] for d in data if d["status"] == "missed"]

    done_count = Counter(done)
    missed_count = Counter(missed)

    print("\n📊 Habit Analysis")

    print("\n✅ Completed Habits:")
    for habit, count in done_count.items():
        print(f"{habit}: {count}")

    print("\n❌ Missed Habits:")
    for habit, count in missed_count.items():
        print(f"{habit}: {count}")

    if missed_count:
        weakest = missed_count.most_common(1)[0][0]
        print(f"\n⚠️ Weakest Habit: {weakest}")

while True:
    print("1. Add Habit")
    print("2. View Habits")
    print("3. Analyze Habits")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_habit()
    elif choice == "2":
        view_habits()
    elif choice == "3":
        analyze_habits()
    elif choice == "4":
        break       