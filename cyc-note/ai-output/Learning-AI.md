---
Title: "Learning-AI：系统化大语言模型学习笔记"
Url: "https://github.com/ChenLinXXXX/Learning-AI"
Author: "ChenLinXXXX"
Origin: "GitHub"
Description: "一份从数学基础、Transformer、训练与推理，到 DeepSeek、RAG、Agent 和多模态应用的大语言模型学习笔记。"
Tags:
  - 人工智能
  - 大语言模型
  - Transformer
  - DeepSeek
  - RAG
  - Agent
  - 开源项目
Created: "2026-08-20"
---

# Learning-AI

> 一份系统化、可复习、面向深入学习的大语言模型知识体系，从数学基础到 Transformer，从训练到推理，再到 DeepSeek-V3 与前沿应用。

## 项目定位

这是一个偏“论文化、教材级、工程师视角”的 LLM 学习笔记仓库。每章采用统一结构，兼顾顺序学习和按主题检索，内容强调公式推导、直觉类比、可运行代码、论文索引和章节交叉引用。

## 仓库结构

| 部分 | 主题 | 章节数 | 难度 |
| --- | --- | ---: | --- |
| Part I | 数学与基础：线性代数、概率、反向传播、优化器 | 4 | ★★☆ |
| Part II | Transformer 架构：Tokenization、Embedding、Attention、FFN、Norm、Block | 6 | ★★★ |
| Part III | 训练原理：数据、预训练、分布式、SFT、RLHF、Scaling Law | 7 | ★★★★ |
| Part IV | 推理与部署：Prefill、Decode、KV Cache、采样、量化、本地部署 | 5 | ★★★ |
| Part V | DeepSeek 专题：MLA、DeepSeekMoE、V3 训练、LLaMA-3 对比、R1 | 6 | ★★★★ |
| Part VI | 应用前沿：多模态、RAG、Agent、Prompt、Skills、MCP | 6 | ★★★ |

附录包括名词字典、公式速查、参考论文与资源、学习路径建议。

## 学习路径

- **系统入门**：`00 前言` → Part I → Part II → Part III → Part IV → Part V → Part VI，预计 80-100 小时。
- **工程师快速通道**：跳过 Part I，重点学习 Transformer、训练原理、推理部署，再进入 DeepSeek 和应用专题，预计 40-50 小时。
- **面试与原理深化**：Self-Attention → 位置编码 → 分布式 → RLHF/GRPO → KV Cache → MLA → MoE，预计 20-30 小时。
- **部署优先**：本地部署 → 推理优化 → 采样 → KV Cache → 推理流程 → RAG → Agent，预计 15-20 小时。

## 主题速查

- Attention 数学推导：第 07 章
- RoPE：第 06 章
- FFN 与 SwiGLU：第 08 章
- RLHF / DPO / GRPO：第 16 章
- Scaling Law：第 17 章
- KV Cache：第 19 章
- 量化：第 21 章
- 本地运行 DeepSeek：第 22 章
- MLA：第 24 章
- MoE：第 25 章
- RAG：第 30 章
- Agent：第 31 章

## 单章结构

每章通常包含章节元数据、摘要与学习目标、正文、通俗类比、常见问题、小结、延伸阅读、实战练习和章节交叉引用。正文按“直觉 → 公式 → 代码 → 复杂度”的顺序组织。

## 项目状态

- GitHub 仓库：公开，默认分支为 `main`。
- 仓库描述：大语言模型原理与实践 — 学习笔记。
- GitHub API 读取到的最近更新时间：2026-06-27。
- README 标记为 WIP，包含 34 章和 4 个附录。
- GitHub API 统计：13 stars、1 fork、0 open issues。

> [!warning] 许可证信息
> README 的徽章和说明写的是 MIT，但仓库中的 `LICENSE` 文件实际为 Apache License 2.0。使用、转载或二次开发前，应以仓库中的 `LICENSE` 文件为准。

## 原始链接

- [GitHub 仓库](https://github.com/ChenLinXXXX/Learning-AI)
- [README](https://github.com/ChenLinXXXX/Learning-AI/blob/main/README.md)
- [LICENSE](https://github.com/ChenLinXXXX/Learning-AI/blob/main/LICENSE)
