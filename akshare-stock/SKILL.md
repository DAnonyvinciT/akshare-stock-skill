---
name: akshare-stock
description: "使用 AKShare 库获取和分析中国 A 股市场数据。AKShare 是免费开源的 Python 金融数据接口库，无需注册或 Token。支持：股票实时行情、历史K线、财务报表、估值指标、资金流向、技术指标、定时任务等。当用户需要获取 A 股股价、分析个股基本面、查询财务数据、计算技术指标、分析资金流向时使用此 skill。"
---

# AKShare A股数据分析 Skill

使用 AKShare 库获取中国 A 股市场数据并进行分析。AKShare 是**免费开源**的金融数据接口，无需注册或 Token。

## 快速开始

### 环境准备

```bash
pip install akshare pandas numpy pyyaml
```

### 典型工作流程

1. **安装依赖** → 确认 `pip install akshare pandas numpy pyyaml` 无报错
2. **获取实时行情** → 验证网络连通和股票代码有效
3. **运行分析** → 根据需要选择智能分析、技术指标或综合报告
4. **检查输出** → 所有脚本输出 Markdown 格式，可保存或直接预览

### 使用脚本

从 skill 目录的 `scripts/` 子目录运行：

```bash
# 智能投资分析（推荐起点）
python scripts/analyze_investment.py 002475

# 实时行情
python scripts/get_realtime_quote.py 002475

# 历史K线
python scripts/get_history_kline.py 002475 --days 60

# 技术指标
python scripts/calc_technical.py 002475

# 综合分析报告
python scripts/stock_analyzer.py 002475 -o report.md
```

**验证成功：** 正常输出以 Markdown 表格或标题开头，例如：

```
## 002475 实时行情
| 指标 | 值 |
|------|-----|
| 最新价 | 28.50 |
| 涨跌幅 | +1.23% |
```

## 脚本列表

### 数据获取脚本

| 脚本 | 功能 | 示例 |
|------|------|------|
| `get_realtime_quote.py` | 实时行情 | `python scripts/get_realtime_quote.py 002475` |
| `get_history_kline.py` | 历史K线 | `python scripts/get_history_kline.py 002475 --days 60` |
| `get_valuation.py` | 估值指标 | `python scripts/get_valuation.py 002475` |
| `get_fund_flow.py` | 资金流向 | `python scripts/get_fund_flow.py 002475 --days 10` |
| `get_financial.py` | 财务数据 | `python scripts/get_financial.py 002475` |
| `get_shareholders.py` | 股东信息 | `python scripts/get_shareholders.py 002475` |
| `get_dividend.py` | 分红数据 | `python scripts/get_dividend.py 002475` |

### 分析脚本

| 脚本 | 功能 | 说明 |
|------|------|------|
| `analyze_investment.py` | 智能投资分析 | 多维度评分 + 投资建议 |
| `calc_technical.py` | 技术指标计算 | MA/MACD/RSI/KDJ/BOLL |
| `stock_analyzer.py` | 综合分析报告 | 合并所有数据的完整报告 |

### 工具脚本

| 脚本 | 功能 | 说明 |
|------|------|------|
| `cache_manager.py` | 数据缓存 | SQLite 本地缓存 |
| `scheduler.py` | 定时任务 | 自动获取数据和生成报告 |

## 核心功能

### 1. 智能投资分析

```bash
python scripts/analyze_investment.py 002475
```

自动分析：
- 估值分析（PE/PB/股息率）
- 成长性分析（营收/利润增速）
- 资金面分析（主力资金流向）
- 技术面分析（均线/MACD/RSI）
- 综合评分 + 投资建议

### 2. 技术指标

```bash
python scripts/calc_technical.py 002475
```

支持指标：
- **MA**: 5/10/20/60日均线
- **MACD**: DIF, DEA, MACD柱
- **RSI**: 6/12/24日
- **KDJ**: K, D, J
- **BOLL**: 上轨/中轨/下轨

### 3. 数据缓存

自动缓存避免重复请求：
- 实时行情：1分钟
- 日K线：1小时
- 财务数据：7天
- 股东数据：30天

### 4. 定时任务

```bash
# 立即执行
python scripts/scheduler.py --run-now

# 后台运行调度器
python scripts/scheduler.py
```

配置 `config.yaml` 设置监控股票和执行时间。

## 错误处理

| 场景 | 错误信息 | 解决方法 |
|------|---------|---------|
| 无效股票代码 | `KeyError` 或空 DataFrame | 确认6位数字代码正确（沪市60xxxx，深市00xxxx/30xxxx） |
| 网络超时 | `ConnectionError` / `Timeout` | 检查网络连接，稍后重试；缓存会自动使用上次成功的数据 |
| 非交易时间 | 实时行情返回空或上一交易日数据 | 正常行为——A股交易时间为工作日 9:30-15:00（北京时间） |
| 依赖缺失 | `ModuleNotFoundError` | 运行 `pip install akshare pandas numpy pyyaml` |

## 输出格式

所有脚本默认输出 **Markdown** 格式，可直接预览或保存：

```bash
python scripts/analyze_investment.py 002475 -o 分析报告.md
```

## 参考资源

- [API 参考文档](references/api_reference.md) — 完整的 AKShare 接口映射
- [AKShare 官方文档](references/official_docs.md) — 官方使用指南索引
- **官网**: https://akshare.akfamily.xyz
- **GitHub**: https://github.com/akfamily/akshare
