"""CareCompanion web app:  streamlit run app.py"""
import streamlit as st

from carecompanion import config
from carecompanion.agent import CareAgent
from carecompanion.data_loader import DataStore
from carecompanion.db import Database
from carecompanion.llm import get_llm
from carecompanion.scripts import get_scripts_for_user
from carecompanion.synthetic import ensure_data, get_all_people, create_new_user

st.set_page_config(page_title="CareCompanion", page_icon="🩺", layout="wide")


@st.cache_resource
def resources():
    ensure_data()
    db = Database(config.DB_PATH)
    for uid, p in get_all_people().items():
        db.ensure_user(uid, p["name"])
    try:
        llm, err = get_llm(), None
    except Exception as e:  # e.g. missing key: fall back to the offline mock
        from carecompanion.mock_llm import MockLLM
        llm, err = MockLLM(), str(e)
    return db, DataStore(), llm, err


db, store, llm, llm_err = resources()
S = st.session_state
all_people = get_all_people()
for u, p in all_people.items():
    db.ensure_user(u, p["name"])

# ---------------- sidebar ----------------
with st.sidebar:
    st.title("🩺 CareCompanion")
    st.caption(f"AI model: **{getattr(llm, 'label', 'mock')}**")
    if llm_err:
        st.warning(f"{llm_err}\n\nUsing the offline mock model instead.")

    person_keys = list(all_people.keys())
    cur_idx = person_keys.index(S["uid"]) if S.get("uid") in person_keys else 0
    uid = st.selectbox("Person", person_keys, index=cur_idx, format_func=lambda u: f"{all_people[u]['name']} ({u})")

    with st.expander("➕ Add New User", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            new_name = st.text_input("Name", placeholder="e.g. Maya")
            new_goal = st.selectbox("Primary Focus", [
                "Increase Daily Steps & Activity",
                "Improve Sleep Quality & Rest",
                "Lower Resting Heart Rate & Cardio Fitness",
                "General Health & Wellness"
            ])
            submitted = st.form_submit_button("Create User", type="primary")
            if submitted and new_name.strip():
                new_uid, info = create_new_user(new_name.strip(), new_goal)
                db.ensure_user(new_uid, info["name"])
                S.update(uid=new_uid, agent=None, chat=[], just_created=info["name"])
                st.rerun()

    if S.get("just_created"):
        st.success(f"Added **{S.pop('just_created')}**! Click **Start new session** to begin.")

    memory_on = st.toggle("Memory ON", value=True, help="Turn OFF to see generic advice with no history.")
    if S.get("uid") != uid or S.get("mem") != memory_on:
        if S.get("agent") and S.get("chat"):
            S.agent.end_session()
        S.update(uid=uid, mem=memory_on, agent=None, chat=[])
    n_done = db.session_count(uid)
    st.write(f"Sessions so far: **{n_done}**")
    if S.agent is None:
        if st.button("▶ Start new session", type="primary"):
            S.agent = CareAgent(db, llm, store, uid, memory_enabled=memory_on)
            S.agent.start_session()
            S.chat = []
            st.rerun()
    else:
        sess = S.agent.session
        st.success(f"Session {sess['session_no']} · data up to {sess['sim_date']}")
        if st.button("⏹ End session & save memory"):
            r = S.agent.end_session()
            S.update(agent=None, chat=[], last_summary=r["summary"])
            st.rerun()
        st.markdown("**Sample messages** (click to send):")
        user_scripts = get_scripts_for_user(uid, all_people[uid]["name"], all_people[uid].get("goal", "wellness"))
        sn = min(sess["session_no"], len(user_scripts)) - 1
        for i, m in enumerate(user_scripts[sn]):
            if st.button(m[:55] + "…", key=f"s{i}"):
                S.pending = m
    if S.get("last_summary"):
        st.info("Saved memory: " + S.last_summary)
    if st.button("🗑 Reset this person's memory"):
        db.reset_user(uid)
        S.update(agent=None, chat=[], last_summary=None)
        st.rerun()

# ---------------- main ----------------
left, right = st.columns([3, 2])
prompt = st.chat_input("Message CareCompanion…", disabled=S.agent is None)
prompt = prompt or S.pop("pending", None)
if prompt and S.agent:
    with st.spinner("Thinking…"):
        out = S.agent.chat(prompt)
    S.chat += [("user", prompt, []), ("assistant", out["reply"], out["trace"])]

with left:
    st.subheader(f"Coaching chat · {all_people[uid]['name']}")
    if S.agent is None:
        st.info("Click **Start new session** in the sidebar. Run session 1, end it, then start session 2 and 3 to see the advice adapt.")
    for role, text, trace in S.chat:
        with st.chat_message(role):
            st.markdown(text)
            if trace:
                with st.expander(f"🔧 {len(trace)} tool call(s)"):
                    for t in trace:
                        st.code(f"{t['tool']}({t['args']})\n→ {t['result']}", language="json")

with right:
    tab1, tab2, tab3 = st.tabs(["🧠 Memory", "✅ Advice tracker", "📈 Fitbit data"])
    with tab1:
        mems = db.memories(uid)
        if not mems:
            st.caption("Nothing remembered yet.")
        for m in mems:
            st.markdown(f"**S{m['session_no']} · {m['category']}**: {m['content']}")
    with tab2:
        adv = db.advice(uid)
        if not adv:
            st.caption("No advice logged yet.")
        for a in adv:
            icon = {"improved": "🟢", "no_change": "🟡", "worse": "🔴", "open": "⏳"}[a["status"]]
            chg = f" ({a['change_pct']:+.0f}%)" if a["change_pct"] is not None else ""
            st.markdown(f"{icon} **S{a['session_no']} · {a['metric']}** {a['baseline']}→{a['current'] if a['current'] else '?'}{chg}  \n{a['text']}")
    with tab3:
        sess_no = S.agent.session["session_no"] if S.agent else n_done + 1
        end = store.date_for_session(uid, sess_no)
        import pandas as pd
        df = pd.DataFrame(store.series(uid, end)).set_index("date")
        for col, label in (("steps", "Steps"), ("sleep_hours", "Sleep (h)"), ("resting_hr", "Resting HR")):
            st.caption(label)
            st.line_chart(df[col], height=120)

