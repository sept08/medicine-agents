# 医学教学病例智能体

这是一个采用文件优先架构、面向单操作者运行的医学教学病例 MVP，用于生成、审核和发布结构化病例及配套问题答案包。S1 使用完全合成数据，不需要商业模型密钥或真实医学资料。

## 项目导航

- [项目当前状态](project/CURRENT_STATUS.md)
- [阶段路线图](project/ROADMAP.md)
- [产品需求文档](docs/requirements/产品需求文档.md)
- [文件优先 MVP 设计规格](docs/design/2026-07-22-文件优先MVP设计.md)
- [质量评价与统计分析方案](docs/quality/质量评价与统计分析方案.md)
- [MVP 医学内容发布治理规范](docs/governance/MVP医学内容发布治理规范.md)
- [医学团队资料准备指南](docs/guides/医学团队资料准备指南.md)
- [仓库数据与隐私策略](docs/security/仓库数据与隐私策略.md)
- [S0 与 S1 实施计划](project/plans/2026-07-22-S0与S1实施计划.md)

## 环境要求

- Windows 10/11 或当前受支持的 macOS。
- Python 3.11 或更高版本。
- Git。首次安装依赖需要访问 Python 包索引。

## 新设备初始化

克隆仓库后，在仓库根目录运行：

Windows：

```powershell
py -3.11 scripts/bootstrap.py
.\.venv\Scripts\Activate.ps1
```

macOS：

```bash
python3 scripts/bootstrap.py
source .venv/bin/activate
```

每台设备还需单独创建 `.local/sensitive_terms.txt`、`.env` 和私有医学资料目录；这些本地内容不会随 Git 克隆。可从 `.env.example` 复制本机配置，但不得提交密钥。

## 测试

激活虚拟环境后，Windows 与 macOS 使用同一命令：

```text
python scripts/test.py
```

该入口依次执行 Ruff 静态检查和全部 pytest 测试。GitHub Actions 也在 `windows-latest` 与 `macos-latest` 上运行同一入口。

## 体验 S1 合成流程

命令行：

```text
python -m medicine_agents demo --order data/samples/orders/synthetic-order.json --data-dir data/runtime
```

命令只打印病例编号与文件路径；合成病例包写入被 Git 忽略的 `data/runtime/`。

HTTP API：

```text
python scripts/run_api.py
```

启动后打开 `http://127.0.0.1:8000/docs`，可通过交互文档提交同一订单；健康检查地址为 `http://127.0.0.1:8000/health`。服务默认只监听本机回环地址。

## 仓库与医学资料边界

`wiki/`、真实医学资料、运行产物、密钥和本机敏感词表均不进入版本库。仓库中的病例与证据样例全部明确标记为合成数据。导入教材、指南或脱敏病例前，请先阅读隐私策略与医学团队资料准备指南。

S2 才会首次接入商业模型：届时需要在本机配置 API Key、费用上限与允许调用外部 API 的脱敏资料。模型、文件仓储与任务执行均通过接口隔离，后续可分别替换为其他商业模型、RDS、OSS 和云端队列。