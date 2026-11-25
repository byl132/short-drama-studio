# 剧本视觉资产总表

请参照 ../../templates/asset-master.md。每项资产先分配 ID、来源、授权、状态和 variant_of，再进入批量生成。

| asset_id | asset_type | level | script_facts | design_needed | fixed_fields | variable_fields | forbidden_fields | source_ref | knowledge_ref | rights_status | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| STYLE-001-v01 | style | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |
| SUBJECT-001-v01 | subject | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |
| SCENE-001-v01 | scene | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |
| PROP-001-v01 | prop | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |

## 场次—资产矩阵

| scene_no | scene_id | subject_id | prop_id | 状态/变体 | shot_id | 资产引用是否完整 |
|---|---|---|---|---|---|---|
| 01 | SCENE-001-v01 | SUBJECT-001-v01 | PROP-001-v01 |  | SHOT-001-v01 | 待检查 |

## 制作优先级

- P0：核心风格、主角、母场景、主角核心道具；
- P1：重要配角、场景和道具；
- P2：次要角色、场景和普通道具；
- P3：只有镜头需要时才制作的背景资产。
