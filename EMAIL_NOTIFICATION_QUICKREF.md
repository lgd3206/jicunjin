"""
邮件通知系统 - 快速参考指南
"""

# ============================================================================
# 📧 邮件通知系统 - 快速参考指南
# ============================================================================

## 🚀 5分钟快速开始

### 1. 复制配置文件
```bash
cp .env.example .env
```

### 2. 编辑 .env 文件
```env
EMAIL_TYPE=qq
EMAIL_ADDRESS=your_email@qq.com
APP_PASSWORD=your_app_password_here
RECIPIENT_EMAILS=recipient1@qq.com,recipient2@163.com
```

### 3. 测试连接
```bash
python test_email_notification.py
```

### 4. 发送测试邮件
```bash
python email_alert_integration.py
```

---

## 📚 常用代码片段

### 初始化邮件系统
```python
from email_alert_integration import EmailAlertIntegration

integration = EmailAlertIntegration('.env')
```

### 发送单个提醒
```python
alert_result = {
    'product_name': 'AU9999',
    'current_price': 380.20,
    'should_alert': True,
    'alert_level': 'high',
    'alert_reasons': ['当前价格是24小时最低价'],
    'extremes': {...},
    'price_diff': {...},
    'timestamp': '2024-01-15T10:30:00'
}

results = integration.send_alert_emails(alert_result)
```

### 批量发送提醒
```python
alert_results = [
    {...},  # 提醒1
    {...},  # 提醒2
    {...},  # 提醒3
]

all_results = integration.send_batch_alerts(alert_results)
```

### 测试邮件连接
```python
if integration.test_email_connection():
    print("连接成功！")
else:
    print("连接失败！")
```

### 获取配置信息
```python
config = integration.config
print(f"收件人: {config['recipients']}")
print(f"下跌阈值: {config['alert']['drop_threshold_percent']}%")
```

---

## 🔧 配置参数详解

| 参数 | 说明 | 示例 |
|------|------|------|
| EMAIL_TYPE | 邮箱类型 (qq/163) | qq |
| EMAIL_ADDRESS | 发件人邮箱 | your_email@qq.com |
| APP_PASSWORD | 应用授权码 | abcdefghijklmnop |
| RECIPIENT_EMAILS | 收件人邮箱 (逗号分隔) | recipient1@qq.com,recipient2@163.com |
| DROP_THRESHOLD_PERCENT | 下跌阈值 (%) | 5.0 |
| ENABLE_EMAIL_NOTIFICATION | 是否启用邮件 | true/false |
| TEST_MODE | 测试模式 | true/false |
| DATABASE_PATH | 数据库路径 | gold_prices.db |
| LOG_LEVEL | 日志级别 | INFO/DEBUG/WARNING/ERROR |
| LOG_FILE | 日志文件路径 | logs/notifications.log |

---

## 📧 邮件模板信息

邮件包含以下信息：

```
主题: 🔔 AU9999金价提醒 - HIGH

内容:
├── 当前金价: 380.20 元/克
├── 24小时最高价: 385.50 元/克
├── 24小时最低价: 380.20 元/克
├── 价格范围: 5.30 元/克
├── 与最高价差值: 5.30 元/克 (1.38%)
├── 发送时间: 2024-01-15 10:30:00
├── 触发原因:
│   ✓ 当前价格是24小时最低价
│   ✓ 价格下跌超过5%
└── 微信接收提示
```

---

## 🐛 常见错误及解决方案

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| FileNotFoundError: .env | 配置文件不存在 | 运行 `cp .env.example .env` |
| 邮箱认证失败 | 授权码错误 | 检查 APP_PASSWORD 是否正确 |
| SMTP连接失败 | 网络问题 | 检查网络连接和防火墙 |
| 邮件发送失败 | 收件人地址错误 | 检查 RECIPIENT_EMAILS 格式 |
| 日志文件无法写入 | 权限问题 | 检查 logs/ 目录权限 |

---

## 📁 文件结构

```
notifications/
├── __init__.py
└── email_notifier.py              # 邮件通知器

config/
├── __init__.py
└── config_loader.py               # 配置加载器

email_alert_integration.py          # 集成脚本
test_email_notification.py          # 测试脚本
email_notification_examples.py      # 示例脚本
.env.example                        # 配置模板
.env                               # 配置文件（自己创建）
EMAIL_NOTIFICATION_GUIDE.md         # 完整指南
EMAIL_NOTIFICATION_QUICKREF.md      # 快速参考
```

---

## 🔗 相关文档

- **EMAIL_NOTIFICATION_GUIDE.md** - 完整使用指南
- **EMAIL_NOTIFICATION_QUICKREF.md** - 快速参考（本文件）
- **README_EXTREME_ALERT.md** - 极值提醒系统说明
- **EXTREME_ALERT_INTEGRATION.md** - 集成指南

---

## 💡 最佳实践

### 1. 安全性
- ✅ 使用 .env 文件存储敏感信息
- ✅ 不要在代码中硬编码密码
- ✅ 定期更新授权码
- ✅ 限制 .env 文件的访问权限

### 2. 可靠性
- ✅ 使用测试模式验证配置
- ✅ 定期测试邮件连接
- ✅ 检查日志文件查看错误
- ✅ 实现重试机制

### 3. 性能
- ✅ 使用批量发送而不是逐个发送
- ✅ 异步处理邮件发送
- ✅ 缓存配置信息
- ✅ 定期清理日志文件

### 4. 维护
- ✅ 记录详细的日志
- ✅ 监控邮件发送状态
- ✅ 定期备份配置文件
- ✅ 文档化自定义配置

---

## 🎯 使用场景

### 场景 1: 单个品种监控
```python
# 监控 AU9999，当价格下跌时发送邮件
result = alert_system.check_trigger_condition('AU9999', 380.20)
if result['should_alert']:
    integration.send_alert_emails(result)
```

### 场景 2: 多品种监控
```python
# 监控多个品种，批量发送提醒
products = ['AU9999', 'AU100G', 'AU50G']
prices = [380.20, 3800.00, 1900.00]
results = alert_system.batch_check_alerts(products, prices)
integration.send_batch_alerts(results)
```

### 场景 3: 定时监控
```python
# 每30分钟检查一次，有提醒时发送邮件
import time
while True:
    # 获取最新价格
    prices = scraper.fetch_prices()

    # 检查提醒
    results = alert_system.batch_check_alerts(products, prices)

    # 发送邮件
    integration.send_batch_alerts(results)

    # 等待30分钟
    time.sleep(1800)
```

---

## 📞 获取帮助

### 查看日志
```bash
tail -f logs/notifications.log
```

### 运行测试
```bash
python test_email_notification.py
```

### 查看示例
```bash
python email_notification_examples.py
```

### 查看配置
```bash
cat .env
```

---

## ✅ 检查清单

- [ ] 复制 .env.example 为 .env
- [ ] 获取邮箱授权码
- [ ] 填写 .env 文件
- [ ] 运行测试脚本
- [ ] 测试邮件连接
- [ ] 发送测试邮件
- [ ] 检查邮件是否收到
- [ ] 配置收件人列表
- [ ] 集成到主系统
- [ ] 部署到生产环境

---

**邮件通知系统快速参考完成！** 📧
"""
