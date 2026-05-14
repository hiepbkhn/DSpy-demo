"""
Demo: dspy.RLM — Recursive Language Model on a large text.

Loads Hegel's Lectures on the History of Philosophy (Vol 3, ~20k lines)
and uses DSPy's RLM module to answer 3 queries about its content.

RLM works by giving the LLM a sandboxed Python REPL. The model writes
and runs code to explore the context, call sub-LLMs for semantic analysis,
and iteratively build answers — ideal for long documents.

Usage:
    export OPENAI_API_KEY="sk-..."
    python demo_dspy_rlm.py
"""

import os
import dspy

DATA_FILE = "data/pg58169.txt"

QUERIES = [
    "What does Hegel identify as the three main periods covered in this volume?",
    "According to the text, what is Hegel's view on the relationship between Christianity and philosophy?",
    "Which specific philosophers or schools are discussed in the section on Arabian philosophy?",
]

# ── 1. Configure the LM ──────────────────────────────────────────────────

lm = dspy.LM('ollama_chat/nemotron-3-nano:30b-cloud', api_base='http://localhost:11434', api_key='')
dspy.configure(lm=lm)

# ── 2. Load the text ─────────────────────────────────────────────────────

with open(DATA_FILE, encoding="utf-8") as f:
    text = f.read()

print(f"Loaded {len(text):,} characters / {text.count(chr(10)):,} lines from {DATA_FILE}\n")

# ── 3. Build RLM and run queries ─────────────────────────────────────────

rlm = dspy.RLM(
    "context, query -> answer",
    max_iterations=15,
    verbose=True,
)

for i, query in enumerate(QUERIES, 1):
    print(f"\n{'='*70}")
    print(f"  Query {i}: {query}")
    print(f"{'='*70}\n")

    result = rlm(context=text, query=query)
    print(f"\n  Answer: {result.answer}")
    print()
