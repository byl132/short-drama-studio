---
schema: ai-short-drama-production-plan-v1
plan_id: PLAN-001
project_id:
status: 待确认
owner:
created_at: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# AI 生产计划表

这是一份给 Agent、人类创作者和后期工具共同读取的执行表。先填计划，再生成角色、场景或视频。字段没有证据时写 `待确认`，不留空；没有实际执行时写 `待生成`，不伪造结果。

## 0. 统一项目与资产 ID

```yaml
project_id: PROJECT-001
script_id: SCRIPT-001-v01
style_id: STYLE-001-v01
subject_ids: [SUBJECT-001-v01]
scene_ids: [SCENE-001-v01]
prop_ids: [PROP-001-v01]
shot_ids: [SHOT-001-v01]
variant_of: null
status_vocabulary: [待确认, 待检索, 待生成, 待复核, 已锁定, 已阻塞]
```

所有资产还要记录 `variant_of`（如果是变体）、输入引用、输出引用、版本、模型/版本、提示词版本、来源、授权、QC 和选中理由。详见 [knowledge-base/project-asset-protocol.md](../knowledge-base/project-asset-protocol.md)。

## 1. 项目解析

| 字段 | 内容 | 证据/来源 | 状态 |
|---|---|---|---|
| 一句话创意 |  |  | 待确认 |
| 叙事目的/情绪变化 |  |  | 待确认 |
| 目标受众 |  |  | 待确认 |
| 成片时长/集数 |  |  | 待确认 |
| 画幅/平台/发布用途 |  |  | 待确认 |
| 2D/3D/AI 输入资产 |  |  | 待确认 |
| 版权/肖像/隐私状态 |  |  | 待确认 |

## 2. 文意转换

| 原始表达 | 类型（事实/偏好/假设/未决） | 结构化变量、关系和约束 | 可观察验收条件 | 处理决定 |
|---|---|---|---|---|
|  |  |  |  |  |

## 3. 阶段执行表

| seq | phase_id | 阶段 | 输入文件/资产 | knowledge_ref | source_ref | 执行动作 | 输出文件/资产 | 模型/工具与参数 | 人工闸门/验收条件 | 依赖 | 失败回退 | 状态 |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | parse | 需求/剧本分流 | 用户输入、剧本、参考图 | story-structure-and-screenwriting.md、sources-and-method-boundaries.md | SRC- | 区分事实/偏好/假设/未决；已有剧本则完整阅读 | project.md、问题清单 | 不适用 | 输入分支和高影响问题已明确 | - | 回到澄清问题 | 待确认 |
| 02 | script-breakdown | 剧本拆解 | SCRIPT-001-v01 | story-structure-and-screenwriting.md、project-asset-protocol.md | SRC- | 标记 SCRIPT FACT/INFERENCE/DESIGN/OPEN QUESTION，去重角色、场景、道具 | script-breakdown.md、场次—资产矩阵 | SCRIPT_ID | 没有把设计推断写成事实 | 01 | 回到剧本医生/补问 | 待确认 |
| 03 | research | 资料与授权 | 公开资料、项目素材 | sources-and-method-boundaries.md、copyright-and-rights.md | SRC- | 检索、核验、提炼并原创改写 | rights-log.csv、source-log.md | 记录版本/访问日期 | 来源可追溯，风险可解释 | 01 | 换用可靠来源或标记不采用 | 待检索 |
| 04 | asset-master | 资产总表 | script-breakdown.md | project-asset-protocol.md | SRC- | 分配 STYLE/SUBJECT/SCENE/PROP/SHOT ID、P0–P3 和变体 | asset-master.md | ID、variant_of | 资产引用、来源、授权、状态齐全 | 02,03 | 暂停批量生成 | 待确认 |
| 05 | style-lock | 风格锁定 | 用户偏好、参考属性 | production-pipeline.md、project-asset-protocol.md | SRC- | 产出 DESIGN-A/B/C，确认后再测 MODEL-A/B/C | style-lock.md、风格候选 | 风格 ID/版本 | 固定/可变/禁止项明确 | 04 | 回到风格确认 | 待确认 |
| 06 | subject-lock | 主体知识库生产 | 概念表、角色参考图 | concept-setting.md、character-consistency.md | SRC- | 建立身份锁/视觉锁/表演锁和角色变体 | character-card、prompt-pack | SUBJECT_ID、variant_of | 主要角色字段完整且能回指来源 | 04,05 | 标记待确认，不生成批量图 | 待确认 |
| 07 | scene-lock | 母场景与变体 | 主体、剧本场次 | production-pipeline.md、project-asset-protocol.md | SRC- | 建立空间骨架、时间字段、锚点和动线 | scene cards、场景资产 | SCENE_ID、variant_of | 结构/时间/天气/比例可复用 | 05,06 | 修正母场景 | 待确认 |
| 08 | prop-lock | 道具/产品生产 | 剧本道具、角色、场景 | copyright-and-rights.md、project-asset-protocol.md | SRC- | 分级、建立母体、多状态和品牌授权记录 | prop cards、道具资产 | PROP_ID、variant_of | 核心道具关系和授权完整 | 06,07 | 改虚构品牌或暂停 | 待确认 |
| 09 | model-test | 三模型候选 | 固定段、参考资产 | model-routing.md | SRC- | 同一固定段测试 3 个模型/模型家族 | 三视图、表情图、场景入镜候选及评分 | 记录版本、尺寸、参数 | 资产齐全且有选中理由 | 06,07,08 | 输出待生成提示词或换模型 | 待生成 |
| 10 | storyboard | 分集与分镜 | 剧情、时长、锁定资产 | storyboard-and-pacing.md、story-structure-and-screenwriting.md | SRC- | 计算节拍与镜头时长，写机位动作声音和资产引用 | episode script、shot list | 时间码、SHOT_ID | 镜头总时长等于目标时长 | 02,05–09 | 回调时长或拆镜头 | 待确认 |
| 11 | video | AI 视频镜头 | 分镜、场景入镜图、prompt pack | video-generation-and-post.md | SRC- | 每镜头只生成一个主要动作/情绪 | 原片段、参数日志 | 主/备/预览模型 | 动作自然、身份稳定、无明显畸形 | 09,10 | 短片段重试/换模型 | 待生成 |
| 12 | post | 后期剪辑 | 原片段、对白、音效、音乐 | video-generation-and-post.md | SRC- | 粗剪、精剪、声音、字幕、合成、调色 | 项目文件、分轨、字幕 | 剪辑软件/音频工具 | 衔接有动作/视线/声音动机 | 11 | 回退到干净母版重剪 | 待确认 |
| 13 | export-qc | 导出与归档 | 母版、字幕、来源日志 | video-generation-and-post.md、copyright-and-rights.md | SRC- | 导出母版与平台版并做全片 QC | 母版、平台版、SRT/VTT、归档包 | 记录编码和版本 | 画幅、帧率、字幕、音频、版权标注通过 | 12 | 修正母版后重新导出 | 待复核 |

## 4. 角色知识依据表

| character_id | 字段 | 锁定内容 | knowledge_ref | source_ref | 事实/假设 | 置信度 | 待确认项 |
|---|---|---|---|---|---|---|---|
| A3D-001 | 身份/年龄 |  | concept-setting.md | SRC- | 事实/假设 | 高/中/低 |  |
| A3D-001 | 脸部/发型锚点 |  | character-consistency.md | SRC- | 事实/假设 | 高/中/低 |  |
| A3D-001 | 服装/道具 |  | concept-setting.md | SRC- | 事实/假设 | 高/中/低 |  |
| A3D-001 | 表演与禁用变化 |  | character-consistency.md | SRC- | 事实/假设 | 高/中/低 |  |

## 5. 反问与假设清单

| id | 原问题/歧义 | 为什么会改变产出 | 给用户的选项 | 用户决定 | 影响阶段 | 状态 |
|---|---|---|---|---|---|---|
| Q-001 |  |  |  |  |  | 待确认 |

## 6. 来源与版本日志

| source_ref | 标题/作者/机构 | URL/DOI | 访问日期 | 提炼内容（自己的话） | 改写/适配内容 | 许可备注 | 核验状态 |
|---|---|---|---|---|---|---|---|
| SRC-001 |  |  | YYYY-MM-DD |  |  |  | 待核验 |

## 7. 交付前机器检查

```yaml
plan_id: PLAN-001
all_major_characters_have_knowledge_refs: false
all_major_characters_have_scene_entry_image: false
all_candidates_have_three_views_and_expression_sheet: false
design_candidates_separated_from_model_candidates: false
asset_master_has_scene_matrix: false
all_variants_have_variant_of: false
all_generation_rows_have_inputs_outputs_and_acceptance: false
all_online_sources_have_url_and_access_date: false
all_ambiguous_high_impact_items_confirmed: false
rights_risk_review: pending
final_status: 待复核
```
