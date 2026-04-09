# howeverpipecat - 实时语音智能体工程分发版 | Real-time Voice Agent Distribution

<p align="center">
  <img src="docs/assets/howeverpipecat-logo.svg" alt="howeverpipecat logo" width="760" />
</p>

🔥 一个面向实时语音与多模态智能体落地的 Pipecat 工程化发行版。  
🚀 在保留 upstream 核心能力的同时，补齐了私有化改造常用的配置治理、命名规范、健康检查、发布安全门禁与迁移文档。  
⭐ 目标是把“示例可跑”升级为“仓库可持续维护”。

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)](https://www.python.org/)
[![Build](https://img.shields.io/badge/Build-uv-6C47FF)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-BSD--2--Clause-16A34A)](./LICENSE)
[![Repository](https://img.shields.io/badge/Repo-however--yir%2Fhoweverpipecat-0EA5E9)](https://github.com/however-yir/howeverpipecat)

---

## 目录

- [1. 项目定位](#1-项目定位)
- [2. 适用人群](#2-适用人群)
- [3. 与 Upstream 的关系与边界](#3-与-upstream-的关系与边界)
- [4. 本仓核心改动概览](#4-本仓核心改动概览)
- [5. 项目文档导航](#5-项目文档导航)
- [6. 快速开始（5 分钟路径）](#6-快速开始5-分钟路径)
- [7. 配置说明（含 DB / Redis / Ollama）](#7-配置说明含-db--redis--ollama)
- [8. 本地健康检查](#8-本地健康检查)
- [9. 依赖与发布策略](#9-依赖与发布策略)
- [10. 命名规范与兼容策略](#10-命名规范与兼容策略)
- [11. 质量门禁与 CI](#11-质量门禁与-ci)
- [12. 测试与检测命令](#12-测试与检测命令)
- [13. 与原版差异清单](#13-与原版差异清单)
- [14. 迁移指南（Upstream -> however）](#14-迁移指南upstream---however)
- [15. 常见故障排查清单](#15-常见故障排查清单)
- [16. 90 天路线图](#16-90-天路线图)
- [17. 贡献方式](#17-贡献方式)
- [18. 许可证与分发说明](#18-许可证与分发说明)

---

## 1. 项目定位

`howeverpipecat` 不是对 upstream 的“简单镜像”，而是一个工程化发行分支：

1. 保留 Pipecat 在实时语音与多模态 pipeline 方面的核心能力。
2. 增强本地化部署与私有化改造的高频薄弱环节。
3. 为二次开发提供可复制、可审查、可持续维护的目录与规范。

---

## 2. 适用人群

- 想基于 Pipecat 做长期迭代项目的个人开发者。
- 需要将语音 Agent 接入内部服务（DB / Redis / Ollama / Telemetry）的团队。
- 希望沉淀“可部署 + 可回归 + 可交接”技术资产的课程或实验项目。
- 希望保留 upstream 能力同时建立自有发布标识与治理规则的维护者。

---

## 3. 与 Upstream 的关系与边界

- Upstream：`pipecat-ai/pipecat`
- 当前仓库：`however` 发行版（fork distribution）
- 保留策略：保留 upstream 许可证与核心目录结构。
- 增量策略：新增 fork 自有配置模板、健康检查脚本、命名规范、CI 门禁与文档。

### 3.1 边界原则

1. 不删除 upstream 许可信息。
2. fork 增量优先放在独立文件（`env.however.example`、`scripts/however_*`、`docs/however_*`）。
3. 尽量避免对 upstream 主流程做破坏性重写。
4. 对兼容性影响提供迁移路径与过渡期。

---

## 4. 本仓核心改动概览

### 4.1 发布与品牌

- 包发布名改为 `howeverpipecat-ai`。
- 项目首页与文档统一 `howeverpipecat` 品牌。
- 新增仓库元信息脚本：`scripts/however_set_repo_metadata.sh`。

### 4.2 命名与兼容

- 新增标准命名 `OllamaLLMService`。
- 旧名 `OLLamaLLMService` 保留兼容，并给出 `DeprecationWarning`。
- 新增命名检查脚本：`scripts/however_naming_lint.py`。

### 4.3 配置与运行时

- 新增 `env.however.example`。
- 新增 `configs/services.example.yaml`。
- 新增运行时配置模块：`src/pipecat/utils/however_runtime_config.py`。
- 新增健康检查模块与脚本：
  - `src/pipecat/utils/however_health.py`
  - `scripts/however_service_health.py`

### 4.4 安全与质量门禁

- 新增敏感信息扫描：`scripts/however_secrets_scan.sh`。
- 新增依赖安全扫描：`scripts/however_dependency_security_scan.sh`。
- 新增 CI 工作流：
  - `.github/workflows/however-quality.yaml`
  - `.github/workflows/however-dependency-security.yaml`
- 发布工作流增加依赖安全检查前置门禁。

---

## 5. 项目文档导航

| 文档 | 目的 |
|---|---|
| [`docs/however_series_map.zh-CN.md`](docs/however_series_map.zh-CN.md) | 系列仓库关系与定位 |
| [`docs/however_versioning.zh-CN.md`](docs/however_versioning.zh-CN.md) | 版本命名与发布策略 |
| [`docs/however_naming_conventions.zh-CN.md`](docs/however_naming_conventions.zh-CN.md) | 类名/脚本/环境变量命名规范 |
| [`docs/however_dependency_strategy.zh-CN.md`](docs/however_dependency_strategy.zh-CN.md) | 核心与扩展依赖边界、升级策略 |
| [`docs/however_python_compatibility.zh-CN.md`](docs/however_python_compatibility.zh-CN.md) | Python 3.11/3.12 兼容说明 |
| [`docs/however_dependency_conflicts_faq.zh-CN.md`](docs/however_dependency_conflicts_faq.zh-CN.md) | 依赖冲突 FAQ |
| [`docs/however_config_change_audit_checklist.zh-CN.md`](docs/however_config_change_audit_checklist.zh-CN.md) | 配置变更审计清单 |
| [`docs/however_migration_from_upstream.zh-CN.md`](docs/however_migration_from_upstream.zh-CN.md) | 上游迁移指南 |
| [`docs/however_troubleshooting_checklist.zh-CN.md`](docs/however_troubleshooting_checklist.zh-CN.md) | 故障排查 checklist |
| [`docs/however_roadmap_90days.zh-CN.md`](docs/however_roadmap_90days.zh-CN.md) | 90 天演进路线图 |
| [`docs/however_projectization_suggestions.zh-CN.md`](docs/however_projectization_suggestions.zh-CN.md) | 60 条改造建议清单 |

---

## 6. 快速开始（5 分钟路径）

### 6.1 环境要求

- Python `3.11+`（建议 `3.12`）
- `uv` 包管理工具

### 6.2 最短可运行路径

```bash
# 1) 克隆
git clone https://github.com/however-yir/howeverpipecat.git
cd howeverpipecat

# 2) 安装基础开发依赖（不要求全量 extras）
uv sync --group dev

# 3) 复制本地模板
cp env.however.example .env.however.local

# 4) 离线健康检查（不依赖真实外部服务）
uv run python scripts/however_service_health.py --skip-network --json

# 5) 跑 fork 新增回归
uv run pytest tests/test_ollama_llm.py tests/test_however_runtime_config.py tests/test_however_health.py
```

---

## 7. 配置说明（含 DB / Redis / Ollama）

本仓将 fork 运行时配置统一为 `HOWEVER_` 前缀，避免与 upstream 服务 API Key 变量混淆。

| 变量名 | 说明 | 示例 |
|---|---|---|
| `HOWEVER_DB_URL` | 业务数据库连接 | `postgresql://hc_user:***@postgres.internal.example:5432/howeverpipecat` |
| `HOWEVER_REDIS_URL` | 缓存或会话存储连接 | `redis://redis.internal.example:6379/0` |
| `HOWEVER_OLLAMA_BASE_URL` | Ollama 网关地址 | `http://ollama.internal.example:11434/v1` |
| `HOWEVER_TELEMETRY_ENDPOINT` | 可观测性上报地址 | `https://telemetry.internal.example/pipecat/events` |
| `HOWEVER_STARTUP_CHECK_TIMEOUT_MS` | 启动检查超时（毫秒） | `1500` |
| `HOWEVER_STRICT_STARTUP_CHECKS` | 检查失败是否阻断 | `true` |

### 7.1 配置优先级

1. 进程环境变量
2. `.env.however.local`
3. 代码默认占位值

### 7.2 变量校验

- URL 会校验 scheme + host。
- timeout 会校验范围。
- 非法值会抛出明确错误，归类为 `config_error`。

---

## 8. 本地健康检查

```bash
# 离线模式
uv run python scripts/however_service_health.py --skip-network --json

# 联网模式
uv run python scripts/however_service_health.py --json
```

输出字段统一包含：`env`、`region`、`status`、`latency_ms`、`fault_type`。

`fault_type` 分类：

- `config_error`
- `network_error`
- `auth_error`
- `unknown_error`

---

## 9. 依赖与发布策略

### 9.1 依赖边界

- Core：最小可运行依赖。
- Extras：按服务能力拆分按需启用。

详细策略见 [`docs/however_dependency_strategy.zh-CN.md`](docs/however_dependency_strategy.zh-CN.md)。

### 9.2 版本命名

- 统一规则：`vX.Y.Z-however.N`
- 详细见 [`docs/however_versioning.zh-CN.md`](docs/however_versioning.zh-CN.md)

### 9.3 月度升级节奏

- 每月固定窗口执行依赖升级、回归对比与发布决策。

---

## 10. 命名规范与兼容策略

### 10.1 推荐命名

- 使用 `OllamaLLMService`。
- 环境变量前缀使用 `HOWEVER_`。
- fork 脚本统一 `however_*` 前缀。

### 10.2 兼容策略

- `OLLamaLLMService` 保留兼容，迁移期内可继续使用。
- 建议在 1-2 个版本周期内迁移到 `OllamaLLMService`。

### 10.3 命名 lint

```bash
python scripts/however_naming_lint.py
```

---

## 11. 质量门禁与 CI

### 11.1 新增门禁

- 命名检查：`scripts/however_naming_lint.py`
- 敏感信息扫描：`scripts/however_secrets_scan.sh`
- 依赖安全扫描：`scripts/however_dependency_security_scan.sh`
- fork 运行时测试与离线健康检查

### 11.2 工作流

- `.github/workflows/however-quality.yaml`
- `.github/workflows/however-dependency-security.yaml`
- 发布流程增加 dependency security scan 前置步骤。

---

## 12. 测试与检测命令

```bash
# fork 新增测试
uv run pytest tests/test_ollama_llm.py tests/test_however_runtime_config.py tests/test_however_health.py

# 健康检查（离线）
uv run python scripts/however_service_health.py --skip-network --json

# 命名 lint
python scripts/however_naming_lint.py

# 敏感信息扫描
bash scripts/however_secrets_scan.sh

# 依赖安全扫描（发布前）
bash scripts/however_dependency_security_scan.sh
```

---

## 13. 与原版差异清单

| 类别 | Upstream | however 发行版 |
|---|---|---|
| 包发布名 | `pipecat-ai` | `howeverpipecat-ai` |
| Ollama 命名 | `OLLamaLLMService` | 推荐 `OllamaLLMService`，保留兼容别名 |
| 配置模板 | `env.example` | 新增 `env.however.example` + `configs/services.example.yaml` |
| 运行时检查 | 无统一脚本 | 新增 `however_service_health.py` + `however_health` 模块 |
| 命名治理 | 无 | 新增 `however_naming_lint.py` |
| 敏感信息扫描 | 无 | 新增 `however_secrets_scan.sh` |
| 依赖安全门禁 | 无 | 新增 `however_dependency_security_scan.sh` 与 CI 门禁 |
| 协议补充 | `LICENSE` | 新增 `LICENSE.HOWEVER` |
| 运维模板 | 无 | 新增 Issue 模板与 Release Notes 模板 |

---

## 14. 迁移指南（Upstream -> however）

快速迁移：

1. 将依赖从 `pipecat-ai` 替换为 `howeverpipecat-ai`。
2. 保持 import 为 `pipecat.*`（无需大规模改代码）。
3. Ollama 类名逐步迁移到 `OllamaLLMService`。
4. 复制并填写 `env.however.example`。
5. 执行健康检查与新增测试。

详细见 [`docs/however_migration_from_upstream.zh-CN.md`](docs/however_migration_from_upstream.zh-CN.md)。

---

## 15. 常见故障排查清单

请按 checklist 执行，不建议跳步：

- 配置检查（变量完整性与格式）
- 依赖检查（是否完整安装）
- 运行时检查（离线 -> 联网）
- 回归检查（测试 + lint + scan）

详细清单见 [`docs/however_troubleshooting_checklist.zh-CN.md`](docs/however_troubleshooting_checklist.zh-CN.md)。

---

## 16. 90 天路线图

- 第 1-30 天：稳定性治理
- 第 31-60 天：性能与回归基线
- 第 61-90 天：生态兼容与发布流程固化

详细路线图见 [`docs/however_roadmap_90days.zh-CN.md`](docs/however_roadmap_90days.zh-CN.md)。

---

## 17. 贡献方式

1. 先阅读 `CONTRIBUTING.md` 与本 README 差异清单。
2. 涉及 fork 增量能力时，优先放在独立目录并补测试。
3. 提交 PR 时建议写清：变更模块、影响范围、回归命令、回滚方案。

### 17.1 模板

- 运行时问题模板：`.github/ISSUE_TEMPLATE/however_runtime_bug.yml`
- 发布说明模板：`.github/RELEASE_NOTES_TEMPLATE.md`

---

## 18. 许可证与分发说明

- Upstream 许可证：`LICENSE`（BSD-2-Clause）
- Fork 补充说明：`LICENSE.HOWEVER`

本仓用于工程开发、测试和部署实践。生产使用前，请自行完成安全、合规与稳定性评估。