# 从 upstream 迁移到 howeverpipecat

## 1. 迁移目标

将已有基于 `pipecat-ai` 的项目平滑迁移到 `howeverpipecat-ai`，并接入 fork 提供的运行时治理能力。

## 2. 步骤

1. 包依赖替换：`pipecat-ai` -> `howeverpipecat-ai`。
2. 保持 import 不变：`import pipecat...` 仍可使用。
3. 若使用 Ollama，优先替换类名到 `OllamaLLMService`。
4. 复制 `env.however.example` 到 `.env.however.local`。
5. 执行健康检查：`python scripts/however_service_health.py --skip-network --json`。

## 3. 兼容说明

- 旧类名 `OLLamaLLMService` 可继续运行，但会出现弃用告警。
- 推荐在 1-2 个版本周期内完成迁移。
