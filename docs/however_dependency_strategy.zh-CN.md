# 依赖与构建策略

## 1. 最小依赖集合（Core）

- 仅包含框架运行必需依赖，保证基础 pipeline 可运行。
- 目标：低冲突、快速安装、最小可用。

## 2. 扩展依赖集合（Extras）

- 按服务能力启用（STT/LLM/TTS/Transport）。
- 目标：按需安装，避免全量依赖膨胀。

## 3. Extras 稳定性评级

| 等级 | 说明 |
|---|---|
| `stable` | 主流程高频使用、维护稳定 |
| `beta` | 可用但持续演进 |
| `experimental` | 仅实验验证，不承诺稳定 API |

## 4. 月度升级策略

1. 每月第 1 周：收集上游依赖变化与安全通告。
2. 每月第 2 周：在 `dependency-upgrade/*` 分支试升级。
3. 每月第 3 周：执行升级前后回归基线对比。
4. 每月第 4 周：决定是否合并到 `main`。

## 5. 回归基线

- 升级前后必须对比：
  - 关键测试通过率
  - 健康检查结果
  - 启动耗时与核心路径延迟

## 6. 开发环境建议

### 本地开发

- Python `3.11/3.12`
- `uv sync --group dev`
- 仅启用当前需要的 extras

### 容器环境

- 推荐基础镜像：`python:3.12-slim`
- 音频依赖建议：`portaudio19-dev`, `ffmpeg`, `libsndfile1`

## 7. 发布前依赖安全检查

- 运行 `scripts/however_dependency_security_scan.sh`
- 在发布工作流中必须通过该检查
