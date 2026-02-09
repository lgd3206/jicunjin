"""
🚀 Vercel 自动部署配置 - 完整的部署自动化方案
"""

# ============================================================================
# 🚀 Vercel 自动部署配置
# ============================================================================

## 📋 部署自动化方案

### ✅ 已配置的自动部署

1. **GitHub 推送自动触发**
   - 当你推送代码到 GitHub 时
   - Vercel 会自动检测到更改
   - 自动构建和部署新版本

2. **环境变量自动加载**
   - vercel.json 中已配置环境变量
   - Vercel 会自动从控制面板读取
   - 无需手动配置

3. **API 端点自动部署**
   - api/monitor.py 自动部署为 API 端点
   - api/health.py 自动部署为健康检查
   - 无需额外配置

---

## 🎯 Vercel 部署后的工作流程

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

### 部署后的 API 调用

**方式 1: 直接调用 Vercel API**
```python
import requests

def send_alert_via_vercel(alert_result):
    url = "https://jicunjin.vercel.app/api/monitor"

    try:
        response = requests.post(url, json=alert_result, timeout=10)
        result = response.json()

        if result.get('status') == 'success':
            print(f"✓ 邮件已发送: {result}")
            return True
        else:
            print(f"✗ 发送失败: {result}")
            return False
    except Exception as e:
        print(f"✗ API 调用失败: {e}")
        return False

# 使用示例
alert_result = {
    'product_name': 'AU9999',
    'current_price': 380.20,
    'should_alert': True,
    'alert_level': 'high',
    'alert_reasons': ['当前价格是24小时最低价'],
    'extremes': {
        'highest_price_24h': 385.50,
        'lowest_price_24h': 380.20,
        'price_range': 5.30,
    },
    'price_diff': {
        'absolute_difference': 5.30,
        'percentage_difference': 1.38,
    },
    'timestamp': '2024-01-15T10:30:00'
}

send_alert_via_vercel(alert_result)
```

**方式 2: 定时调用 Vercel API**
```python
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VercelAlertClient:
    def __init__(self, api_url="https://jicunjin.vercel.app/api/monitor"):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.timeout = 10

    def send_alert(self, alert_result):
        """发送单个提醒"""
        try:
            response = self.session.post(self.api_url, json=alert_result)
            result = response.json()

            if result.get('status') == 'success':
                logger.info(f"✓ 邮件已发送: {alert_result['product_name']}")
                return True
            else:
                logger.error(f"✗ 发送失败: {result}")
                return False
        except Exception as e:
            logger.error(f"✗ API 调用失败: {e}")
            return False

    def send_batch_alerts(self, alert_results):
        """批量发送提醒"""
        results = {}
        for alert in alert_results:
            product_name = alert.get('product_name', '未知')
            success = self.send_alert(alert)
            results[product_name] = success

        return results

    def monitor_loop(self, check_interval=600):
        """定时监控循环"""
        logger.info(f"启动定时监控，检查间隔: {check_interval} 秒")

        while True:
            try:
                # 这里应该调用你的极值提醒系统获取提醒结果
                # alert_results = get_alert_results()
                # self.send_batch_alerts(alert_results)

                logger.info(f"下次检查时间: {check_interval} 秒后")
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logger.info("监控已停止")
                break
            except Exception as e:
                logger.error(f"监控异常: {e}")
                time.sleep(check_interval)

# 使用示例
if __name__ == "__main__":
    client = VercelAlertClient()

    # 发送单个提醒
    alert = {
        'product_name': 'AU9999',
        'current_price': 380.20,
        'should_alert': True,
        'alert_level': 'high',
        'alert_reasons': ['当前价格是24小时最低价'],
        'extremes': {
            'highest_price_24h': 385.50,
            'lowest_price_24h': 380.20,
            'price_range': 5.30,
        },
        'price_diff': {
            'absolute_difference': 5.30,
            'percentage_difference': 1.38,
        },
        'timestamp': '2024-01-15T10:30:00'
    }

    client.send_alert(alert)

    # 或启动定时监控
    # client.monitor_loop(check_interval=600)  # 每 10 分钟检查一次
```

---

## 📊 部署后的监控

### 1. 查看部署历史

```
1. 进入 Vercel 控制面板
2. 选择 jicunjin 项目
3. 点击 "Deployments"
4. 查看所有部署记录
```

### 2. 监控 API 性能

```
1. 点击 "Analytics"
2. 查看以下指标:
   - 请求数
   - 响应时间
   - 错误率
   - 带宽使用
```

### 3. 查看实时日志

```
1. 点击 "Logs"
2. 查看实时日志输出
3. 搜索特定的错误或事件
```

### 4. 设置告警规则

```
1. 点击 "Settings" → "Alerts"
2. 配置告警规则:
   - 部署失败时告警
   - 错误率过高时告警
   - 响应时间过长时告警
```

---

## 🔧 常见部署问题

### 问题 1: 部署失败

**症状**: 部署过程中出现错误

**解决方案**:
1. 查看部署日志找出错误信息
2. 检查 requirements.txt 是否完整
3. 检查环境变量是否正确配置
4. 修复错误后重新推送到 GitHub
5. Vercel 会自动重新部署

### 问题 2: API 无法访问

**症状**: 调用 API 时返回 404 或超时

**解决方案**:
1. 检查部署是否成功
2. 检查 API 端点 URL 是否正确
3. 检查环境变量是否已设置
4. 查看 Vercel 日志找出错误

### 问题 3: 邮件发送失败

**症状**: API 返回成功但邮件未收到

**解决方案**:
1. 检查邮箱配置是否正确
2. 验证授权码是否过期
3. 检查收件人邮箱地址
4. 查看 Vercel 日志找出错误

### 问题 4: 环境变量未生效

**症状**: 修改环境变量后 API 仍使用旧值

**解决方案**:
1. 修改环境变量后需要重新部署
2. 进入 "Deployments"
3. 选择最新部署
4. 点击 "..." → "Redeploy"

---

## 💡 部署最佳实践

### 安全性
- ✅ 使用 Vercel 环境变量存储敏感信息
- ✅ 不要在代码中硬编码密码
- ✅ 定期更新授权码
- ✅ 使用 HTTPS 调用 API

### 可靠性
- ✅ 定期检查部署日志
- ✅ 监控 API 性能指标
- ✅ 设置告警规则
- ✅ 定期备份配置

### 性能
- ✅ 使用 Vercel 的缓存功能
- ✅ 优化 API 响应时间
- ✅ 监控带宽使用
- ✅ 定期清理日志

### 维护
- ✅ 定期更新依赖包
- ✅ 监控系统性能
- ✅ 记录系统变更
- ✅ 文档化自定义配置

---

## 📈 部署后的成本

| 项目 | 免费层 | 付费层 |
|------|--------|--------|
| 带宽 | 100GB/月 | 按使用量计费 |
| 构建 | 100 次/月 | 按使用量计费 |
| 函数 | 100 小时/月 | 按使用量计费 |
| 存储 | - | $5/月起 |
| **总计** | **$0/月** | **$20+/月** |

---

## ✅ 部署后检查清单

### 部署验证
- [ ] 部署成功
- [ ] API 端点可访问
- [ ] 健康检查通过
- [ ] 邮件发送正常

### 功能验证
- [ ] 邮件通知工作正常
- [ ] 环境变量已生效
- [ ] 日志记录正常
- [ ] 错误处理正常

### 监控配置
- [ ] 告警规则已设置
- [ ] 日志收集已启用
- [ ] 性能监控已启用
- [ ] 备份策略已制定

---

## 🚀 部署后的工作流程

### 日常工作流程

```
1. 本地开发
   - 修改代码
   - 运行测试
   - 验证功能

2. 推送到 GitHub
   - git add .
   - git commit -m "Update: description"
   - git push origin main

3. Vercel 自动部署
   - 检测到推送
   - 自动构建
   - 自动部署

4. 验证部署
   - 检查部署日志
   - 测试 API 端点
   - 监控性能指标
```

### 定时监控工作流程

```
1. 在自己的服务器上运行定时任务
   - 每 10 分钟检查一次
   - 调用 Vercel API 发送邮件

2. 监控 Vercel 部署
   - 定期检查部署日志
   - 监控 API 性能
   - 检查错误率

3. 定期维护
   - 更新依赖包
   - 优化代码性能
   - 备份配置文件
```

---

## 📚 相关文档

- **VERCEL_DEPLOYMENT_GUIDE.md** - Vercel 部署完整指南
- **GITHUB_VERCEL_READY.md** - GitHub+Vercel 部署概览
- **DEPLOYMENT_PACKAGE.md** - 完整部署指南
- **README.md** - 项目说明

---

## 🎉 部署完成

✅ 代码已推送到 GitHub
✅ Vercel 已准备好部署
✅ 自动部署已配置
✅ 监控已设置

---

## 🔗 重要链接

- **GitHub 仓库**: https://github.com/lgd3206/jicunjin
- **Vercel 官网**: https://vercel.com
- **部署后的 API**: https://jicunjin.vercel.app/api/health

---

**立即部署到 Vercel！** 🚀

按照 VERCEL_DEPLOYMENT_GUIDE.md 中的步骤，5 分钟内即可完成部署！
"""
