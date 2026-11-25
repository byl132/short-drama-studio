# Evals

本目录是 short-drama-studio 的离线评测，检查 Skill 结构、脚本与示例是否仍然可用。不调用任何外部模型或付费接口。

## 运行

```bash
python evals/run_evals.py
```

退出码 `0` 表示全部通过。

## 评测项

| ID | 检查 | 类型 |
|---|---|---|
| E1 | `doctor.py` 通过（目录、文件、语法、编码） | 结构 |
| E2 | `examples/demo-90s` 通过 `validate_project.py --strict` | 一致性 |
| E3 | `SKILL.md` 无连续重复长段落 | 质量 |
| E4 | 知识库与模板数量符合预期 | 结构 |
| E5 | `validate_project.py` 能识别 ID 悬空（负例） | 回归 |

负例 E5 在临时目录构造一个引用未登记资产的镜头，预期校验返回 `ERROR`。