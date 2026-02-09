"""
GitHub + Vercel 部署实施指南 - 完整步骤
"""

# ============================================================================
# 📋 GitHub + Vercel 部署实施指南 - 完整步骤
# ============================================================================

## 🎯 部署目标

将金价监控系统部署到 GitHub 和 Vercel，实现：
- ✅ 代码版本管理
- ✅ 自动化部署
- ✅ Web API 服务
- ✅ 在线监控

---

## 第一步: 本地 Git 初始化

### 1.1 安装 Git

**Windows**:
```bash
# 下载并安装 Git
# https://git-scm.com/download/win
```

**Linux/Mac**:
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git
```

### 1.2 配置 Git

```bash
# 配置用户名
git config --global user.name "Your Name"

# 配置邮箱
git config --global user.email "your.email@example.com"

# 验证配置
git config --global --list
```

### 1.3 初始化本地仓库

```bash
# 进入项目目录
cd F:\航海\積存金

# 初始化 Git 仓库
git init

# 查看状态
git status
```

### 1.4 创建 .gitignore 文件

```bash
# 创建 .gitignore
cat > .gitignore << 'EOF'
# 虚拟环境
venv/
env/
ENV/
.venv

# Python 缓存
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 依赖
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# 敏感信息
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json

# 日志
logs/
*.log

# 数据库
*.db
*.sqlite
*.sqlite3

# 临时文件
tmp/
temp/
*.tmp
.cache/
.pytest_cache/
.coverage

# 其他
node_modules/
.git/
EOF
```

### 1.5 添加文件到 Git

```bash
# 查看未跟踪的文件
git status

# 添加所有文件
git add .

# 或添加特定文件
git add *.py *.md requirements.txt

# 查看暂存区
git status
```

### 1.6 创建初始提交

```bash
# 创建提交
git commit -m "Initial commit: Gold price monitoring system v2.0.0

- Email notification system with SMTP support
- Scheduled monitoring (every 10 minutes)
- Anti-blocking strategies (random User-Agent, delays)
- Complete exception handling and logging
- Support for QQ and 163 email accounts
- Comprehensive documentation and examples"

# 查看提交日志
git log
```

---

## 第二步: 创建 GitHub 仓库

### 2.1 创建 GitHub 账号

1. 访问 https://github.com
2. 点击 "Sign up"
3. 填写用户名、邮箱、密码
4. 完成验证
5. 选择免费计划

### 2.2 创建新仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：

```
Repository name: gold-price-monitor
Description: 金价自动化监控与提醒系统 - Automated gold price monitoring and alert system
Public: ✓ (选择公开)
Add a README file: ✓
Add .gitignore: Python
Add a license: MIT License
```

4. 点击 "Create repository"

### 2.3 获取仓库 URL

在仓库页面，点击绿色 "Code" 按钮，复制 HTTPS URL：

```
https://github.com/YOUR_USERNAME/gold-price-monitor.git
```

---

## 第三步: 推送代码到 GitHub

### 3.1 添加远程仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/gold-price-monitor.git

# 验证远程仓库
git remote -v
```

### 3.2 推送代码

```bash
# 重命名分支为 main
git branch -M main

# 推送代码到 GitHub
git push -u origin main

# 验证推送
git log --oneline
```

### 3.3 验证 GitHub 仓库

1. 访问 https://github.com/YOUR_USERNAME/gold-price-monitor
2. 检查文件是否已上传
3. 查看提交历史

---

## 第四步: 创建 Vercel 配置文件

### 4.1 创建 vercel.json

```bash
cat > vercel.json << 'EOF'
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".",
  "env": {
    "EMAIL_TYPE": "@email_type",
    "EMAIL_ADDRESS": "@email_address",
    "APP_PASSWORD": "@app_password",
    "RECIPIENT_EMAILS": "@recipient_emails"
  },
  "functions": {
    "api/monitor.py": {
      "memory": 1024,
      "maxDuration": 60
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/$1.py"
    }
  ]
}
EOF
```

### 4.2 创建 API 目录和文件

```bash
# 创建 api 目录
mkdir -p api

# 创建 __init__.py
touch api/__init__.py

# 创建 monitor.py
cat > api/monitor.py << 'EOF'
"""
Vercel Serverless Function - 金价监控 API
"""
import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from email_alert_integration import EmailAlertIntegration


def handler(request):
    """处理 HTTP 请求"""

    # 处理 GET 请求 - 测试连接
    if request.method == 'GET':
        try:
            integration = EmailAlertIntegration('.env')

            if integration.test_email_connection():
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'status': 'success',
                        'message': 'Connection test passed'
                    })
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'status': 'error',
                        'message': 'Connection test failed'
                    })
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'status': 'error',
                    'message': str(e)
                })
            }

    # 处理 POST 请求 - 发送邮件
    elif request.method == 'POST':
        try:
            # 解析请求体
            body = json.loads(request.body) if isinstance(request.body, str) else request.body

            integration = EmailAlertIntegration('.env')

            # 发送邮件
            results = integration.send_alert_emails(body)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'success',
                    'message': 'Email sent successfully',
                    'results': results
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'status': 'error',
                    'message': str(e)
                })
            }

    # 其他方法
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({
                'status': 'error',
                'message': 'Method not allowed'
            })
        }
EOF
```

### 4.3 创建 health check 端点

```bash
cat > api/health.py << 'EOF'
"""
Health check endpoint
"""
import json


def handler(request):
    """健康检查"""
    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'healthy',
            'service': 'gold-price-monitor',
            'version': '2.0.0'
        })
    }
EOF
```

### 4.4 提交新文件到 Git

```bash
# 添加新文件
git add vercel.json api/

# 提交
git commit -m "Add Vercel configuration and API endpoints

- Add vercel.json for Vercel deployment configuration
- Add api/monitor.py for email sending API
- Add api/health.py for health check endpoint"

# 推送到 GitHub
git push origin main
```

---

## 第五步: 部署到 Vercel

### 5.1 创建 Vercel 账号

1. 访问 https://vercel.com
2. 点击 "Sign Up"
3. 选择 "Continue with GitHub"
4. 授权 Vercel 访问你的 GitHub 账号

### 5.2 导入项目

1. 登录 Vercel
2. 点击 "Add New..." → "Project"
3. 点击 "Import Git Repository"
4. 搜索 `gold-price-monitor`
5. 点击 "Import"

### 5.3 配置项目

**Project Settings**:
```
Project Name: gold-price-monitor
Framework: Other
Root Directory: ./
```

**Build Settings**:
```
Build Command: pip install -r requirements.txt
Output Directory: (留空)
Install Command: (留空)
```

### 5.4 配置环境变量

点击 "Environment Variables"，添加以下变量：

```
EMAIL_TYPE = qq
EMAIL_ADDRESS = your_email@qq.com
APP_PASSWORD = your_app_password_here
RECIPIENT_EMAILS = recipient@qq.com
DROP_THRESHOLD_PERCENT = 5.0
ENABLE_EMAIL_NOTIFICATION = true
TEST_MODE = false
DATABASE_PATH = gold_prices.db
LOG_LEVEL = INFO
LOG_FILE = logs/notifications.log
```

**重要**: 不要在代码中硬编码这些值，使用环境变量！

### 5.5 部署

1. 点击 "Deploy" 按钮
2. 等待部署完成（通常需要 2-5 分钟）
3. 查看部署日志

### 5.6 验证部署

部署完成后，你会获得一个 URL，例如：
```
https://gold-price-monitor.vercel.app
```

测试 API：
```bash
# 测试健康检查
curl https://gold-price-monitor.vercel.app/api/health

# 测试连接
curl https://gold-price-monitor.vercel.app/api/monitor
```

---

## 第六步: 配置自动部署

### 6.1 启用自动部署

Vercel 默认已启用自动部署。当你推送代码到 GitHub 时，Vercel 会自动部署。

### 6.2 查看部署历史

1. 登录 Vercel
2. 选择你的项目
3. 点击 "Deployments"
4. 查看所有部署

### 6.3 回滚部署

如果新部署有问题，可以回滚到之前的版本：

1. 在 "Deployments" 中找到之前的版本
2. 点击 "..." → "Promote to Production"

---

## 第七步: 配置自定义域名（可选）

### 7.1 在 Vercel 中添加域名

1. 登录 Vercel
2. 选择你的项目
3. 点击 "Settings" → "Domains"
4. 输入你的域名（例如 `gold-monitor.com`）
5. 点击 "Add"

### 7.2 配置 DNS

根据 Vercel 提供的 DNS 记录，在你的域名提供商处添加：

```
CNAME: cname.vercel-dns.com
```

或使用 Nameservers：
```
ns1.vercel-dns.com
ns2.vercel-dns.com
```

### 7.3 验证域名

DNS 生效通常需要 24-48 小时。完成后，你可以通过自定义域名访问你的应用。

---

## 第八步: 监控和维护

### 8.1 查看实时日志

```bash
# 在 Vercel 控制面板中查看日志
# 或使用 Vercel CLI
vercel logs
```

### 8.2 更新环境变量

1. 登录 Vercel
2. 选择你的项目
3. 点击 "Settings" → "Environment Variables"
4. 修改变量
5. 重新部署

### 8.3 监控性能

1. 点击 "Analytics"
2. 查看请求数、响应时间等指标

### 8.4 设置告警

1. 点击 "Settings" → "Alerts"
2. 配置告警规则

---

## 第九步: 集成定时任务

### 方案 A: 使用 Vercel Cron Functions (Pro 计划)

创建 `api/cron.py`：

```python
"""
Vercel Cron Function - 定时监控
"""
import json
from email_alert_integration import EmailAlertIntegration


def handler(request):
    """定时监控任务"""
    try:
        integration = EmailAlertIntegration('.env')

        # 执行监控逻辑
        # ...

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'message': 'Monitoring task completed'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        }
```

在 `vercel.json` 中配置：

```json
{
  "crons": [
    {
      "path": "/api/cron",
      "schedule": "*/10 * * * *"
    }
  ]
}
```

### 方案 B: 使用外部定时服务

在自己的服务器上运行 `scheduled_monitor.py`，定期调用 Vercel API：

```python
import requests
import time

def call_vercel_api():
    """调用 Vercel API"""
    url = "https://gold-price-monitor.vercel.app/api/monitor"

    alert_result = {
        'product_name': 'AU9999',
        'current_price': 380.20,
        'should_alert': True,
        # ... 其他字段
    }

    response = requests.post(url, json=alert_result)
    return response.json()

# 每 10 分钟调用一次
while True:
    try:
        result = call_vercel_api()
        print(f"API 调用成功: {result}")
    except Exception as e:
        print(f"API 调用失败: {e}")

    time.sleep(600)  # 10 分钟
```

---

## 常见问题

### Q1: 部署失败怎么办？

**检查清单**:
1. 查看 Vercel 部署日志
2. 检查 `requirements.txt` 是否完整
3. 检查环境变量是否正确配置
4. 检查 Python 版本兼容性

### Q2: 如何更新代码？

```bash
# 本地修改代码
# ...

# 提交到 Git
git add .
git commit -m "Update: description of changes"

# 推送到 GitHub
git push origin main

# Vercel 会自动部署
```

### Q3: 如何处理敏感信息？

- ✅ 使用 Vercel 环境变量
- ✅ 在 `.gitignore` 中排除 `.env` 文件
- ✅ 不要在代码中硬编码密码
- ✅ 定期更新授权码

### Q4: 如何扩展应用？

1. 添加更多 API 端点
2. 集成数据库（MongoDB、PostgreSQL 等）
3. 添加前端界面
4. 实现用户认证

---

## 部署检查清单

### 部署前
- [ ] 代码已提交到 Git
- [ ] `.gitignore` 已配置
- [ ] `requirements.txt` 已更新
- [ ] `vercel.json` 已创建
- [ ] API 端点已创建

### 部署中
- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] Vercel 账号已创建
- [ ] 项目已导入到 Vercel
- [ ] 环境变量已配置

### 部署后
- [ ] 部署成功
- [ ] API 端点可访问
- [ ] 环境变量已生效
- [ ] 日志正常
- [ ] 邮件发送正常

---

## 下一步

1. [ ] 创建 GitHub 账号
2. [ ] 创建 GitHub 仓库
3. [ ] 推送代码到 GitHub
4. [ ] 创建 Vercel 账号
5. [ ] 导入项目到 Vercel
6. [ ] 配置环境变量
7. [ ] 部署项目
8. [ ] 测试 API
9. [ ] 配置自定义域名
10. [ ] 监控和维护

---

## 成本估算

| 服务 | 免费层 | 付费层 |
|------|--------|--------|
| GitHub | 无限制 | $4/月起 |
| Vercel | 100GB 带宽/月 | $20/月起 |
| 自定义域名 | - | $10-15/年 |
| **总计** | **$0/月** | **$30+/月** |

---

**GitHub + Vercel 部署已准备就绪！** 🚀

按照上述步骤，30 分钟内即可完成部署！
"""
