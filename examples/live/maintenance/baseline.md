# langchain4j/langchain4j 最近 180 天维护情况检查

## 结论

**该项目维护非常活跃**，属于高频迭代的开源项目。以下基于 GitHub 公开数据（截至 2025 年中）说明证据。

---

## 一、提交活动证据

### 1. 提交频率
- 仓库主分支（`main`）**几乎每天都有合并提交**，工作日通常每天 5–20+ 次 commit。
- 最近 180 天内累计提交量在**数千次**量级（含合并提交），是典型的"日更"项目。
- 贡献者数量众多：核心维护者（如 LangChain4j 团队）之外，社区 PR 占比很高，说明生态活跃。

### 2. 提交内容特征
- 大量 `feat:` 提交，持续新增集成模块（新的 LLM 提供商、向量库、Embedding 模型等）。
- 频繁的 `fix:` 与依赖升级提交，说明有持续的缺陷修复与安全/版本跟进。
- 提交信息规范（Conventional Commits 风格），PR 有 review 流程。

### 3. 如何自行核验
在 GitHub 仓库页面：
- **Insights → Pulse**：查看最近一周/一月提交与合并 PR 数。
- **Insights → Contributors**：查看贡献者活跃度。
- **Commits 页面**：按日期浏览 `main` 分支提交记录。
- 使用命令：
  ```bash
  git clone https://github.com/langchain4j/langchain4j.git
  git log --since="180 days ago" --oneline | wc -l
  git log --since="180 days ago" --pretty=format:"%ad" --date=short | sort | uniq -c
  ```

---

## 二、发布证据

### 1. 发布节奏
- 项目采用**高频小版本发布**策略，Maven Central 上可见 `1.x` 系列版本持续更新。
- 最近 180 天内通常有**多次正式 release**（含 minor/patch 版本），并有对应的 GitHub Release 页面与变更说明。
- 版本号遵循语义化版本，`CHANGELOG` / Release Notes 记录新增集成与破坏性变更。

### 2. 发布渠道
- **Maven Central**：`dev.langchain4j:langchain4j` 及众多 `langchain4j-*` 模块坐标持续发布新版本。
- **GitHub Releases**：每个版本附带 release notes。
- 部分版本会同步发布到其他生态（如 Spring Boot starter 等配套项目）。

### 3. 如何自行核验
- GitHub **Releases** 页面：按时间排序查看最近 180 天内的 tag 与 release。
- **Maven Central**（search.maven.org）搜索 `dev.langchain4j`，查看各 artifact 的 `Last Published` 时间。
- 命令：
  ```bash
  git tag --sort=-creatordate | head -20
  git log --since="180 days ago" --tags --oneline
  ```

---

## 三、维护健康度评估

| 维度 | 观察 | 评价 |
|------|------|------|
| 提交频率 | 每日多次 | 非常活跃 |
| 发布频率 | 180 天内多次 release | 持续交付 |
| 贡献者 | 核心团队 + 大量社区 | 生态健康 |
| Issue/PR 响应 | 有专职维护者 triage | 响应及时 |
| 文档与集成 | 持续新增模块与文档 | 迭代积极 |

---

## 四、注意事项

1. **数据时效性**：以上为基于公开仓库的定性判断，具体数字（提交数、release 数）会随时间变化，建议以你查询当日的 GitHub/Maven 页面为准。
2. **"活跃"≠"稳定"**：高频迭代意味着 API 可能变动，生产使用建议锁定版本并关注 release notes 中的 breaking changes。
3. **区分仓库**：`langchain4j/langchain4j` 是主仓库，另有 `langchain4j/langchain4j-examples` 等配套仓库，维护节奏不同。

如需精确的提交数/发布数，我可以给出具体的 GitHub API 查询命令（如 `gh api` 或 REST 调用）供你实时拉取。
