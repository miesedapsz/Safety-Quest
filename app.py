import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

# Dhalia Safety Quest — illustrative learning prototype, not a compliance certification.
DATA_FILE = Path(__file__).with_name("player_history.json")
PASS_THRESHOLD = 70
QUESTIONS = [
    {
        "topic": "Hazard spotting",
        "q": "You notice liquid spreading across a busy corridor. What should you do first?",
        "options": [
            "Walk around it and assume someone else will clean it",
            "Warn nearby people, isolate the area if safe, and arrange cleanup",
            "Put paper over it and continue working",
            "Wait until the end of the shift to report it",
        ],
        "answer": 1,
        "why": "Prevent exposure immediately: warn others, make the area safe if you can do so without risk, and follow the site’s spill/reporting procedure.",
        "source": "Singapore MOM: workplace risk management; OSHA: hazard identification and assessment",
    },
    {
        "topic": "Risk assessment",
        "q": "A team is about to start an unfamiliar, non-routine task. What is the safest approach?",
        "options": [
            "Start slowly and discuss risks only if something goes wrong",
            "Use the same assessment from any previous job without checking",
            "Identify hazards, assess risk, choose controls, and communicate them before starting",
            "Ask the newest worker to decide what feels safe",
        ],
        "answer": 2,
        "why": "Risk management includes hazard identification, risk evaluation and risk control; routine and non-routine work should be considered.",
        "source": "Singapore MOM: Risk management; Workplace Safety and Health (Risk Management) Regulations",
    },
    {
        "topic": "Hierarchy of controls",
        "q": "A hazardous chemical is used in a process. Which control is generally strongest in the hierarchy of controls?",
        "options": [
            "Remove the hazardous chemical or eliminate the need for it",
            "Put up a warning sign",
            "Remind workers to be careful",
            "Provide PPE while leaving every other condition unchanged",
        ],
        "answer": 0,
        "why": "Elimination is higher in the hierarchy than administrative measures and PPE. The feasible control depends on the task and risk assessment.",
        "source": "Singapore MOM: Risk management; OSHA: Hazard prevention and control",
    },
    {
        "topic": "Working at height",
        "q": "You find a damaged ladder being used to reach a work area. What should you do?",
        "options": [
            "Use it only for a quick task",
            "Ask a colleague to hold it and proceed",
            "Mark it mentally and tell the next shift",
            "Stop using it, prevent others from using it, and report it through site procedure",
        ],
        "answer": 3,
        "why": "Defective equipment should be removed from service and reported; use an approved safe access method under the site’s work-at-height controls.",
        "source": "Singapore MOM: WSH legislation, including Work at Heights Regulations",
    },
    {
        "topic": "Electrical safety",
        "q": "A portable tool has a frayed power cable. What is the safest response?",
        "options": [
            "Wrap it with ordinary tape and finish the job",
            "Stop using it, isolate it if safe, and report/tag it according to procedure",
            "Keep the cable away from water and carry on",
            "Use it only if a supervisor is nearby",
        ],
        "answer": 1,
        "why": "Damaged electrical equipment can create shock or fire risks. Take it out of use and follow the workplace isolation and reporting procedure.",
        "source": "OSHA: Hazard identification and assessment; Singapore MOM: WSH risk management",
    },
    {
        "topic": "Manual handling",
        "q": "A load is too heavy or awkward for you to move safely. What should you do?",
        "options": [
            "Twist quickly so the lift takes less time",
            "Lift it in stages without telling anyone",
            "Use suitable mechanical aid or team assistance, and follow the task assessment",
            "Ask someone to pull while you push without coordinating",
        ],
        "answer": 2,
        "why": "Avoid unsafe lifting; use appropriate equipment or assistance and follow the risk assessment and local manual-handling procedure.",
        "source": "OSHA: Hazard identification and assessment (ergonomic risk factors)",
    },
    {
        "topic": "Emergency response",
        "q": "You discover smoke in a workplace area. What should guide your response?",
        "options": [
            "Raise the alarm and follow the site emergency/evacuation procedure; do not take unsafe risks",
            "Finish your current task before telling anyone",
            "Use the nearest lift to leave quickly",
            "Search for the source alone before alerting others",
        ],
        "answer": 0,
        "why": "Raise the alarm promptly and follow the workplace emergency plan, evacuation route and instructions from trained responders.",
        "source": "OSHA: Hazard identification and assessment (emergency and non-routine situations)",
    },
    {
        "topic": "PPE",
        "q": "A task risk assessment requires eye protection. Your goggles are cracked. What should you do?",
        "options": [
            "Wear them because some protection is better than none",
            "Borrow any glasses, even if they are not rated for the task",
            "Skip the task’s eye protection if you work carefully",
            "Obtain suitable, serviceable protection and follow the site procedure before starting",
        ],
        "answer": 3,
        "why": "PPE must be suitable for the hazard and in serviceable condition; it should be used as part of the risk controls, not improvised.",
        "source": "OSHA: Hazard prevention and control; Singapore MOM: Risk management",
    },
    {
        "topic": "Near misses",
        "q": "A suspended object nearly hits a worker, but nobody is injured. What is the best next step?",
        "options": [
            "Do nothing because no injury occurred",
            "Report the near miss promptly and help ensure the hazard is controlled",
            "Discuss it informally but avoid the reporting system",
            "Wait to see if the same thing happens again",
        ],
        "answer": 1,
        "why": "Near misses can reveal hazards and control failures. Reporting and investigation help prevent a future injury; follow the organization’s process.",
        "source": "OSHA: Hazard identification and assessment; worker participation",
    },
    {
        "topic": "Worker participation",
        "q": "You are unsure whether a task is safe because the conditions have changed. What is the best action?",
        "options": [
            "Continue because the task was approved earlier",
            "Copy what a coworker does without checking",
            "Pause if needed, raise the concern, and confirm the controls with the responsible person",
            "Stay silent so the team does not lose time",
        ],
        "answer": 2,
        "why": "Workers should participate in identifying hazards and raising concerns. Reassess when conditions change and clarify controls before proceeding.",
        "source": "OSHA: Worker participation; Singapore MOM: Risk management",
    },
]

PIXEL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
.stApp { background: #071629; color: #d8f6ff; }
.block-container { max-width: 1100px; padding-top: 1.4rem; }
h1, h2, h3 { color: #72f1ff !important; }
.pixel-title { font-family: 'Press Start 2P', monospace; font-size: clamp(18px, 2.5vw, 29px); line-height: 1.7; color:#78f2ff; text-shadow: 3px 3px #173b74; }
.pixel-sub { font-family: 'VT323', monospace; font-size: 25px; color:#ff91d4; }
.panel { background:#102b4a; border:3px solid #2377a8; box-shadow: 5px 5px 0 #03101f; padding:18px; margin:8px 0; }
.stat { background:#0c2440; border:2px solid #2b8fbd; padding:14px; min-height:88px; }
.stat-label { font-family:'VT323',monospace; color:#a4d8ec; font-size:21px; }
.stat-value { font-family:'Press Start 2P',monospace; font-size:20px; color:#a4ffcf; margin-top:8px; }
.pixel-bar { height:18px; border:2px solid #65eaff; background:#071629; padding:2px; }
.pixel-fill { height:100%; background:repeating-linear-gradient(90deg,#65f4cf 0 12px,#1bb99d 12px 14px); }
div.stButton > button { border-radius:0; border:2px solid #73f4ff; background:#123e63; color:#e5fbff; font-family:'VT323',monospace; font-size:22px; box-shadow:3px 3px 0 #020a14; }
div.stButton > button:hover { background:#1e6785; border-color:#ff91d4; color:white; }
div[data-testid="stRadio"] label { color:#e1f7ff; }
.small-note { font-size: 0.85rem; color:#a9c7d9; }
</style>
"""

def load_history():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_history(rows):
    DATA_FILE.write_text(json.dumps(rows, indent=2), encoding="utf-8")

def weekly_status(rows):
    # A "week" is Monday–Sunday in the player's local date. This demo uses the
    # machine's local date; production systems need explicit timezone handling.
    monday = date.today() - timedelta(days=date.today().weekday())
    current = [r for r in rows if date.fromisoformat(r["date"]) >= monday]
    if not current:
        return None, current
    return current[-1], current

if "page" not in st.session_state:
    st.session_state.page = "home"
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "feedback" not in st.session_state:
    st.session_state.feedback = None


st.set_page_config(page_title=" Dhalia Safety Quest ", page_icon="🌱", layout="wide")
st.markdown(PIXEL_CSS, unsafe_allow_html=True)

history = load_history()
latest, this_week = weekly_status(history)
weekly_best = max([r["score"] for r in this_week], default=0)
weekly_pass = weekly_best >= PASS_THRESHOLD
total_runs = len(history)
avg_score = round(sum(r["score"] for r in history) / total_runs) if total_runs else 0


st.markdown('<div class="pixel-title">...', unsafe_allow_html=True)
st.markdown('<div class="pixel-title">PROJECT DHALIA // SAFETY QUEST</div>', unsafe_allow_html=True)
st.markdown('<div class="pixel-sub">Grow safer habits🌱</div>', unsafe_allow_html=True)
st.caption("Pixel-art inspired prototype • General workplace hazard awareness • 10 questions per run")

# Dashboard
st.markdown("### PLAYER STATUS")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat"><div class="stat-label">WEEKLY SAFETY METER</div><div class="stat-value">{weekly_best if this_week else 0}%</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat"><div class="stat-label">SETS PLAYED</div><div class="stat-value">{total_runs}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat"><div class="stat-label">ALL-TIME AVERAGE</div><div class="stat-value">{avg_score}%</div></div>', unsafe_allow_html=True)
with c4:
    garden = "BLOOMING" if weekly_pass else ("WILTING" if this_week else "SEEDLING")
    st.markdown(f'<div class="stat"><div class="stat-label">GARDEN STATUS</div><div class="stat-value">{garden}</div></div>', unsafe_allow_html=True)

meter = weekly_best if this_week else 0
st.markdown(f'<div class="pixel-bar"><div class="pixel-fill" style="width:{meter}%;"></div></div>', unsafe_allow_html=True)
if weekly_pass:
    st.success(f"Garden thriving! Your best set this week is {weekly_best}%. Keep refreshing your knowledge.")
else:
    st.warning(f"Weekly target: at least {PASS_THRESHOLD}%. Current weekly best: {weekly_best if this_week else 0}%. Play a set or review and try again.")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("### 🌿 YOUR GARDEN")
    if weekly_pass:
        st.markdown("```text\n      .-*-.\n   🌼  \\|/  🌼\n  🌿---🌳---🌿\n     / | \\\n  🌱  🌱  🌱\n```")
        st.write("The garden blooms when your weekly score reaches the target.")
    elif this_week:
        st.markdown("```text\n      .\n     / \\\n  🌱--|--🌱\n     / \\\n   .   .\n```")
        st.write("Your garden is growing. Review missed topics and play again.")
    else:
        st.markdown("```text\n      .\n      |\n   ___|___\n  /_______\\\n```")
        st.write("A new week is a fresh start. Play a set to grow your garden.")
with right:
    st.markdown("### 🎮 MISSION RULES")
    st.write(f"- 10 questions per run")
    st.write("- Correct answer = 10 safety points")
    st.write("- Incorrect answer = 0 points for that question")
    st.write(f"- Weekly target = {PASS_THRESHOLD}% or higher")
    st.write("- Review feedback after each answer")
    st.write("- Your history is stored locally in this demo")

st.info("Important: this meter represents quiz performance, not a worker's actual health, competence, legal compliance, or workplace safety. A quiz cannot replace task-specific training, risk assessment, supervision, or emergency procedures.")

if st.session_state.page == "home":
    if st.button("▶ START NEW SAFETY RUN", use_container_width=True):
        st.session_state.page = "quiz"
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.session_state.feedback = None
        st.rerun()

elif st.session_state.page == "quiz":
    i = st.session_state.q_index
    if i >= len(QUESTIONS):
        st.session_state.page = "results"
        st.rerun()
    q = QUESTIONS[i]
    st.markdown("---")
    st.markdown(f"### LEVEL {i+1:02d}/10 // {q['topic'].upper()}")
    st.progress(i / len(QUESTIONS))
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f"**MISSION:** {q['q']}")
    choice = st.radio("Choose one action:", q["options"], index=None, key=f"answer_{i}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("LOCK IN ANSWER", use_container_width=True, disabled=choice is None):
        selected = q["options"].index(choice)
        correct = selected == q["answer"]
        st.session_state.answers[i] = {"selected": selected, "correct": correct}
        st.session_state.feedback = {"correct": correct, "why": q["why"], "source": q["source"]}
        st.rerun()
    if st.session_state.feedback is not None and i in st.session_state.answers:
        fb = st.session_state.feedback
        if fb["correct"]:
            st.success("✔ SAFE DECISION // +10 SAFETY POINTS")
        else:
            st.error("✖ HAZARD DETECTED // 0 POINTS — LEARN FROM IT")
        st.write(fb["why"])
        st.caption("Learning basis: " + fb["source"])
        if st.button("NEXT LEVEL →", use_container_width=True):
            st.session_state.q_index += 1
            st.session_state.feedback = None
            st.rerun()

elif st.session_state.page == "results":
    correct_count = sum(1 for a in st.session_state.answers.values() if a["correct"])
    score = correct_count * 10
    st.markdown("---")
    st.markdown("### 🏁 RUN COMPLETE")
    st.markdown(f'<div class="pixel-title">{score}% SAFETY METER</div>', unsafe_allow_html=True)
    st.progress(score / 100)
    if score >= PASS_THRESHOLD:
        st.success("TARGET REACHED — your garden blooms this week! 🌼")
    else:
        st.warning("TARGET NOT REACHED — review the feedback and replay to practise.")
    results = []
    for i, q in enumerate(QUESTIONS):
        a = st.session_state.answers.get(i, {})
        results.append({"Topic": q["topic"], "Result": "Correct" if a.get("correct") else "Review", "Learning point": q["why"]})
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    if st.button("SAVE RUN TO PLAYER HISTORY", use_container_width=True):
        history = load_history()
        history.append({
            "date": date.today().isoformat(),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "score": score,
            "correct": correct_count,
            "total": len(QUESTIONS),
            "topic_scores": {q["topic"]: (100 if st.session_state.answers.get(i, {}).get("correct") else 0) for i, q in enumerate(QUESTIONS)},
        })
        save_history(history)
        st.session_state.page = "home"
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.session_state.feedback = None
        st.success("Run saved. Dashboard updated.")
        st.rerun()
    if st.button("DISCARD RUN AND RETURN"):
        st.session_state.page = "home"
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.session_state.feedback = None
        st.rerun()

st.markdown("---")
st.markdown("### 📈 PLAYER HISTORY")
history = load_history()
if history:
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    st.line_chart(df.sort_values("date").set_index("date")["score"], y_label="Safety meter (%)")
    display_df = df.sort_values("timestamp", ascending=False)[["date", "score", "correct", "total"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df.columns = ["Date", "Score (%)", "Correct answers", "Questions"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.caption("No saved runs yet. Finish a quiz and save it to start your progress chart.")

with st.expander("📚 Sources and scope"):
    st.markdown("""
    This prototype uses general hazard-awareness principles, not a claim that one quiz satisfies every jurisdiction's law.

    - [Singapore Ministry of Manpower — Risk management](https://www.mom.gov.sg/workplace-safety-and-health/safety-and-health-management-systems/risk-management)
    - [Singapore Ministry of Manpower — WSH legislation](https://www.mom.gov.sg/legislation/workplace-safety-and-health)
    - [Singapore Statutes Online — Workplace Safety and Health (Risk Management) Regulations](https://sso.agc.gov.sg/SL/WSHA2006-RG8)
    - [US OSHA — Hazard identification and assessment](https://www.osha.gov/safety-management/hazard-identification)
    - [US OSHA — Worker participation](https://www.osha.gov/safety-management/worker-participation)
    - [US OSHA — Hazard Identification Training Tool](https://www.osha.gov/hazfinder/manual)

    Before using this commercially, have a qualified workplace safety professional validate the content against the customer's country, sector, risk assessments, safe-work procedures, and latest legal requirements. Healthcare and construction need separate specialist modules.
    """)

st.caption("DHΛLIA prototype • Local demo only • Do not enter real employee or incident data.")
