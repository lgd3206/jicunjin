"""
系统完善方案 - 定时运行、防封策略、异常处理
"""

# ============================================================================
# 🚀 系统完善方案 - 定时运行、防封策略、异常处理
# ============================================================================

## 📋 完善内容

本方案包含以下三个核心改进：

1. ✅ **定时运行方案** - 每 10 分钟自动运行一次
2. ✅ **防封策略** - 随机 User-Agent 和延时
3. ✅ **异常处理** - 完整的日志记录和错误恢复

---

## 1️⃣ 定时运行方案

### 方案 A: 使用 Python 内置 schedule 库（推荐）

#### 安装依赖

```bash
pip install schedule
```

#### 代码示例

```python
import schedule
import time
from scheduled_monitor import ScheduledMonitor

def job():
    monitor = ScheduledMonitor('.env')
    monitor.check_and_send_alerts()

# 每 10 分钟运行一次
schedule.every(10).minutes.do(job)

# 持续运行
while True:
    schedule.run_pending()
    time.sleep(1)
```

### 方案 B: 使用 Windows 任务计划程序

#### 步骤 1: 创建批处理文件

创建 `run_monitor.bat` 文件：

```batch
@echo off
cd /d "F:\航海\積存金"
python scheduled_monitor.py
```

#### 步骤 2: 打开任务计划程序

1. 按 `Win + R`，输入 `taskschd.msc`
2. 点击"创建基本任务"
3. 输入任务名称：`金价监控`
4. 选择"触发器" → "新建" → "重复"
5. 设置间隔为 10 分钟
6. 选择"操作" → "新建" → "启动程序"
7. 程序路径：`F:\航海\積存金\run_monitor.bat`

### 方案 C: 使用 Linux/Mac cron

#### 编辑 crontab

```bash
crontab -e
```

#### 添加定时任务

```cron
# 每 10 分钟运行一次
*/10 * * * * cd /path/to/project && python scheduled_monitor.py
```

### 方案 D: 使用 Docker 容器

#### Dockerfile

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "scheduled_monitor.py"]
```

#### docker-compose.yml

```yaml
version: '3'
services:
  monitor:
    build: .
    volumes:
      - ./logs:/app/logs
      - ./.env:/app/.env
    restart: always
```

---

## 2️⃣ 防封策略

### 实现方式

#### 随机 User-Agent

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)
```

#### 随机延时

```python
def get_random_delay(min_delay=1.0, max_delay=5.0):
    return random.uniform(min_delay, max_delay)

# 使用
delay = get_random_delay(1.0, 3.0)
time.sleep(delay)
```

#### 请求头配置

```python
headers = {
    'User-Agent': get_random_user_agent(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
```

#### IP 轮换（可选）

```python
# 使用代理池
PROXIES = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
    'http://proxy3.com:8080',
]

def get_random_proxy():
    return random.choice(PROXIES)

# 使用
response = requests.get(url, proxies={'http': get_random_proxy()})
```

---

## 3️⃣ 异常处理

### 完整的异常处理框架

```python
import logging
import traceback
from datetime import datetime

class RobustMonitor:
    def __init__(self):
        self.logger = self._setup_logger()
        self.error_count = 0
        self.success_count = 0

    def _setup_logger(self):
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # 文件处理器
        file_handler = logging.FileHandler('logs/monitor.log')
        file_handler.setLevel(logging.DEBUG)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def safe_execute(self, func, *args, **kwargs):
        """安全执行函数，捕获所有异常"""
        try:
            self.logger.info(f"执行: {func.__name__}")
            result = func(*args, **kwargs)
            self.success_count += 1
            self.logger.info(f"✓ {func.__name__} 成功")
            return result
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"✗ {func.__name__} 失败: {str(e)}")
            self.logger.exception("详细错误信息:")
            return None

    def get_statistics(self):
        """获取统计信息"""
        total = self.success_count + self.error_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        return {
            'success_count': self.success_count,
            'error_count': self.error_count,
            'total': total,
            'success_rate': success_rate,
        }
```

### 异常处理最佳实践

#### 1. 网络异常处理

```python
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    RequestException
)

def fetch_with_retry(url, max_retries=3):
    """带重试的网络请求"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            logger.warning(f"连接错误，重试 {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)  # 指数退避
        except Timeout:
            logger.warning(f"请求超时，重试 {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)
        except RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            return None

    logger.error(f"在 {max_retries} 次重试后仍然失败")
    return None
```

#### 2. 数据库异常处理

```python
import sqlite3

def safe_db_query(db_path, query, params=None):
    """安全的数据库查询"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.DatabaseError as e:
        logger.error(f"数据库错误: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return None
```

#### 3. 邮件发送异常处理

```python
import smtplib
from email.mime.text import MIMEText

def safe_send_email(email_config, recipient, subject, content):
    """安全的邮件发送"""
    try:
        server = smtplib.SMTP(
            email_config['smtp_server'],
            email_config['smtp_port'],
            timeout=10
        )
        server.starttls()
        server.login(email_config['email'], email_config['password'])

        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = email_config['email']
        msg['To'] = recipient

        server.send_message(msg)
        server.quit()

        logger.info(f"✓ 邮件已发送到 {recipient}")
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("邮箱认证失败")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP 错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")
        return False
```

#### 4. 配置加载异常处理

```python
def safe_load_config(env_path):
    """安全的配置加载"""
    try:
        if not os.path.exists(env_path):
            logger.error(f"配置文件不存在: {env_path}")
            return None

        config = ConfigLoader(env_path)
        config.validate_email_config()
        config.validate_recipient_emails()

        logger.info("✓ 配置加载成功")
        return config
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {str(e)}")
        return None
    except ValueError as e:
        logger.error(f"配置验证失败: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"配置加载失败: {str(e)}")
        return None
```

---

## 📦 完整代码包结构

```
gold_monitor/
├── config/
│   ├── __init__.py
│   └── config_loader.py
├── notifications/
│   ├── __init__.py
│   └── email_notifier.py
├── alerts/
│   ├── __init__.py
│   └── extreme_price_alert.py
├── database/
│   ├── __init__.py
│   └── db_manager.py
├── scrapers/
│   ├── __init__.py
│   └── api_scraper.py
├── logs/                          # 日志目录
│   ├── monitor.log
│   ├── notifications.log
│   └── scheduled_monitor.log
├── main.py                        # 主程序
├── scheduled_monitor.py           # 定时监控脚本
├── email_alert_integration.py     # 邮件集成
├── test_email_notification.py     # 测试脚本
├── .env.example                   # 配置模板
├── .env                          # 配置文件（需自己创建）
├── requirements.txt              # 依赖包
├── run_monitor.bat              # Windows 批处理文件
├── run_monitor.sh               # Linux/Mac 脚本
├── Dockerfile                   # Docker 配置
├── docker-compose.yml           # Docker Compose 配置
└── README.md                    # 项目说明
```

---

## 🚀 部署指南

### 第一步: 准备环境

```bash
# 克隆或下载项目
cd /path/to/project

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 第二步: 配置系统

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
# 填入邮箱信息、收件人等
```

### 第三步: 测试系统

```bash
# 运行测试脚本
python test_email_notification.py

# 运行演示脚本
python email_alert_integration.py

# 运行定时监控（演示模式）
python scheduled_monitor.py
```

### 第四步: 部署到服务器

#### Windows 服务器

```batch
# 1. 创建 run_monitor.bat
@echo off
cd /d "F:\航海\積存金"
python scheduled_monitor.py

# 2. 使用任务计划程序设置定时任务
# 或使用 NSSM 创建 Windows 服务
nssm install GoldMonitor "F:\航海\積存金\run_monitor.bat"
nssm start GoldMonitor
```

#### Linux/Mac 服务器

```bash
# 1. 创建 run_monitor.sh
#!/bin/bash
cd /path/to/project
source venv/bin/activate
python scheduled_monitor.py

# 2. 添加执行权限
chmod +x run_monitor.sh

# 3. 使用 cron 设置定时任务
crontab -e
# 添加: */10 * * * * /path/to/project/run_monitor.sh

# 或使用 systemd 服务
# 创建 /etc/systemd/system/gold-monitor.service
[Unit]
Description=Gold Price Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/venv/bin/python scheduled_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# 启动服务
sudo systemctl start gold-monitor
sudo systemctl enable gold-monitor
```

#### Docker 部署

```bash
# 构建镜像
docker build -t gold-monitor .

# 运行容器
docker run -d \
  --name gold-monitor \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --restart always \
  gold-monitor

# 或使用 docker-compose
docker-compose up -d
```

---

## 📊 监控和维护

### 查看日志

```bash
# 实时查看日志
tail -f logs/scheduled_monitor.log

# 查看最后 100 行
tail -100 logs/scheduled_monitor.log

# 搜索错误
grep ERROR logs/scheduled_monitor.log

# 统计错误次数
grep -c ERROR logs/scheduled_monitor.log
```

### 性能监控

```bash
# 监控进程
ps aux | grep scheduled_monitor

# 监控内存使用
top -p $(pgrep -f scheduled_monitor)

# 监控网络连接
netstat -an | grep ESTABLISHED
```

### 日志轮转

```bash
# 使用 logrotate（Linux）
# 创建 /etc/logrotate.d/gold-monitor
/path/to/project/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 ubuntu ubuntu
    sharedscripts
}
```

---

## ✅ 检查清单

### 部署前检查

- [ ] 配置文件已创建和验证
- [ ] 邮箱授权码已获取
- [ ] 依赖包已安装
- [ ] 测试脚本已运行成功
- [ ] 日志目录已创建
- [ ] 防火墙已配置（如需要）

### 部署后检查

- [ ] 定时任务已创建
- [ ] 监控脚本已启动
- [ ] 日志文件已生成
- [ ] 邮件已正常发送
- [ ] 错误处理已验证
- [ ] 性能监控已配置

### 定期维护

- [ ] 每周检查日志文件
- [ ] 每月清理旧日志
- [ ] 每季度更新依赖包
- [ ] 每半年审查配置
- [ ] 定期备份配置文件

---

## 🔧 故障排查

### 问题 1: 定时任务不执行

**症状**: 任务计划中显示已创建，但没有执行

**解决方案**:
1. 检查任务计划程序中的历史记录
2. 验证脚本路径是否正确
3. 检查用户权限
4. 查看日志文件

### 问题 2: 邮件发送失败

**症状**: 日志显示邮件发送失败

**解决方案**:
1. 检查邮箱配置是否正确
2. 验证授权码是否过期
3. 检查网络连接
4. 查看 SMTP 错误信息

### 问题 3: 内存泄漏

**症状**: 程序运行时间越长，内存占用越多

**解决方案**:
1. 检查是否有未关闭的数据库连接
2. 验证是否有循环引用
3. 定期重启程序
4. 使用内存分析工具

### 问题 4: 高 CPU 占用

**症状**: 程序占用 CPU 过高

**解决方案**:
1. 增加检查间隔
2. 优化数据库查询
3. 减少日志输出
4. 检查是否有死循环

---

## 📈 性能优化

### 1. 数据库优化

```python
# 添加索引
CREATE INDEX idx_timestamp ON gold_prices(timestamp);
CREATE INDEX idx_product ON gold_prices(product_name);

# 定期清理旧数据
DELETE FROM gold_prices WHERE timestamp < datetime('now', '-30 days');
```

### 2. 网络优化

```python
# 使用连接池
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 3. 内存优化

```python
# 使用生成器而不是列表
def process_large_data():
    for item in get_data():
        yield process_item(item)

# 及时释放资源
import gc
gc.collect()
```

---

## 🎯 最佳实践

### 1. 安全性

- ✅ 使用 .env 文件存储敏感信息
- ✅ 定期更新依赖包
- ✅ 使用 HTTPS 连接
- ✅ 限制日志中的敏感信息

### 2. 可靠性

- ✅ 实现完整的异常处理
- ✅ 添加重试机制
- ✅ 定期备份数据
- ✅ 监控系统健康状态

### 3. 可维护性

- ✅ 编写清晰的代码注释
- ✅ 使用日志记录
- ✅ 定期更新文档
- ✅ 版本控制

### 4. 性能

- ✅ 优化数据库查询
- ✅ 使用缓存
- ✅ 异步处理
- ✅ 定期监控

---

## 📞 获取帮助

### 查看日志

```bash
tail -f logs/scheduled_monitor.log
```

### 运行测试

```bash
python test_email_notification.py
```

### 查看配置

```bash
cat .env
```

---

**系统完善方案已准备就绪！** 🚀
"""
