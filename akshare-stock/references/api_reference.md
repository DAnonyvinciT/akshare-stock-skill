# AKShare A股接口参考文档

本文档包含 AKShare 库中常用 A 股数据接口的详细说明。

## 目录

1. [实时行情接口](#1-实时行情接口)
2. [历史K线接口](#2-历史k线接口)
3. [估值指标接口](#3-估值指标接口)
4. [财务报表接口](#4-财务报表接口)
5. [资金流向接口](#5-资金流向接口)
6. [股东信息接口](#6-股东信息接口)
7. [板块数据接口](#7-板块数据接口)
8. [龙虎榜接口](#8-龙虎榜接口)
9. [分红配股接口](#9-分红配股接口)
10. [业绩预告接口](#10-业绩预告接口)

---

## 1. 实时行情接口

### stock_zh_a_spot_em

获取沪深京 A 股实时行情数据。

```python
import akshare as ak
df = ak.stock_zh_a_spot_em()
```

**返回字段**：
| 字段 | 说明 |
|------|------|
| 序号 | 序号 |
| 代码 | 股票代码 |
| 名称 | 股票名称 |
| 最新价 | 当前价格 |
| 涨跌幅 | 涨跌百分比 |
| 涨跌额 | 涨跌金额 |
| 成交量 | 成交量(手) |
| 成交额 | 成交额(元) |
| 振幅 | 振幅百分比 |
| 最高 | 最高价 |
| 最低 | 最低价 |
| 今开 | 今日开盘价 |
| 昨收 | 昨日收盘价 |
| 量比 | 量比 |
| 换手率 | 换手率百分比 |
| 市盈率-动态 | 动态市盈率 |
| 市净率 | 市净率 |
| 总市值 | 总市值(元) |
| 流通市值 | 流通市值(元) |
| 60日涨跌幅 | 60日涨跌幅 |
| 年初至今涨跌幅 | 年初至今涨跌幅 |

### stock_individual_info_em

获取个股基本信息。

```python
df = ak.stock_individual_info_em(symbol="002475")
```

**返回字段**：最新、股票代码、股票简称、总股本、流通股、总市值、流通市值、行业、上市时间

---

## 2. 历史K线接口

### stock_zh_a_hist

获取沪深京 A 股历史行情数据（**最常用接口**）。

```python
df = ak.stock_zh_a_hist(
    symbol="002475",        # 股票代码，不带后缀
    period="daily",         # 周期：daily/weekly/monthly
    start_date="20240101",  # 开始日期
    end_date="20241231",    # 结束日期
    adjust="qfq"            # 复权：qfq前复权/hfq后复权/""不复权
)
```

**参数说明**：
| 参数 | 类型 | 说明 |
|------|------|------|
| symbol | str | 股票代码，如 "002475" |
| period | str | 周期，可选 "daily"、"weekly"、"monthly" |
| start_date | str | 开始日期，格式 YYYYMMDD |
| end_date | str | 结束日期，格式 YYYYMMDD |
| adjust | str | 复权类型，"qfq"前复权、"hfq"后复权、""不复权 |

**返回字段**：日期、股票代码、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率

---

## 3. 估值指标接口

### stock_individual_spot_xq（推荐）

获取雪球个股数据，包含完整的估值指标。

```python
df = ak.stock_individual_spot_xq(symbol="SZ002475")
```

**注意**：symbol 需要带交易所前缀，如 `SZ002475`（深交所）或 `SH600519`（上交所）

**返回字段**：
| 字段 | 说明 |
|------|------|
| 代码 | 股票代码 |
| 名称 | 股票名称 |
| 现价 | 当前价格 |
| 涨幅 | 涨跌幅(%) |
| 市盈率(动) | 动态市盈率 |
| 市盈率(静) | 静态市盈率 |
| 市盈率(TTM) | TTM市盈率 |
| 市净率 | 市净率 |
| 每股收益 | 每股收益 |
| 每股净资产 | 每股净资产 |
| 股息(TTM) | TTM股息 |
| 股息率(TTM) | TTM股息率(%) |
| 52周最高 | 52周最高价 |
| 52周最低 | 52周最低价 |
| 今年以来涨幅 | 年初至今涨跌幅 |

### stock_zh_valuation_baidu

获取百度股市通估值数据（历史估值）。

```python
df = ak.stock_zh_valuation_baidu(symbol="002475", indicator="总市值")
```

**indicator 可选值**："总市值"、"市盈率"、"市净率"、"市销率"

---

## 4. 财务报表接口

**注意**：财务接口的 symbol 格式为 `SZ002475` 或 `SH600519`（交易所前缀+代码）

### stock_financial_analysis_indicator

获取财务分析指标。

```python
df = ak.stock_financial_analysis_indicator(symbol="SZ002475")
```

**主要返回字段**：
- 日期（报告期）
- 摊薄净资产收益率
- 加权净资产收益率
- 摊薄每股收益(元)
- 每股净资产_调整后(元)
- 每股经营性现金流(元)
- 销售毛利率(%)
- 销售净利率(%)
- 资产负债率(%)

### stock_balance_sheet_by_report_em

资产负债表-按报告期。

```python
df = ak.stock_balance_sheet_by_report_em(symbol="SZ002475")
```

### stock_profit_sheet_by_report_em

利润表-按报告期。

```python
df = ak.stock_profit_sheet_by_report_em(symbol="SZ002475")
```

### stock_cash_flow_sheet_by_report_em

现金流量表-按报告期。

```python
df = ak.stock_cash_flow_sheet_by_report_em(symbol="SZ002475")
```

---

## 5. 资金流向接口

### stock_individual_fund_flow

获取个股资金流向。

```python
df = ak.stock_individual_fund_flow(stock="002475", market="sz")
```

**参数说明**：
| 参数 | 说明 |
|------|------|
| stock | 股票代码（纯数字） |
| market | 市场，"sh"上海/"sz"深圳 |

**返回字段**：日期、收盘价、涨跌幅、主力净流入-净额、主力净流入-净占比、超大单净流入、大单净流入、中单净流入、小单净流入

### stock_individual_fund_flow_rank

资金流向排名。

```python
df = ak.stock_individual_fund_flow_rank(indicator="今日")
```

**indicator 可选值**："今日"、"3日"、"5日"、"10日"

### stock_market_fund_flow

大盘资金流向。

```python
df = ak.stock_market_fund_flow()
```

---

## 6. 股东信息接口

### stock_main_stock_holder（推荐）

获取主要股东（十大股东）信息。

```python
df = ak.stock_main_stock_holder(stock="002475")
```

**返回字段**：编号、股东名称、持股数量、持股比例、股本性质、截至日期、公告日期、股东总数、平均持股数

### stock_circulate_stock_holder

获取流通股东信息。

```python
df = ak.stock_circulate_stock_holder(symbol="002475")
```

---

## 7. 板块数据接口

### stock_board_industry_name_em

获取行业板块名称列表。

```python
df = ak.stock_board_industry_name_em()
```

### stock_board_industry_cons_em

获取行业板块成份股。

```python
df = ak.stock_board_industry_cons_em(symbol="消费电子")
```

### stock_board_concept_name_em

获取概念板块名称列表。

```python
df = ak.stock_board_concept_name_em()
```

### stock_board_concept_cons_em

获取概念板块成份股。

```python
df = ak.stock_board_concept_cons_em(symbol="锂电池")
```

---

## 8. 龙虎榜接口

### stock_lhb_detail_em

龙虎榜详情数据。

```python
df = ak.stock_lhb_detail_em(start_date="20241201", end_date="20241215")
```

### stock_lhb_jgmmtj_em

机构买卖每日统计。

```python
df = ak.stock_lhb_jgmmtj_em(start_date="20241201")
```

---

## 9. 分红配股接口

### stock_history_dividend_detail

历史分红明细。

```python
df = ak.stock_history_dividend_detail(symbol="002475", indicator="分红")
```

**indicator 可选值**："分红"、"配股"

**返回字段**：公告日期、送股、转增、派息、进度、除权除息日、股权登记日、红股上市日

### stock_history_dividend

全市场分红统计。

```python
df = ak.stock_history_dividend()
```

**返回字段**：代码、名称、上市日期、累计股息、年均股息、分红次数、融资总额、融资次数

---

## 10. 业绩预告接口

### stock_yjyg_em

业绩预告。

```python
df = ak.stock_yjyg_em(date="20241231")
```

### stock_yjkb_em

业绩快报。

```python
df = ak.stock_yjkb_em(date="20241231")
```

### stock_yjbb_em

业绩报表。

```python
df = ak.stock_yjbb_em(date="20241231")
```

---

## 常见问题

### 1. 股票代码格式问题

不同接口对股票代码格式要求不同：
- 行情类接口：使用纯数字，如 `"002475"`
- 财务、雪球接口：使用交易所前缀，如 `"SZ002475"` 或 `"SH600519"`

### 2. 日期格式

统一使用 `YYYYMMDD` 格式，如 `"20241231"`

### 3. 接口限流

AKShare 会对频繁请求进行限流，建议：
- 批量获取时增加延时：`time.sleep(0.5)`
- 使用缓存避免重复请求

### 4. 数据更新时间

- 实时行情：交易时间实时更新
- 历史K线：收盘后更新
- 财务数据：披露后更新

### 5. 已废弃接口

以下接口已不可用，请使用替代方案：
- ~~`stock_a_indicator_lg`~~ → 使用 `stock_individual_spot_xq`
- ~~`stock_gdfx_free_top_10_em`~~ → 使用 `stock_main_stock_holder`
