"""The CareCompanion agent: an LLM in a tool-calling loop, with persistent memory."""
import json

from . import reflection, safety
from .memory import Memory
from .tools import ToolBox

MAX_STEPS = 6

SYSTEM = """You are CareCompanion, a warm, practical, and empathetic wellness coach for {name}. This is session {n} (Fitbit data up to {date}).
Long-term memory is {mem}.

{how}

RULES
- You are not a doctor: never diagnose, never suggest medication, supplements or extreme diets. Respect injuries and limits the user told you.
- Use only numbers returned by tools. Never invent data.
- Be concise (under 170 words), friendly, plain language. Use the user's own preferences (activities, time of day) in your advice.
- CRITICAL TONE: Speak directly to the user as a supportive, human wellness coach. NEVER mention internal tool names, function calls, database operations, or "saving to memory" to the user.
- NEVER output raw XML tags, code snippets, or <tool_call> in your user-facing message.
- ALWAYS PROVIDE ACTIONABLE COACHING: Acknowledge the user's situation and constraints supportively (e.g. protecting their lower back), and provide 1-2 concrete, realistic recommendations tailored to their goal and preferred schedule.
"""
HOW_ON = """HOW YOU WORK. On your FIRST reply of every session, in this order:
1. get_user_profile  2. recall_memories (query = what the user just said)  3. get_health_summary  4. check_advice_outcomes
Then reply: say what you remember; report earlier advice outcomes honestly with the real numbers (celebrate what worked;
if advice did NOT work, say so and CHANGE the strategy, never repeat it); then give 1-2 specific recommendations.
For EACH recommendation call log_advice (metric = steps, sleep_hours or resting_hr) so it can be checked next session.
On later replies: call recall_memories if useful, stay consistent with the plan, answer the user's question.
Always provide warm, empathetic, and actionable coaching advice directly to the user."""
HOW_OFF = """Memory is OFF: you have NO user profile or history. Use only get_health_summary, give general advice, and never claim to remember anything."""


class CareAgent:
    def __init__(self, db, llm, store, user_id, memory_enabled=True):
        self.db, self.llm, self.store, self.user_id, self.memory_enabled = db, llm, store, user_id, memory_enabled
        self.mem = Memory(db, user_id)
        self.session = self.tools = None
        self.messages = []

    # ---------- session lifecycle ----------
    def start_session(self):
        n = self.db.session_count(self.user_id) + 1
        sim_date = self.store.date_for_session(self.user_id, n)
        self.session = self.db.new_session(self.user_id, sim_date)
        self.tools = ToolBox(self.db, self.mem, self.store, self.user_id, self.session, self.memory_enabled)
        name = self.db.user(self.user_id)["name"]
        system = SYSTEM.format(name=name, n=self.session["session_no"], date=sim_date,
                               mem="ON" if self.memory_enabled else "OFF", how=HOW_ON if self.memory_enabled else HOW_OFF)
        self.messages = [{"role": "system", "content": system}]
        return self.session

    def end_session(self):
        """Reflection step: summarise the session and store durable memories."""
        sid = self.session["id"]
        convo = self.db.messages(sid)
        if not self.memory_enabled:
            self.db.end_session(sid, "(memory off: nothing stored)")
            return {"summary": "", "saved": 0}
        users = [m["content"] for m in convo if m["role"] == "user"]
        advice = [a["text"] for a in self.db.advice(self.user_id) if a["session_id"] == sid]
        result = None
        if not getattr(self.llm, "is_mock", False):
            try:
                transcript = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in convo)
                result = reflection.llm_reflect(self.llm, transcript, advice)
            except Exception:
                result = None  # fall back to the rule-based version
        result = result or reflection.heuristic_reflect(users, self.session["session_no"], advice)
        saved = sum(self.mem.add(self.session, m["category"], m["content"], m["importance"]) for m in result["memories"])
        self.mem.add(self.session, "summary", result["summary"], 4)
        self.db.end_session(sid, result["summary"])
        return {"summary": result["summary"], "saved": saved}

    # ---------- chatting ----------
    def chat(self, text):
        self.db.add_message(self.session["id"], "user", text)
        trace = []
        flag = safety.check_red_flags(text)
        if flag:
            self.messages.append({"role": "user", "content": text})
            self.messages.append({"role": "assistant", "content": flag})
            self.db.add_message(self.session["id"], "assistant", flag)
            return {"reply": flag, "trace": [{"tool": "safety_check", "args": {}, "result": "red flag detected"}]}
        self.messages.append({"role": "user", "content": text})
        self._live_capture(text)
        try:
            reply = self._loop(trace)
        except Exception as e:
            trace.append({"tool": "error", "args": {}, "result": f"{type(e).__name__}: {e} (using fallback)"})
            reply = self._fallback(text, trace)
        reply = self._clean_reply(reply).strip()
        if not reply:
            name = self.db.user(self.user_id)["name"]
            reply = f"Hi {name}! I've noted your goals and limitations carefully. Let's start with a gentle routine tailored to your schedule, and we'll track your progress together step by step."
        reply = reply + safety.DISCLAIMER
        self.db.add_message(self.session["id"], "assistant", reply)
        return {"reply": reply, "trace": trace}

    def _live_capture(self, text):
        """Offline mock only: store goals/limits/preferences the moment they are said, so advice in the same
        reply can use them. (A real LLM does this itself via the save_memory tool.)"""
        if self.memory_enabled and getattr(self.llm, "is_mock", False):
            for m in reflection.heuristic_reflect([text], self.session["session_no"], [])["memories"]:
                if m["category"] in ("goal", "constraint", "preference"):
                    self.mem.add(self.session, m["category"], m["content"], m["importance"])

    def _clean_reply(self, text):
        import re
        if not text:
            return ""
        # Strip any tool call XML or pseudo tags completely
        cleaned = re.sub(r"<tool_call>[\s\S]*?</tool_call>", "", text, flags=re.IGNORECASE)
        cleaned = re.sub(r"<tool_call>[\s\S]*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<\/?(?:function|parameter|tool_call)[^>]*>", "", cleaned, flags=re.IGNORECASE)
        # Strip internal developer meta-text
        cleaned = re.sub(r"(?:I need to|Let me|I'm going to)\s+save[^\n.]*(?:memory|facts)[^.\n]*\.?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"I have saved [^\n.]* to (?:my )?memory\.*", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def _loop(self, trace):
        import re
        for _ in range(MAX_STEPS):
            out = self.llm.chat(self.messages, self.tools.schemas())
            text = out.get("content") or ""

            # If the model emitted tool call XML in text, parse and execute it
            if "<tool_call>" in text:
                match = re.search(r"<function=(\w+)>[\s\S]*?<parameter=content>([\s\S]*?)</parameter>", text)
                if match:
                    fn_name, fn_content = match.group(1), match.group(2).strip()
                    if fn_name == "save_memory":
                        self.tools.call("save_memory", json.dumps({"category": "constraint", "content": fn_content}))
                        trace.append({"tool": "save_memory", "args": {"content": fn_content}, "result": "saved from text call"})

            if not out["tool_calls"]:
                cleaned = self._clean_reply(text)
                if len(cleaned) > 25:
                    self.messages.append({"role": "assistant", "content": cleaned})
                    return cleaned
                # If content was only leaked tool calls or meta-text, prompt for warm conversational reply
                self.messages.append({"role": "user", "content": "Please give your warm, encouraging wellness coaching recommendations directly to me now. Do not mention tools, code, or memory."})
                final_out = self.llm.chat(self.messages, None)
                final_clean = self._clean_reply(final_out.get("content") or "")
                self.messages.append({"role": "assistant", "content": final_clean})
                return final_clean

            self.messages.append({"role": "assistant", "content": out["content"] or None, "tool_calls": [
                {"id": c["id"], "type": "function", "function": {"name": c["name"], "arguments": c["arguments"]}}
                for c in out["tool_calls"]]})
            for c in out["tool_calls"]:
                result = self.tools.call(c["name"], c["arguments"])
                trace.append({"tool": c["name"], "args": c["arguments"], "result": result[:600]})
                self.messages.append({"role": "tool", "tool_call_id": c["id"], "content": result})
        final_out = self.llm.chat(self.messages, None)  # tool budget used up: force a final answer
        final_clean = self._clean_reply(final_out.get("content") or "")
        self.messages.append({"role": "assistant", "content": final_clean})
        return final_clean

    def _fallback(self, text, trace):
        """If tool calling fails (some models do sometimes), gather context ourselves and ask without tools."""
        ctx = {}
        for name, args in (("get_user_profile", {}), ("recall_memories", {"query": text}),
                           ("get_health_summary", {}), ("check_advice_outcomes", {})):
            if name in self.tools.names():
                ctx[name] = json.loads(self.tools.call(name, args))
        plain = [m for m in self.messages if m["role"] in ("system", "user") or (m["role"] == "assistant" and m.get("content"))]
        plain = [{"role": m["role"], "content": m["content"]} for m in plain if not m.get("tool_calls")]
        plain.insert(1, {"role": "system", "content": "Context from your tools (use it, do not invent data):\n" + json.dumps(ctx)})
        content = self.llm.chat(plain, None)["content"]
        self.messages.append({"role": "assistant", "content": content})
        return content
