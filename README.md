# Short Drama Studio

面向 AI 短剧、短视频与分镜生产的 Agent Skill。把一句话创意、剧本或分镜整理成一套可复用的视觉资产系统：剧本拆解、资产总表、风格/角色/场景/道具锁定、角色候选、分镜与提示词、视频生成、声音与后期、QC 与导出。

## 与同类 Skill 的差异

| 维度 | 本仓库的做法 |
|---|---|
| 资产一致性 | 统一资产 ID（`STYLE/SUBJECT/SCENE/PROP/SHOT` + `variant_of`）互相引用，脚本校验悬空引用 |
| 状态管理 | 只使用 `待确认 / 待检索 / 待生成 / 待复核 / 已锁定 / 已阻塞`，不写"差不多" |
| 方案与模型 | `DESIGN-A/B/C` 是创意方向，`MODEL-A/B/C` 才是模型候选，两者不混用 |
| 模型选型 | 按能力卡（T2V/I2V/R2V/首尾帧/音频/编辑/多镜/图像）选，不按品牌排名 |
| 生成运营 | 门禁式生成、请求指纹与幂等键、`unknown` 找回、费用与授权分档 |
| 全程校验 | `validate_project.py` 软门禁（ERROR/WARNING 分级 + 跨文档一致性 + 时长合计），零依赖 |
| 边界 | 明确"证据边界"四分类与"按任务范围交付"，不伪造生成结果 |

## 目录

```text
short-drama-studio/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE                      # Apache-2.0
├── examples/                    # 最小可验证示例
├── evals/                       # 离线评测用例
└── short-drama-studio-resources/
    ├── knowledge-base/          # 20 个知识模块
    ├── templates/               # 17 个模板（含 3 个 CSV）
    └── scripts/                 # create_project / validate_project / doctor
```

Skill 入口是 `SKILL.md`，知识库与模板由入口按需引用。安装时把 `SKILL.md` 与同级 `short-drama-studio-resources` 放在同一个 Skill 目录；**不要只复制资源文件夹**。

## 快速开始

```bash
# 1. 自检
python short-drama-studio-resources/scripts/doctor.py

# 2. 新建项目
python short-drama-studio-resources/scripts/create_project.py my-drama --output short-drama-studio-resources

# 3. 填写 planning/、styles/、characters/、scenes/、episodes/

# 4. 校验（默认软门禁；--strict 让 WARNING 也失败）
python short-drama-studio-resources/scripts/validate_project.py my-drama
python short-drama-studio-resources/scripts/validate_project.py my-drama --strict --json
```

便携包模式请把项目生成到 `short-drama-studio-resources` 内，保证项目中的 `../../templates` 引用有效。

## 生产顺序

```text
需求/剧本分流 → 剧本拆解 → 资产总表
→ STYLE → SUBJECT → SCENE → PROP → SHOT
→ 声音路线 → 视频生成 → 剪辑/字幕 → QC → 导出
```

每个阶段先写计划再执行；每集先声明成片时长，再做节拍与分镜，镜头时长合计必须等于总时长。

## 知识模块

| 模块 | 文件 |
|---|---|
| 生产流程与资产模型 | `knowledge-base/production-pipeline.md` |
| 剧本结构与分流 | `knowledge-base/story-structure-and-screenwriting.md` |
| 概念设定与角色锁 | `knowledge-base/concept-setting.md` |
| 角色一致性与换脸 | `knowledge-base/character-consistency.md` |
| 风格系统 | `knowledge-base/style-system.md` |
| 场景生成 | `knowledge-base/scene-generation.md` |
| 分集脚本与分镜节奏 | `knowledge-base/storyboard-and-pacing.md` |
| 提示词工程 | `knowledge-base/prompt-engineering.md` |
| 模型能力卡 | `knowledge-base/model-capability-cards.md` |
| 声音与对白路线 | `knowledge-base/audio-and-voice.md` |
| 物理门与连续性 | `knowledge-base/physics-and-continuity-gate.md` |
| 生成运营 | `knowledge-base/generation-operations.md` |
| 场景站位 | `knowledge-base/staging-and-blocking.md` |
| 系列记忆 | `knowledge-base/series-memory.md` |
| 视频生成与后期 | `knowledge-base/video-generation-and-post.md` |
| 版权与授权 | `knowledge-base/copyright-and-rights.md` |
| 资料与方法边界 | `knowledge-base/sources-and-method-boundaries.md` |
| 资产交接协议 | `knowledge-base/project-asset-protocol.md` |

## 能力边界

- 本 Skill 负责**方案、模板、校验与执行约束**；不内置付费 API，不代替用户做审美与商业决策。
- 未实际调用生成工具时，输出标注「待生成」，不声称已产出图片或视频。
- 真实模型接口、价格、时长上限以平台当次官方文档为准，不写成永久事实。
- 密钥只来自环境变量或本地 secrets 文件，不得进入仓库。

## 许可证

Apache License 2.0，见 `LICENSE`。