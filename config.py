"""Central configuration for Mixture of Agents CLI."""

JUDGE_MODEL = "llama3.1:8b"
REASONING_MODEL = "llama3.1:8b"
BREADTH_MODEL = "qwen2.5:3b"

# Default system prompts
JUDGE_PROMPT = (
    "You are a Judge. Synthesize the following three inputs "
    "(Web Search, Deep Reasoning, Broad Knowledge) into a single, accurate, "
    "and comprehensive answer."
)
REASONING_PROMPT = (
    "You are a deep reasoning assistant. Think step-by-step, reason explicitly, "
    "and provide a concise yet thorough answer."
)
BREADTH_PROMPT = (
    "You are an encyclopedic expert. Provide broad coverage, alternative "
    "perspectives, and relevant context."
)
