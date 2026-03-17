#!/usr/bin/env python3
"""
translate_workflow.py

Automation helper for SPL -> CrowdStrike LogScale prompt workflows.
It does not call Claude directly. Instead, it builds consistent prompts,
stores metadata, and creates a run directory so the analyst can work in a
repeatable way from VS Code / terminal / Claude Code.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "ai" / "prompts"
RUNS_DIR = ROOT / "runs"


@dataclass
class RunMetadata:
    run_id: str
    mode: str
    created_at: str
    title: str
    source: str
    goal: str
    fields: list[str]
    input_file: str | None = None
    error_file: str | None = None
    expected: str | None = None
    notes: str | None = None


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"(^-|-$)", "", text) or "query"


def load_text(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8").strip()


def load_template(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8")


def replace_tokens(template: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def split_fields(raw: str) -> list[str]:
    if not raw.strip():
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def make_run_dir(title: str) -> tuple[str, Path]:
    timestamp = utc_now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{timestamp}-{slugify(title)[:50]}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_id, run_dir


def write_file(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_translate_prompt(args: argparse.Namespace, spl: str) -> str:
    template = load_template("translate_query.md")
    return replace_tokens(
        template,
        {
            "SPL_QUERY": spl,
            "SOURCE": args.source,
            "FIELDS": ", ".join(split_fields(args.fields)) or "Not provided",
            "GOAL": args.goal,
        },
    )


def build_debug_prompt(args: argparse.Namespace, query: str, error: str) -> str:
    template = load_template("debug_query.md")
    return replace_tokens(
        template,
        {
            "QUERY": query,
            "ERROR": error,
            "FIELDS": ", ".join(split_fields(args.fields)) or "Not provided",
            "EXPECTED": args.expected or "Not provided",
        },
    )


def build_review_prompt(args: argparse.Namespace, spl: str, cql: str) -> str:
    template = load_template("review_query.md")
    return replace_tokens(template, {"SPL": spl, "CQL": cql})


def write_summary(run_dir: Path, meta: RunMetadata, files: dict[str, str]) -> None:
    body = dedent(
        f"""
        # Run Summary

        - **Run ID:** {meta.run_id}
        - **Mode:** {meta.mode}
        - **Created at:** {meta.created_at}
        - **Title:** {meta.title}
        - **Source:** {meta.source}
        - **Goal:** {meta.goal}
        - **Fields:** {', '.join(meta.fields) if meta.fields else 'Not provided'}

        ## Files
        """
    ).strip()
    for label, rel in files.items():
        body += f"\n- **{label}:** `{rel}`"
    write_file(run_dir / "SUMMARY.md", body)


def do_translate(args: argparse.Namespace) -> int:
    spl = load_text(Path(args.spl_file))
    run_id, run_dir = make_run_dir(args.title)

    prompt = build_translate_prompt(args, spl)
    meta = RunMetadata(
        run_id=run_id,
        mode="translate",
        created_at=utc_now().isoformat(),
        title=args.title,
        source=args.source,
        goal=args.goal,
        fields=split_fields(args.fields),
        input_file=str(Path(args.spl_file).resolve()),
        notes=args.notes,
    )

    write_file(run_dir / "input.spl", spl)
    write_file(run_dir / "prompt_translate.md", prompt)
    write_file(run_dir / "response_from_claude.md", "<!-- Paste Claude response here -->")
    write_file(run_dir / "metadata.json", json.dumps(asdict(meta), indent=2))
    write_summary(
        run_dir,
        meta,
        {
            "SPL input": "input.spl",
            "Translation prompt": "prompt_translate.md",
            "Claude response placeholder": "response_from_claude.md",
            "Metadata": "metadata.json",
        },
    )

    print(f"[+] Created translation run: {run_dir}")
    print(f"[+] Prompt ready: {run_dir / 'prompt_translate.md'}")
    return 0


def do_debug(args: argparse.Namespace) -> int:
    query = load_text(Path(args.query_file))
    error = load_text(Path(args.error_file))
    run_id, run_dir = make_run_dir(args.title)

    prompt = build_debug_prompt(args, query, error)
    meta = RunMetadata(
        run_id=run_id,
        mode="debug",
        created_at=utc_now().isoformat(),
        title=args.title,
        source=args.source,
        goal=args.goal,
        fields=split_fields(args.fields),
        input_file=str(Path(args.query_file).resolve()),
        error_file=str(Path(args.error_file).resolve()),
        expected=args.expected,
        notes=args.notes,
    )

    write_file(run_dir / "input.cql", query)
    write_file(run_dir / "error.txt", error)
    write_file(run_dir / "prompt_debug.md", prompt)
    write_file(run_dir / "response_from_claude.md", "<!-- Paste Claude response here -->")
    write_file(run_dir / "metadata.json", json.dumps(asdict(meta), indent=2))
    write_summary(
        run_dir,
        meta,
        {
            "CQL input": "input.cql",
            "Error": "error.txt",
            "Debug prompt": "prompt_debug.md",
            "Claude response placeholder": "response_from_claude.md",
            "Metadata": "metadata.json",
        },
    )

    print(f"[+] Created debug run: {run_dir}")
    print(f"[+] Prompt ready: {run_dir / 'prompt_debug.md'}")
    return 0


def do_review(args: argparse.Namespace) -> int:
    spl = load_text(Path(args.spl_file))
    cql = load_text(Path(args.cql_file))
    run_id, run_dir = make_run_dir(args.title)

    prompt = build_review_prompt(args, spl, cql)
    meta = RunMetadata(
        run_id=run_id,
        mode="review",
        created_at=utc_now().isoformat(),
        title=args.title,
        source=args.source,
        goal=args.goal,
        fields=split_fields(args.fields),
        input_file=str(Path(args.cql_file).resolve()),
        notes=args.notes,
    )

    write_file(run_dir / "input.spl", spl)
    write_file(run_dir / "input.cql", cql)
    write_file(run_dir / "prompt_review.md", prompt)
    write_file(run_dir / "response_from_claude.md", "<!-- Paste Claude response here -->")
    write_file(run_dir / "metadata.json", json.dumps(asdict(meta), indent=2))
    write_summary(
        run_dir,
        meta,
        {
            "SPL input": "input.spl",
            "CQL input": "input.cql",
            "Review prompt": "prompt_review.md",
            "Claude response placeholder": "response_from_claude.md",
            "Metadata": "metadata.json",
        },
    )

    print(f"[+] Created review run: {run_dir}")
    print(f"[+] Prompt ready: {run_dir / 'prompt_review.md'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automate structured SPL -> LogScale prompt workflows."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--title", required=True, help="Short title for the run")
    common.add_argument("--source", default="CrowdStrike LogScale", help="Data source name")
    common.add_argument("--goal", default="Translate query faithfully", help="Analytical goal")
    common.add_argument(
        "--fields",
        default="",
        help="Comma-separated list of known fields (e.g. aid, FileName, TargetFileName)",
    )
    common.add_argument("--notes", default="", help="Optional notes for metadata")

    p_translate = sub.add_parser("translate", parents=[common], help="Create a translation run")
    p_translate.add_argument("--spl-file", required=True, help="Path to file containing SPL")
    p_translate.set_defaults(func=do_translate)

    p_debug = sub.add_parser("debug", parents=[common], help="Create a debug run")
    p_debug.add_argument("--query-file", required=True, help="Path to file containing CQL")
    p_debug.add_argument("--error-file", required=True, help="Path to file containing error output")
    p_debug.add_argument("--expected", default="", help="Expected behavior/result")
    p_debug.set_defaults(func=do_debug)

    p_review = sub.add_parser("review", parents=[common], help="Create a review run")
    p_review.add_argument("--spl-file", required=True, help="Path to file containing SPL")
    p_review.add_argument("--cql-file", required=True, help="Path to file containing CQL")
    p_review.set_defaults(func=do_review)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # pragma: no cover
        print(f"[!] Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
