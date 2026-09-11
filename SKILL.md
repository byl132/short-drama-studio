---
name: short-drama-studio
description: 将一句话创意、剧本或分镜整理为可执行的 AI 短剧视觉生产方案，包含主角概念设定表、分集脚本、拍摄分镜、时长节奏规范、AI 视频生成与后期剪辑、2D/3D 输入输出和平台导出标准、角色与道具锁定、三模型候选生成、三视图/表情图/场景入镜图、逐角色提示词转换、自然换脸质检及版权风险控制。Use when users ask for AI short dramas, episode scripts, shooting storyboards, pacing plans, AI video generation, video editing, 2D/3D asset specs, export profiles, character concept tables, scene-integrated character images, bilingual character prompts, consistent characters, face replacement, image prompts, or multi-model visual development.
---

# Short Drama Studio

把短剧当作一套可复用的视觉资产系统来制作，而不是逐镜头随机出图。唯一的资产设计顺序是：`STYLE → SUBJECT → SCENE → PROP → SHOT → VIDEO / POST`。下面的章节是能力模块，按项目分支调用；章节编号不应被理解为可以跳过资产交接的另一套顺序。

## 不可跳过的规则

- 先建立资产表，再生成图片；没有锁定的角色、服装、道具、时间和风格，不进入批量分镜。
- 每集先声明成片时长，再做节拍表和拍摄分镜；镜头时长合计必须等于总时长，第一镜头优先在 0–5 秒内完成钩子。
- 在视频生成前先锁定画幅、分辨率、帧率、色彩、音频、字幕和导出平台；不得把平台压缩版当作母版反复加工。
- 每个主要角色至少生成 3 套候选，且来自 3 个不同模型或模型家族。每套必须同时包含：三视图（正面、侧面、背面）、一张表情图（至少 6 种表情）和一张场景入镜图（角色穿着锁定服装进入实际剧情场景）。记录模型、版本、参数、参考图、生成日期和选中理由；没有图像工具时，输出三套可直接复制的模型适配提示词，不声称已经生成。
- 用固定字段描述角色，不用“帅、漂亮、很有气质”这类不可复核的词。核心字段为：身份、年龄段、地域/时代、脸部锚点、发型、肤色/特殊标记、身材比例、服装、道具、表演习惯、禁用变化。
- 换脸只处理获得授权的素材和自创角色。保持目标图的头身比、头部姿态、光向、遮挡、肤色过渡和表情，不用大面积拉伸或过度磨皮掩盖失败。
- 不复制在世艺术家的独特风格、影视角色、品牌角色、明星脸、Logo、受保护道具或原作台词；把参考改写为可观察的画面属性。版权和肖像/隐私检查见 [knowledge-base/copyright-and-rights.md](short-drama-studio-resources/knowledge-base/copyright-and-rights.md)。
- 发现授权不明、真人未同意、未成年人换脸、冒充真实人物或可能造成欺骗的用途时，暂停相关生成并说明需要获得授权或改为虚构角色。
- 任何人物、场景或镜头生成前，先建立一份可被 AI 读取的生产计划表；计划表没有输入、知识依据、输出物、验收门槛和状态字段时，不进入批量生成。
- 已有完整剧本时，先完整阅读并拆解剧本，再做视觉资产；不得为了生成画面重新编造剧本事实。
- 每个项目必须维护资产总表和场次—资产矩阵；角色、场景、道具和镜头必须通过稳定 ID 互相引用。
- `DESIGN-A/B/C` 只表示创意方案，`MODEL-A/B/C` 才表示不同模型或模型家族的候选；除非工具实际返回文件，不声称已经生成图片或视频。

## 工作流

### 0. 资料来源、方法边界与 AI 生产计划

开始任何人物、场景或镜头生产前，先读取 [knowledge-base/project-asset-protocol.md](short-drama-studio-resources/knowledge-base/project-asset-protocol.md) 和 [knowledge-base/sources-and-method-boundaries.md](short-drama-studio-resources/knowledge-base/sources-and-method-boundaries.md)，并用 [templates/ai-production-plan.md](short-drama-studio-resources/templates/ai-production-plan.md) 创建本项目唯一的 `plan_id`。已有剧本时再用 [templates/script-breakdown.md](short-drama-studio-resources/templates/script-breakdown.md) 做完整拆解，用 [templates/asset-master.md](short-drama-studio-resources/templates/asset-master.md) 建立资产总表。计划表必须把“需求/剧本 → 拆解 → 资产总表 → STYLE → SUBJECT → SCENE → PROP → SHOT → 视频/后期 → QC/导出”排成有依赖关系的行；每行至少包含输入、`knowledge_ref`、`source_ref`、动作、输出文件、模型/工具、参数、人工闸门、状态和失败回退。状态只使用 `待确认 / 待检索 / 待生成 / 待复核 / 已锁定 / 已阻塞`，禁止用“差不多”代替状态。

先把用户话语拆成四类：**事实**（用户明确给出的内容）、**偏好**（可替换的审美或平台偏好）、**假设**（为继续工作而暂定的内容）、**未决问题**（会改变人物身份、版权、时长、画幅、模型或成片用途的内容）。已有剧本时同时标记 `SCRIPT FACT / INFERENCE / DESIGN / OPEN QUESTION`。未决问题先反问；只影响措辞且风险低的问题可以给出带编号的假设并让用户一次确认。没有实际检索或生成时，标注“待检索/待生成”，不伪造来源、模型结果或图片。

需要在线补充资料时，优先查官方文档、标准、出版机构/作者页面、模型当前帮助页和公开可靠的教学材料；提示词案例只提炼结构、变量和评价方法，必须用自己的话重写，记录标题、作者/机构、URL、访问日期、提炼内容、改写内容和许可风险。不得整段复制付费、盗版、来源不明的提示词或书籍内容，也不得把搜索结果当成事实而不核验。资料等级、引用格式和停止条件见 [knowledge-base/sources-and-method-boundaries.md](short-drama-studio-resources/knowledge-base/sources-and-method-boundaries.md)。
需要在线补充资料时，优先查官方文档、标准、出版机构/作者页面、模型当前帮助页和公开可靠的教学材料；提示词案例只提炼结构、变量和评价方法，必须用自己的话重写，记录标题、作者/机构、URL、访问日期、提炼内容、改写内容和许可风险。不得整段复制付费、盗版、来源不明的提示词或书籍内容，也不得把搜索结果当成事实而不核验。资料等级、引用格式和停止条件见 [knowledge-base/sources-and-method-boundaries.md](short-drama-studio-resources/knowledge-base/sources-and-method-boundaries.md)。

### 剧本分流与写作模式

当任务涉及创作或修改剧本时，先读取 [knowledge-base/story-structure-and-screenwriting.md](short-drama-studio-resources/knowledge-base/story-structure-and-screenwriting.md)：

- 模糊创意：最多问 5 个真正影响剧情的问题，再给出 3 条差异明显的故事路径；
- 用户明确要求“直接写”：不强制先给三条路径，但先列已知事实、工作假设、未决问题、时长和交付格式；
- 已有完整剧本：进入剧本医生/剧本拆解模式，不重启剧情；
- 只改局部：只改指定镜头、场景、对白或结尾，并说明对因果和资产连续性的影响。

剧本进入视觉生产前，必须补齐 `Want / Need / 阻力 / 失败代价 / 关键选择 / 可见变化`，并用三幕式、15 Beats 或 Story Circle 中合适的工具做结构诊断。

### 资产设计顺序

先锁定风格的固定项、可变项、禁止项（可用 [templates/style-lock.md](short-drama-studio-resources/templates/style-lock.md)）；再建立主体；然后建立母场景和场景变体（可用 [templates/scene-card.md](short-drama-studio-resources/templates/scene-card.md)）；随后制作道具或产品（可用 [templates/prop-card.md](short-drama-studio-resources/templates/prop-card.md)）；最后把这些资产引用进镜头。已有完整剧本时，先完成剧本拆解和资产总表，才进入这条资产顺序。

### 风格锁定要求

风格模块可以输出 `DESIGN-A/B/C` 三种方向，用户确认方向后才建立 `MODEL-A/B/C` 模型候选。风格固定项至少包括画面类别、材质、主辅色关系、光线逻辑、镜头语言和画面质感；天气、单镜头景别、构图和局部光强属于可变项。最终风格提示词只写视觉语言，不写具体人物、地点、道具或剧情动作；参考电影、摄影或艺术作品时，转写成色温、对比度、颗粒、焦段、构图、材质、光线和景深等可观察属性。详细模式、测试和交接见 [knowledge-base/style-system.md](short-drama-studio-resources/knowledge-base/style-system.md)。

### 1. 读取需求并建立资产表

从用户输入提取或补齐：一句话卖点、受众、时长、平台比例、集数、叙事基调、角色列表、场景列表、对白/旁白、参考素材及其授权状态。缺少信息时只问会改变产出的关键问题。

为方便理科背景用户复核，同时输出三层文意转换：`自然语言原意`、`结构化变量/约束/验收条件`、`目标模型提示词`。对“有感觉、电影感、自然、像某人”等不可计算表达，转换成可观察属性、范围、单位、镜头行为和失败示例；不擅自把文学隐喻当作人物事实。具体转换表见 [knowledge-base/sources-and-method-boundaries.md](short-drama-studio-resources/knowledge-base/sources-and-method-boundaries.md)。

先交付一张简短的资产表：

```text
项目：
核心冲突/情绪钩子：
画幅与时长：
角色：身份 | 脸部锚点 | 身体比例 | 服装 | 表演禁区
道具：名称 | 形状/材质 | 叙事作用 | 连续性规则
风格：画面类型 | 氛围参考 | 色调/光源 | 镜头语言
场景：时间 | 空间结构 | 天气 | 视角/机位
授权状态：用户自有 / 已获许可 / 公版待核实 / 不明（不明不可直接使用）
```

提示词统一拆成四个维度：**光影/时间 + 主体 + 场景 + 风格**。场景再拆为时间、空间、天气、视角；风格再拆为画面类型、氛围参考、色彩/光源、镜头语言。详见 [knowledge-base/production-pipeline.md](short-drama-studio-resources/knowledge-base/production-pipeline.md)。

### 2. 主体概念设定表（STYLE 锁定后）

对每个主要角色先建立一行“主角概念设定表”，再扩展成完整角色卡。表格至少包含：序号、人物姓名/ID、人物资产关键词、英文提示词、头像/半身参考图、全身参考图、授权状态。中文关键词是人工审核版，英文提示词是可直接复制给模型的版本；二者必须表达同一组身份、外形、服装、道具和风格约束。

人物字段必须能回指知识库或项目来源：在角色卡中为身份、年龄段、外形锚点、服装、道具、表演习惯和禁用变化记录 `knowledge_ref`、`source_ref`、置信度和待确认项。知识库是生产约束的底稿，用户明确设定优先于通用建议；来源冲突时列出冲突并暂停受影响的生成，不用猜测消除冲突。

每行英文提示词使用固定顺序：`主体类型 + 身份/年龄/地域 + 身高体型 + 脸部锚点 + 发型/肤色/特殊标记 + 服装/道具 + 画面风格 + 构图/背景 + 连续性禁区`。不要把参考图中的品牌 Logo、原作角色名或不明版权元素直接写进提示词。使用 [templates/character-concept-table.md](short-drama-studio-resources/templates/character-concept-table.md)，详细规则见 [knowledge-base/concept-setting.md](short-drama-studio-resources/knowledge-base/concept-setting.md)。

概念表中的参考图不是装饰：头像用于脸部识别，全身图用于身材、服装和道具锁定。两张图必须绑定同一个角色 ID，且记录来源和授权。若只有一张参考图，先标记缺失，不把它假设成完整角色资产。

### 3. 锁定角色与道具

为每个主要角色创建一张 `character-card`，字段使用 [templates/character-card.md](short-drama-studio-resources/templates/character-card.md)。角色提示词分为三层：

1. 身份锁：性别呈现、年龄段、地域/时代、职业、社会关系和一句话识别句。
2. 外形锁：脸型、眉眼鼻口比例、发型、肤色、特殊标记、身高体型、服装材质与配件；至少写 3 个不可变锚点。
3. 表演锁：常用表情、气质、动作习惯、情绪范围和禁用表演。

道具也要有形状、材质、磨损、颜色、尺寸和入镜规则。换场景、换景别、换表情时，只改变允许变化的字段。

如果剧本要求变老、受伤、换装、淋湿、弄脏或身份变化，建立 `SUBJECT-001-VAR-01`，记录 `variant_of`、保持不变的字段、允许变化的字段、发生位置、变体资产和母版连续性检查。不要把剧情变体当成随机漂移。

核心道具按 `P0 核心道具 / P1 重要道具 / P2 普通道具 / P3 场景陈设` 分级。核心道具要记录它与角色身份、职业、经历或关键选择的关系，并从同一母体派生标准图、多角度图、细节图、手持/使用图、场景图和必要状态图。真实品牌、Logo、包装和商业用途授权不明时，默认改为虚构品牌。

### 4. 一次性生成角色候选

执行“3 模型 × 2 资产”的最小批次：

```text
模型 A：三视图 + 表情图
模型 B：三视图 + 表情图
模型 C：三视图 + 表情图
```

每套图的固定段必须完全相同，只替换模型适配语法、尺寸和采样参数。三视图必须同一角色、同一服装、同一光线、同一中性姿态；表情图必须保持脸部锚点和发型不变，使用统一网格或统一画布。表情至少包括：平静、喜悦、惊讶、恐惧、愤怒、悲伤；如果剧情需要，增加克制、疲惫、讥讽等角色专属情绪。

用 [knowledge-base/model-routing.md](short-drama-studio-resources/knowledge-base/model-routing.md) 的评分表选出主版本和备份版本。不要只看单张“最好看”的脸，要看跨视图、跨表情和换装后的稳定度。

### 5. 锁定风格并生产场景资产

先选定一套画面风格，再建立母场景 `SCENE-001-v01` 和必要的场景变体 `SCENE-001-VAR-01`。每个场景必须分别记录 `world_time`（世界观年代）、`season`（季节）、`shot_time`（镜头时段）、`weather`（天气）和 `continuity_time`（叙事连续时间），同时写清空间结构、入口出口、人物活动区、道具位置、动线、视角、画面类型、氛围、色彩/光源和镜头语言。保持色彩、光向、材质和景深逻辑一致；时间或天气改变时只改允许变化的字段，不重构建筑骨架和主要动线。可按 [knowledge-base/production-pipeline.md](short-drama-studio-resources/knowledge-base/production-pipeline.md) 的场景表和 [templates/scene-card.md](short-drama-studio-resources/templates/scene-card.md) 执行，详细生成和验收见 [knowledge-base/scene-generation.md](short-drama-studio-resources/knowledge-base/scene-generation.md)。

每个核心场景至少做全景空间骨架、中景活动区域、近景材质/陈设和一个反向角度测试，并用主体场景入镜图或道具使用图验证比例、接触面和阴影关系。场景至少有 3 个稳定空间识别锚点。

场景资产锁定后，为每个主要角色生成一张“场景入镜图”：角色以最终服装和主要道具进入实际剧情场景，至少包含一个中景或全身构图。它不是海报，而是连续性测试图，用于检查角色与环境的比例、接触阴影、光向、景深、色温、服装材质和道具位置；通过后才进入视频动作生成。

### 6. 为每个角色做提示词转换

把自然语言角色设定转换成“固定段 + 变量段 + 镜头段 + 负面段”，而不是把整部剧本塞进一个长提示词。每个角色生成一份双语或目标模型语言的 prompt pack，包含：

- 角色固定段：身份、脸部锚点、发型、体型、服装、道具、连续性禁区；
- 表演变量段：情绪、动作、视线、姿态；
- 镜头变量段：景别、机位、焦段感、构图、光线；
- 负面段：畸形、额外肢体、年龄漂移、发型漂移、服装漂移、文字水印、Logo、头身比异常等；
- 模型适配段：模型名称/版本、参考图权重、宽高比、采样或控制参数。

提示词转换先过“文意—工程—模型”三栏：文意栏保留用户真正想表达的情绪和叙事目的；工程栏把它改写为可观测动作、空间关系、时长、强度和验收条件；模型栏才选择目标模型能识别的词序、参考图和负面词。若用户只给出模糊的文学表达，先提出最少但关键的澄清问题；若用户同意在线检索，才查找公开的详细提示词案例并重写，不把案例原文当作成品提示词。

转换规则和可复制模板见 [templates/prompt-converter.md](short-drama-studio-resources/templates/prompt-converter.md) 与 [knowledge-base/prompt-engineering.md](short-drama-studio-resources/knowledge-base/prompt-engineering.md)。

### 7. 自然换脸与连续性检查

换脸前先确认：两张图均有授权、目标人物与剧情用途合规、源脸和目标头部姿态接近。按以下顺序处理：

1. 对齐眼睛、鼻尖、嘴角和下颌，优先修正头部角度，不先拉伸脸。
2. 只建立贴合脸部边界的软蒙版，避开头发、耳朵、手、眼镜和明显遮挡；保留目标图的光向、阴影、表情和透视。
3. 低强度融合，逐步增加变化；先观察头身比、脸部宽高、颈部连接和肤色，再处理细节。
4. 用局部修复补齐发际线、耳侧、下颌、眼白和牙齿；不要用强 face restore 把人物磨成“塑料脸”。
5. 输出换脸前后对比及问题标注。若出现大头/小头、五官漂移、边缘光晕、肤色断层、表情僵硬或光向冲突，退回重新对齐和遮罩。

具体参数策略、风险边界和质检表见 [knowledge-base/character-consistency.md](short-drama-studio-resources/knowledge-base/character-consistency.md) 与 [templates/face-swap-qc.md](short-drama-studio-resources/templates/face-swap-qc.md)。

### 8. 编写分集脚本与拍摄分镜

每一集先选择总时长（30/60/90/180/300 秒或自定义），套用 [knowledge-base/storyboard-and-pacing.md](short-drama-studio-resources/knowledge-base/storyboard-and-pacing.md) 的节奏表，再填写 [templates/episode-script-and-storyboard.md](short-drama-studio-resources/templates/episode-script-and-storyboard.md)。完成后计算镜头、对白、停顿、动作反应和转场的总时长；必须等于目标时长，估算值要写出范围和误差。剧本确定后，将角色、母场景/变体、核心道具、场次—资产矩阵和 AI 制作难点交接给视觉资产模块。必须同时输出：

- 节拍表：时间码、剧情目的、角色目标、冲突变化、转折和悬念；
- 场景脚本：地点/时间、人物、动作、台词、道具、表演、声音和光线；
- 拍摄分镜表：镜头时长、景别、机位、运镜、主体动作、声音、AI 提示词、真人拍摄备注和连续性 QC。

默认节奏：钩子约占 5–10%，建立人物/目标约占 10–20%，冲突升级约占 35–50%，高潮/转折约占 15–25%，结尾回报或悬念约占 10–15%。若偏离默认比例，说明叙事原因。不要只交图片提示词，因为那不能直接用于拍摄。

### 9. AI 视频生成与后期剪辑

按照 [knowledge-base/video-generation-and-post.md](short-drama-studio-resources/knowledge-base/video-generation-and-post.md) 和 [templates/video-production-spec.md](short-drama-studio-resources/templates/video-production-spec.md) 执行。先锁定目标平台和母版规格，再选择“主模型 + 备份模型 + 快速预览模型”。每个 AI 视频镜头只承担一个主要动作或情绪变化，记录参考资产、模型版本、时长、帧率、提示词和 QC，不直接生成整集。

后期顺序固定为：备份素材 → 粗剪 → 精剪/镜头衔接 → 对白/环境声/拟音/音乐 → 2D/3D/AI 合成与调色 → 字幕 → 母版导出 → 平台版本 → 全片 QC。默认硬切，动作切、视线切、匹配剪辑和声音桥必须有动机；不要用炫技转场遮盖 AI 穿帮。同步输出干净版、烧录字幕版和 SRT/VTT（按项目需要），保留归档母版和音频分轨。

### 10. 交付分镜与资产包

最终输出按以下顺序组织：

1. 故事概要和镜头节奏；
2. 分集脚本、节拍表和拍摄版分镜；
3. AI 视频生成与后期交付规格（模型、输入、镜头衔接、音效、字幕、导出）；
4. 主角概念设定表（中文关键词、英文提示词、头像/全身/场景入镜参考图）；
5. 角色/道具资产表；
6. 选中的角色三视图、表情图、场景入镜图和模型备选记录；
7. 风格锁定卡和场景资产表；
8. 按镜头排列的提示词（四维结构）；
9. 每个角色的 prompt pack 与提示词转换说明；
10. 换脸/一致性 QC 记录；
11. AI 生产计划表、假设/未决问题清单和阶段状态；
12. 授权、资料来源、知识库引用、生成模型和版本日志。

分镜镜头至少写出：时间码、景别、机位、运镜、主体动作、台词/声音、光影、场景连续性、提示词和负面词。短片创作时可参考 [knowledge-base/production-pipeline.md](short-drama-studio-resources/knowledge-base/production-pipeline.md) 的镜头模板。

## 可运行工具

在目标目录执行：

```bash
python short-drama-studio-resources/scripts/create_project.py my-drama
python short-drama-studio-resources/scripts/validate_project.py my-drama
```

`create_project.py` 创建剧本拆解表、资产总表、角色、场景、提示词和授权日志模板，不会覆盖已有文件；`validate_project.py` 检查必备目录、ID/变体/来源字段、资产表、计划表、模型候选数量、三视图/表情图/场景入镜图记录和授权日志。脚本只使用 Python 标准库，详细用法见 [scripts/README.md](short-drama-studio-resources/scripts/README.md)。

## 最终门槛

交付前逐项确认：

- [ ] 主要角色均有 3 个不同模型候选；每套都有三视图和表情图。
- [ ] DESIGN-A/B/C 与 MODEL-A/B/C 已分开记录；主版本有选中理由。
- [ ] 已完成剧本拆解和资产总表；角色去重、母场景/变体、道具分级和场次—资产矩阵完整。
- [ ] 角色身份、脸部、身体、服装、道具和表演字段已锁定。
- [ ] 每个主要角色都有概念设定表行，中文关键词与英文提示词语义一致，并绑定头像/全身参考图或明确标记缺失。
- [ ] 每个主要角色都有场景入镜图，且通过比例、光向、阴影、景深、服装和道具连续性检查。
- [ ] 每集已声明总时长，节拍时间码完整，所有镜头时长合计与总时长一致。
- [ ] 分镜同时包含 AI 提示词和真人拍摄备注，现场可以按机位、动作、声音直接执行。
- [ ] 视频规格已锁定 2D/3D/AI 输入、画幅、分辨率、帧率、色彩、音频和平台导出版本。
- [ ] 每个视频模型有主/备/预览定位和测试评分，镜头衔接有动作、视线或声音动机。
- [ ] 音效、对白、音乐、字幕、干净版、烧录版和归档母版已分别检查。
- [ ] 场景同时定义时间、空间、天气、视角；画面同时定义光影、主体、场景、风格。
- [ ] 场景分别记录 world_time、season、shot_time、weather、continuity_time，并通过全景/中景/近景/反向角度检查。
- [ ] 核心道具具有标准、多角度、细节、手持/使用、场景和状态资产；真实品牌或 Logo 有明确授权，未授权时已虚构化。
- [ ] 每个角色都有可复用 prompt pack 和目标模型转换版本。
- [ ] 换脸素材有授权，且通过头身比、边缘、光照、肤色、表情五项检查。
- [ ] 参考素材、模型版本、提示词、参数、选片理由和版权风险均有记录。
- [ ] 已建立 AI 生产计划表；每个生成动作都有输入、知识/资料引用、输出物、验收门槛、依赖和状态。
- [ ] 所有主要人物字段均能回指知识库或项目来源，事实、偏好、假设和未决问题没有混写。
- [ ] 文意已转换为理科用户可复核的变量、约束、单位和验收条件；模糊要求已反问或显式标为假设。
- [ ] 在线资料已记录来源和访问日期，内容经过核验与原创改写，没有整段复用受版权保护的提示词或书籍文本。
- [ ] 存在明显版权、肖像、隐私或冒充风险的内容已停止、替换或取得明确许可。
- [ ] 剧本变更已执行影响检查和 SCRIPT DIFF，旧版本保留，受影响资产重新 QC。

## 参考资料

- 生产流程与资产模型：[knowledge-base/production-pipeline.md](short-drama-studio-resources/knowledge-base/production-pipeline.md)
- 主角概念设定表与双语转换：[knowledge-base/concept-setting.md](short-drama-studio-resources/knowledge-base/concept-setting.md)
- 分集脚本、拍摄分镜与节奏：[knowledge-base/storyboard-and-pacing.md](short-drama-studio-resources/knowledge-base/storyboard-and-pacing.md)
- 知识点与参考书目：[knowledge-base/reading-list.md](short-drama-studio-resources/knowledge-base/reading-list.md)
- AI 视频生成、后期与导出：[knowledge-base/video-generation-and-post.md](short-drama-studio-resources/knowledge-base/video-generation-and-post.md)
- 角色一致性、表情图与换脸：[knowledge-base/character-consistency.md](short-drama-studio-resources/knowledge-base/character-consistency.md)
- 提示词结构与转换：[knowledge-base/prompt-engineering.md](short-drama-studio-resources/knowledge-base/prompt-engineering.md)
- 三模型路由与评估：[knowledge-base/model-routing.md](short-drama-studio-resources/knowledge-base/model-routing.md)
- 版权、肖像和隐私：[knowledge-base/copyright-and-rights.md](short-drama-studio-resources/knowledge-base/copyright-and-rights.md)
- 资料来源与方法边界：[knowledge-base/sources-and-method-boundaries.md](short-drama-studio-resources/knowledge-base/sources-and-method-boundaries.md)
- AI 生产计划表：[templates/ai-production-plan.md](short-drama-studio-resources/templates/ai-production-plan.md)
- 项目视觉生产交接协议：[knowledge-base/project-asset-protocol.md](short-drama-studio-resources/knowledge-base/project-asset-protocol.md)
- 剧本结构与视觉交接：[knowledge-base/story-structure-and-screenwriting.md](short-drama-studio-resources/knowledge-base/story-structure-and-screenwriting.md)
- 剧本拆解模板：[templates/script-breakdown.md](short-drama-studio-resources/templates/script-breakdown.md)
- 资产总表模板：[templates/asset-master.md](short-drama-studio-resources/templates/asset-master.md)
- 风格锁定卡：[templates/style-lock.md](short-drama-studio-resources/templates/style-lock.md)
- 场景卡：[templates/scene-card.md](short-drama-studio-resources/templates/scene-card.md)
- 道具/产品卡：[templates/prop-card.md](short-drama-studio-resources/templates/prop-card.md)
- 视觉风格识别与定位：[knowledge-base/style-system.md](short-drama-studio-resources/knowledge-base/style-system.md)
- 场景生成与连续性：[knowledge-base/scene-generation.md](short-drama-studio-resources/knowledge-base/scene-generation.md)
