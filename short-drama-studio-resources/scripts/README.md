# 辅助脚本

脚本只使用 Python 标准库，建议 Python 3.9 或更高版本。

## 自检

```bash
python scripts/doctor.py
python scripts/doctor.py --root ./short-drama-studio-resources
```

检查 Python 版本、`SKILL.md` frontmatter、`knowledge-base/` 与 `templates/` 齐全度、脚本语法、文本编码，以及 `LICENSE`、`CHANGELOG.md`、`examples/` 是否存在。默认根目录为脚本上级（即 `short-drama-studio-resources`）。

## 创建项目模板

```bash
python scripts/create_project.py my-drama
python scripts/create_project.py my-drama --output D:/projects
python scripts/create_project.py my-drama --output D:/projects --force
```

默认在当前目录创建项目；只补写缺失文件，不覆盖已有内容。会初始化 `rights/rights-log.csv`、`rights/continuity-ledger.csv`、`rights/generation-jobs.csv`、`planning/candidate-scorecard.csv`。

## 验证项目（软门禁）

```bash
python scripts/validate_project.py my-drama
python scripts/validate_project.py my-drama --strict
python scripts/validate_project.py my-drama --json
```

退出码：`0` 通过，`1` 失败，`2` 项目目录不存在。

- `ERROR`（确定性、阻断）：缺目录/文件、CSV 表头缺字段、授权日志必填为空、分镜引用未登记资产、镜头时长合计与总时长不等。
- `WARNING`（启发式、默认不阻断）：模板字段未填、缺少 3 个模型候选、无角色卡、无成片总时长等。`--strict` 让 WARNING 也导致失败。

脚本不判断图片审美、节奏是否好看、模型输出是否自然，也不替代人工版权审核。