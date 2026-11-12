# 运行示例与评测数据

最新检索与双模型核验记录见 [v0.2.0 示例](v0.2/README.md)。下列为 v0.1.0 历史记录。

下列目录保存 2026-11-12 的真实模型与 GitHub 调研结果。每个目录包含 report.md、report.json、events.jsonl 和同模型单次回答 baseline.md。

- [技术栈调研](live/stack/report.md)
- [维护情况](live/maintenance/report.md)
- [使用与部署资料](live/deployment/report.md)
- [候选项目比较](live/comparison/report.md)
- [证据不足时的未确认结果](live/insufficient/report.md)

[最终真实评测](evaluation-live.json)、[离线合成回放](evaluation-offline.json)、[来源抽查](source-review.json) 和 [费用汇总](cost-summary.json) 分别记录执行方式、检查结果与实际用量。

evaluation-initial.json、evaluation-intermediate.json 和 evaluation-before-compact-summary.json 保存调试期间各轮结果。调试阶段存在题目地址与分析范围调整，详细经过见 [评测说明](../docs/EVALUATION.md)。

baseline.md 完整保留单次模型原始回答，其中的事实、代码和检索声明需要结合来源抽查记录阅读。全部报告的读取时间与固定 commit 均保留在 JSON 证据中。
