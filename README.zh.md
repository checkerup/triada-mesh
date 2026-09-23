# Triada Mesh (三联协同网格)

> **自主多智能体中继调度、看门狗仲裁器与跨环境知识网格**  
> *连接 Google Antigravity、Hermes Agent 与 OpenCode，打造自主验证、持续演进的高可靠工程三联体。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Multi-Harness](https://img.shields.io/badge/Harness-Antigravity%20%7C%20Hermes%20%7C%20OpenCode-blueviolet)](docs/architecture.md)

[**English (README.md)**](README.md) | [**Русская версия (README.ru.md)**](README.ru.md)

---

## 什么是 Triada？

**Triada (三联体)** 是一个开源去中心化多智能体协同引擎。其核心理念是：**任何单一 AI 模型或单一智能体执行环境都不应孤立工作**。

通过将三个独立的智能体环境与多元化的顶级推理模型相结合，Triada 消除了单一模型的认知盲区与群体幻觉，并通过严格的事实证据机制 (Evidence-Based Verification) 确保工程任务的端到端闭环交付。

```
                      ┌──────────────────────────────────────┐
                      │        Obsidian 共享知识网格          │
                      │        (Vault MCP Server)            │
                      └──────────────────┬───────────────────┘
                                         │ 架构决策 (ADR) 与上下文共享
                                         ▼
┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│   Mark (Antigravity) │◄─────►│     Kat (Hermes)     │◄─────►│    Nika (OpenCode)   │
│  - 系统架构设计      │       │  - 服务端守护进程    │       │  - 代码 Diff 精准修改│
│  - 任务拆解与规范    │       │  - 集成测试与验证    │       │  - 性能优化与重构    │
│  - 深度多步推理      │       │  - Linux 运维与长任务│       │  - 边界用例自动化验证│
└──────────┬───────────┘       └──────────┬───────────┘       └──────────┬───────────┘
           │                              │                              │
           └──────────────────────────────┼──────────────────────────────┘
                                          │
                                          ▼
                      ┌──────────────────────────────────────┐
                      │    Jev Pacer 看门狗与中继调度器      │
                      │  - 反虚假交付 (Anti-False Finish)    │
                      │  - 自动化接力中继调度                │
                      │  - 双重证据门禁验证                  │
                      └──────────────────────────────────────┘
```

---

## 核心支柱

### 1. 跨环境认知分层 (Cognitive Tiering)
避免将所有智能体强行绑定至同一种模型架构，实现真正的模型多样性：
- **Mark (Antigravity)**: 顶级架构设计与规划模型 (Gemini 2.5 Pro / Claude 3.7 Sonnet)。
- **Kat (Hermes)**: 长生命周期服务器后台进程与顺序推理 (Moonshot Kimi K3 / DeepSeek R1)。
- **Nika (OpenCode)**: 高速代码修改与测试生成 (GLM-5.2 / Qwen Coder)。

### 2. Jev Pacer 看门狗 (防止虚假交付)
大语言模型容易出现“提前宣布完成”的虚假交付缺陷。Jev Pacer 是基于 TypeSafe Jev System One 概率引擎的独立看门狗。它实时比对 git diff 和单元测试退出码。若智能体在测试未通过前宣称完成，Jev 将直接触发纠错 **kick (踢回重试)**。

### 3. 自主中继调度器 (Relay Dispatcher)
执行全自动闭环接力中继 (`Mark -> Kat -> Nika -> Mark`)。包含严格的**双重验证门禁**（测试退出码为 0、产物存在、无未解决的 kick）以及针对 Windows 文件锁的 **15–30 秒缓冲保护期 (Grace Period)**。

### 4. Obsidian 共享知识网格 (Vault MCP)
基于本地 Markdown 的人类可读知识库，集中管理架构决策记录 (ADR)、任务执行日志 (`triada-ledger.jsonl`) 与协作协议。

---

## 快速上手

### 环境要求
- Python 3.9+
- Git

### 安装
```bash
git clone https://github.com/checkerup/triada-mesh.git
cd triada-mesh
python scripts/install.py
```

### 环境健康检查
```bash
python scripts/doctor.py
```

### 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 设置 TRIADA_JEV_API_KEY
```

### 运行测试套件
```bash
python tests/run_tests.py
```

---

## 可插拔密钥池架构

Triada 核心引擎与账户来源完全解耦：
- **内置支持 (`env`)**: 直接从 `TRIADA_JEV_API_KEY` 环境变量读取多个密钥并支持自动轮换。
- **私有账户池扩展**: 如拥有专有的自动化注册池，可通过实现抽象接口 `KeyPoolProvider` 轻松接入，避免向开源公开仓库泄露任何私有代码。参见 [src/triada/providers/README.md](src/triada/providers/README.md)。

---

## 开源协议

MIT License。详见 [LICENSE](LICENSE) 文件。
