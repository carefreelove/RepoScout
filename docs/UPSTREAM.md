# 上游来源与实现范围

参考 Deep Agents commit `7eee17462177b7079940587523af01f315edfd46`，运行 SDK 为 PyPI 0.7.35，传递依赖由 uv.lock 固定。

| 模块 | 上游来源 | RepoScout 的处理 |
| --- | --- | --- |
| Agent 编排 | Deep Agents create_deep_agent | 复用，配置单 Agent 与领域提示词 |
| 规划工具 | LangChain TodoListMiddleware | 复用 SDK 生态能力 |
| 上下文管理 | Deep Agents SummarizationMiddleware | 复用，使用统一计费模型 |
| 文件工作区 | Deep Agents StateBackend | 复用虚拟文件和 checkpoint |
| 研究流程 | Deep Research agent.py / prompts.py | 改写为 GitHub 搜索、源码取证、条件比较和结构化提交 |
| 研究工具 | Deep Research tools.py 的通用网页检索模式 | 开发 GitHub REST 客户端与 4 个只读工具 |
| 子 Agent | 上游与示例支持委派 | 第一版关闭默认子 Agent |
| 证据与输出 | 上游工具消息和文件能力 | 开发 Evidence、ReportDraft、引用校验和双格式输出 |
| 状态与故障 | LangGraph checkpoint | 复用原语，开发任务记录、缓存、锁与错误分类 |
| 预算 | SDK 模型调用入口 | 开发预留、结算、未知用量冻结和持久化账本 |
| 评测 | SDK 图与 LangChain 模型接口 | 开发合成模型、MockTransport、固定问题集及单次回答对照 |
| 仓库资料检索 | SQLite FTS5/BM25 | 开发 commit 隔离、文本分块、行号映射、中文子串补充、证据转换与检索评测 |
| 双模型核验 | LangChain 模型与结构化输出接口 | 开发 Pro 独立上下文、逐项覆盖检查、有限补证、无进展停止和审查状态恢复 |

项目使用 AI 编程助手协作完成开发与验证。复用、改造与验证范围见上述模块说明及评测记录。
