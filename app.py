import streamlit as st
import json
import os
from collections import Counter
import pandas as pd


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "thrusha" and password == "thrusha":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()


# ================= FILE =================
FILE = "data.json"

# ================= LOAD DATA =================
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# ================= SAVE DATA =================
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🌿",
    layout="centered"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* Center content */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}

/* Headings */
h1, h2, h3 {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
}

/* Cards (glass effect) */
.card {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
}

/* Buttons */
.stButton button {
    background: #ff4b4b;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
}

.stButton button:hover {
    background: #ff2e2e;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# ================= APP TITLE =================
st.markdown("<h1>🌿 Habit Tracker Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Track your habits. Improve your life ✨</p>", unsafe_allow_html=True)

# ================= MENU =================
menu = st.sidebar.radio(
    "✨ Menu",
    ["Add Habit", "View Habits", "Analysis"]
)

data = load_data()

# ================= ADD HABIT =================
if menu == "Add Habit":
    st.subheader("➕ Add New Habit")

    habit_name = st.text_input("Enter habit name")
    status = st.selectbox("Status", ["done", "missed"])

    if st.button("Add Habit"):
        if habit_name:
            data.append({
                "name": habit_name,
                "status": status
            })
            save_data(data)   
            st.success("Habit added!")
            st.balloons()
        else:
            st.warning("Please enter a habit name")

# ================= VIEW HABITS =================
elif menu == "View Habits":
    st.subheader("📋 Your Habits")

    if data:
        for i, habit in enumerate(data):
            name = habit.get("name") or habit.get("habit") or "Unknown"
            status = habit.get("status") or "Unknown"

            emoji = "✅" if status == "done" else "❌"

            st.markdown(f"""
            <div class="card">
                {emoji} <b>{name}</b> — {status}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Delete {name}", key=f"del_{i}"):
                st.session_state[f"confirm_{i}"] = True

    # 👇 Confirmation UI
            if st.session_state.get(f"confirm_{i}", False):
                st.warning(f"Delete '{name}'?")

                col_yes, col_no = st.columns(2)

                with col_yes:
                    if st.button("Yes", key=f"yes_{i}"):
                        data = [h for idx, h in enumerate(data) if idx != i]
                        save_data(data)
                        st.success("Deleted!")
                        st.session_state[f"confirm_{i}"] = False
                        st.rerun()

                with col_no:
                    if st.button("No", key=f"no_{i}"):
                        st.session_state[f"confirm_{i}"] = False
    else:
        st.info("No habits yet")

# ================= ANALYSIS =================
elif menu == "Analysis":
    st.subheader("📊 Habit Analysis")

    if data:
        completed = [
        h.get("name") or h.get("habit") or "Unknown"
        for h in data
        if h.get("status") == "done"
        ]
        missed = [
        h.get("name") or h.get("habit") or "Unknown"
        for h in data
        if h.get("status") == "missed"
        ]

        completed_count = Counter(completed)
        missed_count = Counter(missed)

        st.success("✅ Completed Habits")
        st.json(completed_count)

        st.error("❌ Missed Habits")
        st.json(missed_count)

        st.subheader("📊 Habit Chart")
        all_counts = Counter([h.get("name") or h.get("habit") or "Unknown" for h in data])
        df = pd.DataFrame.from_dict(all_counts, orient="index", columns=["Count"])
        st.bar_chart(df)

    else:
        st.info("No data to analyze")