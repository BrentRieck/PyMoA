"""Web search agent powered by You.com unified search."""
from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Dict, List

from dotenv import load_dotenv
from youdotcom import SearchClient


@dataclass
class WebSearchResult:
    """Structured representation of a search response."""

    summary: str
    results: List[Dict[str, Any]]

    def format_for_judge(self) -> str:
        """Return a compact textual summary for the judge agent."""
        bullet_points = []
        for item in self.results:
            title = item.get("title") or item.get("name") or "Result"
            snippet = item.get("snippet") or item.get("description") or ""
            bullet_points.append(f"- {title}: {snippet}")
        bullets_text = "\n".join(bullet_points) if bullet_points else "No details available."
        return f"Summary: {self.summary}\nDetails:\n{bullets_text}"


class WebSearcher:
    """Wrapper around the You.com unified search endpoint."""

    def __init__(self, api_key_env: str = "YOU_COM_API_KEY") -> None:
        load_dotenv()
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing {api_key_env}. Please set it in your environment or .env file."
            )
        self.client = SearchClient(api_key=api_key)

    async def search(self, query: str) -> WebSearchResult:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, self._sync_search, query)
        results = response.get("hits", []) if isinstance(response, dict) else []
        summary = response.get("summary", "") if isinstance(response, dict) else ""
        return WebSearchResult(summary=summary, results=results)

    def _sync_search(self, query: str) -> Dict[str, Any]:
        return self.client.search.unified(query=query)  # type: ignore[attr-defined]
