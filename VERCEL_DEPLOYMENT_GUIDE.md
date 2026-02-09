"""
🚀 Vercel 部署完整指南 - 一步步部署到 Vercel
"""

# ============================================================================
# 🚀 Vercel 部署完整指南
# ============================================================================

## 📋 部署前准备

### ✅ 已完成的准备工作
- [x] 代码已推送到 GitHub: https://github.com/lgd3206/jicunjin
- [x] vercel.json 配置文件已创建
- [x] API 端点已实现 (api/monitor.py, api/health.py)
- [x] .env.example 配置模板已创建
- [x] requirements.txt 依赖列表已完成

---

## 🎯 Vercel 部署步骤

### 第一步: 创建 Vercel 账号 (5 分钟)

1. **访问 Vercel 官网**
   - 打开 https://vercel.com
   - 点击右上角 "Sign Up"

2. **选择 GitHub 登录**
   - 点击 "Continue with GitHub"
   - 授权 Vercel 访问你的 GitHub 账号

3. **完成注册**
   - 选择免费计划
   - 完成邮箱验证

---

### 第二步: 导入 GitHub 仓库 (5 分钟)

1. **进入 Vercel 控制面板**
   - 登录后进入 https://vercel.com/dashboard

2. **创建新项目**
   - 点击 "Add New..." 按钮
   - 选择 "Project"

3. **导入 GitHub 仓库**
   - 点击 "Import Git Repository"
   - 搜索 "jicunjin" 仓库
   - 点击 "Import"

---

### 第三步: 配置项目 (5 分钟)

1. **项目设置**
   ```
   Project Name: jicunjin
   Framework: Other
   Root Directory: ./
   ```

2. **构建设置**
   ```
   Build Command: pip install -r requirements.txt
   Output Directory: (留空)
   Install Command: (留空)
   ```

3. **环境变量配置** ⭐ 重要

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

---

### 第四步: 部署 (5 分钟)

1. **点击 Deploy 按钮**
   - 所有配置完成后，点击 "Deploy"
   - 等待部署完成 (通常需要 2-5 分钟)

2. **查看部署日志**
   - 在部署过程中可以查看实时日志
   - 如果有错误，会显示在日志中

3. **部署完成**
   - 部署成功后，会显示你的项目 URL
   - 例如: https://jicunjin.vercel.app

---

### 第五步: 验证部署 (5 分钟)

1. **测试健康检查**
   ```bash
   curl https://jicunjin.vercel.app/api/health
   ```

   预期响应:
   ```json
   {
     "status": "healthy",
     "service": "gold-price-monitor",
     "version": "2.0.0"
   }
   ```

2. **测试连接**
   ```bash
   curl https://jicunjin.vercel.app/api/monitor
   ```

   预期响应:
   ```json
   {
     "status": "success",
     "message": "Connection test passed"
   }
   ```

3. **测试邮件发送**
   ```bash
   curl -X POST https://jicunjin.vercel.app/api/monitor \
     -H "Content-Type: application/json" \
     -d '{
       "product_name": "AU9999",
       "current_price": 380.20,
       "should_alert": true,
       "alert_level": "high",
       "alert_reasons": ["当前价格是24小时最低价"],
       "extremes": {
         "highest_price_24h": 385.50,
         "lowest_price_24h": 380.20,
         "price_range": 5.30
       },
       "price_diff": {
         "absolute_difference": 5.30,
         "percentage_difference": 1.38
       },
       "timestamp": "2024-01-15T10:30:00"
     }'
   ```

---

## 📊 部署后的配置

### 1. 自定义域名 (可选)

1. **在 Vercel 中添加域名**
   - 进入项目设置
   - 点击 "Domains"
   - 输入你的域名 (例如: gold-monitor.com)

2. **配置 DNS**
   - 根据 Vercel 提供的 DNS 记录
   - 在你的域名提供商处添加 CNAME 记录

3. **等待 DNS 生效**
   - 通常需要 24-48 小时

### 2. 自动部署配置

Vercel 默认已启用自动部署：
- 当你推送代码到 GitHub 时
- Vercel 会自动检测到更改
- 自动构建和部署新版本

### 3. 环境变量管理

1. **更新环境变量**
   - 进入项目设置
   - 点击 "Environment Variables"
   - 修改或添加新的变量

2. **重新部署**
   - 修改环境变量后
   - 需要重新部署才能生效
   - 点击 "Deployments" → 选择最新部署 → "Redeploy"

---

## 🔧 常见问题

### Q1: 部署失败怎么办？

**检查清单**:
1. 查看部署日志找出错误信息
2. 检查 requirements.txt 是否完整
3. 检查环境变量是否正确配置
4. 检查 Python 版本兼容性

**解决方案**:
- 修复错误后，重新推送到 GitHub
- Vercel 会自动重新部署

### Q2: 如何查看实时日志？

1. 进入项目
2. 点击 "Deployments"
3. 选择最新的部署
4. 点击 "Logs" 查看实时日志

### Q3: 如何回滚到之前的版本？

1. 进入 "Deployments"
2. 找到之前的版本
3. 点击 "..." → "Promote to Production"

### Q4: 如何禁用自动部署？

1. 进入项目设置
2. 点击 "Git"
3. 关闭 "Automatic Deployments"

---

## 📈 部署后的监控

### 1. 查看部署历史

- 进入项目
- 点击 "Deployments"
- 查看所有部署记录

### 2. 监控性能

- 点击 "Analytics"
- 查看请求数、响应时间等指标

### 3. 设置告警

- 点击 "Settings" → "Alerts"
- 配置告警规则

### 4. 查看日志

- 点击 "Logs"
- 查看实时日志

---

## 🎯 部署后的工作流程

### 自动部署流程

```
本地修改代码
    ↓
git add .
git commit -m "Update: description"
git push origin main
    ↓
GitHub 接收推送
    ↓
Vercel 检测到更改
    ↓
自动构建 (2-3 分钟)
    ↓
自动部署 (1-2 分钟)
    ↓
部署完成，API 可用
```

### 调用 API 的方式

**方式 1: 直接调用 Vercel API**
```python
import requests

url = "https://jicunjin.vercel.app/api/monitor"
alert_result = {
    "product_name": "AU9999",
    "current_price": 380.20,
    "should_alert": True,
    ...
}

response = requests.post(url, json=alert_result)
print(response.json())
```

**方式 2: 在自己的服务器上定时调用**
```python
import requests
import time

def call_vercel_api():
    url = "https://jicunjin.vercel.app/api/monitor"
    alert_result = {...}
    response = requests.post(url, json=alert_result)
    return response.json()

# 每 10 分钟调用一次
while True:
    try:
        result = call_vercel_api()
        print(f"✓ API 调用成功: {result}")
    except Exception as e:
        print(f"✗ API 调用失败: {e}")

    time.sleep(600)  # 10 分钟
```

---

## 💡 最佳实践

### 安全性
- ✅ 使用 Vercel 环境变量存储敏感信息
- ✅ 不要在代码中硬编码密码
- ✅ 定期更新授权码
- ✅ 使用 HTTPS

### 可靠性
- ✅ 定期检查部署日志
- ✅ 监控 API 性能
- ✅ 设置告警规则
- ✅ 定期备份配置

### 性能
- ✅ 使用 Vercel 的缓存功能
- ✅ 优化 API 响应时间
- ✅ 监控带宽使用
- ✅ 定期清理日志

---

## 📊 部署成本

| 项目 | 免费层 | 付费层 |
|------|--------|--------|
| 带宽 | 100GB/月 | 按使用量计费 |
| 构建 | 100 次/月 | 按使用量计费 |
| 函数 | 100 小时/月 | 按使用量计费 |
| 存储 | - | $5/月起 |
| **总计** | **$0/月** | **$20+/月** |

---

## ✅ 部署检查清单

### 部署前
- [ ] 代码已推送到 GitHub
- [ ] vercel.json 已创建
- [ ] requirements.txt 已完成
- [ ] .env.example 已创建

### 部署中
- [ ] Vercel 账号已创建
- [ ] GitHub 仓库已导入
- [ ] 环境变量已配置
- [ ] 部署已启动

### 部署后
- [ ] 部署成功
- [ ] API 端点可访问
- [ ] 健康检查通过
- [ ] 邮件发送正常

---

## 🚀 快速部署总结

### 5 分钟快速部署

1. **访问 Vercel**
   ```
   https://vercel.com
   ```

2. **导入仓库**
   ```
   Sign Up → Continue with GitHub → Import jicunjin
   ```

3. **配置环境变量**
   ```
   EMAIL_TYPE=qq
   EMAIL_ADDRESS=your_email@qq.com
   APP_PASSWORD=your_app_password_here
   RECIPIENT_EMAILS=recipient@qq.com
   ```

4. **部署**
   ```
   Click Deploy
   ```

5. **验证**
   ```bash
   curl https://jicunjin.vercel.app/api/health
   ```

---

## 📚 相关文档

- **GITHUB_VERCEL_READY.md** - GitHub+Vercel 部署概览
- **GITHUB_VERCEL_IMPLEMENTATION.md** - 详细实施步骤
- **DEPLOYMENT_PACKAGE.md** - 完整部署指南
- **README.md** - 项目说明

---

## 🎉 部署完成

✅ 代码已推送到 GitHub: https://github.com/lgd3206/jicunjin
✅ 已准备好部署到 Vercel
✅ 所有配置已完成
✅ 系统已可投入使用

---

## 🔗 重要链接

- **GitHub 仓库**: https://github.com/lgd3206/jicunjin
- **Vercel 官网**: https://vercel.com
- **部署后的 API**: https://jicunjin.vercel.app/api/health

---

**立即部署到 Vercel！** 🚀

按照上述步骤，5 分钟内即可完成部署！
"""
