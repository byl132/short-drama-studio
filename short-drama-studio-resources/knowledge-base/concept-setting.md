# 主角概念设定表与双语提示词

## 一、它解决什么问题

主角概念设定表是角色资产的第一层索引，适合在正式角色卡、三视图和表情图之前快速统一全体角色。它把“谁、长什么样、穿什么、拿什么”压缩成一行，并同时保留人工审核用的中文关键词和模型执行用的英文提示词。

它不是最终角色卡，不能替代三视图、表情图、换脸 QC 或授权日志。它的作用是让团队先确认方向，避免每个人用不同语言描述同一个角色。

## 二、表格字段

| 字段 | 写法 | 验收点 |
|---|---|---|
| 序号 | P-001、P-002 等稳定 ID | 后续图片、文件、镜头和授权记录都复用同一 ID |
| 人物姓名/ID | 角色名 + 英文/数字 ID | 不用明星名、影视角色名或品牌角色名 |
| 人物资产关键词 | 中文短语，用分号分组 | 身份、年龄/时代、体型、脸部锚点、发型、服装、道具、风格可逐项核对 |
| 英文提示词 | 面向目标模型的自然英文 | 与中文关键词语义一致，不添加中文没有的身份或版权元素 |
| 头像参考图 | 正面或 3/4 脸部图 | 绑定 ID、来源和授权；用于脸部锚点 |
| 全身参考图 | 完整头身和服装图 | 绑定同一 ID；用于比例、衣服、鞋和道具 |
| 状态/授权 | 草稿、候选、已锁定、授权状态 | 不明授权不得进入发布资产 |

## 三、中文关键词顺序

推荐固定顺序：

```text
主体类型；身份/年龄/地域/时代；身高体型；脸型与 3 个脸部锚点；发型/肤色/特殊标记；服装材质与颜色；鞋/配件/道具；画面类型与光线；允许变化；禁止变化。
```

每个字段尽量写成可观察属性。例如把“很帅、很有故事、气质沉稳”改成“窄长脸、深眼窝、眉尾浅疤、嘴角收紧、肩膀略前倾”。抽象词可以保留在表演字段，但不能作为唯一的识别依据。

## 四、英文提示词顺序

```text
{subject type}, {identity/age/origin/era}, {height and build},
{face shape and three facial anchors}, {hair/skin/special mark},
{wardrobe/material/color}, {shoes/accessories/prop},
{visual medium and lighting}, {allowed variations}, {forbidden changes}.
```

英文版的任务是“可执行”，不是逐字翻译。模型需要的关键身份和外形字段放在前面；风格、光线和背景放在后面；连续性禁区放在末尾并与负面提示词同步。

## 五、参考图绑定规则

- 头像和全身图都写角色 ID，文件名建议为 `{character-id}_portrait_v01.png` 与 `{character-id}_fullbody_v01.png`；
- 头像优先使用正面或 3/4 角度，避免滤镜、严重遮挡和夸张表情；
- 全身图必须露出头、脚、服装轮廓和主要道具；
- 如果两张图不是同一个人或来源不明，标记为“待核实”，不要强行合并；
- 生成三视图和表情图时，概念表只提供初始约束，最终以选定的角色资产版本为准，并回写文件名和版本。

## 六、示例

以下只示范结构，不是固定角色：

```text
中文：超写实全身 CG；中国男性，21 岁，现代城市调查员；185cm，匀称健壮；窄长脸、深眼窝、眉骨明显、左脸颊浅疤；深棕短发、自然肤色；深灰耐磨夹克、灰色速干衫、棕色斜挎包；冷色侧光，电影感中性背景；允许衣物褶皱和轻微雨水；禁止年龄漂移、疤痕消失、发型变化、头身比异常。

English: Hyper-realistic full-body CG character concept of a 21-year-old Chinese male urban investigator, 185 cm tall, athletic and well-proportioned, narrow long face, deep-set eyes, defined brow ridge, a subtle scar on the left cheek, short dark-brown hair, natural skin tone, rugged dark-gray jacket, gray quick-dry shirt, brown crossbody bag, cool side lighting, cinematic neutral background. Allow natural fabric wrinkles and light rain only. Keep the age, facial anchors, scar, hairstyle, body proportions, outfit and prop consistent; no head-to-body distortion, no facial drift, no logos, no watermark.
```

若参考素材中出现 Logo、影视角色名、明星脸或艺术家名字，应先改写成原创且可观察的视觉属性，并把来源和许可写入授权日志。

## 七、完成判定

主角概念表可以进入下一阶段，当且仅当：每个主要角色有唯一 ID；中文关键词和英文提示词逐项对应；至少绑定头像/全身参考图，或明确记录缺失；至少写出 3 个脸部锚点；授权状态可追溯；没有把不明版权元素当作原创资产。
