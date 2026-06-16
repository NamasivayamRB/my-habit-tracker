import streamlit as st
import json
from datetime import datetime, date

st.set_page_config(page_title="21/90 Habit Tracker", page_icon="🏃‍♂️", layout="centered")

# Initialize Local Storage for tracking data
if "tracker_data" not in st.session_state:
    init_data = {"start_date": str(date.today()), "days": {}}
    for i in range(1, 91):
        init_data["days"][str(i)] = {"walk": False, "water": False, "study": False, "sleep": False, "completed": False}
    st.session_state.tracker_data = init_data

data = st.session_state.tracker_data

# Calculate the current day on your journey
start_dt = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
current_day = (date.today() - start_dt).days + 1
current_day = max(1, min(current_day, 90))

st.title("🏃‍♂️ Mr. Bharathy's 21/90 Habit Tracker")
st.write("Track your physical health wins and evening study sprints daily.")

# Progress dashboard metrics
completed_days = sum(1 for d in data["days"].values() if d["completed"])
progress_pct = completed_days / 90.0

st.metric(label="Timeline Status", value=f"Day {current_day} of 90", 
          delta="Phase 1: Habit Formation" if current_day <= 21 else "Phase 2: Routine Lock")
st.progress(progress_pct)
st.write(f"🏆 Overall Progress: **{progress_pct*100:.1f}%** ({completed_days}/90 Days)")

st.markdown("---")
st.subheader(f"📝 Mark Today's Habits (Day {current_day})")

day_str = str(current_day)
d_data = data["days"][day_str]

# Large, mobile-friendly touch targets
d_data["walk"] = st.checkbox("🚶‍♂️ Doctor's Advised Morning Walk (45 Min)", value=d_data["walk"])
d_data["water"] = st.checkbox("💧 3 Litres Water Target (Flush Pus Cells)", value=d_data["water"])

today_name = date.today().strftime("%A")
study_label = "💻 Weekend Deep-Dive Study (2.5 Hours)" if today_name in ["Saturday", "Sunday"] else "💻 Weekday Sprint Study (1 Hour)"
d_data["study"] = st.checkbox(study_label, value=d_data["study"])
d_data["sleep"] = st.checkbox("🛌 Sleep Lockout (In bed by 10:00 PM)", value=d_data["sleep"])

d_data["completed"] = all([d_data["walk"], d_data["water"], d_data["study"], d_data["sleep"]])

if st.button("💾 Save Daily Progress", type="primary"):
    st.session_state.tracker_data = data
    st.success("Progress updated successfully for today!")

st.markdown("---")
with st.expander("🤖 Copy Code to Share with your AI Assistant"):
    share_json = {"day": current_day, "metrics": d_data, "total_completed_days": completed_days}
    st.code(json.dumps(share_json, indent=2), language="json")
