#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Doctor: 检查 short-drama-studio 的目录、文件、编码与脚本可运行性。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_KNOWLEDGE = (
    "character-consistency.md",
    "concept-setting.md",
    "copyright-and-rights.md",
    "model-routing.md",
    "model-capability-cards.md",
    "audio-and-voice.md",
    "physics-and-continuity-gate.md",
    "generation-operations.md",
    "staging-and-blocking.md",
    "series-memory.md",
    "production-pipeline.md",
    "project-asset-protocol.md",
    "prompt-engineering.md",
    "reading-list.md",
    "scene-generation.md",
    "sources-and-method-boundaries.md",
    "story-structure-and-screenwriting.md",
    "storyboard-and-pacing.md",
    "style-system.md",
    "video-generation-and-post.md",
)

REQUIRED_TEMPLATES = (
    "ai-production-plan.md",
    "asset-master.md",
    "character-card.md",
    "character-concept-table.md",
    "episode-script-and-storyboard.md",
    "face-swap-qc.md",
    "prompt-converter.md",
    "prop-card.md",
    "scene-card.md",
    "script-breakdown.md",
    "shot-list.md",
    "style-lock.md",
    "video-production-spec.md",
    "staging.md",
    "continuity-ledger.csv",
    "generation-jobs.csv",
    "candidate-scorecard.csv",
)

REQUIRED_SCRIPTS = ("create_project.py", "validate_project.py", "doctor.py")


class Doctor:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.warnings: list[str] = []
        self.failures: list[str] = []

    def ok(self, message: str) -> None:
        self.passed.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    @property
    def healthy(self) -> bool:
        return not self.failures


def check_python(doctor: Doctor) -> None:
    if sys.version_info < (3, 8):
        doctor.fail(f"Python 版本过低: {sys.version.split()[0]}，需要 >= 3.8")
    else:
        doctor.ok(f"Python {sys.version.split()[0]}")


def check_structure(doctor: Doctor, root: Path) -> None:
    skill_md = next(
        (
            candidate
            for candidate in (root / "SKILL.md", root.parent / "SKILL.md")
            if candidate.is_file()
        ),
        None,
    )
    if skill_md is None:
        doctor.fail("缺少 SKILL.md（应在资源目录或其上级仓库根）")
    else:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---") or "name:" not in text or "description:" not in text:
            doctor.fail("SKILL.md frontmatter 缺少 name 或 description")
        else:
            doctor.ok("SKILL.md frontmatter 正常")
    for name in ("knowledge-base", "templates", "scripts"):
        if (root / name).is_dir():
            doctor.ok(f"目录 {name}/ 存在")
        else:
            doctor.fail(f"缺目录 {name}/")


def check_files(doctor: Doctor, root: Path) -> None:
    for filename in REQUIRED_KNOWLEDGE:
        if (root / "knowledge-base" / filename).is_file():
            continue
        doctor.fail(f"缺知识库文件 knowledge-base/{filename}")
    for filename in REQUIRED_TEMPLATES:
        if (root / "templates" / filename).is_file():
            continue
        doctor.fail(f"缺模板 templates/{filename}")
    for filename in REQUIRED_SCRIPTS:
        if (root / "scripts" / filename).is_file():
            continue
        doctor.fail(f"缺脚本 scripts/{filename}")
    if not any(doctor.failures):
        doctor.ok(f"知识库 {len(REQUIRED_KNOWLEDGE)} 个、模板 {len(REQUIRED_TEMPLATES)} 个、脚本 {len(REQUIRED_SCRIPTS)} 个齐全")


def check_syntax(doctor: Doctor, root: Path) -> None:
    for path in sorted((root / "scripts").glob("*.py")):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
            doctor.ok(f"脚本语法通过 {path.name}")
        except (SyntaxError, UnicodeError) as exc:
            doctor.fail(f"脚本语法错误 {path.name}: {exc}")


def check_encoding(doctor: Doctor, root: Path) -> None:
    bad: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".py", ".csv", ".json", ".yml", ".yaml"}:
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeError:
            bad.append(str(path.relative_to(root)))
    if bad:
        doctor.warn(f"非 UTF-8 文件 {len(bad)} 个: {', '.join(bad[:5])}")
    else:
        doctor.ok("文本文件均为 UTF-8")


def check_artifacts(doctor: Doctor, root: Path) -> None:
    repo = root.parent
    for name in ("LICENSE", "CHANGELOG.md"):
        if (repo / name).is_file():
            doctor.ok(f"仓库文件 {name} 存在")
        else:
            doctor.warn(f"仓库缺 {name}")
    examples = repo / "examples"
    if examples.is_dir() and any(examples.iterdir()):
        doctor.ok("examples/ 存在")
    else:
        doctor.warn("examples/ 为空")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="资源目录（默认脚本上级，即 short-drama-studio-resources）",
    )
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()

    if not root.is_dir():
        print(f"FAIL: 根目录不存在: {root}")
        return 1

    doctor = Doctor()
    check_python(doctor)
    check_structure(doctor, root)
    check_files(doctor, root)
    check_syntax(doctor, root)
    check_encoding(doctor, root)
    check_artifacts(doctor, root)

    for message in doctor.passed:
        print(f"PASS: {message}")
    for message in doctor.warnings:
        print(f"WARN: {message}")
    for message in doctor.failures:
        print(f"FAIL: {message}")
    print(f"{'OK' if doctor.healthy else 'FAIL'}: {len(doctor.passed)} pass / {len(doctor.warnings)} warn / {len(doctor.failures)} fail")
    return 0 if doctor.healthy else 1


if __name__ == "__main__":
    sys.exit(main())