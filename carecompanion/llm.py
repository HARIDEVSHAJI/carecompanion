"""LLM providers. Groq and Azure OpenAI both use the OpenAI SDK; 'mock' needs no internet."""
import os
import time

from . import config

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


class OpenAICompatLLM:
    is_mock = False

    def __init__(self, client, model, label):
        self.client, self.model, self.label = client, model, label

    def chat(self, messages, tools=None, temperature=0.4):
        from openai import RateLimitError
        kwargs = dict(model=self.model, messages=messages, temperature=temperature, max_tokens=900)
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        for attempt in range(4):  # simple back-off for free-tier rate limits
            try:
                resp = self.client.chat.completions.create(**kwargs)
                break
            except RateLimitError:
                if attempt == 3:
                    raise
                time.sleep(8 * (attempt + 1))
        m = resp.choices[0].message
        calls = [{"id": c.id, "name": c.function.name, "arguments": c.function.arguments or "{}"}
                 for c in (m.tool_calls or [])]
        return {"content": m.content or "", "tool_calls": calls}


def get_llm(name=None):
    name = (name or config.provider()).lower()
    if name == "mock":
        from .mock_llm import MockLLM
        return MockLLM()
    from openai import AzureOpenAI, OpenAI
    if name == "groq":
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise RuntimeError("GROQ_API_KEY is missing. Put it in your .env file (see .env.example).")
        model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL)
        return OpenAICompatLLM(OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1"), model, f"groq:{model}")
    if name == "azure":
        key, ep = os.getenv("AZURE_OPENAI_API_KEY"), os.getenv("AZURE_OPENAI_ENDPOINT")
        if not key or not ep:
            raise RuntimeError("AZURE_OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT missing in .env")
        dep = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
        client = AzureOpenAI(api_key=key, azure_endpoint=ep, api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"))
        return OpenAICompatLLM(client, dep, f"azure:{dep}")
    raise ValueError(f"Unknown LLM_PROVIDER '{name}' (use groq, azure or mock)")
