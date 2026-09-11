# 剧本视觉资产总表

这是剧本拆解之后、批量生成之前的唯一资产索引。每个资产只建立一个母版 ID；剧情状态、时间和天气变化用 `variant_of` 建立变体。

## 项目头

```yaml
project_id: PROJECT-001
script_id: SCRIPT-001-v01
status: 待确认
last_updated: YYYY-MM-DD
```

## 资产总览

| asset_id | asset_type | level | script_facts | design_needed | fixed_fields | variable_fields | forbidden_fields | source_ref | knowledge_ref | rights_status | status | selected_reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| STYLE-001-v01 | style | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |  |
| SUBJECT-001-v01 | subject | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |  |
| SCENE-001-v01 | scene | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |  |
| PROP-001-v01 | prop | P0 |  |  |  |  |  | SRC- |  | 虚构原创 | 待确认 |  |

## 角色资产表

| subject_id | level | 出现场次 | 剧本事实 | 需要设计 | 状态变化/variant_of | 三视图 | 6格表情图 | 场景入镜图 | 模型候选 | QC/授权 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SUBJECT-001-v01 | P0 |  |  |  |  | 待生成 | 待生成 | 待生成 | MODEL-A/B/C |  | 待确认 |

## 场景资产表

| scene_id | variant_of | 出现场次 | world_time | season | shot_time | weather | 空间锚点/入口出口/动线 | 复用关系 | 人物道具比例 QC | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| SCENE-001-v01 |  |  |  |  |  |  |  | 母场景 |  | 待确认 |

## 道具资产表

| prop_id | level | 类型 | 使用人物/动作 | 出现场次 | variant_of/状态 | 关键部件/材质 | 品牌授权 | 场景/手持图 | QC | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| PROP-001-v01 | P0 | 剧情道具 |  |  |  |  | 虚构原创 | 待生成 |  | 待确认 |

## 场次—资产矩阵

| scene_no | scene_id | subject_id | prop_id | 状态/变体 | 需要新增的设计 | shot_id | 资产引用是否完整 |
|---|---|---|---|---|---|---|---|
| 01 | SCENE-001-v01 | SUBJECT-001-v01 | PROP-001-v01 |  |  | SHOT-001-v01 | 待检查 |

## 制作优先级

- `P0`：风格、核心主角、最重要母场景、主角核心道具；
- `P1`：重要配角、重要场景、重要道具；
- `P2`：次要角色、次要场景、普通道具；
- `P3`：只有镜头需要时才制作的背景资产。

## 版本和变更记录

| change_id | 日期 | 触发原因 | 受影响 asset_id/shot_id | 冲突字段 | 处理决定 | 旧版本保留位置 | 重新 QC | 状态 |
|---|---|---|---|---|---|---|---|---|
| CHG-001 | YYYY-MM-DD |  |  |  |  |  |  | 待确认 |
