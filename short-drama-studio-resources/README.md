# Short Drama Studio

这是一个面向 AI 短剧、短视频和分镜生产的 Codex Skill。它把剧本分流、剧本拆解、资产总表、风格/主体/场景/道具交接、角色一致性、三模型候选、三视图/表情图、场景入镜图、自然换脸、资料来源、AI 生产计划、提示词转换和版权记录放进一套可复用流程。

## 安装

安装时把 `SKILL.md` 与同级的 `short-drama-studio-resources` 文件夹放在同一个 Skill 目录中；内部安装版则使用标准的 `short-drama-studio/knowledge-base`、`templates` 和 `scripts` 目录。Skill 的入口是 `SKILL.md`，知识库和模板由入口按需引用。不要只复制资源文件夹。

## 快速开始

从内部安装版目录运行：

```bash
python scripts/create_project.py my-drama
python scripts/validate_project.py my-drama
```

从桌面“一个文件 + 一个文件夹”的便携包父目录运行：

```bash
python short-drama-studio-resources/scripts/create_project.py my-drama --output short-drama-studio-resources
python short-drama-studio-resources/scripts/validate_project.py my-drama
```

先填写 `my-drama/planning/script-breakdown.md`、`my-drama/planning/asset-master.md` 和 `my-drama/planning/ai-production-plan.md`，再完善 `styles/style-lock.md`、角色/场景/道具卡、来源日志和授权日志，最后让 Agent 按 `SKILL.md` 生成角色候选、视频镜头和分镜。便携包模式请把项目生成到 `short-drama-studio-resources` 内，保证项目中的 `../../templates` 引用有效。计划表先锁定输入、知识库依据、来源、输出物、验收条件、依赖、失败回退和状态；概念表统一中文关键词、英文提示词、头像/全身/场景入镜图；分集模板先锁定总时长，再填节拍和镜头；视频规格先锁定输入、模型、后期和平台导出。

## 目录

```text
short-drama-studio/
├── SKILL.md
├── README.md
├── knowledge-base/
├── templates/
└── scripts/
```

运行 `create_project.py` 后，项目目录会另外生成 `planning/`、`styles/`、`props/`、`characters/`、`scenes/`、`episodes/` 等工作目录。

风格模块规则见 `knowledge-base/style-system.md`；场景模块规则见 `knowledge-base/scene-generation.md`。两者都必须遵守项目视觉生产交接协议和统一资产 ID。

桌面便携包的实际结构为：

```text
short-drama-studio-package/
├── SKILL.md
└── short-drama-studio-resources/
    ├── README.md
    ├── knowledge-base/
    ├── templates/
    └── scripts/
```
