# howeverpipecat 版本策略

## 版本命名

- 开发分支快照：`vX.Y.Z-however.N-dev`
- 可发布版本：`vX.Y.Z-however.N`
- 长期维护标签：`lts-howeverpipecat-YYYYMMDD`

## 分支策略

- `main`：持续开发分支。
- `release/*`：发布稳定分支。
- `hotfix/*`：线上紧急修复。

## 发布节奏

1. 每周可选一次 RC（候选版本）。
2. 每月 1 次稳定发行。
3. 上游重大变更触发专项兼容发布。
