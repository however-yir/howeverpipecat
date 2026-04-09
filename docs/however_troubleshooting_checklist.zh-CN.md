# 故障排查清单（可执行）

## A. 配置检查

- [ ] `.env.however.local` 是否存在
- [ ] `HOWEVER_DB_URL` / `HOWEVER_REDIS_URL` / `HOWEVER_OLLAMA_BASE_URL` 是否有效
- [ ] `HOWEVER_STARTUP_CHECK_TIMEOUT_MS` 是否在合理范围

## B. 依赖检查

- [ ] 是否完成 `pip install -e .` 或 `uv sync`
- [ ] 是否缺 `websockets`、`loguru` 等基础依赖

## C. 运行时检查

- [ ] 执行 `python scripts/however_service_health.py --skip-network --json`
- [ ] 执行 `python scripts/however_service_health.py --json`
- [ ] 查看 `fault_type` 是否为 `config_error` / `network_error` / `auth_error`

## D. 回归检查

- [ ] 执行新增测试集
- [ ] 执行命名 lint 与 secrets scan
