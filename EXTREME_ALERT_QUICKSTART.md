"""
极值价格提醒系统 - 快速启动指南
"""

# ============================================================================
# 🚀 极值价格提醒系统 - 5分钟快速启动
# ============================================================================

## ⚡ 最快开始方式

### 第1步：确保有数据（如果是第一次）

```bash
# 启动主监控系统抓取数据
python main.py

# 等待至少一次抓取完成（30分钟）
# 或者如果已经有数据，跳过此步
```

### 第2步：运行演示

```bash
# 自动演示所有功能
python extreme_alert_demo.py

# 选择 1 - 自动演示
# 系统会自动展示所有功能
```

### 第3步：查看结果

演示脚本会输出：
- ✅ 24小时极值信息
- ✅ 价格差值计算
- ✅ 触发条件检查
- ✅ 批量检查结果
- ✅ 提醒摘要
- ✅ 格式化消息

**完成！** 🎉

## 📊 核心功能一览

### 功能1：获取24小时极值

```python
extremes = alert_system.get_24h_extremes('AU9999')
# 返回：最高价、最低价、价格范围、数据点数
```

### 功能2：计算价格差值

```python
price_diff = alert_system.calculate_price_difference(382.50, 385.50)
# 返回：绝对差值、百分比差值、是否低于最高价
```

### 功能3：检查触发条件

```python
result = alert_system.check_trigger_condition('AU9999', 382.50)
# 返回：是否需要提醒、提醒等级、触发原因
```

## 🎯 常用命令

| 命令 | 说明 |
|------|------|
| `python extreme_alert_demo.py` | 自动演示 |
| `python extreme_alert_examples.py` | 运行示例 |
| `python test_extreme_alert.py` | 运行测试 |
| `python main_with_extreme_alert.py` | 集成运行 |

## 💡 3个使用场景

### 场景1：我想快速了解功能

```bash
python extreme_alert_demo.py
# 选择 1 - 自动演示
# 5分钟内了解所有功能
```

### 场景2：我想交互式操作

```bash
python extreme_alert_demo.py
# 选择 2 - 交互式模式
# 按照菜单提示操作
```

### 场景3：我想集成到主系统

```bash
python main_with_extreme_alert.py
# 自动抓取数据并检查提醒
```

## 📈 关键参数

### 下跌触发阈值

```python
# 默认值：5%
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

# 修改为3%
alert_system.set_drop_threshold(3.0)

# 推荐值：
# - 保守：10%（只关注大幅下跌）
# - 平衡：5%（一般投资者）
# - 激进：2%（对小幅波动敏感）
```

## ✅ 触发条件

| 条件 | 说明 | 等级 |
|------|------|------|
| 是最低价 | 当前价格是24小时最低价 | HIGH |
| 下跌超过阈值 | 从最高价下跌超过X% | MEDIUM |
| 两个都满足 | 既是最低价又下跌超过阈值 | HIGH |

## 📊 输出示例

### 极值信息

```
品种: AU9999
24小时最高价: 385.50元/克
24小时最低价: 380.20元/克
价格范围: 5.30元/克
数据点数: 48
```

### 提醒信息

```
🔔 价格提醒 - AU9999
当前价格: 380.2元/克
提醒等级: HIGH

极值信息:
  24小时最高价: 385.5元/克
  24小时最低价: 380.2元/克
  价格范围: 5.3元/克

价格差值:
  与最高价差值: 5.3元/克
  下跌百分比: 1.37%

触发原因:
  1. 当前价格 380.2 是24小时最低价
```

## 🔧 配置示例

### 基础配置

```python
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert

db = DatabaseManager('gold_prices.db')
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)
```

### 检查单个品种

```python
result = alert_system.check_trigger_condition('AU9999', 382.50)

if result['should_alert']:
    print(f"需要提醒！等级: {result['alert_level']}")
    for reason in result['alert_reasons']:
        print(f"  - {reason}")
```

### 批量检查

```python
products = ['AU9999', '黄金T+D']
current_prices = {'AU9999': 382.50, '黄金T+D': 385.20}

results = alert_system.batch_check_alerts(products, current_prices)
summary = alert_system.get_alert_summary(results)

print(f"触发提醒: {summary['total_triggered']}")
```

## 🎓 学习路径

### 5分钟快速了解
1. 运行 `python extreme_alert_demo.py`
2. 选择自动演示
3. 查看输出结果

### 15分钟深入学习
1. 阅读 EXTREME_ALERT_QUICK_REFERENCE.md
2. 运行 `python extreme_alert_examples.py`
3. 查看示例代码

### 30分钟完全掌握
1. 阅读 EXTREME_ALERT_GUIDE.md
2. 运行 `python test_extreme_alert.py`
3. 查看源代码注释

## 📁 文件导航

```
核心模块:
  alerts/extreme_price_alert.py

演示脚本:
  extreme_alert_demo.py          # 自动演示 + 交互式
  extreme_alert_examples.py      # 6个实际应用示例
  test_extreme_alert.py          # 完整测试套件
  main_with_extreme_alert.py     # 集成到主系统

文档:
  EXTREME_ALERT_QUICK_REFERENCE.md   # 快速参考
  EXTREME_ALERT_GUIDE.md             # 详细指南
  EXTREME_ALERT_INTEGRATION.md       # 集成指南
  EXTREME_ALERT_SUMMARY.md           # 功能总结
```

## 🚨 常见问题

### Q: 如何开始？
A: 运行 `python extreme_alert_demo.py`

### Q: 如何修改阈值？
A: 使用 `alert_system.set_drop_threshold(3.0)`

### Q: 如何集成到主系统？
A: 运行 `python main_with_extreme_alert.py`

### Q: 如何自定义逻辑？
A: 继承 `ExtremePriceAlert` 类

### Q: 性能如何？
A: 单个品种 < 20ms，批量 < 200ms

## 🎯 下一步

### 立即可做
- [x] 运行演示脚本
- [x] 查看示例代码
- [x] 运行测试脚本

### 可选扩展
- [ ] 集成邮件通知
- [ ] 集成微信通知
- [ ] 自定义触发条件
- [ ] 添加Web界面

## 📞 获取帮助

### 快速参考
- 查看 EXTREME_ALERT_QUICK_REFERENCE.md

### 详细文档
- 查看 EXTREME_ALERT_GUIDE.md

### 集成帮助
- 查看 EXTREME_ALERT_INTEGRATION.md

### 代码示例
- 运行 extreme_alert_examples.py

## 🎉 开始使用

```bash
# 最简单的开始方式
python extreme_alert_demo.py

# 选择 1 - 自动演示
# 5分钟内了解所有功能！
```

---

**快速启动指南版本**: 1.0.0
**最后更新**: 2024-01-15
**状态**: ✅ 可立即使用
"""
