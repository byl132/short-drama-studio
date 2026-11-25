#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a short-drama-studio project with soft gates.

ERROR   确定性结构或一致性问题（缺目录/文件、CSV 表头缺失、资产 ID 悬空、镜头时长合计不等）
WARNING 启发式内容缺失（字段未填、模板未完成），默认不阻断
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REQUIRED_DIRS = (
    "concepts", "characters", "scenes", "prompts", "episodes",
    "video", "shots", "rights", "planning", "styles", "props",
)

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

ID_RE = re.compile(
    r"(?:STYLE|SUBJECT|SCENE|PROP|SHOT)-[0-9]{3}(?:-VAR-[0-9]{2})?(?:-v[0-9]{2})?"
)
TOTAL_RE = re.compile(r"成片总时长[\s:：`]*(\d+(?:\.\d+)?)\s*(?:秒|s)")
TIME_RANGE_RE = re.compile(r"(\d{2}):(\d{2})\s*[–—\-]\s*(\d{2}):(\d{2})")
SECONDS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*s\b")
SHOT_ROW_RE = re.compile(r"^\|\s*(SHOT-[^|\s]+)")
RIGHTS_REQUIRED = ("asset_id", "source", "owner", "license", "scope")
LEDGER_REQUIRED = ("asset_id", "shot_id", "state_id")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        self.infos.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_structure(report: Report, project: Path) -> None:
    for directory in REQUIRED_DIRS:
        if not (project / directory).is_dir():
            report.error(f"缺目录: {directory}/")
    for filename in REQUIRED_FILES:
        if not (project / filename).is_file():
            report.error(f"缺文件: {filename}")


def check_csv_header(report: Report, path: Path, required: tuple[str, ...]) -> None:
    if not path.is_file():
        return
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            header = next(csv.reader(handle), [])
    except (OSError, UnicodeError, csv.Error) as exc:
        report.error(f"{path.name}: 无法读取 CSV: {exc}")
        return
    missing = [column for column in required if column not in header]
    if missing:
        report.error(f"{path.name}: 表头缺字段 {missing}")


def check_rights(report: Report, project: Path) -> None:
    path = project / "rights" / "rights-log.csv"
    check_csv_header(report, path, RIGHTS_REQUIRED)
    if not path.is_file():
        return
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        report.error(f"rights-log.csv: 无法读取: {exc}")
        return
    if not rows:
        report.warn("rights-log.csv 还没有资产行")
        return
    for index, row in enumerate(rows, start=2):
        for field in RIGHTS_REQUIRED:
            if not (row.get(field) or "").strip():
                report.error(f"rights-log.csv 第 {index} 行: {field} 为空")


def check_content_markers(report: Report, project: Path) -> None:
    markers: dict[str, tuple[str, tuple[str, ...]]] = {
        "concepts/character-concept-table.md": (
            "概念表",
            ("人物资产关键词", "English prompt", "头像参考图", "全身参考图", "场景入镜图", "状态/授权"),
        ),
        "episodes/episode-01-script.md": (
            "分集脚本",
            ("成片总时长", "节拍表", "时间码", "台词", "声音", "拍摄备注"),
        ),
        "video/video-production-spec.md": (
            "视频规格",
            ("输出画幅", "模型选择", "镜头衔接", "音效", "字幕", "导出"),
        ),
        "planning/ai-production-plan.md": (
            "生产计划",
            ("plan_id", "knowledge_ref", "source_ref", "验收条件", "依赖", "失败回退", "状态"),
        ),
        "planning/asset-master.md": (
            "资产总表",
            ("variant_of", "rights_status", "场次—资产矩阵", "P0"),
        ),
        "planning/script-breakdown.md": (
            "剧本拆解",
            ("SCRIPT FACT", "INFERENCE", "DESIGN", "OPEN QUESTION"),
        ),
        "scenes/scene-template.md": (
            "场景模板",
            ("variant_of", "world_time", "season", "shot_time", "weather", "continuity_time"),
        ),
        "styles/style-lock.md": (
            "风格锁定",
            ("DESIGN-A", "MODEL-A", "固定项", "可变项", "禁止项"),
        ),
        "props/prop-card.md": (
            "道具卡",
            ("PROP-", "variant_of", "授权状态"),
        ),
    }
    for relative, (label, required) in markers.items():
        path = project / relative
        if not path.is_file():
            continue
        text = read_text(path)
        missing = [marker for marker in required if marker not in text]
        if missing:
            report.warn(f"{label}: 缺少字段 {missing}")


def check_character_cards(report: Report, project: Path) -> None:
    characters = project / "characters"
    if not characters.is_dir():
        return
    cards = [path for path in characters.glob("*.md") if path.name != "character-template.md"]
    if not cards:
        report.warn("characters/ 下还没有角色卡")
        return
    for card in cards:
        text = read_text(card)
        missing = [marker for marker in ("角色", "脸部", "表演", "场景入镜", "禁止") if marker not in text]
        if missing:
            report.warn(f"{card.name}: 缺少角色字段 {missing}")
        if "variant_of" not in text:
            report.warn(f"{card.name}: 缺少 variant_of")
        missing_candidates = [
            candidate for candidate in ("A", "B", "C")
            if f"| {candidate} |" not in text and f"候选 {candidate}" not in text
        ]
        if missing_candidates:
            report.warn(f"{card.name}: 缺少模型候选 {missing_candidates}（建议 3 个不同模型）")


def parse_episode(text: str) -> tuple[float | None, list[tuple[str, float | None, str]]]:
    total: float | None = None
    match = TOTAL_RE.search(text)
    if match:
        total = float(match.group(1))
    shots: list[tuple[str, float | None, str]] = []
    for line in text.splitlines():
        shot_match = SHOT_ROW_RE.match(line.strip())
        if not shot_match:
            continue
        shot_id = shot_match.group(1)
        duration: float | None = None
        range_match = TIME_RANGE_RE.search(line)
        if range_match:
            h1, m1, h2, m2 = (int(value) for value in range_match.groups())
            duration = float((h2 * 60 + m2) - (h1 * 60 + m1))
        else:
            seconds_match = SECONDS_RE.search(line)
            if seconds_match:
                duration = float(seconds_match.group(1))
        shots.append((shot_id, duration, line))
    return total, shots


def check_cross_document(report: Report, project: Path) -> None:
    asset_master = project / "planning" / "asset-master.md"
    episode = project / "episodes" / "episode-01-script.md"
    if not asset_master.is_file() or not episode.is_file():
        return

    asset_ids = set(ID_RE.findall(read_text(asset_master)))
    if not asset_ids:
        report.warn("asset-master.md 未解析到资产 ID，跳过引用校验")
    else:
        report.info(f"asset-master.md 登记资产 {len(asset_ids)} 个")

    total, shots = parse_episode(read_text(episode))
    if not shots:
        report.warn("分集脚本未解析到 SHOT 镜头行，跳过时长校验")
        return

    for shot_id, _duration, line in shots:
        for reference in ID_RE.findall(line):
            if reference.startswith(("SUBJECT-", "SCENE-", "PROP-")) and reference not in asset_ids:
                report.error(f"分镜 {shot_id} 引用未登记资产 {reference}")

    filled = [duration for _shot, duration, _line in shots if duration is not None]
    unfilled = [shot_id for shot_id, duration, _line in shots if duration is None]
    if unfilled:
        report.warn(f"{len(unfilled)} 个镜头未填时长: {', '.join(unfilled[:5])}")
    if total is None:
        report.warn("未解析到成片总时长，跳过时长合计校验")
        return

    subtotal = sum(filled)
    if not unfilled and abs(subtotal - total) > 0.5:
        report.error(f"镜头时长合计 {subtotal:g}s 不等于成片总时长 {total:g}s")
    elif unfilled and subtotal > total + 0.5:
        report.error(f"已填镜头时长合计 {subtotal:g}s 已超过成片总时长 {total:g}s")
    elif not unfilled:
        report.info(f"镜头时长合计与总时长一致（{subtotal:g}s）")


def check_csvs(report: Report, project: Path) -> None:
    check_rights(report, project)
    check_csv_header(report, project / "rights" / "continuity-ledger.csv", LEDGER_REQUIRED)
    check_csv_header(report, project / "rights" / "generation-jobs.csv", ("job_id", "status"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="项目目录")
    parser.add_argument("--strict", action="store_true", help="把 WARNING 也视为失败")
    parser.add_argument("--json", action="store_true", dest="as_json", help="输出 JSON")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"ERROR: 项目目录不存在: {project}")
        return 2

    report = Report()
    check_structure(report, project)
    check_csvs(report, project)
    check_content_markers(report, project)
    check_character_cards(report, project)
    check_cross_document(report, project)

    failed = bool(report.errors) or (args.strict and bool(report.warnings))

    if args.as_json:
        print(json.dumps(
            {
                "project": str(project),
                "ok": not failed,
                "errors": report.errors,
                "warnings": report.warnings,
                "infos": report.infos,
            },
            ensure_ascii=False,
            indent=2,
        ))
    else:
        for message in report.errors:
            print(f"ERROR: {message}")
        for message in report.warnings:
            print(f"WARNING: {message}")
        for message in report.infos:
            print(f"INFO: {message}")
        verdict = "FAIL" if failed else "OK"
        print(f"{verdict}: {len(report.errors)} error / {len(report.warnings)} warning")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())