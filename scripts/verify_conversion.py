#!/usr/bin/env python3
"""Static checks for VHDL-to-SystemVerilog conversion artifacts.

This script does not run Efinity, Questa, or any synthesis/simulation flow.
It checks generated SV and conversion notes for reviewability and rule
consistency. It is not a formal equivalence checker.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Check:
    level: str
    status: str
    name: str
    message: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def combined_text(paths: Iterable[Path]) -> str:
    return "\n".join(read_text(path) for path in paths)


def add(checks: list[Check], level: str, status: str, name: str, message: str) -> None:
    checks.append(Check(level, status, name, message))


def pattern_found(pattern: str, text: str) -> bool:
    try:
        return re.search(pattern, text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE) is not None
    except re.error:
        return pattern.lower() in text.lower()


def load_eval_case(config_path: Path | None, eval_id: int | None) -> dict:
    if config_path is None or eval_id is None:
        return {}
    data = json.loads(read_text(config_path))
    for case in data.get("evals", []):
        if case.get("id") == eval_id:
            return case
    raise SystemExit(f"eval id {eval_id} not found in {config_path}")


def check_l0(checks: list[Check], notes_text: str) -> None:
    if not notes_text.strip():
        add(checks, "L0", "WARN", "report-text", "No conversion notes/report text was provided.")
        return
    required = [
        "Generated Files",
        "Conversion Notes",
        "Manual Review Items",
        "Synthesizability Checklist",
        "Validation Results",
    ]
    missing = [section for section in required if section not in notes_text]
    if missing:
        add(checks, "L0", "FAIL", "required-sections", "Missing sections: " + ", ".join(missing))
    else:
        add(checks, "L0", "PASS", "required-sections", "All required response sections are present.")


def check_l1_static(checks: list[Check], vhdl_text: str, sv_text: str, notes_text: str) -> None:
    review_text = sv_text + "\n" + notes_text

    if re.search(r"\b(module|package)\b", sv_text):
        add(checks, "L1", "PASS", "design-unit", "Generated SV contains module/package.")
    else:
        add(checks, "L1", "FAIL", "design-unit", "Generated SV contains no module/package.")

    if re.search(r"\bmodule\b", sv_text):
        typed_port = r"\b(input|output|inout)\b\s+(?:wire\s+|logic\s+|bit\s+|reg\s+|signed\s+|\[[^]]+\]\s+)"
        if re.search(typed_port, sv_text):
            add(checks, "L1", "PASS", "typed-ports", "Module ports appear explicitly typed.")
        else:
            add(checks, "L1", "WARN", "typed-ports", "No clearly typed module ports were detected.")

        if re.search(r"\b(input|output|inout)\s+var\b", sv_text):
            add(checks, "L1", "FAIL", "portable-ports", "Synthesizable module ports must not use explicit var port kind.")
        else:
            add(checks, "L1", "PASS", "portable-ports", "No explicit var port kind detected on module ports.")

    if re.search(r"\b(rising_edge|falling_edge)\s*\(", vhdl_text, flags=re.IGNORECASE):
        if "always_ff" in sv_text:
            add(checks, "L1", "PASS", "clocked-process", "Clocked process maps to always_ff.")
        else:
            add(checks, "L1", "FAIL", "clocked-process", "Clocked VHDL process found but no always_ff detected.")

    if re.search(r"\bprocess\s*\(", vhdl_text, flags=re.IGNORECASE) and not re.search(
        r"\b(rising_edge|falling_edge)\s*\(", vhdl_text, flags=re.IGNORECASE
    ):
        if "always_comb" in sv_text or re.search(r"\bassign\b", sv_text):
            add(checks, "L1", "PASS", "comb-process", "Combinational process maps to always_comb or assign.")
        else:
            add(checks, "L1", "WARN", "comb-process", "Combinational process found but no always_comb/assign detected.")

    forbidden = {
        "dynamic-array": r"\b(?:logic|bit|reg|wire|int|byte|\w+_t)\b\s+(?:signed\s+)?(?:\[[^]]+\]\s*)?\w+\s*\[\s*\]\s*;",
        "queue": r"\[$\]",
        "initial-block": r"\binitial\b",
        "delay-control": r"(?<!')#\s*\d",
        "wait-statement": r"\bwait\s*(?:\(|;)",
        "file-io": r"\$(?:fopen|fclose|fread|fwrite|display|monitor)\b",
    }
    for name, regex in forbidden.items():
        if re.search(regex, sv_text):
            add(checks, "L1", "FAIL", name, f"Forbidden or testbench-oriented SV construct detected: {name}.")
        else:
            add(checks, "L1", "PASS", name, f"No {name} pattern detected.")

    risky = {
        "resize": r"\bresize\s*\(",
        "ext": r"\bext\s*\(",
        "sxt": r"\bsxt\s*\(",
        "attribute": r"'(?:length|range|left|right|high|low)\b",
        "constrained-integer": r"\b(?:integer|natural|positive)\s+range\b",
        "shift": r"\bshift_(?:left|right)\s*\(|\b(?:sll|srl|sla|sra)\b",
        "inout-buffer": r"\b(?:inout|buffer|linkage)\b",
        "file-wait": r"\b(?:file|textio|wait)\b",
    }
    for name, regex in risky.items():
        if re.search(regex, vhdl_text, flags=re.IGNORECASE):
            tokens = name.split("-")
            if any(token in review_text.lower() for token in tokens):
                add(checks, "L1", "PASS", f"documented-{name}", f"{name} appears documented.")
            else:
                add(checks, "L1", "WARN", f"documented-{name}", f"VHDL uses {name}; document the conversion decision.")

    if re.search(r"\b(?:resize|ext|sxt)\s*\(", vhdl_text, flags=re.IGNORECASE):
        if "$signed" in sv_text or "$unsigned" in sv_text:
            add(checks, "L1", "WARN", "resize-shorthand", "$signed/$unsigned found; document target-width proof.")

    if re.search(r"\b(?:integer|natural|positive)\s+range\b", vhdl_text, flags=re.IGNORECASE):
        suspicious_int_storage = [
            r"\btypedef\s+int(?:\s+(?:signed|unsigned))?\s+\w+\s*\[[^]]+\]\s*;",
            r"\btypedef\s+int(?:\s+(?:signed|unsigned))?\s+\w+\s*;",
            r"\bstruct\b[\s\S]*?\bint(?:\s+(?:signed|unsigned))?\s+\w+\s*(?:\[[^]]+\])?\s*;",
        ]
        if any(re.search(pattern, sv_text, flags=re.IGNORECASE) for pattern in suspicious_int_storage):
            status = "WARN" if re.search(r"manual review|Manual Review|人工审查|人工确认", review_text) else "FAIL"
            add(
                checks,
                "L1",
                status,
                "constrained-integer-int-storage",
                "VHDL contains constrained integer ranges, but generated SV appears to store them as 32-bit int. Use fixed-width logic for storage or keep it only with an explicit manual-review exception.",
            )
        elif re.search(r"\blogic(?:\s+signed)?\s*\[[^]]+\]", sv_text):
            add(checks, "L1", "PASS", "constrained-integer-width", "Constrained integer range appears converted to explicit logic width.")
        else:
            add(
                checks,
                "L1",
                "WARN",
                "constrained-integer-width",
                "VHDL contains constrained integer ranges; verify generated SV uses explicit logic widths for hardware storage.",
            )
        if "VHDL2SV:" not in review_text or "integer range" not in review_text.lower():
            add(
                checks,
                "L1",
                "WARN",
                "constrained-integer-comment",
                "Document constrained integer conversions with a local VHDL2SV comment or Conversion Notes including the original range.",
            )

    if re.search(r"\bshift_(?:left|right)\s*\(|\b(?:sll|srl|sla|sra)\b", vhdl_text, flags=re.IGNORECASE):
        if re.search(r"\bshift_(?:left|right)\s*\(", sv_text, flags=re.IGNORECASE):
            add(
                checks,
                "L1",
                "FAIL",
                "vhdl-shift-left-in-sv",
                "Generated SV still contains VHDL shift_left/shift_right calls. Convert to SV shift operators or a documented helper.",
            )
        elif re.search(r"(?:<<<|>>>|<<|>>)", sv_text):
            add(checks, "L1", "PASS", "shift-operator", "VHDL shift operation appears mapped to an SV shift operator.")
        else:
            add(
                checks,
                "L1",
                "WARN",
                "shift-operator",
                "VHDL shift operation found; verify generated SV explicitly implements the shift behavior.",
            )
        if "shift" not in review_text.lower() and "VHDL2SV:" not in review_text:
            add(
                checks,
                "L1",
                "WARN",
                "shift-documentation",
                "Document non-trivial VHDL shift conversion, including logical/arithmetic behavior and result width.",
            )


def check_eval_patterns(checks: list[Check], case: dict, sv_text: str, notes_text: str) -> None:
    if not case:
        add(checks, "L1", "SKIP", "eval-patterns", "No eval case selected.")
        return
    text = sv_text + "\n" + notes_text
    for pattern in case.get("must_have", []):
        if pattern_found(pattern, text):
            add(checks, "L1", "PASS", f"must-have:{pattern}", "Required eval pattern found.")
        else:
            add(checks, "L1", "FAIL", f"must-have:{pattern}", "Required eval pattern not found.")
    for pattern in case.get("must_not_have", []):
        if pattern_found(pattern, text):
            add(checks, "L1", "FAIL", f"must-not-have:{pattern}", "Forbidden eval pattern found.")
        else:
            add(checks, "L1", "PASS", f"must-not-have:{pattern}", "Forbidden eval pattern not found.")


def render_markdown(checks: list[Check]) -> str:
    priority = {"FAIL": 0, "WARN": 1, "SKIP": 2, "PASS": 3}
    checks = sorted(checks, key=lambda c: (c.level, priority.get(c.status, 9), c.name))
    lines = ["## Validation Results", "", "| Level | Status | Check | Message |", "| --- | --- | --- | --- |"]
    for check in checks:
        msg = check.message.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check.level} | {check.status} | {check.name} | {msg} |")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Static VHDL-to-SV conversion checker.")
    parser.add_argument("--vhdl", action="append", default=[], help="Source VHDL file. Repeat for multiple files.")
    parser.add_argument("--sv", action="append", default=[], help="Generated SV file. Repeat for multiple files.")
    parser.add_argument("--notes", help="Optional conversion report/notes markdown.")
    parser.add_argument("--eval-config", help="Optional evals/evals.json path.")
    parser.add_argument("--eval-id", type=int, help="Optional eval id.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    vhdl_paths = [Path(p) for p in args.vhdl]
    sv_paths = [Path(p) for p in args.sv]
    if not vhdl_paths:
        raise SystemExit("at least one --vhdl file is required")
    if not sv_paths:
        raise SystemExit("at least one --sv file is required")

    notes_path = Path(args.notes) if args.notes else None
    for path in [*vhdl_paths, *sv_paths, *([notes_path] if notes_path else [])]:
        if path is not None and not path.exists():
            raise SystemExit(f"file not found: {path}")

    vhdl_text = combined_text(vhdl_paths)
    sv_text = combined_text(sv_paths)
    notes_text = read_text(notes_path) if notes_path else ""
    case = load_eval_case(Path(args.eval_config) if args.eval_config else None, args.eval_id)

    checks: list[Check] = []
    check_l0(checks, notes_text)
    check_l1_static(checks, vhdl_text, sv_text, notes_text)
    check_eval_patterns(checks, case, sv_text, notes_text)
    add(checks, "L2", "SKIP", "syntax-tool", "Not run in this conversion-only workflow.")
    add(checks, "L3", "SKIP", "functional-simulation", "Not run; Questa simulation is a later external workflow.")
    add(checks, "L4", "SKIP", "efinity-synthesis", "Not run; Efinity project flow is out of scope for this workflow.")

    if args.format == "json":
        print(json.dumps({"checks": [asdict(c) for c in checks]}, indent=2))
    else:
        print(render_markdown(checks))

    return 1 if any(check.status == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
