---
schema: ai-short-drama-production-plan-v1
plan_id: PLAN-001
project_id: demo-90s
script_id: SCRIPT-001-v01
status: 待确认
created_at: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# AI 生产计划表

请参照 ../../templates/ai-production-plan.md。生产顺序为：SCRIPT → SCRIPT BREAKDOWN → ASSET MASTER → STYLE → SUBJECT → SCENE → PROP → SHOT → VIDEO / POST。生成任何人物、场景或视频前，先填写输入、knowledge_ref、source_ref、输出物、验收条件、依赖、失败回退和状态。

## 统一资产 ID

```yaml
style_id: STYLE-001-v01
subject_ids: SUBJECT-001-v01
scene_ids: SCENE-001-v01
prop_ids: PROP-001-v01
shot_ids: SHOT-001-v01
status_vocabulary: 待确认 / 待检索 / 待生成 / 待复核 / 已锁定 / 已阻塞
```

## 阶段执行表

| seq | phase_id | 阶段 | 输入文件/资产 | knowledge_ref | source_ref | 执行动作 | 输出文件/资产 | 验收条件 | 依赖 | 失败回退 | 状态 |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 01 | parse | 需求/剧本分流 | 用户输入、剧本、参考图 | story-structure-and-screenwriting.md | SRC- | 区分事实/偏好/假设/未决 | project.md、问题清单 | 高影响歧义已明确 | - | 回到澄清问题 | 待确认 |
| 02 | script-breakdown | 剧本拆解 | SCRIPT-001-v01 | project-asset-protocol.md | SRC- | 标记 SCRIPT FACT/INFERENCE/DESIGN/OPEN QUESTION | planning/script-breakdown.md | 角色、场景、道具已去重 | 01 | 回到剧本医生 | 待确认 |
| 03 | asset-master | 资产总表 | script-breakdown.md | project-asset-protocol.md | SRC- | 分配资产 ID、变体和 P0–P3 | planning/asset-master.md | 引用、来源、授权齐全 | 02 | 暂停批量生成 | 待确认 |
| 04 | style-lock | 风格锁定 | 用户偏好、参考属性 | production-pipeline.md | SRC- | 产出 DESIGN-A/B/C，确认后测试 MODEL-A/B/C | style-lock.md | 固定/可变/禁止项明确 | 03 | 回到风格确认 | 待确认 |
| 05 | subject-lock | 主体锁定 | 概念表、角色参考图 | concept-setting.md、character-consistency.md | SRC- | 建立身份/视觉/表演锁 | character-card、prompt-pack | 角色字段可回溯 | 03,04 | 标记待确认 | 待确认 |
| 06 | scene-lock | 场景锁定 | 主体、剧本场次 | production-pipeline.md | SRC- | 建立母场景、时间字段、变体和动线 | scenes/ | 空间骨架可复用 | 04,05 | 修正母场景 | 待确认 |
| 07 | prop-lock | 道具/产品 | 剧本道具、角色、场景 | copyright-and-rights.md | SRC- | 分级、建母体、多状态和授权记录 | prop cards | 核心道具关系和授权完整 | 05,06 | 改虚构品牌或暂停 | 待确认 |
| 08 | storyboard | 分镜 | 剧情、锁定资产 | storyboard-and-pacing.md | SRC- | 计算节拍和镜头时长，填写资产引用 | episodes/、shots/ | 镜头时长等于目标时长 | 02,04–07 | 回调时长或拆镜头 | 待确认 |
| 09 | video-post | 视频与后期 | 分镜、原片段 | video-generation-and-post.md | SRC- | 生成、剪辑、声音、字幕、导出 | 母版、平台版、归档包 | 全片 QC 通过 | 08 | 回退到干净母版 | 待生成 |

## 反问、来源和当前阻塞

- 未决问题：
- 来源记录：
- 当前阻塞：
