"""Mixture of Agents CLI entrypoint."""
from __future__ import annotations

import argparse
import asyncio
from typing import Dict

from colorama import Fore, Style, init

import config
from agents.judge import Judge
from agents.local_experts import LocalExperts
from agents.web_searcher import WebSearcher


async def run_layer0(query: str, experts: LocalExperts, web_agent: WebSearcher) -> Dict[str, str]:
    async def web_task() -> str:
        print(f"{Fore.GREEN}Running web search...{Style.RESET_ALL}")
        result = await web_agent.search(query)
        return result.format_for_judge()

    async def reasoning_task() -> str:
        print(f"{Fore.BLUE}Running reasoning model ({config.REASONING_MODEL})...{Style.RESET_ALL}")
        return await experts.run_reasoning(query)

    async def breadth_task() -> str:
        print(f"{Fore.YELLOW}Running breadth model ({config.BREADTH_MODEL})...{Style.RESET_ALL}")
        return await experts.run_breadth(query)

    web_result, reasoning_result, breadth_result = await asyncio.gather(
        web_task(), reasoning_task(), breadth_task()
    )

    return {
        "web": web_result,
        "reasoning": reasoning_result,
        "breadth": breadth_result,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mixture of Agents CLI")
    parser.add_argument("query", type=str, help="User query to send to the agent swarm")
    parser.add_argument(
        "--ollama-url",
        type=str,
        default="http://localhost:11434",
        help="Base URL for Ollama server.",
    )
    return parser


async def main_async(query: str, ollama_url: str) -> None:
    init(autoreset=True)

    web_agent = WebSearcher()
    experts = LocalExperts(base_url=ollama_url)
    judge = Judge(experts)

    layer0_outputs = await run_layer0(query, experts, web_agent)

    print(f"{Fore.CYAN}Layer 0 complete. Synthesizing with Judge...{Style.RESET_ALL}")
    final_answer = await judge.evaluate(
        query,
        web=layer0_outputs["web"],
        reasoning=layer0_outputs["reasoning"],
        breadth=layer0_outputs["breadth"],
    )

    print(f"{Style.BRIGHT + Fore.WHITE}Final Answer:\n{final_answer}{Style.RESET_ALL}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(main_async(query=args.query, ollama_url=args.ollama_url))


if __name__ == "__main__":
    main()
