"""Judge agent that synthesizes outputs from other agents."""
from __future__ import annotations

from typing import Dict

import config
from agents.local_experts import LocalExperts


class Judge:
    """Combines inputs from web, reasoning, and breadth agents."""

    def __init__(self, experts: LocalExperts) -> None:
        self.experts = experts

    async def evaluate(self, query: str, web: str, reasoning: str, breadth: str) -> str:
        judge_prompt = (
            f"{config.JUDGE_PROMPT}\n\n"
            f"User Query:\n{query}\n\n"
            "Web Search Findings:\n"
            f"{web}\n\n"
            "Deep Reasoning:\n"
            f"{reasoning}\n\n"
            "Broad Knowledge:\n"
            f"{breadth}"
        )
        return await self.experts.run_judge(judge_prompt)


def format_layer0_outputs(outputs: Dict[str, str]) -> str:
    return "\n\n".join(f"{k.title()} Agent:\n{v}" for k, v in outputs.items())
