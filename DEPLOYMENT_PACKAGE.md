"""
完整部署包 - 包含所有必要的脚本和配置
"""

# ============================================================================
# 📦 完整部署包 - 一键部署指南
# ============================================================================

## 🎯 部署目标

创建一个完整的、可立即部署的金价监控系统，包括：

✅ 定时运行（每 10 分钟）
✅ 防封策略（随机 User-Agent 和延时）
✅ 异常处理（完整的日志和错误恢复）
✅ 一键部署（简化的部署流程）

---

## 📋 部署包内容

### 核心文件

```
项目根目录/
├── 核心模块/
│   ├── config/config_loader.py          # 配置加载器
│   ├── notifications/email_notifier.py  # 邮件通知器
│   ├── alerts/extreme_price_alert.py    # 极值提醒
│   ├── database/db_manager.py           # 数据库管理
│   └── scrapers/api_scraper.py          # API 抓取
│
├── 脚本文件/
│   ├── main.py                          # 主程序
│   ├── scheduled_monitor.py             # 定时监控
│   ├── email_alert_integration.py       # 邮件集成
│   └── test_email_notification.py       # 测试脚本
│
├── 配置文件/
│   ├── .env.example                     # 配置模板
│   ├── requirements.txt                 # 依赖包
│   ├── run_monitor.bat                  # Windows 脚本
│   ├── run_monitor.sh                   # Linux/Mac 脚本
│   ├── Dockerfile                       # Docker 配置
│   └── docker-compose.yml               # Docker Compose
│
├── 文档文件/
│   ├── README.md                        # 项目说明
│   ├── DEPLOYMENT_GUIDE.md              # 部署指南
│   ├── SYSTEM_ENHANCEMENT_GUIDE.md      # 系统完善指南
│   └── TROUBLESHOOTING.md               # 故障排查
│
└── 日志目录/
    └── logs/                            # 日志文件（运行时生成）
```

---

## 🚀 一键部署步骤

### Windows 系统

#### 步骤 1: 准备环境

```batch
# 1. 打开命令提示符，进入项目目录
cd F:\航海\積存金

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt
```

#### 步骤 2: 配置系统

```batch
# 1. 复制配置文件
copy .env.example .env

# 2. 编辑 .env 文件（使用记事本或其他编辑器）
# 填入以下信息：
# - EMAIL_TYPE=qq
# - EMAIL_ADDRESS=your_email@qq.com
# - APP_PASSWORD=your_app_password_here
# - RECIPIENT_EMAILS=recipient1@qq.com,recipient2@163.com
```

#### 步骤 3: 测试系统

```batch
# 1. 运行测试脚本
python test_email_notification.py

# 2. 如果所有测试通过，继续下一步
```

#### 步骤 4: 设置定时任务

**方法 A: 使用任务计划程序（推荐）**

```batch
# 1. 按 Win + R，输入 taskschd.msc，打开任务计划程序
# 2. 点击"创建基本任务"
# 3. 输入任务名称：金价监控
# 4. 选择"触发器" → "新建" → "重复"
# 5. 设置间隔为 10 分钟
# 6. 选择"操作" → "新建" → "启动程序"
# 7. 程序路径：F:\航海\積存金\run_monitor.bat
# 8. 点击"确定"完成
```

**方法 B: 使用 NSSM 创建 Windows 服务**

```batch
# 1. 下载 NSSM: https://nssm.cc/download
# 2. 解压到项目目录
# 3. 运行以下命令：
nssm install GoldMonitor "F:\航海\積存金\run_monitor.bat"
nssm start GoldMonitor

# 查看服务状态
nssm status GoldMonitor

# 停止服务
nssm stop GoldMonitor

# 删除服务
nssm remove GoldMonitor
```

#### 步骤 5: 验证部署

```batch
# 1. 查看日志文件
type logs\scheduled_monitor.log

# 2. 实时查看日志（需要安装 tail）
tail -f logs\scheduled_monitor.log

# 3. 检查任务是否运行
tasklist | findstr python
```

---

### Linux/Mac 系统

#### 步骤 1: 准备环境

```bash
# 1. 进入项目目录
cd /path/to/project

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
```

#### 步骤 2: 配置系统

```bash
# 1. 复制配置文件
cp .env.example .env

# 2. 编辑 .env 文件
nano .env
# 或
vim .env

# 填入邮箱信息
```

#### 步骤 3: 测试系统

```bash
# 1. 运行测试脚本
python test_email_notification.py

# 2. 如果所有测试通过，继续下一步
```

#### 步骤 4: 设置定时任务

**方法 A: 使用 cron（推荐）**

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加以下行（每 10 分钟运行一次）
*/10 * * * * cd /path/to/project && source venv/bin/activate && python scheduled_monitor.py >> logs/cron.log 2>&1

# 3. 保存并退出
# 按 Ctrl+X，然后按 Y，再按 Enter
```

**方法 B: 使用 systemd 服务**

```bash
# 1. 创建服务文件
sudo nano /etc/systemd/system/gold-monitor.service

# 2. 添加以下内容
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

# 3. 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable gold-monitor
sudo systemctl start gold-monitor

# 4. 查看服务状态
sudo systemctl status gold-monitor

# 5. 查看日志
sudo journalctl -u gold-monitor -f
```

#### 步骤 5: 验证部署

```bash
# 1. 查看日志文件
tail -f logs/scheduled_monitor.log

# 2. 检查进程
ps aux | grep scheduled_monitor

# 3. 检查 cron 日志
grep CRON /var/log/syslog
```

---

### Docker 部署

#### 步骤 1: 安装 Docker

```bash
# Windows/Mac: 下载 Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux: 使用包管理器
sudo apt-get install docker.io docker-compose
```

#### 步骤 2: 构建镜像

```bash
# 进入项目目录
cd /path/to/project

# 构建镜像
docker build -t gold-monitor:latest .
```

#### 步骤 3: 运行容器

```bash
# 方法 A: 使用 docker run
docker run -d \
  --name gold-monitor \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --restart always \
  gold-monitor:latest

# 方法 B: 使用 docker-compose（推荐）
docker-compose up -d
```

#### 步骤 4: 管理容器

```bash
# 查看容器状态
docker ps

# 查看容器日志
docker logs -f gold-monitor

# 停止容器
docker stop gold-monitor

# 启动容器
docker start gold-monitor

# 删除容器
docker rm gold-monitor
```

---

## 📊 部署验证清单

### 部署前检查

- [ ] Python 3.7+ 已安装
- [ ] 虚拟环境已创建
- [ ] 依赖包已安装
- [ ] .env 文件已创建和配置
- [ ] 邮箱授权码已获取
- [ ] 测试脚本已运行成功

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

---

## 🔍 监控和维护

### 查看系统状态

```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep scheduled_monitor
```

### 查看日志

```bash
# 实时查看
tail -f logs/scheduled_monitor.log

# 查看最后 100 行
tail -100 logs/scheduled_monitor.log

# 搜索错误
grep ERROR logs/scheduled_monitor.log
```

### 性能监控

```bash
# 监控内存使用
top -p $(pgrep -f scheduled_monitor)

# 监控网络连接
netstat -an | grep ESTABLISHED

# 监控磁盘使用
du -sh logs/
```

---

## 🆘 常见问题

### Q1: 如何停止监控？

**Windows**:
```batch
# 使用任务计划程序禁用任务
# 或使用 NSSM 停止服务
nssm stop GoldMonitor
```

**Linux/Mac**:
```bash
# 使用 cron
crontab -e
# 注释掉相应的行

# 或使用 systemd
sudo systemctl stop gold-monitor
```

### Q2: 如何修改检查间隔？

编辑 `scheduled_monitor.py`：

```python
# 修改这一行
monitor = ScheduledMonitor(
    env_path='.env',
    check_interval=600  # 改为需要的秒数
)
```

### Q3: 如何查看邮件发送历史？

```bash
# 查看邮件发送日志
grep "邮件已发送" logs/scheduled_monitor.log

# 统计发送次数
grep -c "邮件已发送" logs/scheduled_monitor.log
```

### Q4: 如何处理邮件发送失败？

1. 检查 .env 文件配置
2. 验证邮箱授权码是否过期
3. 检查网络连接
4. 查看详细错误日志

---

## 📈 性能优化建议

### 1. 增加检查间隔

如果系统负载过高，可以增加检查间隔：

```python
# 从 10 分钟改为 30 分钟
check_interval=1800
```

### 2. 减少日志输出

编辑 `config_loader.py`：

```python
LOG_LEVEL=WARNING  # 改为 WARNING 或 ERROR
```

### 3. 定期清理日志

```bash
# 删除 7 天前的日志
find logs/ -name "*.log" -mtime +7 -delete
```

### 4. 使用数据库连接池

```python
# 在 db_manager.py 中实现连接池
from sqlalchemy import create_engine
engine = create_engine('sqlite:///gold_prices.db', pool_size=10)
```

---

## 🎯 下一步行动

### 立即行动（今天）

1. [ ] 下载完整部署包
2. [ ] 按照部署指南进行部署
3. [ ] 运行测试脚本验证
4. [ ] 设置定时任务

### 短期行动（本周）

1. [ ] 监控系统运行状态
2. [ ] 检查日志文件
3. [ ] 验证邮件发送
4. [ ] 调整配置参数

### 中期行动（本月）

1. [ ] 优化系统性能
2. [ ] 添加更多监控指标
3. [ ] 实现数据分析
4. [ ] 创建仪表板

### 长期行动（持续）

1. [ ] 定期维护和更新
2. [ ] 监控系统健康状态
3. [ ] 收集用户反馈
4. [ ] 持续改进

---

## 📞 技术支持

### 获取帮助

1. 查看相关文档
2. 检查日志文件
3. 运行测试脚本
4. 查看示例代码

### 常用命令

```bash
# 查看日志
tail -f logs/scheduled_monitor.log

# 运行测试
python test_email_notification.py

# 查看配置
cat .env

# 查看进程
ps aux | grep scheduled_monitor
```

---

## ✅ 部署完成确认

当你看到以下信息时，说明部署成功：

```
✓ 配置加载成功
✓ 邮件连接成功
✓ 定时任务已创建
✓ 监控脚本已启动
✓ 日志文件已生成
```

---

**完整部署包已准备就绪！** 🚀

**立即开始部署**: 按照上述步骤进行部署，5 分钟内即可完成！
"""
