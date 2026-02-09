"""
极值价格提醒 - 快速参考指南
"""

# ============================================================================
# 极值价格提醒系统 - 快速参考
# ============================================================================

## 📋 核心概念

### 三大核心功能

1. **极值计算** - 获取过去24小时的最高价和最低价
2. **差值计算** - 计算当前价格与最高价的差值
3. **触发判断** - 根据条件判断是否需要发送提醒

### 触发条件

| 条件 | 说明 | 提醒等级 |
|------|------|---------|
| 条件1 | 当前价格是24小时最低价 | HIGH |
| 条件2 | 价格下跌超过阈值(默认5%) | MEDIUM |
| 两个都满足 | 同时满足两个条件 | HIGH |

## 🚀 快速开始

### 方式1: 自动演示（推荐新手）

```bash
python extreme_alert_demo.py
# 选择 1 - 自动演示
```

### 方式2: 交互式模式

```bash
python extreme_alert_demo.py
# 选择 2 - 交互式模式
```

### 方式3: 运行示例

```bash
python extreme_alert_examples.py
```

### 方式4: 运行测试

```bash
python test_extreme_alert.py
```

### 方式5: 集成到主系统

```bash
python main_with_extreme_alert.py
```

## 💻 代码示例

### 基本使用

```python
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert

# 初始化
db = DatabaseManager('gold_prices.db')
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

# 检查单个品种
result = alert_system.check_trigger_condition('AU9999', 382.50)

# 输出结果
if result['should_alert']:
    print(f"需要提醒！等级: {result['alert_level']}")
    print(f"原因: {result['alert_reasons']}")
```

### 获取24小时极值

```python
# 获取极值
extremes = alert_system.get_24h_extremes('AU9999')

print(f"最高价: {extremes['highest_price_24h']}")
print(f"最低价: {extremes['lowest_price_24h']}")
print(f"范围: {extremes['price_range']}")
```

### 计算价格差值

```python
# 计算差值
price_diff = alert_system.calculate_price_difference(382.50, 385.50)

print(f"绝对差值: {price_diff['absolute_difference']}元/克")
print(f"百分比差值: {price_diff['percentage_difference']}%")
```

### 批量检查

```python
# 准备数据
products = ['AU9999', '黄金T+D']
current_prices = {'AU9999': 382.50, '黄金T+D': 385.20}

# 批量检查
results = alert_system.batch_check_alerts(products, current_prices)

# 获取摘要
summary = alert_system.get_alert_summary(results)
print(f"触发提醒: {summary['total_triggered']}")
```

### 修改阈值

```python
# 设置新阈值
alert_system.set_drop_threshold(3.0)  # 改为3%

# 获取当前阈值
threshold = alert_system.get_drop_threshold()
```

### 格式化消息

```python
# 生成提醒消息
message = alert_system.format_alert_message(result)
print(message)
```

## 📊 返回值说明

### check_trigger_condition() 返回值

```python
{
    'product_name': 'AU9999',           # 品种名称
    'current_price': 382.50,            # 当前价格
    'should_alert': True,               # 是否需要提醒
    'alert_reasons': [...],             # 触发原因列表
    'extremes': {...},                  # 24小时极值信息
    'price_diff': {...},                # 价格差值信息
    'alert_level': 'high',              # 提醒等级
    'timestamp': '2024-01-15T10:30:00'  # 时间戳
}
```

### get_24h_extremes() 返回值

```python
{
    'product_name': 'AU9999',
    'highest_price_24h': 385.50,
    'lowest_price_24h': 380.20,
    'price_range': 5.30,
    'data_points': 48,
    'time_range': '24小时',
    'timestamp': '2024-01-15T10:30:00'
}
```

### calculate_price_difference() 返回值

```python
{
    'current_price': 382.50,
    'highest_price_24h': 385.50,
    'absolute_difference': 3.00,
    'percentage_difference': 0.78,
    'is_below_highest': True
}
```

## ⚙️ 配置参数

### 初始化参数

```python
# 默认配置
alert_system = ExtremePriceAlert(db)

# 自定义下跌阈值
alert_system = ExtremePriceAlert(db, drop_threshold_percent=3.0)
```

### 推荐阈值

| 策略 | 阈值 | 适用场景 |
|------|------|---------|
| 保守 | 10% | 只关注大幅下跌 |
| 平衡 | 5% | 一般投资者（默认） |
| 激进 | 2% | 对小幅波动敏感 |

## 📁 文件清单

| 文件 | 说明 |
|------|------|
| alerts/extreme_price_alert.py | 核心模块 |
| extreme_alert_demo.py | 演示脚本 |
| extreme_alert_examples.py | 使用示例 |
| test_extreme_alert.py | 测试脚本 |
| main_with_extreme_alert.py | 集成脚本 |
| EXTREME_ALERT_GUIDE.md | 详细文档 |

## 🔍 常见操作

### 查看24小时极值

```bash
python extreme_alert_demo.py
# 选择 1 - 自动演示
# 查看演示1的输出
```

### 检查单个品种

```bash
python extreme_alert_demo.py
# 选择 2 - 交互式模式
# 选择 2 - 检查触发条件
```

### 批量检查所有品种

```bash
python extreme_alert_demo.py
# 选择 2 - 交互式模式
# 选择 4 - 批量检查所有品种
```

### 修改下跌阈值

```bash
python extreme_alert_demo.py
# 选择 2 - 交互式模式
# 选择 3 - 修改下跌阈值
```

### 运行完整测试

```bash
python test_extreme_alert.py
```

## 🎯 使用场景

### 场景1: 监控单个品种

```python
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)
result = alert_system.check_trigger_condition('AU9999', current_price)

if result['should_alert']:
    send_notification(result)
```

### 场景2: 监控多个品种

```python
products = ['AU9999', '黄金T+D', '黄金延期']
current_prices = {...}

results = alert_system.batch_check_alerts(products, current_prices)
for result in results:
    if result['should_alert']:
        send_notification(result)
```

### 场景3: 定时监控

```python
# 在主监控循环中
while True:
    # 获取最新数据
    gold_data = scraper.fetch_shanghai_gold()

    # 检查极值提醒
    for item in gold_data:
        result = alert_system.check_trigger_condition(
            item['name'],
            item['price']
        )

        if result['should_alert']:
            send_notification(result)

    time.sleep(FETCH_INTERVAL)
```

## 📞 故障排查

### 问题1: 没有检测到提醒

**检查清单**:
1. 数据库中是否有24小时内的数据
2. 当前价格是否真的满足触发条件
3. 下跌阈值是否设置过高

**解决方案**:
```python
# 检查数据
extremes = alert_system.get_24h_extremes('AU9999')
print(f"最高价: {extremes['highest_price_24h']}")
print(f"最低价: {extremes['lowest_price_24h']}")

# 检查阈值
print(f"当前阈值: {alert_system.get_drop_threshold()}%")

# 降低阈值重试
alert_system.set_drop_threshold(2.0)
```

### 问题2: 提醒过于频繁

**解决方案**:
```python
# 提高阈值
alert_system.set_drop_threshold(10.0)
```

### 问题3: 数据库中没有数据

**解决方案**:
```bash
# 先运行主程序抓取数据
python main.py

# 等待至少一次抓取完成（30分钟）
# 然后再运行极值提醒系统
```

## 📈 性能指标

| 操作 | 耗时 |
|------|------|
| 获取24小时极值 | < 10ms |
| 计算价格差值 | < 1ms |
| 检查单个品种 | < 20ms |
| 批量检查10个品种 | < 200ms |

## 🔗 相关文档

- **详细文档**: EXTREME_ALERT_GUIDE.md
- **项目说明**: README.md
- **快速开始**: QUICKSTART.md
- **完整手册**: COMPLETE_MANUAL.md

## 💡 提示

1. **首次使用**: 先运行演示脚本了解功能
2. **生产环境**: 使用 main_with_extreme_alert.py
3. **自定义**: 继承 ExtremePriceAlert 类实现自定义逻辑
4. **集成**: 使用 format_alert_message() 生成通知消息

## 🎓 学习路径

1. **初级**: 运行演示脚本 → 理解基本概念
2. **中级**: 运行示例脚本 → 学习代码用法
3. **高级**: 阅读源代码 → 自定义实现

---

**快速参考版本**: 1.0.0
**最后更新**: 2024-01-15
"""
