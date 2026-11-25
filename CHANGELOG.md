# Changelog

本文件记录 short-drama-studio 的重要变更。格式参考 Keep a Changelog，版本号遵循语义化版本。

## [1.1.0] - 2026-11-25

融合同期开源短剧 Skill 的可迁移做法，并去掉本仓库的重复与薄弱环节。

### Added

- `knowledge-base/model-capability-cards.md`：按能力（T2V / I2V / R2V / 首尾帧 / 音频 / 编辑 / 多镜 / 图像）选模型，含五镜测试法与能力卡模板。
- `knowledge-base/audio-and-voice.md`：五条对白路线、声线锚点、多人对白 P0 规则、分轨与响度、口型保护。
- `knowledge-base/physics-and-continuity-gate.md`：接触点清单、动作原语、精确物理事件编译、空间遮挡与连续性账本。
- `knowledge-base/generation-operations.md`：门禁式生成顺序、幂等与中断恢复、费用/授权分档、候选评分、证据边界、按范围交付、命名与密钥。
- `knowledge-base/staging-and-blocking.md` 与 `templates/staging.md`：场景站位、开场 blocking 句与分镜交接。
- `knowledge-base/series-memory.md`：长篇改编的四层记忆、原著抽样快评、章节索引、伏笔台账与跨集连续性。
- `templates/continuity-ledger.csv`、`templates/generation-jobs.csv`、`templates/candidate-scorecard.csv`。
- `scripts/doctor.py`：环境与仓库自检。
- `examples/`：最小可验证示例项目。
- `evals/`：离线评测用例与运行脚本。
- `LICENSE`（Apache-2.0）。

### Changed

- `scripts/validate_project.py` 重写为软门禁：确定性结构问题记 `ERROR`，启发式内容缺失记 `WARNING`，新增跨文档资产 ID 引用与镜头时长合计校验，支持 `--strict`。
- `SKILL.md` 删除重复段落，`0` 节下三个子节改为 `0.1 / 0.2 / 0.3`，补充模型能力卡、声音路线、物理门、生成运营、证据边界与按范围交付的引用。
- `README.md` 重写：定位、与同类 Skill 的差异、安装、快速开始、验证与边界。

### Fixed

- 修复 `SKILL.md` 中「需要在线补充资料时……」整段重复出现两次的问题。
- 修复章节编号从 `0` 直接跳到 `1`、中间三个无编号子节造成的阅读断点。

## [1.0.0] - 2026-11-01

- 首个公开版本：SKILL.md、knowledge-base、templates、create_project.py、validate_project.py。