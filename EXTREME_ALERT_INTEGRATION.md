"""
极值价格提醒系统 - 集成指南
"""

# ============================================================================
# 极值价格提醒系统 - 完整集成指南
# ============================================================================

## 📋 集成概述

本指南说明如何将极值价格提醒系统集成到现有的金价监控系统中。

### 集成方式

1. **方式A**: 独立运行（推荐用于测试）
2. **方式B**: 集成到主监控系统（推荐用于生产）
3. **方式C**: 自定义集成（高级用户）

## 🚀 方式A: 独立运行

### 步骤1: 准备环境

```bash
# 确保数据库中有数据
python main.py
# 等待至少一次抓取完成（30分钟）
```

### 步骤2: 运行演示

```bash
# 自动演示所有功能
python extreme_alert_demo.py

# 或交互式模式
python extreme_alert_demo.py
# 选择 2 - 交互式模式
```

### 步骤3: 查看结果

演示脚本会输出：
- 24小时极值信息
- 价格差值计算
- 触发条件检查
- 批量检查结果
- 提醒摘要
- 格式化消息

## 🔗 方式B: 集成到主监控系统

### 步骤1: 修改主程序

**选项1**: 使用现成的集成脚本

```bash
# 直接运行集成版本
python main_with_extreme_alert.py
```

**选项2**: 手动集成到 main.py

编辑 `main.py`，在导入部分添加：

```python
from alerts.extreme_price_alert import ExtremePriceAlert
```

在主循环中添加极值检查：

```python
# 初始化极值提醒系统
extreme_alert = ExtremePriceAlert(db, drop_threshold_percent=5.0)

# 在数据保存后添加
if saved_count > 0:
    # 检查极值提醒
    current_prices = {item['name']: item['price'] for item in gold_data}
    products = list(current_prices.keys())

    alert_results = extreme_alert.batch_check_alerts(products, current_prices)

    # 处理触发的提醒
    for result in alert_results:
        if result['should_alert']:
            message = extreme_alert.format_alert_message(result)
            logger.warning(message)
            # 发送通知
```

### 步骤2: 配置参数

在 `config/settings.py` 中添加：

```python
# 极值提醒配置
EXTREME_ALERT_ENABLED = True
EXTREME_ALERT_DROP_THRESHOLD = 5.0  # 下跌阈值（%）
```

### 步骤3: 启动系统

```bash
python main.py
# 或
python main_with_extreme_alert.py
```

### 步骤4: 监控输出

系统会输出：
- 数据抓取信息
- 极值检查结果
- 触发的提醒信息
- 提醒统计

## 🛠️ 方式C: 自定义集成

### 步骤1: 创建自定义类

```python
from alerts.extreme_price_alert import ExtremePriceAlert

class CustomPriceAlert(ExtremePriceAlert):
    """自定义极值提醒系统"""

    def check_trigger_condition(self, product_name, current_price):
        # 调用父类方法
        result = super().check_trigger_condition(product_name, current_price)

        # 添加自定义条件
        # 例如：特定时间段的提醒
        if self._is_trading_hours():
            result['alert_level'] = 'high'

        return result

    def _is_trading_hours(self):
        """检查是否在交易时间"""
        from datetime import datetime
        hour = datetime.now().hour
        return 9 <= hour <= 16
```

### 步骤2: 使用自定义类

```python
# 使用自定义类
alert_system = CustomPriceAlert(db, drop_threshold_percent=5.0)

# 其他使用方式相同
result = alert_system.check_trigger_condition('AU9999', 382.50)
```

### 步骤3: 添加通知功能

```python
def send_notification(alert_result):
    """发送通知"""
    if not alert_result['should_alert']:
        return

    message = alert_system.format_alert_message(alert_result)

    # 邮件通知
    send_email(
        to='user@example.com',
        subject=f"金价提醒 - {alert_result['product_name']}",
        body=message
    )

    # 微信通知
    send_wechat(message)

    # 钉钉通知
    send_dingtalk(message)
```

## 📊 集成架构

```
┌─────────────────────────────────────┐
│      主监控系统 (main.py)            │
├─────────────────────────────────────┤
│  1. 获取金价数据                     │
│  2. 保存到数据库                     │
│  3. 检查极值提醒 ← 新增              │
│  4. 发送通知 ← 新增                  │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│   极值提醒系统                       │
│  (ExtremePriceAlert)                │
├─────────────────────────────────────┤
│  • 极值计算                          │
│  • 差值计算                          │
│  • 触发判断                          │
│  • 消息格式化                        │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│   通知系统                           │
├─────────────────────────────────────┤
│  • 邮件通知                          │
│  • 微信通知                          │
│  • 钉钉通知                          │
│  • 日志记录                          │
└─────────────────────────────────────┘
```

## 🔧 配置选项

### 基础配置

```python
# 初始化极值提醒系统
alert_system = ExtremePriceAlert(
    db=db_manager,
    drop_threshold_percent=5.0  # 下跌阈值
)
```

### 高级配置

```python
# 创建配置字典
alert_config = {
    'enabled': True,
    'drop_threshold': 5.0,
    'check_interval': 1800,  # 检查间隔（秒）
    'notification_channels': ['email', 'wechat', 'dingtalk'],
    'alert_levels': {
        'high': {'send_immediately': True},
        'medium': {'send_immediately': False},
        'low': {'send_immediately': False}
    }
}

# 使用配置
alert_system = ExtremePriceAlert(db, alert_config['drop_threshold'])
```

## 📝 集成检查清单

### 前置条件
- [ ] 数据库中有24小时内的数据
- [ ] 已安装所有依赖包
- [ ] 配置文件已正确设置

### 集成步骤
- [ ] 导入 ExtremePriceAlert 类
- [ ] 初始化提醒系统
- [ ] 在主循环中添加检查逻辑
- [ ] 配置通知方式
- [ ] 测试提醒功能

### 测试验证
- [ ] 运行演示脚本验证功能
- [ ] 运行测试脚本验证正确性
- [ ] 检查日志输出
- [ ] 验证通知发送

### 生产部署
- [ ] 配置合适的下跌阈值
- [ ] 设置通知接收人
- [ ] 配置日志轮转
- [ ] 设置监控告警

## 🎯 集成示例

### 示例1: 基础集成

```python
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert
from scrapers.api_scraper import GoldAPIScraper

# 初始化
db = DatabaseManager('gold_prices.db')
scraper = GoldAPIScraper(API_KEY)
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

# 主循环
while True:
    # 获取数据
    gold_data = scraper.fetch_shanghai_gold()

    if gold_data:
        # 保存数据
        db.save_prices_batch(gold_data)

        # 检查提醒
        current_prices = {item['name']: item['price'] for item in gold_data}
        results = alert_system.batch_check_alerts(
            list(current_prices.keys()),
            current_prices
        )

        # 处理提醒
        for result in results:
            if result['should_alert']:
                print(alert_system.format_alert_message(result))

    time.sleep(1800)  # 30分钟
```

### 示例2: 带通知的集成

```python
def send_notification(alert_result):
    """发送通知"""
    message = alert_system.format_alert_message(alert_result)

    # 邮件
    if alert_result['alert_level'] == 'high':
        send_email(message)

    # 微信
    send_wechat(message)

    # 日志
    logger.warning(message)

# 在主循环中
for result in results:
    if result['should_alert']:
        send_notification(result)
```

### 示例3: 带配置的集成

```python
# 配置文件
ALERT_CONFIG = {
    'enabled': True,
    'drop_threshold': 5.0,
    'notification': {
        'email': True,
        'wechat': True,
        'dingtalk': False
    }
}

# 使用配置
if ALERT_CONFIG['enabled']:
    alert_system = ExtremePriceAlert(
        db,
        drop_threshold_percent=ALERT_CONFIG['drop_threshold']
    )

    # 检查并通知
    for result in results:
        if result['should_alert']:
            if ALERT_CONFIG['notification']['email']:
                send_email(result)
            if ALERT_CONFIG['notification']['wechat']:
                send_wechat(result)
```

## 🔍 集成验证

### 验证步骤1: 功能验证

```bash
# 运行测试脚本
python test_extreme_alert.py

# 预期输出: ✅ 所有测试通过
```

### 验证步骤2: 集成验证

```bash
# 运行集成脚本
python main_with_extreme_alert.py

# 预期输出:
# - 数据抓取成功
# - 极值检查完成
# - 提醒信息输出
```

### 验证步骤3: 性能验证

```bash
# 检查性能指标
# - 单个品种检查 < 20ms
# - 批量检查 < 200ms
# - 内存占用 < 100MB
```

## 📊 监控指标

### 关键指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 检查成功率 | > 99% | 提醒检查成功率 |
| 平均响应时间 | < 20ms | 单个品种检查时间 |
| 内存占用 | < 100MB | 系统内存使用 |
| 数据准确率 | 100% | 极值计算准确率 |

### 监控命令

```bash
# 查看系统状态
python check_status.py

# 查看数据库统计
python query_tool.py
# 选择 4 - 查看数据库统计

# 查看日志
tail -f gold_monitor.log
```

## 🐛 故障排查

### 问题1: 提醒不工作

**检查清单**:
1. 数据库中是否有数据
2. 极值提醒系统是否初始化
3. 检查日志是否有错误

**解决方案**:
```bash
# 运行测试
python test_extreme_alert.py

# 查看日志
tail -f gold_monitor.log

# 手动检查
python extreme_alert_demo.py
```

### 问题2: 性能下降

**检查清单**:
1. 数据库大小是否过大
2. 是否有其他进程占用资源
3. 网络连接是否正常

**解决方案**:
```python
# 清理旧数据
db.cleanup_old_data(days=30)

# 重建索引
import sqlite3
conn = sqlite3.connect('gold_prices.db')
cursor = conn.cursor()
cursor.execute('REINDEX')
conn.commit()
conn.close()
```

### 问题3: 通知未发送

**检查清单**:
1. 通知配置是否正确
2. 网络连接是否正常
3. 通知服务是否可用

**解决方案**:
```python
# 测试邮件
send_email("test@example.com", "测试", "测试消息")

# 测试微信
send_wechat("测试消息")

# 查看日志
grep "notification" gold_monitor.log
```

## 📚 相关文档

- **快速参考**: EXTREME_ALERT_QUICK_REFERENCE.md
- **详细指南**: EXTREME_ALERT_GUIDE.md
- **功能总结**: EXTREME_ALERT_SUMMARY.md
- **项目说明**: README.md

## 🎓 学习资源

### 初级
1. 阅读本集成指南
2. 运行演示脚本
3. 查看示例代码

### 中级
1. 运行集成脚本
2. 修改配置参数
3. 添加通知功能

### 高级
1. 自定义提醒类
2. 实现自定义逻辑
3. 优化性能

## 🎉 集成完成

完成以上步骤后，你的系统将具有：

✅ 自动极值计算
✅ 智能触发判断
✅ 灵活的阈值配置
✅ 完整的提醒通知
✅ 详细的日志记录
✅ 高效的性能表现

---

**集成指南版本**: 1.0.0
**最后更新**: 2024-01-15
"""
