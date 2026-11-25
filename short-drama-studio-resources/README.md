# short-drama-studio-resources

本目录是 Short Drama Studio Skill 的资源包，包含：

- `knowledge-base/`：领域知识与生产规则
- `templates/`：可填写模板（含连续性账本、生成任务、候选评分三个 CSV）
- `scripts/`：`create_project.py`、`validate_project.py`、`doctor.py`

安装、快速开始、知识模块与能力边界见上级仓库的 [README.md](../README.md)。

不要单独分发本目录；必须与上级 `SKILL.md` 放在同一个 Skill 目录内使用，否则项目里的 `../../templates` 引用会失效。