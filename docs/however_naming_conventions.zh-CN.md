# 命名规范（howeverpipecat）

## 1. 类名

- 新增类使用 `PascalCase`。
- 优先使用标准拼写，例如 `OllamaLLMService`。
- 兼容别名保留在迁移期，并注明弃用窗口。

## 2. 文件名

- Python 模块使用 `snake_case.py`。
- fork 新增脚本统一前缀：`however_*`。

## 3. 环境变量

- fork 运行时变量前缀统一为 `HOWEVER_`。
- upstream 服务 key 可继续保留原名（如 `OPENAI_API_KEY`）。

## 4. 命名检查

- 使用 `scripts/however_naming_lint.py` 进行快速检查。
