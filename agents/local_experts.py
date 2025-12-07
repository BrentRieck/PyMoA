"""Local Ollama-based experts for reasoning and breadth."""
from __future__ import annotations

from typing import Dict, Optional

from ollama import AsyncClient

import config


class LocalExperts:
    """Manages local Ollama interactions for reasoning and breadth."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.client = AsyncClient(host=base_url)
        self._shared_reasoning_model = config.REASONING_MODEL
        self._breadth_model = config.BREADTH_MODEL

    async def run_reasoning(self, prompt: str, context: Optional[str] = None) -> str:
        system_prompt = config.REASONING_PROMPT
        full_prompt = self._compose_prompt(system_prompt, prompt, context)
        response = await self.client.chat(
            model=self._shared_reasoning_model,
            messages=[{"role": "user", "content": full_prompt}],
        )
        return self._extract_content(response)

    async def run_breadth(self, prompt: str, context: Optional[str] = None) -> str:
        system_prompt = config.BREADTH_PROMPT
        full_prompt = self._compose_prompt(system_prompt, prompt, context)
        response = await self.client.chat(
            model=self._breadth_model,
            messages=[{"role": "user", "content": full_prompt}],
        )
        return self._extract_content(response)

    async def run_judge(self, prompt: str) -> str:
        response = await self.client.chat(
            model=config.JUDGE_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return self._extract_content(response)

    def _compose_prompt(self, system_prompt: str, user_prompt: str, context: Optional[str]) -> str:
        if context:
            return f"{system_prompt}\n\nContext:\n{context}\n\nUser Query:\n{user_prompt}"
        return f"{system_prompt}\n\nUser Query:\n{user_prompt}"

    def _extract_content(self, response: Dict[str, str]) -> str:
        message = response.get("message") or {}
        return message.get("content", "")
