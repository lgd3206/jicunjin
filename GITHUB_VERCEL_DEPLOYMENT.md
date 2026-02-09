"""
GitHub + Vercel 部署指南
"""

# ============================================================================
# 🚀 GitHub + Vercel 部署指南
# ============================================================================

## 📋 部署架构

```
本地项目
    ↓
GitHub 仓库
    ↓
Vercel 自动部署
    ↓
在线服务
```

---

## 第一步: 准备 GitHub 仓库

### 1.1 创建 GitHub 账号

访问 https://github.com 创建账号（如果还没有的话）

### 1.2 创建新仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `gold-price-monitor` (或其他名称)
   - Description: `金价自动化监控与提醒系统`
   - Public (公开) 或 Private (私有)
   - 勾选 "Add a README file"
4. 点击 "Create repository"

### 1.3 初始化本地 Git

```bash
cd F:\航海\積存金

# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/gold-price-monitor.git

# 验证远程仓库
git remote -v
```

### 1.4 创建 .gitignore 文件

```bash
# 创建 .gitignore 文件
cat > .gitignore << 'EOF'
# 虚拟环境
venv/
env/
ENV/

# Python 缓存
__pycache__/
*.py[cod]
*$py.class
*.so

# 依赖
.Python
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

# 操作系统
.DS_Store
Thumbs.db

# 敏感信息
.env
.env.local
.env.*.local
*.key
*.pem

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

# 其他
.cache/
.pytest_cache/
.coverage
htmlcov/
EOF
```

### 1.5 推送代码到 GitHub

```bash
# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: Gold price monitoring system"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 第二步: 配置 Vercel 部署

### 2.1 创建 Vercel 账号

1. 访问 https://vercel.com
2. 点击 "Sign Up"
3. 选择 "Continue with GitHub"
4. 授权 Vercel 访问你的 GitHub 账号

### 2.2 导入项目到 Vercel

1. 登录 Vercel
2. 点击 "Add New..." → "Project"
3. 选择 "Import Git Repository"
4. 搜索并选择 `gold-price-monitor` 仓库
5. 点击 "Import"

### 2.3 配置 Vercel 项目

#### 项目设置

```
Project Name: gold-price-monitor
Framework Preset: Other
Root Directory: ./
```

#### 环境变量

点击 "Environment Variables"，添加以下变量：

```
EMAIL_TYPE=qq
EMAIL_ADDRESS=your_email@qq.com
APP_PASSWORD=your_app_password_here
RECIPIENT_EMAILS=recipient@qq.com
DROP_THRESHOLD_PERCENT=5.0
ENABLE_EMAIL_NOTIFICATION=true
TEST_MODE=false
DATABASE_PATH=gold_prices.db
LOG_LEVEL=INFO
LOG_FILE=logs/notifications.log
```

#### 构建设置

```
Build Command: (留空或 npm run build)
Output Directory: (留空)
Install Command: pip install -r requirements.txt
```

### 2.4 部署

点击 "Deploy" 按钮，Vercel 会自动部署你的项目。

---

## 第三步: 创建 Vercel 配置文件

### 3.1 创建 vercel.json

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".",
  "env": {
    "EMAIL_TYPE": "@email_type",
    "EMAIL_ADDRESS": "@email_address",
    "APP_PASSWORD": "@app_password",
    "RECIPIENT_EMAILS": "@recipient_emails",
    "DROP_THRESHOLD_PERCENT": "5.0",
    "ENABLE_EMAIL_NOTIFICATION": "true",
    "TEST_MODE": "false",
    "DATABASE_PATH": "gold_prices.db",
    "LOG_LEVEL": "INFO",
    "LOG_FILE": "logs/notifications.log"
  },
  "functions": {
    "api/monitor.py": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

### 3.2 创建 API 端点

创建 `api/monitor.py`：

```python
"""
Vercel Serverless Function - 金价监控 API
"""
from http.server import BaseHTTPRequestHandler
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from email_alert_integration import EmailAlertIntegration


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 初始化集成
            integration = EmailAlertIntegration('.env')

            # 测试连接
            if integration.test_email_connection():
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success", "message": "Connection test passed"}')
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Connection test failed"}')

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(f'{{"status": "error", "message": "{str(e)}"}}'.encode())

    def do_POST(self):
        """处理 POST 请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # 初始化集成
            integration = EmailAlertIntegration('.env')

            # 发送邮件
            import json
            alert_result = json.loads(body)
            results = integration.send_alert_emails(alert_result)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "Email sent successfully",
                "results": results
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(f'{{"status": "error", "message": "{str(e)}"}}'.encode())
```

---

## 第四步: 更新 GitHub 仓库

### 4.1 添加新文件

```bash
# 添加 vercel.json
git add vercel.json

# 添加 api/monitor.py
git add api/monitor.py

# 提交更改
git commit -m "Add Vercel configuration and API endpoint"

# 推送到 GitHub
git push origin main
```

### 4.2 Vercel 自动部署

当你推送代码到 GitHub 时，Vercel 会自动检测到更改并重新部署。

---

## 第五步: 配置自定义域名（可选）

### 5.1 在 Vercel 中添加域名

1. 登录 Vercel
2. 选择你的项目
3. 点击 "Settings" → "Domains"
4. 输入你的域名（例如 `gold-monitor.com`）
5. 按照提示配置 DNS 记录

### 5.2 配置 DNS

根据 Vercel 提供的 DNS 记录，在你的域名提供商处添加：

```
CNAME: your-project.vercel.app
```

---

## 第六步: 监控和维护

### 6.1 查看部署日志

1. 登录 Vercel
2. 选择你的项目
3. 点击 "Deployments"
4. 选择最新的部署
5. 查看构建日志和运行日志

### 6.2 设置环境变量

1. 点击 "Settings" → "Environment Variables"
2. 添加或更新环境变量
3. 重新部署项目

### 6.3 配置自动部署

Vercel 默认会在以下情况自动部署：
- 推送到 main 分支
- 创建 Pull Request
- 手动触发部署

---

## 常见问题

### Q1: Vercel 支持 Python 吗？

**A**: 是的，Vercel 支持 Python Serverless Functions。但 Vercel 主要针对 Web 应用优化，对于长时间运行的任务（如定时监控），建议使用其他方案。

### Q2: 如何在 Vercel 上运行定时任务？

**A**: Vercel 不支持长时间运行的后台任务。建议使用以下方案：

1. **Vercel Cron Functions** (需要 Pro 计划)
2. **AWS Lambda + CloudWatch Events**
3. **Google Cloud Functions + Cloud Scheduler**
4. **自己的服务器 + cron**

### Q3: 如何保存数据库文件？

**A**: Vercel 的文件系统是临时的，不适合保存持久化数据。建议使用：

1. **MongoDB Atlas** (免费层)
2. **Firebase Realtime Database**
3. **Supabase** (PostgreSQL)
4. **自己的服务器**

### Q4: 如何处理敏感信息？

**A**: 使用 Vercel 的环境变量功能：

1. 在 Vercel 控制面板中设置环境变量
2. 不要在代码中硬编码敏感信息
3. 使用 `.env.example` 作为模板
4. 在 `.gitignore` 中排除 `.env` 文件

---

## 推荐的完整部署方案

### 方案 A: Vercel + 自己的服务器（推荐）

```
GitHub 仓库
    ↓
Vercel (Web API)
    ↓
自己的服务器 (定时监控)
    ↓
调用 Vercel API 发送邮件
```

**优点**:
- 充分利用 Vercel 的 Web 功能
- 定时任务在自己的服务器上运行
- 成本低，可靠性高

**实现步骤**:
1. 在 Vercel 上部署 API 端点
2. 在自己的服务器上运行 `scheduled_monitor.py`
3. 修改 `scheduled_monitor.py` 调用 Vercel API

### 方案 B: Vercel + AWS Lambda

```
GitHub 仓库
    ↓
Vercel (Web API)
    ↓
AWS Lambda (定时任务)
    ↓
CloudWatch Events (触发器)
```

**优点**:
- 完全云端部署
- 自动扩展
- 按使用量付费

**缺点**:
- 配置复杂
- 成本可能较高

### 方案 C: Vercel + Render

```
GitHub 仓库
    ↓
Vercel (Web API)
    ↓
Render (后台服务)
    ↓
定时监控
```

**优点**:
- 简单易用
- 免费层支持
- 与 GitHub 集成良好

**缺点**:
- 免费层有限制
- 性能不如 AWS

---

## 快速部署步骤总结

### 1. 本地准备
```bash
cd F:\航海\積存金
git init
git add .
git commit -m "Initial commit"
```

### 2. GitHub 推送
```bash
git remote add origin https://github.com/YOUR_USERNAME/gold-price-monitor.git
git branch -M main
git push -u origin main
```

### 3. Vercel 部署
1. 访问 https://vercel.com
2. 点击 "Import Project"
3. 选择 GitHub 仓库
4. 配置环境变量
5. 点击 "Deploy"

### 4. 配置定时任务
- 在自己的服务器上运行 `scheduled_monitor.py`
- 或使用 Vercel Cron Functions (Pro 计划)

---

## 部署后的验证

### 1. 检查部署状态
```bash
# 访问 Vercel 控制面板
https://vercel.com/dashboard
```

### 2. 测试 API
```bash
# 测试连接
curl https://your-project.vercel.app/api/monitor

# 发送邮件
curl -X POST https://your-project.vercel.app/api/monitor \
  -H "Content-Type: application/json" \
  -d '{"product_name": "AU9999", "current_price": 380.20}'
```

### 3. 查看日志
```bash
# 在 Vercel 控制面板中查看实时日志
```

---

## 成本估算

| 服务 | 免费层 | 付费层 |
|------|--------|--------|
| Vercel | 100GB 带宽/月 | $20/月起 |
| GitHub | 无限制 | $4/月起 |
| 自己的服务器 | - | $5-50/月 |
| AWS Lambda | 100万次请求/月 | 按使用量计费 |
| MongoDB Atlas | 512MB 存储 | 按使用量计费 |

**推荐方案成本**: $0-10/月 (使用免费层)

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
9. [ ] 配置定时任务
10. [ ] 监控和维护

---

**GitHub + Vercel 部署方案已准备就绪！** 🚀
"""
