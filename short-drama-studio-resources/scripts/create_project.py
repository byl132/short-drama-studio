#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a starter project for the short-drama-studio skill."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT_FILES = {
    "project.md": """# {name}\n\n## 项目概要\n\n- 核心钩子：\n- 时长/集数：\n- 画幅/平台：\n- 目标观众：\n- 授权状态总览：\n\n## 资产进度\n\n- [ ] 剧本拆解表与资产总表\n- [ ] 角色卡与道具卡\n- [ ] 三模型角色候选\n- [ ] 风格锁定\n- [ ] 场景资产\n- [ ] 分镜与提示词\n- [ ] 换脸/一致性 QC\n- [ ] 发布前版权复核\n""",
    "planning/ai-production-plan.md": """---\nschema: ai-short-drama-production-plan-v1\nplan_id: PLAN-001\nproject_id: {name}\nscript_id: SCRIPT-001-v01\nstatus: 待确认\ncreated_at: YYYY-MM-DD\nlast_updated: YYYY-MM-DD\n---\n\n# AI 生产计划表\n\n请参照 ../../templates/ai-production-plan.md。生产顺序为：SCRIPT → SCRIPT BREAKDOWN → ASSET MASTER → STYLE → SUBJECT → SCENE → PROP → SHOT → VIDEO / POST。生成任何人物、场景或视频前，先填写输入、knowledge_ref、source_ref、输出物、验收条件、依赖、失败回退和状态。\n\n## 统一资产 ID\n\n```yaml\nstyle_id: STYLE-001-v01\nsubject_ids: SUBJECT-001-v01\nscene_ids: SCENE-001-v01\nprop_ids: PROP-001-v01\nshot_ids: SHOT-001-v01\nstatus_vocabulary: 待确认 / 待检索 / 待生成 / 待复核 / 已锁定 / 已阻塞\n```\n\n## 阶段执行表\n\n| seq | phase_id | 阶段 | 输入文件/资产 | knowledge_ref | source_ref | 执行动作 | 输出文件/资产 | 验收条件 | 依赖 | 失败回退 | 状态 |\n|---:|---|---|---|---|---|---|---|---|---|---|---|\n| 01 | parse | 需求/剧本分流 | 用户输入、剧本、参考图 | story-structure-and-screenwriting.md | SRC- | 区分事实/偏好/假设/未决 | project.md、问题清单 | 高影响歧义已明确 | - | 回到澄清问题 | 待确认 |\n| 02 | script-breakdown | 剧本拆解 | SCRIPT-001-v01 | project-asset-protocol.md | SRC- | 标记 SCRIPT FACT/INFERENCE/DESIGN/OPEN QUESTION | planning/script-breakdown.md | 角色、场景、道具已去重 | 01 | 回到剧本医生 | 待确认 |\n| 03 | asset-master | 资产总表 | script-breakdown.md | project-asset-protocol.md | SRC- | 分配资产 ID、变体和 P0–P3 | planning/asset-master.md | 引用、来源、授权齐全 | 02 | 暂停批量生成 | 待确认 |\n| 04 | style-lock | 风格锁定 | 用户偏好、参考属性 | production-pipeline.md | SRC- | 产出 DESIGN-A/B/C，确认后测试 MODEL-A/B/C | style-lock.md | 固定/可变/禁止项明确 | 03 | 回到风格确认 | 待确认 |\n| 05 | subject-lock | 主体锁定 | 概念表、角色参考图 | concept-setting.md、character-consistency.md | SRC- | 建立身份/视觉/表演锁 | character-card、prompt-pack | 角色字段可回溯 | 03,04 | 标记待确认 | 待确认 |\n| 06 | scene-lock | 场景锁定 | 主体、剧本场次 | production-pipeline.md | SRC- | 建立母场景、时间字段、变体和动线 | scenes/ | 空间骨架可复用 | 04,05 | 修正母场景 | 待确认 |\n| 07 | prop-lock | 道具/产品 | 剧本道具、角色、场景 | copyright-and-rights.md | SRC- | 分级、建母体、多状态和授权记录 | prop cards | 核心道具关系和授权完整 | 05,06 | 改虚构品牌或暂停 | 待确认 |\n| 08 | storyboard | 分镜 | 剧情、锁定资产 | storyboard-and-pacing.md | SRC- | 计算节拍和镜头时长，填写资产引用 | episodes/、shots/ | 镜头时长等于目标时长 | 02,04–07 | 回调时长或拆镜头 | 待确认 |\n| 09 | video-post | 视频与后期 | 分镜、原片段 | video-generation-and-post.md | SRC- | 生成、剪辑、声音、字幕、导出 | 母版、平台版、归档包 | 全片 QC 通过 | 08 | 回退到干净母版 | 待生成 |\n\n## 反问、来源和当前阻塞\n\n- 未决问题：\n- 来源记录：\n- 当前阻塞：\n""",
    "planning/asset-master.md": """# 剧本视觉资产总表\n\n请参照 ../../templates/asset-master.md。每项资产先分配 ID、来源、授权、状态和 variant_of，再进入批量生成。\n\n| asset_id | asset_type | level | script_facts | design_needed | fixed_fields | variable_fields | forbidden_fields | source_ref | knowledge_ref | rights_status | status |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n| STYLE-001-v01 | style | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |\n| SUBJECT-001-v01 | subject | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |\n| SCENE-001-v01 | scene | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |\n| PROP-001-v01 | prop | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |\n\n## 场次—资产矩阵\n\n| scene_no | scene_id | subject_id | prop_id | 状态/变体 | shot_id | 资产引用是否完整 |\n|---|---|---|---|---|---|---|\n| 01 | SCENE-001-v01 | SUBJECT-001-v01 | PROP-001-v01 |  | SHOT-001-v01 | 待检查 |\n\n## 制作优先级\n\n- P0：核心风格、主角、母场景、主角核心道具；\n- P1：重要配角、场景和道具；\n- P2：次要角色、场景和普通道具；\n- P3：只有镜头需要时才制作的背景资产。\n""",
    "planning/script-breakdown.md": """# 剧本拆解表\n\n请参照 ../../templates/script-breakdown.md。完整阅读剧本后，标记 SCRIPT FACT、INFERENCE、DESIGN、OPEN QUESTION，并完成角色、场景、道具去重。\n\n## 事实与设计\n\n| item_id | 类别 | 原文/场次 | 提取内容 | 需要设计的部分 | 影响资产 | 是否待确认 |\n|---|---|---|---|---|---|---|\n| ITEM-001 | SCRIPT FACT |  |  |  |  |  |\n| ITEM-002 | INFERENCE |  |  |  |  |  |\n| ITEM-003 | DESIGN |  |  |  |  |  |\n| ITEM-004 | OPEN QUESTION |  |  |  |  | 是 |\n\n## 角色/场景/道具索引\n\n- 角色去重与群像：\n- 母场景与变体：\n- P0–P3 道具分级：\n- SCRIPT DIFF：\n""",
    "styles/style-lock.md": "# 风格锁定卡\n\n请参照 ../../templates/style-lock.md 和 ../../knowledge-base/style-system.md。先记录 DESIGN-A/B/C，用户确认方向后再测试 MODEL-A/B/C。\n\n- 风格 ID：STYLE-001-v01\n- 状态：待确认\n- 固定项：\n- 可变项：\n- 禁止项：\n\n| 方案 | 类型 | 记录 |\n|---|---|---|\n| DESIGN-A | 创意方向 |  |\n| DESIGN-B | 创意方向 |  |\n| DESIGN-C | 创意方向 |  |\n| MODEL-A | 模型候选 |  |\n| MODEL-B | 模型候选 |  |\n| MODEL-C | 模型候选 |  |\n",
    "props/prop-card.md": "# 道具/产品卡\n\n请参照 ../../templates/prop-card.md。真实品牌或 Logo 授权不明时改为虚构品牌。\n\n- 道具 ID：PROP-001-v01\n- 类型：剧情道具 / 产品 / 道具+产品 / 场景陈设\n- variant_of：\n- 授权状态：\n- 状态：待确认\n- 固定项：母体轮廓、比例、关键部件、主色、材质\n- 可变项：磨损、污渍、开合、亮灭、破损\n- 禁止项：关键部件漂移、比例改变、无授权品牌/Logo\n",
    "concepts/character-concept-table.md": "# 主角概念设定表\n\n请参照 ../../templates/character-concept-table.md。中文关键词、英文提示词、头像参考图、全身参考图和场景入镜图必须绑定同一个角色 ID。\n\n| 序号/角色 ID | 人物姓名 | 人物资产关键词（中文） | English prompt | 头像参考图 | 全身参考图 | 场景入镜图 | 状态/授权 |\n|---|---|---|---|---|---|---|---|\n| P-001 |  |  |  |  |  |  | 草稿 / 授权待核实 |\n",
    "characters/character-template.md": "# 角色卡模板\n\n复制此文件，为每个主要角色建立独立角色卡。\n\n请参照 ../../templates/character-card.md。\n",
    "scenes/scene-template.md": "# 场景模板\n\n请参照 ../../templates/scene-card.md 和 ../../knowledge-base/scene-generation.md。\n\n- 母场景 ID：SCENE-001-v01\n- 变体 ID/variant_of：\n- world_time：\n- season：\n- shot_time：\n- weather：\n- continuity_time：\n- 空间结构/入口/出口：\n- 人物活动区域与动线：\n- 道具出现位置：\n- 主光源/色温：\n- 至少 3 个空间识别锚点：\n- 全景/中景/近景/反向角度测试：\n- 比例/接触面/阴影 QC：\n",
    "prompts/prompt-pack-template.md": "# Prompt Pack\n\n请参照 ../../templates/prompt-converter.md，为每个角色复制一份。\n",
    "episodes/episode-01-script.md": "# 第 01 集：脚本与拍摄分镜\n\n请参照 ../../templates/episode-script-and-storyboard.md。\n\n- 成片总时长：\n\n## 节拍表\n\n时间码：\n\n## 场景脚本\n\n台词：\n声音：\n\n## 拍摄分镜\n\n镜头：\n拍摄备注：\n",
    "video/video-production-spec.md": "# AI 视频生成与后期交付规格\n\n请参照 ../../templates/video-production-spec.md，先锁定平台、画幅、分辨率、帧率、音频、字幕和母版，再记录模型选择、镜头衔接与导出版本。\n\n- 输出画幅/分辨率：\n- 时间线帧率：\n- 模型选择：主模型 / 备份模型 / 快速预览模型\n- 2D/3D/AI 输入资产：\n- 镜头衔接：\n- 音效/对白/音乐：\n- 字幕：\n- 导出：母版 / 平台版\n",
    "shots/shot-list.md": "# 分镜表\n\n请参照 ../../templates/shot-list.md。\n",
}


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="project directory name")
    parser.add_argument("--output", default=".", help="parent directory")
    parser.add_argument("--force", action="store_true", help="kept for compatibility; never overwrites")
    args = parser.parse_args()

    project = (Path(args.output).expanduser().resolve() / args.name).resolve()
    project.mkdir(parents=True, exist_ok=True)
    created = []
    for relative, content in ROOT_FILES.items():
        if write_if_missing(project / relative, content.format(name=args.name)):
            created.append(relative)

    rights = project / "rights" / "rights-log.csv"
    if not rights.exists():
        rights.parent.mkdir(parents=True, exist_ok=True)
        with rights.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle)
            writer.writerow(["asset_id", "asset_type", "source", "owner", "license", "scope", "expiry", "notes"])
        created.append("rights/rights-log.csv")

    print(f"Project: {project}")
    print("Created:")
    for item in created:
        print(f"  - {item}")
    if not created:
        print("  (no files; existing files were preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
