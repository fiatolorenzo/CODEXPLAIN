"""
Executes Pylint on a target Python file and returns
normalized static analysis findings.

Part of the CODEXPLAIN pipeline.
"""
import sys
import os
import json
import shutil
from rich import print
from rich.console import Console
from rich.panel import Panel
from run_pylint import run_pylint_on_path
from run_bandit import run_bandit_on_path
from run_radon import run_radon_on_path
from ai_explainer import explain_finding

console = Console()

pylint_findings = []
PYLINT_CODE = 0
PYLINT_STDERR = ""
PYLINT_STDOUT = ""

bandit_findings = []
BANDIT_CODE = 0
BANDIT_STDERR = ""
BANDIT_STDOUT = ""

radon_findings = []
RADON_CODE = 0
RADON_STDERR = ""
RADON_STDOUT = ""


def _write_match(finding, tool_name, ef, file_path):
    out = {
        "tool": tool_name,
        "file": file_path,
        "line": finding.get("line"),
        "message-id": finding.get("message-id"),
        "symbol": finding.get("symbol"),
        "message": finding.get("message"),
        "severity": finding.get("severity"),
        "code_context": finding.get("code_context")
    }
    ef.write(json.dumps(out, ensure_ascii=False) + "\n")

def _finding_message_id(finding):
    raw = finding.get("raw")
    if isinstance(raw, dict):
        mid = raw.get("message-id")
        if mid:
            return mid
    if finding.get("message-id"):
        return finding.get("message-id")
    return None

def main():

    """This function serves as the entry point of the program."""

    if len(sys.argv) < 2:
        print("Usage: python run_review.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    export_file = None

    if "--export" in sys.argv:
        index = sys.argv.index("--export")
        export_file = sys.argv[index + 1]

    if not os.path.exists(file_path):
        print(f"Error: file '{file_path}' does not exist.")
        sys.exit(2)

    if os.path.isdir(file_path):
        print(f"Error: '{file_path}' is a directory. Pass a .py file.")
        sys.exit(2)

    if not file_path.endswith(".py"):
        print(f"Warning: '{file_path}' does not end with .py — continuing anyway.")

    p_findings, _, _, _ = run_pylint_on_path(file_path)
    p_findings.sort(key=lambda f: f.get("line") or 0)
    b_findings, _, _, _ = run_bandit_on_path(file_path)
    b_findings.sort(key=lambda f: f.get("line") or 0)
    r_findings, _, _, _ = run_radon_on_path(file_path)
    r_findings.sort(key=lambda f: f.get("line") or 0)

    if export_file:

        expected_code = os.path.splitext(os.path.basename(file_path))[0]
        with open(export_file, "a", encoding="utf-8") as ef:
            all_tool_findings = [
                ("pylint", p_findings),
                ("bandit", b_findings),
                ("radon", r_findings),
            ]

            matched_count = 0
            for tool_name, findings in all_tool_findings:
                for finding in findings:
                    mid = _finding_message_id(finding)
                    if mid == expected_code:
                        _write_match(finding, tool_name, ef, file_path)
                        matched_count += 1

        if matched_count == 0:
            print(f"WARNING: No findings matched expected code {expected_code} — "
                  f"check filename or tool output.")
        elif matched_count > 1:
            print(f"WARNING: {matched_count} findings matched {expected_code};"
                  f" appended all matches.")

    console.print(
        Panel(
            "[bold cyan]CODEXPLAIN[/bold cyan]",
            expand=False
        )
    )


    print("\n[bold cyan]=== PYLINT FINDINGS ===[/bold cyan]\n")
    if not p_findings:
        print("No findings")
    else:
        for finding in p_findings:
            explanation = explain_finding(finding)
            severity = finding.get("severity")
            if severity == "HIGH":
                color = "bold red"
            elif severity == "MEDIUM":
                color = "bold yellow"
            else:
                color = "bold green"

            print(f"[{color}][{severity}][/] Line {finding['line']} - {finding['symbol']}")
            print(f"[bold]Issue:[/bold] {finding['message']}")
            if explanation.startswith("AI explanation skipped"):
                print(f"[dim]{explanation}[/dim]")
            else:
                print("[bold]Explanation:[/bold]")
                for line in explanation.split("\n"):
                    print(f"   [dim]{line}[/dim]")
            width = shutil.get_terminal_size().columns
            print(f"[blue]{'-' * width}[/blue]")

    width = shutil.get_terminal_size().columns
    print(f"[blue]{'-' * width}[/blue]")

    print("\n[bold cyan]=== BANDIT FINDINGS ===[/bold cyan]\n")
    if not b_findings:
        print("No findings")
    else:
        for finding in b_findings:
            explanation = explain_finding(finding)
            severity = finding.get("severity")
            if severity == "HIGH":
                color = "bold red"
            elif severity == "MEDIUM":
                color = "bold yellow"
            else:
                color = "bold green"

            print(f"[{color}][{severity}][/] Line {finding['line']} - {finding['symbol']}")
            print(f"[bold]Issue:[/bold] {finding['message']}")
            if explanation.startswith("AI explanation skipped"):
                print(f"[dim]{explanation}[/dim]")
            else:
                print("[bold]Explanation:[/bold]")
                for line in explanation.split("\n"):
                    print(f"   [dim]{line}[/dim]")
            width = shutil.get_terminal_size().columns
            print(f"[blue]{'-' * width}[/blue]")

    width = shutil.get_terminal_size().columns
    print(f"[blue]{'-' * width}[/blue]")

    print("\n[bold cyan]=== RADON FINDINGS === [/bold cyan]\n")
    if not r_findings:
        print("No findings")
    else:
        for finding in r_findings:
            explanation = explain_finding(finding)
            severity = finding.get("severity")
            if severity == "HIGH":
                color = "bold red"
            elif severity == "MEDIUM":
                color = "bold yellow"
            else:
                color = "bold green"

            print(f"[{color}][{severity}][/] Line {finding['line']} - Complexity Issue")
            print(f"[bold]Issue:[/bold] {finding['message']}")
            if explanation.startswith("AI explanation skipped"):
                print(f"[dim]{explanation}[/dim]")
            else:
                print("[bold]Explanation:[/bold]")
                for line in explanation.split("\n"):
                    print(f"   [dim]{line}[/dim]")
            width = shutil.get_terminal_size().columns
            print(f"[blue]{'-' * width}[/blue]")

    width = shutil.get_terminal_size().columns
    print(f"[blue]{'-' * width}[/blue]")

if __name__ == "__main__":
    main()
