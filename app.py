import streamlit as st
import json
import os
from collections import Counter

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

/* ===== MAIN BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}

/* ===== REMOVE WHITE BLOCKS ===== */
.block-container {
    background: transparent !important;
    padding-top: 2rem;
}

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.3);
}

/* ===== GLASS EFFECT CARD ===== */
.css-1r6slb0, .css-12oz5g7 {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
}

/* ===== INPUT FIELDS ===== */
.stTextInput input, 
.stSelectbox div {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2);
}

/* ===== BUTTON ===== */
.stButton button {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

/* ===== TEXT VISIBILITY FIX ===== */
h1, h2, h3, p, label {
    color: white !important;
}

/* ===== REMOVE DEFAULT WHITE BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)

# ================= APP TITLE =================
st.title("🌿 Habit Tracker Dashboard")
st.write("Track your habits. Improve your life ✨")

# ================= MENU =================
menu = st.sidebar.selectbox("Menu", ["Add Habit", "View Habits", "Analysis"])

data = load_data()

# ================= ADD HABIT =================
if menu == "Add Habit":
    st.subheader("➕ Add New Habit")

    name = st.text_input("Habit Name")
    status = st.selectbox("Status", ["done", "missed"])

    if st.button("Save"):
        if name:
            data.append({
            "name": name,
            "status": status
            })
            save_data(data)
            st.success("Habit saved ✅")
        else:
            st.warning("Enter habit name!")

# ================= VIEW HABITS =================
elif menu == "View Habits":
    st.subheader("📋 Your Habits")

    if data:
        for habit in data:
            name = habit.get("name") or habit.get("habit") or "Unknown"
            status = habit.get("status", "Unknown")
            st.write(f"👉 {name} - {status}")
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
        st.bar_chart(all_counts)

    else:
        st.info("No data to analyze")