# 项目当前状态

> 这是项目管理总入口。每完成一个可验收切片都必须更新本文件。

## 当前阶段

- 阶段：S1 最小运行骨架
- 状态：main 已推送，等待远端 Windows/macOS CI 门禁结果
- 当前分支：`main`
- 最近更新：2026-07-23

## 本阶段验收目标

使用完全合成的数据，通过 CLI 和 HTTP 将病例订单转换为符合 Schema 的固定病例包，并原子保存到被 Git 忽略的运行目录。

## 已完成

- S0 项目、Git、隐私、文档和跨平台安全基线；
- 中文 PRD、质量统计方案、医学发布治理与资料准备指南；
- 六病种配置、严格领域 Schema、合成订单与证据引用完整性校验；
- 文件仓储、固定合成生成工作流、CLI 与 HTTP 接口；
- Windows/macOS 统一安装、测试、启动入口和双平台 CI 配置；
- Windows 本地依赖安装、全量测试、CLI、API 与 Git 隐私边界验收。

## 正在进行

- 确认 GitHub Actions 的 Windows/macOS 实际运行结果。

## 当前阻塞

S1 功能和本地验收无阻塞。`main` 已推送，S1 最终门禁仍需 GitHub Actions 的 Windows/macOS 作业实际通过；当前不能把“已配置/已触发”表述为“已通过”。

S2 的工程接口设计可继续，但真实医学有效性验证会在最小医学输入包未到位时阻塞。

## 等待医学团队输入

S2 开始真实生成验证前，需要同一试点病种的指南或教材节选、至少 3 例脱敏病例、3–5 条教学目标，以及一名可答疑并完成最终审核的医学专业人员。准备工作可与分支集成和 S2 接口设计并行。

## 下一可体验入口

- 测试：`python scripts/test.py`
- CLI：`python -m medicine_agents demo --order data/samples/orders/synthetic-order.json --data-dir data/runtime`
- API：`python scripts/run_api.py`
- 交互文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

所有入口当前只使用合成内容；运行数据不会进入 Git。

## 下一步

1. 检查 Windows/macOS CI，全部通过后关闭 S1 最终门禁；
2. 由项目负责人并行协调 S2 最小医学输入包；
3. 在 S2 接入可替换的模型与检索端口，验证单病种真实闭环。