# Skills

`.harness/skills/` 下每个子目录是一个可按触发条件显式加载的本地工作流技能。它们**不注册到全局**，由 `.harness/README.md` 的任务路由表和根 `AGENTS.md` 显式引导加载。

## 每个技能的结构

```text
<skill-name>/
├── SKILL.md            # 唯一事实源：frontmatter(name/description) + 触发条件 + 步骤
└── agents/openai.yaml  # Codex 适配层（预留，当前不生效）：display_name/short_description/default_prompt
```

## 新增 / 改名技能的约定

1. 同时提供 `SKILL.md` 和 `agents/openai.yaml`。
2. 保持三处一致：**目录名 = `SKILL.md` frontmatter 的 `name` = `openai.yaml` 里 `default_prompt` 的 `$name`**。
3. 在 `.harness/README.md` 的「任务路由」表加/改对应一行（用户意图 → 本技能 → 必读规则 / 按需 Wiki）。
4. `SKILL.md` 只写触发条件与步骤，不复制 `rules/` 的约束正文——需要时引用规则文件路径即可。
5. `agents/openai.yaml` 只是适配元数据；行为变化改 `SKILL.md`，不要让两者漂移。

## 现有技能与标准闭环

`request-analysis` → `implement-change` →（`write-unit-tests` / `run-quality-gates`）→ `expert-review` → `deploy-verify`。

- 修复缺陷 / 改产品代码走 `implement-change`（内部先用 `write-unit-tests` 固化失败用例再修）。
- 仅补测试 / 复现回归用例才独立走 `write-unit-tests`。
