"""
快速开始指南 - 3 步部署金价监控系统
"""

# ============================================================================
# 🚀 快速开始指南 - 3 步部署
# ============================================================================

## 📋 系统要求

- Python 3.7+
- pip 包管理器
- 网络连接
- 邮箱账号（QQ 或 163）

---

## 🎯 3 步快速部署

### 第一步: 下载并进入项目目录

**Windows**:
```batch
cd F:\航海\積存金
```

**Linux/Mac**:
```bash
cd /path/to/project
```

---

### 第二步: 运行部署脚本

**Windows** (推荐):
```batch
deploy.bat
```

**Linux/Mac** (推荐):
```bash
chmod +x deploy.sh
./deploy.sh
```

**或手动部署**:
```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 复制配置文件
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env

# 5. 编辑配置文件
# 填入邮箱信息

# 6. 运行测试
python test_email_notification.py
```

---

### 第三步: 配置邮箱信息

编辑 `.env` 文件，填入以下信息：

```env
# 邮箱配置
EMAIL_TYPE=qq                          # qq 或 163
EMAIL_ADDRESS=your_email@qq.com        # 你的邮箱地址
APP_PASSWORD=your_app_password_here    # 应用授权码

# 收件人配置
RECIPIENT_EMAILS=recipient@qq.com      # 收件人邮箱

# 其他配置（可选）
DROP_THRESHOLD_PERCENT=5.0             # 下跌阈值
ENABLE_EMAIL_NOTIFICATION=true         # 启用邮件通知
TEST_MODE=false                        # 测试模式
```

---

## 📧 获取邮箱授权码

### QQ 邮箱

1. 登录 QQ 邮箱 (https://mail.qq.com)
2. 点击"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 点击"生成授权码"
5. 按照提示完成验证，复制授权码

### 163 邮箱

1. 登录 163 邮箱 (https://mail.163.com)
2. 点击"设置" → "POP3/SMTP/IMAP"
3. 点击"开启"
4. 按照提示完成验证，获取授权码

---

## ✅ 验证部署

运行测试脚本：

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

...

🎉 所有测试通过！
```

---

## 🚀 启动监控

### 方式 1: 直接运行（演示）

```bash
python scheduled_monitor.py
```

### 方式 2: 定时运行（生产环境）

#### Windows 任务计划程序

1. 按 `Win + R`，输入 `taskschd.msc`
2. 点击"创建基本任务"
3. 输入任务名称：`金价监控`
4. 选择"触发器" → "新建" → "重复"
5. 设置间隔为 10 分钟
6. 选择"操作" → "新建" → "启动程序"
7. 程序路径：`F:\航海\積存金\run_monitor.bat`
8. 点击"确定"完成

#### Linux/Mac cron

```bash
crontab -e

# 添加以下行（每 10 分钟运行一次）
*/10 * * * * cd /path/to/project && source venv/bin/activate && python scheduled_monitor.py >> logs/cron.log 2>&1
```

#### Docker

```bash
docker-compose up -d
docker logs -f gold-monitor
```

---

## 📊 监控系统

### 查看日志

```bash
# 实时查看
tail -f logs/scheduled_monitor.log

# 查看最后 100 行
tail -100 logs/scheduled_monitor.log

# 搜索错误
grep ERROR logs/scheduled_monitor.log
```

### 查看进程

```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep scheduled_monitor
```

### 查看配置

```bash
cat .env
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
    check_interval=600  # 改为需要的秒数（600 = 10 分钟）
)
```

### Q3: 如何查看邮件发送历史？

```bash
grep "邮件已发送" logs/scheduled_monitor.log
```

### Q4: 邮件发送失败怎么办？

1. 检查 .env 文件配置是否正确
2. 验证邮箱授权码是否过期
3. 检查网络连接
4. 查看详细错误日志

---

## 📚 更多文档

- **DEPLOYMENT_PACKAGE.md** - 完整部署指南
- **SYSTEM_ENHANCEMENT_GUIDE.md** - 系统完善指南
- **EMAIL_NOTIFICATION_GUIDE.md** - 邮件系统完整指南
- **PROJECT_COMPLETION_REPORT.md** - 项目完成报告

---

## 💡 提示

### 安全性建议

- ✅ 使用 .env 文件存储敏感信息
- ✅ 不要在代码中硬编码密码
- ✅ 定期更新授权码
- ✅ 限制 .env 文件的访问权限

### 性能优化

- ✅ 根据需要调整检查间隔
- ✅ 定期清理日志文件
- ✅ 监控系统资源使用
- ✅ 使用批量发送而不是逐个发送

### 可靠性

- ✅ 定期检查日志文件
- ✅ 监控邮件发送状态
- ✅ 设置备份收件人
- ✅ 定期备份配置文件

---

## 🎯 下一步

1. ✅ 运行部署脚本
2. ✅ 配置邮箱信息
3. ✅ 运行测试脚本
4. ✅ 启动监控系统
5. ✅ 检查日志文件

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

### 查看示例
```bash
python email_notification_examples.py
```

---

**系统已准备就绪，立即开始部署！** 🚀

按照上述步骤，5 分钟内即可完成部署！
"""
