# AKShare Stock Skill for AI Assistants

这是一个专为 AI 助手（如 Claude, ChatGPT, Moss 等）设计的 Skill 工具集，旨在赋予大语言模型获取、处理和分析中国 A 股市场数据的能力。本工具基于强大的 [AKShare](https://github.com/akfamily/akshare) 开源财经数据接口。

## 🤖 核心价值

*   **赋予 AI 实时数据能力**：让您的 AI 助手能够查询实时股价、历史 K 线、财务报表等。
*   **结构化分析输出**：所有脚本默认输出 Markdown 格式的报告，便于 LLM 阅读和理解。
*   **智能缓存机制**：内置 SQLite 缓存，减少重复请求，提高响应速度并降低 API 调用频率。
*   **自动化任务**：支持定时任务调度，自动生成日报或监控特定股票。

## 📂 仓库结构

仓库采用了模块化的目录结构，核心功能位于 `akshare-stock` 目录下：

```text
.
├── README.md                # 项目说明文档（本文件）
├── LICENSE                  # 许可证文件
└── akshare-stock/           # Skill 核心目录
    ├── SKILL.md             # AI 助手使用的 Skill 定义文件
    ├── config.yaml          # 配置文件
    ├── scripts/             # Python 功能脚本
    │   ├── analyze_investment.py   # 智能投资分析
    │   ├── stock_analyzer.py       # 综合分析报告
    │   ├── scheduler.py            # 定时任务调度
    │   └── ... (其他数据获取脚本)
    └── references/          # 参考文档
```

## 🚀 快速开始

### 1. 环境准备

确保您的环境已安装 Python 3.8+，并安装必要的依赖库：

```bash
pip install akshare pandas numpy pyyaml
```

### 2. 作为 Skill 使用

将 `akshare-stock` 目录集成到您的 AI Agent 系统中。AI 助手可以通过读取 `SKILL.md` 理解如何调用 `scripts/` 下的工具。

### 3. 独立运行脚本

您也可以直接运行脚本进行测试或数据获取：

```bash
cd akshare-stock/scripts

# 📊 智能投资分析（生成包含估值、资金面、技术面的综合建议）
python analyze_investment.py 600519

# 📈 获取贵州茅台的实时行情
python get_realtime_quote.py 600519

# 🕯️ 获取最近 60 天的历史 K 线
python get_history_kline.py 600519 --days 60

# 📑 生成markdown格式的研报
python stock_analyzer.py 600519 -o report.md
```

## ✨ 功能特性

| 功能模块 | 描述 | 对应脚本 |
| :--- | :--- | :--- |
| **智能分析** | 多维度评分模型，提供买入/卖出建议 | `analyze_investment.py` |
| **实时行情** | 获取最新的个股报价和成交量 | `get_realtime_quote.py` |
| **技术指标** | 计算 MA, MACD, RSI, KDJ, BOLL 等 | `calc_technical.py` |
| **基本面数据** | 财务报表、估值分析 (PE/PB)、股息分红 | `get_financial.py`, `get_valuation.py` |
| **资金流向** | 主力资金流入流出分析 | `get_fund_flow.py` |
| **定时任务** | 后台自动监控和生成报告 | `scheduler.py` |

## 🛠️ 配置

在 `akshare-stock/config.yaml` 中可以自定义配置：
*   **默认股票池**：设置您关注的股票列表。
*   **缓存策略**：调整不同类型数据的缓存过期时间。
*   **定时任务**：设置数据自动更新的时间点。

## 📚 参考资源

*   [AKShare 官方文档](https://akshare.akfamily.xyz)
*   [API 接口列表](akshare-stock/references/api_reference.md)
