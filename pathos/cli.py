from __future__ import annotations
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from pathos.services import AnalysisService, AnalysisOptions
from pathos.core.contradiction import ContradictionKind
from pathos.infrastructure.logging import get_logger

console = Console()
logger = get_logger("cli")

SEVERITY_COLORS = {1: "yellow", 2: "orange3", 3: "red"}
REGISTER_COLORS = {
    "Symbolic": "blue",
    "Imaginary": "green",
    "Real": "magenta",
}


@click.group()
def main() -> None:
    """PathOs — topological code analysis with dialectical contradiction detection."""


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--interpret",
    is_flag=True,
    default=False,
    help="Send top contradiction to Claude for interpretation.",
)
@click.option(
    "--all-interpret",
    is_flag=True,
    default=False,
    help="Send all contradictions to Claude for interpretation.",
)
def check(path: str, interpret: bool, all_interpret: bool) -> None:
    """Analyse PATH (file or directory) for topological contradictions."""
    target = Path(path)

    with console.status("[bold cyan]Parsing codebase topology...", spinner="dots"):
        service = AnalysisService()
        options = AnalysisOptions(interpret=interpret, interpret_all=all_interpret)
        
        if target.is_dir():
            result = service.analyze_directory(target, options)
        else:
            result = service.analyze_file(target, options)

    summary = result.summary
    contradictions = result.contradictions

    # Summary table
    table = Table(title="Topology Summary", box=box.ROUNDED, border_style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    table.add_row("Nodes", str(summary["node_count"]))
    table.add_row("Edges", str(summary["edge_count"]))
    table.add_row("Cycles", str(summary["cycle_count"]))
    table.add_row("Entangled clusters", str(summary["scc_count"]))
    table.add_row("Isolated nodes", str(summary["isolated_nodes"]))
    console.print(table)

    if not contradictions:
        console.print(
            Panel(
                "[bold green]No structural contradictions detected.[/]\n"
                "The topological space is clean — no holes, no loops, no dead ends.",
                border_style="green",
            )
        )
        return

    console.print(f"\n[bold]Found [red]{len(contradictions)}[/] contradiction(s):[/]\n")

    for i, c in enumerate(contradictions, 1):
        severity_color = SEVERITY_COLORS.get(c.severity, "white")
        register_color = REGISTER_COLORS.get(c.lacanian_register, "white")

        console.print(
            Panel(
                f"[bold {severity_color}]{c.kind.value.replace('_', ' ').upper()}[/]  "
                f"[{register_color}][{c.lacanian_register}][/]  "
                f"Severity: [{severity_color}]{'●' * c.severity}{'○' * (3 - c.severity)}[/]\n\n"
                f"{c.description}\n\n"
                f"[dim]Affected: {', '.join(c.nodes[:3])}"
                + (f" +{len(c.nodes)-3} more" if len(c.nodes) > 3 else "")
                + "[/]",
                title=f"[{i}]",
                border_style=severity_color,
            )
        )

    # Claude interpretation
    if interpret or all_interpret:
        try:
            from pathos.ai.claude import ClaudeSynthesizer
            synthesizer = ClaudeSynthesizer()
      Show interpretations if generated
    if result.interpretations:
        for kind, interpretation in result.interpretations.items():
            console.print(
                Panel(
                    interpretation,
                    title=f"[magenta]PathOs Interpretation — {kind