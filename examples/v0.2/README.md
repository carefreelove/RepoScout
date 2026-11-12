# v0.2.0 运行与核验记录

本目录保存仓库资料检索和双模型辅助核验的运行结果。

- [技术栈调研](live/stack/report.md)
- [维护情况](live/maintenance/report.md)
- [使用与部署资料](live/deployment/report.md)
- [候选比较](live/comparison/report.md)
- [证据不足](live/insufficient/report.md)
- [受控错误补证案例](repair-demo/report.md)
- [请求中断后的恢复案例](recovery/report.md)

每个真实调研目录包含 report.md、report.json、review.json 与 events.jsonl，live 目录还保留同模型单次回答 baseline.md。

repair-demo 使用真实仓库和真实模型，初始 Java 8 陈述为刻意注入的测试错误，详见 manifest.json、initial-draft.json 与 initial-review.json。可在项目根目录通过以下命令复现，调用会计入同一预算。

```bash
uv run python examples/v0.2/repair_demo.py
```

[检索与核验回归](evidence-live.json) 使用固定合成证据；[离线协议回放](evidence-offline.json) 使用预置标签。[最终真实问题集](evaluation-live.json)、[首次故障记录](evaluation-initial.json) 与 [费用汇总](cost-summary.json) 保留各次执行状态和用量信息。

费用汇总含一笔人工接受的未知用量最高预留，实际账单以服务商为准。
