"""Check that your AI provider works (including tool calling):  python check_connection.py"""
import json

from carecompanion import config
from carecompanion.llm import get_llm

print("Provider:", config.provider())
llm = get_llm()
print("Model   :", getattr(llm, "label", "mock"))
if getattr(llm, "is_mock", False):
    print("Mock mode: no real AI is used. Add GROQ_API_KEY to .env to use a real model.")
    raise SystemExit(0)
tool = [{"type": "function", "function": {"name": "get_number", "description": "Returns a number.",
         "parameters": {"type": "object", "properties": {}, "required": []}}}]
out = llm.chat([{"role": "user", "content": "Call the get_number tool."}], tool)
if out["tool_calls"]:
    print("OK: connection works and the model can call tools ->", out["tool_calls"][0]["name"])
else:
    print("Connected, but the model did not call the tool. Reply was:", out["content"][:200])
