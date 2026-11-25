#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline evals for short-drama-studio. No network, no paid APIs."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "short-drama-studio-resources"
SCRIPTS = RESOURCES / "scripts"
PY = sys.executable

results: list[tuple[str, bool, str]] = []


def record(code: str, ok: bool, detail: str = "") -> None:
    results.append((code, ok, detail))


def run(code: str, label: str, args: list[str]) -> None:
    proc = subprocess.run(args, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    record(code, proc.returncode == 0, label if proc.returncode == 0 else output[-1500:])
    if proc.returncode == 0:
        print(f"[PASS] {code} {label}")
    else:
        print(f"[FAIL] {code} {label}")
        print(output[-1500:])


def eval_duplicate_paragraphs() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    duplicates = [
        (left, right)
        for left, right in zip(lines, lines[1:])
        if left == right and len(left) >= 40
    ]
    ok = not duplicates
    record("E3", ok, "SKILL.md 无连续重复长段落" if ok else f"发现 {len(duplicates)} 处连续重复")
    print(f"[{'PASS' if ok else 'FAIL'}] E3 SKILL.md 无连续重复长段落")


def eval_counts() -> None:
    knowledge = list((RESOURCES / "knowledge-base").glob("*.md"))
    templates = list((RESOURCES / "templates").iterdir())
    ok = len(knowledge) >= 20 and len(templates) >= 17
    detail = f"知识库 {len(knowledge)} / 模板 {len(templates)}"
    record("E4", ok, detail)
    print(f"[{'PASS' if ok else 'FAIL'}] E4 {detail}")


def eval_dangling_reference() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "neg"
        subprocess.run(
            [PY, str(SCRIPTS / "create_project.py"), "neg", "--output", str(Path(tmp))],
            capture_output=True,
            text=True,
        )
        episode = project / "episodes" / "episode-01-script.md"
        episode.write_text(
            "# EP01\n\n- 成片总时长：90 秒\n\n"
            "| 镜头 ID | 时间码 | SUBJECT_ID |\n|---|---|---|\n"
            "| SHOT-001-v01 | 00:00–01:30 / 90s | SUBJECT-999-v01 |\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [PY, str(SCRIPTS / "validate_project.py"), str(project), "--json"],
            capture_output=True,
            text=True,
        )
        promoted = proc.returncode == 1 and "SUBJECT-999-v01" in proc.stdout
        record("E5", promoted, "校验能报出未登记资产引用" if promoted else "负例未被识别")
        print(f"[{'PASS' if promoted else 'FAIL'}] E5 负例：未登记资产引用应触发 ERROR")


def main() -> int:
    run("E1", "doctor.py", [PY, str(SCRIPTS / "doctor.py")])
    run(
        "E2",
        "demo-90s 严格校验",
        [PY, str(SCRIPTS / "validate_project.py"), str(ROOT / "examples" / "demo-90s"), "--strict"],
    )
    eval_duplicate_paragraphs()
    eval_counts()
    eval_dangling_reference()

    failures = [code for code, ok, _detail in results if not ok]
    print(f"\n{'OK' if not failures else 'FAIL'}: {len(results) - len(failures)} pass / {len(failures)} fail")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())