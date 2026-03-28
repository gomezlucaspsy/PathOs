from __future__ import annotations
import os
from typing import Any

import anthropic
from dotenv import load_dotenv

from pathos.core.contradiction import Contradiction

load_dotenv()


class ClaudeSynthesizer:
    """
    The synthesis engine.

    In the dialectical loop:
      Thesis     = current code topology
      Antithesis = detected contradiction
      Synthesis  = Claude's interpretation

    Claude does not "fix" — it interprets. It names the structural
    tension and opens it up for the developer (the subject) to work through.
    This is analytic interpretation, not automated repair.
    """

    MODEL = "claude-opus-4-5"
    MAX_TOKENS = 1024

    SYSTEM_PROMPT = """You are PathOs — a structural analyst for codebases.
You interpret code not as sequences of instructions, but as topological spaces:
networks of relations, holes, loops, and tensions.

Your theoretical framework:
- Lacanian topology: Symbolic (syntax/structure), Imaginary (intent/model), Real (runtime/behavior)
- Dialectical materialism: contradictions are not errors to fix, but tensions that drive evolution
- Hillman's archetypal psychology: codebases have interiority, depth, and shadow

When presented with a contradiction in code topology, you:
1. Name what is structurally happening (precise, technical)
2. Interpret what it reveals about the system's deeper structure
3. Offer possible paths through the contradiction — not one "correct fix"
4. Note what the contradiction might be protecting or expressing

Be precise. Be honest about uncertainty. Do not reduce complexity prematurely.
Speak to the developer as a subject who must decide, not as a user who needs instructions."""

    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not found. "
                "Copy .env.example to .env and add your key."
            )
        self._client = anthropic.Anthropic(api_key=api_key)

    def interpret(
        self,
        contradiction: Contradiction,
        graph_summary: dict[str, Any],
    ) -> str:
        prompt = self._build_prompt(contradiction, graph_summary)
        message = self._client.messages.create(
            model=self.MODEL,
            max_tokens=self.MAX_TOKENS,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def _build_prompt(
        self,
        contradiction: Contradiction,
        graph_summary: dict[str, Any],
    ) -> str:
        nodes_preview = contradiction.nodes[:10]
        nodes_str = "\n".join(f"  - {n}" for n in nodes_preview)
        if len(contradiction.nodes) > 10:
            nodes_str += f"\n  ... and {len(contradiction.nodes) - 10} more"

        return f"""## Codebase topology summary
- Total nodes: {graph_summary.get('node_count', '?')}
- Total edges: {graph_summary.get('edge_count', '?')}
- Detected cycles: {graph_summary.get('cycle_count', '?')}
- Entangled clusters: {graph_summary.get('scc_count', '?')}
- Isolated nodes: {graph_summary.get('isolated_nodes', '?')}

## Contradiction detected
- Kind: {contradiction.kind.value}
- Lacanian register: {contradiction.lacanian_register}
- Severity: {contradiction.severity}/3
- Internal description: {contradiction.description}

## Affected nodes
{nodes_str}

## Your task
Interpret this contradiction. What does it reveal about the system?
What structural tensions is it expressing?
What are the possible paths through it?"""
