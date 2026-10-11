"""Offline check: every turn sends all previous turns. Run: python test_memory.py"""
from types import SimpleNamespace

from study_buddy import ask


class FakeClient:
    def __init__(self):
        self.seen = []
        self.chat = SimpleNamespace(complete=self.complete)

    def complete(self, model, messages, temperature, max_tokens):
        self.seen.append(len(messages))
        msg = SimpleNamespace(content=f"reply {len(self.seen)}")
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])


c, msgs = FakeClient(), [{"role": "system", "content": "s"}]
for q in ("What is a variable?", "Give an example", "Why is it useful?"):
    ask(c, msgs, q)
assert c.seen == [2, 4, 6], c.seen  # context grows each turn
assert [m["role"] for m in msgs] == ["system"] + ["user", "assistant"] * 3
print("memory OK")
