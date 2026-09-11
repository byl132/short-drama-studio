# 辅助脚本

脚本只使用 Python 标准库，建议 Python 3.9 或更高版本。

## 创建项目模板

```bash
python scripts/create_project.py my-drama
python scripts/create_project.py my-drama --output D:/projects
python scripts/create_project.py my-drama --output D:/projects --force
```

默认在当前目录创建项目；`--force` 只允许补写缺失模板，不覆盖已有文件。

## 验证项目

```bash
python scripts/validate_project.py my-drama
```

验证 AI 生产计划表、剧本拆解表、资产总表、风格卡、道具卡、主角概念设定表、分集脚本、视频交付规格、角色目录、场景目录、提示词目录、授权日志和关键字段，并检查角色卡至少保留 A/B/C 三个候选记录。它不会判断图片审美、节奏是否好看、模型输出是否自然，也不会替代人工版权审核。
