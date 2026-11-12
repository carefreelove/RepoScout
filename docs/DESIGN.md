# RepoScout 设计与架构

## 问题背景

开源选型涉及动态元数据、文档声明和源码实现。推荐理由需要来源，网络或模型失败后也需要保留已收集的资料。项目围绕这些问题建立证据记录与持久化研究流程。

## 选择依据与方案取舍

| 需求 | 选择依据 | 实现方式 |
| --- | --- | --- |
| 多步工具调用 | Deep Agents 已提供 Agent 图与上下文管理 | 复用 create_deep_agent，添加领域工具 |
| 仓库调研 | GitHub 为元数据、文件和 commit 提供标准 API | REST GET 客户端与读取上限 |
| 可核查结论 | 默认分支会变化 | 首次分析固定 SHA，文件读取始终指定 ref |
| 跨进程恢复 | 需要同时保存资料和执行位置 | SQLite 领域数据与 LangGraph checkpoints |
| 调用预算 | 主调用之外还会发生上下文压缩 | 在模型同步生成入口统一计量 |
| 单人 CLI 项目 | 本地事务和文件足以支持演示 | SQLite、进程锁、Markdown/JSON |

第一版使用单 Agent，关闭默认 general-purpose subagent，保留规划和压缩能力。StateBackend 将 Agent 文件操作限制在图状态中。execute 缺少 shell 后端，并从可见工具集中移除。

## 实现步骤与数据流

1. CLI 建立任务 ID，保存原始需求与本次配置。
2. Agent 提取用户明确条件，以 write_todos 生成简短研究计划。
3. 搜索候选，记录查询和时间，空结果可调整查询。
4. inspect_repository 检查公开状态，固定 commit，补充提交与 release 记录。
5. 根据目录和资料缺口读取文本，工具生成来源字段与唯一 evidence ID。
6. Agent 调用 submit_report，程序校验条件覆盖、仓库归属、commit 和引用。
7. 同一 Report 生成双格式报告。中断时也导出证据、错误及用量。

Pydantic 公开结构的 schema_version 为 1.0。Candidate 包含 Assessment、Claim、推荐决定和未知项。Evidence 来源字段由工具生成，模型引用 ID。

## 持久化与故障

state.sqlite 保存 runs、objects、events 和 ledger。objects 保存仓库 pin、证据、查询与 HTTP 缓存。checkpoints.sqlite 由 LangGraph SqliteSaver 保存图状态。恢复时复用领域资料，并检查图是否还有待执行节点。

同一任务通过 flock 拒绝重复执行。领域写入和预算使用 SQLite 事务。报告先写临时文件再替换，show 可重新导出。GitHub 网络失败与短期限流最多重试两次，长时间限流保留恢复信息。Ctrl+C 保存 cancelled，运行时间在恢复时累计。

模型 API 自动重试与流式生成关闭，统一适配器处理 429 重试并计数。发送前以消息和工具定义的 UTF-8 大小估算输入 token 上界，再加协议余量和最大输出额度。使用高峰价格预留 micro-CNY，usage 完整时结算。未知用量保留预留并暂停新调用，压缩调用使用同一模型对象。

## 验证与边界

测试覆盖图入口、文件边界、引用、并发预算、取消恢复和故障导出。真实结果见 EVALUATION.md。

引用校验验证证据存在、仓库归属与 commit，语义正确性由人工检查。提示词要求严格提取用户条件，并区分资料依据。当前模型仍可能解释过度，固定评测用于发现这些问题。

维护记录适用于采集时间，证据缓存属于单次任务。目标项目的构建、部署和性能需要独立实测。恢复沿用原总限额，耗尽后需新建任务并明确新的调研需求。
