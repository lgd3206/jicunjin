"""
邮件通知系统 - 使用指南
"""

# ============================================================================
# 📧 邮件通知系统 - 完整使用指南
# ============================================================================

## 📋 目录

1. [系统概述](#系统概述)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [功能详解](#功能详解)
5. [集成示例](#集成示例)
6. [常见问题](#常见问题)
7. [故障排查](#故障排查)

---

## 系统概述

### 功能特性

✅ **多邮箱支持**
- QQ邮箱 (smtp.qq.com:587)
- 163邮箱 (smtp.163.com:587)
- 易于扩展支持其他邮箱

✅ **专业邮件模板**
- HTML格式，美观专业
- 包含所有关键信息：品种、价格、极值、差值、时间
- 响应式设计，支持各种邮件客户端

✅ **灵活配置**
- 使用 .env 文件管理配置
- 支持多收件人
- 可配置的提醒阈值
- 测试模式支持

✅ **完整集成**
- 与极值提醒系统无缝集成
- 支持批量发送
- 详细的日志记录

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   极值价格提醒系统                        │
│              (ExtremePriceAlert)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   邮件提醒集成                            │
│            (EmailAlertIntegration)                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ 配置   │  │ 邮件   │  │ 日志   │
    │ 加载器 │  │ 通知器 │  │ 系统   │
    │ Config │  │ Email  │  │ Logger │
    │Loader  │  │Notifier│  │        │
    └────────┘  └────────┘  └────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   SMTP服务器    │
            │  (QQ/163邮箱)   │
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   收件人邮箱    │
            │  (多个收件人)   │
            └─────────────────┘
```

---

## 快速开始

### 1. 准备工作

#### 获取QQ邮箱授权码

1. 登录 QQ邮箱 (https://mail.qq.com)
2. 点击"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 点击"生成授权码"
5. 按照提示完成验证，复制授权码

#### 获取163邮箱授权码

1. 登录 163邮箱 (https://mail.163.com)
2. 点击"设置" → "POP3/SMTP/IMAP"
3. 点击"开启"
4. 按照提示完成验证，获取授权码

### 2. 配置文件

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的邮箱信息：

```env
# 邮箱配置
EMAIL_TYPE=qq
EMAIL_ADDRESS=your_email@qq.com
APP_PASSWORD=your_app_password_here

# 收件人配置
RECIPIENT_EMAILS=recipient1@qq.com,recipient2@163.com

# 提醒配置
DROP_THRESHOLD_PERCENT=5.0
ENABLE_EMAIL_NOTIFICATION=true
TEST_MODE=false

# 数据库配置
DATABASE_PATH=gold_prices.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/notifications.log
```

### 3. 测试连接

运行测试脚本验证配置：

```bash
python test_email_notification.py
```

预期输出：

```
============================================================
邮件通知系统 - 完整测试套件
============================================================

============================================================
测试 1: 配置加载器
============================================================
✓ 配置加载成功

邮件配置:
  - 邮箱类型: QQ
  - 邮箱地址: your_email@qq.com

...

🎉 所有测试通过！
```

### 4. 发送测试邮件

运行集成脚本发送测试邮件：

```bash
python email_alert_integration.py
```

---

## 配置说明

### .env 文件详解

#### 邮箱配置

```env
# 邮箱类型: 'qq' 或 '163'
EMAIL_TYPE=qq

# 邮箱地址
EMAIL_ADDRESS=your_email@qq.com

# 应用授权码（不是邮箱密码！）
APP_PASSWORD=your_app_password_here
```

**重要提示**：
- `APP_PASSWORD` 是应用授权码，不是邮箱密码
- 获取方式见上面的"快速开始"部分
- 不要在代码中硬编码密码

#### 收件人配置

```env
# 主要收件人邮箱（多个邮箱用逗号分隔）
RECIPIENT_EMAILS=recipient1@qq.com,recipient2@163.com
```

**支持多个收件人**：
- 用逗号分隔多个邮箱
- 每个邮箱会收到相同的提醒邮件
- 支持任何邮箱类型（QQ、163、Gmail等）

#### 提醒配置

```env
# 价格下跌阈值（百分比，默认5%）
DROP_THRESHOLD_PERCENT=5.0

# 是否启用邮件通知
ENABLE_EMAIL_NOTIFICATION=true

# 是否启用测试模式（测试模式下不会真正发送邮件）
TEST_MODE=false
```

**测试模式说明**：
- 设置 `TEST_MODE=true` 时，系统会模拟发送邮件但不真正发送
- 用于测试配置和流程，不会消耗邮件配额
- 生产环境应设置为 `false`

#### 数据库配置

```env
# SQLite 数据库路径
DATABASE_PATH=gold_prices.db
```

#### 日志配置

```env
# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# 日志文件路径
LOG_FILE=logs/notifications.log
```

---

## 功能详解

### 1. 配置加载器 (ConfigLoader)

**位置**: `config/config_loader.py`

**主要方法**:

```python
# 初始化
config_loader = ConfigLoader('.env')

# 获取邮件配置
email_config = config_loader.get_email_config()
# 返回: {'email_type': 'qq', 'email_address': '...', 'app_password': '...'}

# 获取收件人列表
recipients = config_loader.get_recipient_emails()
# 返回: ['recipient1@qq.com', 'recipient2@163.com']

# 获取提醒配置
alert_config = config_loader.get_alert_config()
# 返回: {'drop_threshold_percent': 5.0, 'enable_email_notification': True, ...}

# 验证配置
config_loader.validate_email_config()  # 验证邮件配置
config_loader.validate_recipient_emails()  # 验证收件人配置
```

### 2. 邮件通知器 (EmailNotifier)

**位置**: `notifications/email_notifier.py`

**主要方法**:

```python
# 初始化
notifier = EmailNotifier(
    email_address='your_email@qq.com',
    app_password='your_app_password',
    email_type='qq'
)

# 发送单个邮件
success = notifier.send_alert_email(
    recipient_email='recipient@qq.com',
    alert_result={...}
)

# 批量发送邮件
results = notifier.send_batch_emails(
    recipient_emails=['recipient1@qq.com', 'recipient2@163.com'],
    alert_result={...}
)
# 返回: {'recipient1@qq.com': True, 'recipient2@163.com': True}

# 测试连接
success = notifier.test_connection()

# 获取支持的邮箱类型
types = EmailNotifier.get_supported_email_types()
# 返回: {'qq': 'QQ邮箱', '163': '163邮箱'}
```

### 3. 邮件提醒集成 (EmailAlertIntegration)

**位置**: `email_alert_integration.py`

**主要方法**:

```python
# 初始化
integration = EmailAlertIntegration('.env')

# 测试邮件连接
success = integration.test_email_connection()

# 发送提醒邮件
results = integration.send_alert_emails(alert_result)

# 为特定品种发送提醒
results = integration.send_alert_for_product(
    product_name='AU9999',
    current_price=380.20,
    alert_result={...}
)

# 批量发送提醒
all_results = integration.send_batch_alerts(alert_results)

# 获取配置摘要
summary = integration.get_config_summary()
```

---

## 集成示例

### 示例 1: 基础使用

```python
from config.config_loader import ConfigLoader
from notifications.email_notifier import EmailNotifier

# 加载配置
config_loader = ConfigLoader('.env')
email_config = config_loader.get_email_config()
recipients = config_loader.get_recipient_emails()

# 初始化邮件通知器
notifier = EmailNotifier(
    email_address=email_config['email_address'],
    app_password=email_config['app_password'],
    email_type=email_config['email_type']
)

# 测试连接
if notifier.test_connection():
    print("邮件连接成功！")
else:
    print("邮件连接失败！")
```

### 示例 2: 与极值提醒集成

```python
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert
from email_alert_integration import EmailAlertIntegration

# 初始化系统
db = DatabaseManager('gold_prices.db')
alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)
email_integration = EmailAlertIntegration('.env')

# 检查极值提醒
result = alert_system.check_trigger_condition('AU9999', 380.20)

# 如果需要提醒，发送邮件
if result['should_alert']:
    email_integration.send_alert_emails(result)
    print(f"已发送 {result['product_name']} 的提醒邮件")
```

### 示例 3: 批量处理

```python
from email_alert_integration import EmailAlertIntegration

# 初始化集成
integration = EmailAlertIntegration('.env')

# 模拟多个提醒结果
alert_results = [
    {
        'product_name': 'AU9999',
        'current_price': 380.20,
        'should_alert': True,
        'alert_level': 'high',
        'alert_reasons': ['当前价格是24小时最低价'],
        'extremes': {...},
        'price_diff': {...},
        'timestamp': '2024-01-15T10:30:00'
    },
    # ... 更多提醒结果
]

# 批量发送
all_results = integration.send_batch_alerts(alert_results)

# 显示结果
for product_name, email_results in all_results.items():
    success_count = sum(1 for v in email_results.values() if v)
    print(f"{product_name}: {success_count}/{len(email_results)} 个收件人")
```

### 示例 4: 完整工作流

```python
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert
from email_alert_integration import EmailAlertIntegration

# 初始化
db = DatabaseManager('gold_prices.db')
alert_system = ExtremePriceAlert(db)
email_integration = EmailAlertIntegration('.env')

# 定义要监控的品种和价格
products = ['AU9999', 'AU100G', 'AU50G']
current_prices = [380.20, 3800.00, 1900.00]

# 批量检查极值提醒
alert_results = alert_system.batch_check_alerts(products, current_prices)

# 批量发送邮件
all_results = email_integration.send_batch_alerts(alert_results)

# 显示摘要
summary = alert_system.get_alert_summary(alert_results)
print(f"总共触发 {summary['total_triggered']} 个提醒")
print(f"  - 高级提醒: {summary['high_level']}")
print(f"  - 中级提醒: {summary['medium_level']}")
```

---

## 常见问题

### Q1: 如何获取应用授权码？

**A**: 见"快速开始"部分的详细步骤。注意：
- 授权码不是邮箱密码
- 授权码通常是16位字符
- 不要在代码中硬编码，使用 .env 文件

### Q2: 支持哪些邮箱类型？

**A**: 目前支持：
- QQ邮箱 (smtp.qq.com:587)
- 163邮箱 (smtp.163.com:587)

可以通过修改 `EmailNotifier.SMTP_CONFIG` 添加其他邮箱类型。

### Q3: 如何添加新的邮箱类型？

**A**: 编辑 `notifications/email_notifier.py`：

```python
SMTP_CONFIG = {
    'qq': {
        'smtp_server': 'smtp.qq.com',
        'smtp_port': 587,
        'description': 'QQ邮箱'
    },
    '163': {
        'smtp_server': 'smtp.163.com',
        'smtp_port': 587,
        'description': '163邮箱'
    },
    'gmail': {  # 新增
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'description': 'Gmail'
    }
}
```

### Q4: 如何在微信上接收邮件通知？

**A**: 使用"QQ邮箱提醒"小程序或公众号：
1. 在微信中搜索"QQ邮箱提醒"
2. 绑定你的QQ邮箱账号
3. 即可在微信上实时接收邮件通知

### Q5: 测试模式有什么用？

**A**: 测试模式用于：
- 测试配置是否正确
- 验证邮件模板是否正常
- 不消耗邮件配额
- 调试工作流程

设置 `TEST_MODE=true` 后，系统会模拟发送但不真正发送邮件。

### Q6: 如何处理多个收件人？

**A**: 在 .env 文件中用逗号分隔：

```env
RECIPIENT_EMAILS=recipient1@qq.com,recipient2@163.com,recipient3@gmail.com
```

系统会自动为每个收件人发送邮件。

---

## 故障排查

### 问题 1: 邮件连接失败

**症状**: `✗ 连接失败: 邮箱认证失败`

**解决方案**:
1. 检查 `EMAIL_ADDRESS` 是否正确
2. 检查 `APP_PASSWORD` 是否正确（不是邮箱密码）
3. 确保授权码未过期
4. 检查网络连接

### 问题 2: 邮件发送失败

**症状**: `✗ 邮件发送失败: SMTP错误`

**解决方案**:
1. 检查收件人邮箱地址是否正确
2. 检查 SMTP 服务器是否可访问
3. 查看日志文件获取详细错误信息
4. 尝试在测试模式下运行

### 问题 3: 配置文件找不到

**症状**: `FileNotFoundError: .env 文件不存在`

**解决方案**:
1. 确保 `.env` 文件存在
2. 检查文件路径是否正确
3. 使用绝对路径指定 .env 文件位置

### 问题 4: 日志文件无法写入

**症状**: `PermissionError: 无法写入日志文件`

**解决方案**:
1. 检查 `logs/` 目录是否存在
2. 检查目录权限
3. 确保有写入权限

### 问题 5: 邮件模板显示不正常

**症状**: 邮件中 HTML 格式混乱

**解决方案**:
1. 使用支持 HTML 的邮件客户端
2. 检查邮件编码是否为 UTF-8
3. 尝试在不同邮件客户端中查看

---

## 文件清单

```
notifications/
├── __init__.py
└── email_notifier.py          # 邮件通知器核心模块

config/
├── __init__.py
└── config_loader.py           # 配置加载器

email_alert_integration.py      # 邮件提醒集成脚本
test_email_notification.py      # 测试脚本
.env.example                    # 配置模板
.env                           # 配置文件（需要自己创建）
```

---

## 下一步

1. ✅ 配置 .env 文件
2. ✅ 运行测试脚本验证配置
3. ✅ 发送测试邮件
4. ✅ 与极值提醒系统集成
5. ✅ 部署到生产环境

---

**邮件通知系统已准备就绪！** 📧
"""
