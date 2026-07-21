# Changes

每个跨文件需求、缺陷修复、数据变更或发布工作使用独立目录记录上下文和验证证据：

```text
changes/<change-name>/
├── summary.md          # 必需：范围、设计、进度、验证、结论
├── evidence.md         # 可选：命令、截图、日志摘要、评估结果
├── db-migration.sql    # 可选：数据库迁移草案
└── rollback.sql        # 可选：数据回滚草案
```

目录使用小写 kebab-case，例如 `improve-error-handling`，不要按日期或人员命名。

## 生命周期

1. 从 `_template/summary.md` 创建档案，状态为 `draft`。
2. 需求和方案确认后改为 `approved`。
3. 开始编码时改为 `in_progress`，持续更新文件清单和决策日志。
4. 进入验证时改为 `verifying`，记录真实结果。
5. 验收满足后改为 `done`；发生回滚则改为 `rolled_back`。

逐节实例化模板；不适用的小节保留标题并写明 `N/A + 原因`。不要把旧项目档案当模板照抄。

已完成档案用于解释单次决策，不替代长期规则或项目 Wiki。档案不得包含秘密、内网地址、个人数据、客户数据或未经筛选的生产日志。
