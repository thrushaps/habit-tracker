import streamlit as st
import json
import os
from collections import Counter
import pandas as pd

# ================= PAGE CONFIG (MUST BE FIRST) =================
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🌿",
    layout="centered"
)

# ================= FILES =================
USER_FILE = "users.json"
DATA_FILE = "data.json"

# create files if not exist
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ================= LOGIN / SIGNUP =================
if not st.session_state.logged_in:
    st.title("🔐 Login / Signup")

    choice = st.radio("Choose", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    with open(USER_FILE, "r") as f:
        users = json.load(f)

    if choice == "Signup":
        if st.button("Create Account"):

        # ❗ STEP 1: Check empty fields
            if username.strip() == "" or password.strip() == "":
                st.error("Username and Password cannot be empty")

        # ❗ STEP 2: Check existing user
            elif username in users:
                st.error("User already exists")

        # ❗ STEP 3: Create account
            else:
                users[username] = password
                with open(USER_FILE, "w") as f:
                    json.dump(users, f)

                st.success("Account created! Now login")

    if choice == "Login":
        if st.button("Login"):

        # ❗ Check empty
            if username.strip() == "" or password.strip() == "":
                st.error("Enter username and password")

        # ❗ Validate
            elif username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid username or password")

    st.stop()

# ================= MAIN APP =================
st.title("🌱 Habit Tracker")
st.write(f"Welcome **{st.session_state.username}** 👋")

# ================= LOAD DATA =================
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):  # fix old wrong format
                return {}
            return data
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()
# ensure user has their own list
if st.session_state.username not in data:
    data[st.session_state.username] = []
    save_data(data)

# 👉 FILTER ONLY CURRENT USER DATA
user_data = data.get(st.session_state.username, [])

# ================= MENU =================
menu = st.sidebar.radio(
    "✨ Menu",
    ["Add Habit", "View Habits", "Analysis"]
)

# ================= ADD HABIT =================
if menu == "Add Habit":
    st.subheader("➕ Add Habit")

    habit_name = st.text_input("Enter habit")
    status = st.selectbox("Status", ["done", "missed"])

    if st.button("Add Habit"):
        if habit_name:
            user_data.append({
                "name": habit_name,
                "status": status
            })
            data[st.session_state.username] = user_data
            save_data(data)
            st.success("Habit added!")
        else:
            st.warning("Enter a habit")

# ================= VIEW HABITS =================
elif menu == "View Habits":
    st.subheader("📋 Your Habits")

    if user_data:
        for i, h in enumerate(user_data):
            emoji = "✅" if h["status"] == "done" else "❌"

            st.write(f"{emoji} {h['name']} - {h['status']}")

            if st.button(f"Delete {h['name']}", key=i):
                user_data.pop(i)
                data[st.session_state.username] = user_data
                save_data(data)
                st.rerun()
    else:
        st.info("No habits yet")

# ================= ANALYSIS =================
elif menu == "Analysis":
    st.subheader("📊 Analysis")

    if user_data:
        completed = [h["name"] for h in user_data if h["status"] == "done"]
        missed = [h["name"] for h in user_data if h["status"] == "missed"]

        st.success("Completed")
        st.write(Counter(completed))

        st.error("Missed")
        st.write(Counter(missed))

        df = pd.DataFrame(Counter([h["name"] for h in user_data]).items(), columns=["Habit", "Count"])
        st.bar_chart(df.set_index("Habit"))

    else:
        st.info("No data yet")