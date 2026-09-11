#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the minimum metadata for a short-drama-studio project."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_DIRS = ("concepts", "characters", "scenes", "prompts", "episodes", "video", "shots", "rights", "planning", "styles", "props")
REQUIRED_FILES = (
    "project.md",
    "concepts/character-concept-table.md",
    "episodes/episode-01-script.md",
    "video/video-production-spec.md",
    "shots/shot-list.md",
    "rights/rights-log.csv",
    "planning/ai-production-plan.md",
    "planning/asset-master.md",
    "planning/script-breakdown.md",
    "styles/style-lock.md",
    "props/prop-card.md",
)


def require_markers(errors: list[str], label: str, path: Path, markers: tuple[str, ...]) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    for marker in markers:
        if marker not in text:
            errors.append(f"{label}: missing field containing {marker}")
    return text


def check_project(project: Path) -> list[str]:
    errors: list[str] = []
    for directory in REQUIRED_DIRS:
        if not (project / directory).is_dir():
            errors.append(f"missing directory: {directory}/")
    for filename in REQUIRED_FILES:
        if not (project / filename).is_file():
            errors.append(f"missing file: {filename}")

    concept_table = project / "concepts" / "character-concept-table.md"
    require_markers(errors, "character-concept-table.md", concept_table, ("人物资产关键词", "English prompt", "头像参考图", "全身参考图", "场景入镜图", "状态/授权"))

    episode_script = project / "episodes" / "episode-01-script.md"
    require_markers(errors, "episode-01-script.md", episode_script, ("成片总时长", "节拍表", "时间码", "镜头", "台词", "声音", "拍摄备注"))

    video_spec = project / "video" / "video-production-spec.md"
    require_markers(errors, "video-production-spec.md", video_spec, ("输出画幅", "模型选择", "2D/3D/AI", "镜头衔接", "音效", "字幕", "导出"))

    plan = project / "planning" / "ai-production-plan.md"
    require_markers(errors, "ai-production-plan.md", plan, ("plan_id", "project_id", "script_id", "style_id", "subject_ids", "scene_ids", "prop_ids", "shot_ids", "knowledge_ref", "source_ref", "输出文件/资产", "验收条件", "依赖", "失败回退", "状态", "已锁定"))

    asset_master = project / "planning" / "asset-master.md"
    require_markers(errors, "asset-master.md", asset_master, ("asset_id", "fixed_fields", "variable_fields", "forbidden_fields", "variant_of", "rights_status", "场次—资产矩阵", "P0", "P1", "P2", "P3"))

    breakdown = project / "planning" / "script-breakdown.md"
    require_markers(errors, "script-breakdown.md", breakdown, ("SCRIPT FACT", "INFERENCE", "DESIGN", "OPEN QUESTION", "角色", "场景", "道具", "SCRIPT DIFF"))

    scene_template = project / "scenes" / "scene-template.md"
    require_markers(errors, "scene-template.md", scene_template, ("variant_of", "world_time", "season", "shot_time", "weather", "continuity_time", "空间识别锚点"))

    style_lock = project / "styles" / "style-lock.md"
    require_markers(errors, "style-lock.md", style_lock, ("STYLE-", "DESIGN-A", "DESIGN-B", "DESIGN-C", "MODEL-A", "MODEL-B", "MODEL-C", "固定项", "可变项", "禁止项"))

    prop_card = project / "props" / "prop-card.md"
    require_markers(errors, "prop-card.md", prop_card, ("PROP-", "variant_of", "固定项", "可变项", "禁止项", "授权状态"))

    character_files = [
        path for path in (project / "characters").glob("*.md")
        if path.name != "character-template.md"
    ] if (project / "characters").is_dir() else []
    if not character_files:
        errors.append("no character card found in characters/")

    for card in character_files:
        text = card.read_text(encoding="utf-8", errors="replace")
        for marker in ("角色", "脸部", "表演", "场景入镜", "可变", "禁止"):
            if marker not in text:
                errors.append(f"{card.name}: missing character field containing {marker}")
        if "variant_of" not in text:
            errors.append(f"{card.name}: missing variant_of field")
        for candidate in ("A", "B", "C"):
            if f"| {candidate} |" not in text and f"候选 {candidate}" not in text:
                errors.append(f"{card.name}: missing model candidate {candidate}")

    rights = project / "rights" / "rights-log.csv"
    if rights.is_file():
        try:
            with rights.open(newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                errors.append("rights-log.csv has no asset rows")
            for index, row in enumerate(rows, start=2):
                for field in ("asset_id", "source", "owner", "license", "scope"):
                    if not (row.get(field) or "").strip():
                        errors.append(f"rights-log.csv row {index}: empty {field}")
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f"cannot read rights-log.csv: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="project directory")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"ERROR: project directory does not exist: {project}")
        return 2
    errors = check_project(project)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: project metadata passes the minimum checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
