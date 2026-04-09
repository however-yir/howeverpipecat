# 依赖冲突 FAQ

## Q1: `ModuleNotFoundError: websockets`

- 原因：未安装 websocket 相关 extra 或运行环境未同步依赖。
- 处理：`pip install websockets` 或启用对应 extras。

## Q2: `PackageNotFoundError: pipecat-ai`

- 原因：源码运行时未安装包元数据。
- 处理：`pip install -e .`，或使用本仓已做的版本回退逻辑。

## Q3: 本地 `uv` 不可用

- 原因：未安装 uv。
- 处理：按 README 的安装步骤先安装 uv，再同步依赖。

## Q4: 音频相关依赖安装失败

- 原因：缺系统库。
- 处理：先安装 `portaudio`、`ffmpeg`、`libsndfile` 再安装 Python 包。
