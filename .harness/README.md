# Vibe Harness

`.harness/` 是项目内的 AI 开发控制面：把稳定规则、可复用技能、项目知识和单次变更证据组织成可渐进读取、可验证、可持续修正的系统。

代码、权威文档和可重复验证结果是最终事实。Harness 与实际项目不一致时，先确认真实行为，再修正规则或 Wiki。

## 四层职责

| 层 | 回答的问题 | 生命周期 | 是否允许记录任务进度 |
|---|---|---|---|
| `rules/` | 代码必须怎样写、怎样验证 | 长期稳定 | 否 |
| `skills/` | Agent 应按什么步骤完成一类任务 | 随流程迭代 | 否 |
| `wiki/` | 项目是什么、术语和事实源在哪里 | 随项目演进 | 否 |
| `changes/` | 本次具体改什么、做到哪、证据是什么 | 单次变更 | 是 |

`checks/` 用于把上述约束机械化，不构成新的内容层。未实现的检查不得描述成已由 CI 强制。

## 任务路由

| 用户意图 | 首选技能 | 必读规则 | 按需 Wiki |
|---|---|---|---|
| 新需求、复杂缺陷、技术影响分析 | `skills/request-analysis/SKILL.md` | 开发流程、工程结构 | 项目概览、业务模型、数据模型、接口协议 |
| 按确认方案实现或修复 | `skills/implement-change/SKILL.md` | 工程结构、编码、测试 | 与变更相关的 Wiki |
| 仅补测试或固化回归 | `skills/write-unit-tests/SKILL.md` | 测试、编码 | 数据模型、接口协议 |
| 开发或修改 subagent | `skills/implement-change/SKILL.md` | Subagent 开发、AI 功能开发、工程结构、测试 | 业务模型、领域术语 |
| 判断验证是否充分 | `skills/run-quality-gates/SKILL.md` | 测试、开发流程 | 环境与运行 |
| 代码审查、合并前审计 | `skills/expert-review/SKILL.md` | 全部相关规则 | 全部相关 Wiki |
| 启动、环境或发布验证 | `skills/deploy-verify/SKILL.md` | 开发流程、测试、数据库 | 环境与运行、接口协议 |

每次任务先读本文件，然后只加载一个主技能及其直接要求的规则和 Wiki。不要因为“可能有用”就扫描全部历史变更。

## 标准闭环

```text
需求/缺陷 → request-analysis → changes/<change>/summary.md
         → implement-change → 代码 + 测试
         → run-quality-gates → 验证证据
         → expert-review → 审查结论
         → deploy-verify（适用时）→ done / rolled_back
```

允许状态：`draft`、`approved`、`in_progress`、`verifying`、`done`、`rolled_back`。

## 接入项目

1. 填写 `wiki/`，将占位说明换成真实事实和可定位的代码路径。
2. 校准 `rules/`，保留适用规则并明确例外。
3. 把项目真实的构建、测试和部署命令记录到 `wiki/环境与运行.md`。
4. 从 `changes/_template/` 创建变更档案。
5. 运行 `python3 .harness/checks/check_harness.py`。

任何技能都不能跳过用户授权边界，也不能把未执行的验证写成已通过。
