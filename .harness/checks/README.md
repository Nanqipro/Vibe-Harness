# Harness Checks

这里存放可机械执行的 Harness 自检。检查必须只读、无网络、无第三方依赖，并输出可行动的错误信息。

运行：

```bash
python3 .harness/checks/check_harness.py
```

当前检查技能目录、元数据、任务路由和 Harness 内部链接的一致性。项目源码路径、构建命令和技术栈因仓库而异，不在通用检查中硬编码。
