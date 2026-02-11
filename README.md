# 积存金价格监控系统

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-brightgreen)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

一个基于 GitHub Actions 的自动化黄金价格监控系统，帮助投资者及时捕捉黄金价格波动，不错过最佳买入时机。

## ✨ 核心特性

### 📊 全面的数据覆盖（6大类数据源）

- **上海黄金交易所**：Au99.99、Au(T+D) 等官方权威数据
- **银行投资金条**：6家主流银行实时金价（工商、建设、中国、农业、浦发、平安）
- **上海期货交易所**：沪金主力合约价格
- **品牌金店价格**：11家知名品牌（周大福、老凤祥等）
- **黄金回收价格**：10种回收类型（24K、18K、14K等）
- **实时价格分析**：24小时最高/最低价、波动幅度分析

### 🎯 智能监控与提醒

- ✅ 自动监控金价波动，每30分钟检查一次
- ✅ 智能分析24小时价格趋势
- ✅ 多条件触发提醒（最低价、下跌阈值、大幅波动）
- ✅ 精美的HTML邮件报告，数据一目了然
- ✅ 完全免费，无需服务器

### 🆚 竞品对比

| 对比项 | 本项目 | 闲鱼竞品（¥3.9/周） |
|--------|--------|---------------------|
| **数据源数量** | 6类数据源 | 仅1类（银行金价） |
| **银行金价** | 6家银行 | 5家银行 |
| **品牌金店** | 11家品牌 | ❌ 无 |
| **回收价格** | 10种类型 | ❌ 无 |
| **官方交易所** | ✅ 上海金交所 + 期货 | ❌ 无 |
| **价格分析** | ✅ 24小时趋势分析 | ❌ 无 |
| **费用** | 🎉 完全免费 | ¥3.9/周 |
| **开源** | ✅ GitHub开源 | ❌ 闭源 |

## 🚀 快速开始

### 前置要求

- GitHub 账号
- 邮箱账号（QQ邮箱或163邮箱）

### 部署步骤

#### 1. Fork 本仓库

点击右上角的 `Fork` 按钮，将项目复制到你的 GitHub 账号下。

#### 2. 配置 GitHub Secrets

进入你的仓库 `Settings` → `Secrets and variables` → `Actions`，添加以下密钥：

| 密钥名称 | 说明 | 示例 |
|---------|------|------|
| `EMAIL_TYPE` | 邮箱类型 | `qq` 或 `163` |
| `EMAIL_ADDRESS` | 发件邮箱地址 | `your_email@qq.com` |
| `APP_PASSWORD` | 邮箱授权码 | `abcdefghijklmnop` |
| `RECIPIENT_EMAILS` | 收件人邮箱（多个用逗号分隔） | `user1@qq.com,user2@163.com` |
| `DROP_THRESHOLD_PERCENT` | 下跌提醒阈值（百分比） | `5` |
| `ENABLE_EMAIL_NOTIFICATION` | 是否启用邮件通知 | `true` |
| `TEST_MODE` | 测试模式（不发送真实邮件） | `false` |

**可选配置**（用于获取更多数据源）：

| 密钥名称 | 说明 | 获取方式 |
|---------|------|---------|
| `JUHE_API_KEY` | 官方数据接口密钥 | 注册获取免费额度 |

#### 3. 获取邮箱授权码

<details>
<summary>QQ邮箱授权码获取方法</summary>

1. 登录 [QQ邮箱网页版](https://mail.qq.com/)
2. 点击 `设置` → `账户`
3. 找到 `POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务`
4. 开启 `IMAP/SMTP服务`
5. 点击 `生成授权码`，按提示操作
6. 复制生成的授权码（16位字符）

</details>

<details>
<summary>163邮箱授权码获取方法</summary>

1. 登录 [163邮箱网页版](https://mail.163.com/)
2. 点击 `设置` → `POP3/SMTP/IMAP`
3. 开启 `IMAP/SMTP服务`
4. 点击 `客户端授权密码`
5. 按提示发送短信验证
6. 复制生成的授权码

</details>

#### 4. 启用 GitHub Actions

1. 进入你的仓库 `Actions` 标签页
2. 点击 `I understand my workflows, go ahead and enable them`
3. 系统将自动开始监控（每30分钟运行一次）

#### 5. 手动测试（可选）

进入 `Actions` → `积存金价格监控` → `Run workflow`，可以手动触发一次运行来测试配置是否正确。

## 📧 邮件提醒示例

当金价满足以下任一条件时，系统会发送邮件提醒：

1. **当前价格是24小时最低价**
2. **价格从最高点下跌超过设定阈值**（默认5%）
3. **24小时价格波动幅度超过2%**

邮件内容包括：
- 📊 当前金价及24小时价格趋势
- 🏦 6家银行投资金条价格对比
- 💍 11家品牌金店价格（周大福、老凤祥等）
- ♻️ 10种黄金回收价格
- 📈 价格分析与投资建议

## ⚙️ 高级配置

### 调整监控频率

编辑 `.github/workflows/gold-monitor.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '*/30 * * * *'  # 每30分钟运行一次
```

常用频率参考：
- 每15分钟：`*/15 * * * *`
- 每小时：`0 * * * *`
- 每天早上9点：`0 9 * * *`

### 自定义提醒阈值

修改 `DROP_THRESHOLD_PERCENT` 密钥的值：
- `3`：价格下跌3%时提醒（更敏感）
- `5`：价格下跌5%时提醒（默认）
- `10`：价格下跌10%时提醒（更保守）

## 📁 项目结构

```
积存金/
├── api/                          # API接口模块
│   ├── juhe_gold_api.py         # 官方数据接口
│   └── xiaoxiao_gold_api.py     # 银行金价接口
├── config/                       # 配置模块
│   └── config_loader.py         # 配置加载器
├── notifications/                # 通知模块
│   └── enhanced_email_notifier.py  # 邮件通知器
├── .github/workflows/           # GitHub Actions工作流
│   └── gold-monitor.yml         # 监控任务配置
├── run_once.py                  # 主程序入口
├── requirements.txt             # Python依赖
└── README.md                    # 项目文档
```

## 🔧 故障排查

### 问题1：没有收到邮件

**可能原因**：
- 邮箱授权码配置错误
- 金价未触发提醒条件
- 邮件被拦截进入垃圾箱

**解决方法**：
1. 检查 GitHub Secrets 中的邮箱配置是否正确
2. 手动触发 workflow 并设置 `force_alert` 为 `true` 进行测试
3. 检查邮箱的垃圾邮件文件夹

### 问题2：GitHub Actions 运行失败

**可能原因**：
- API密钥配置错误或已过期
- 网络连接问题

**解决方法**：
1. 查看 Actions 运行日志，定位具体错误
2. 检查所有 Secrets 配置是否完整
3. 等待几分钟后重试（可能是临时网络问题）

### 问题3：数据不完整

**可能原因**：
- 某些数据源暂时不可用
- API配额已用完

**解决方法**：
- 系统会自动使用备用数据源
- 检查是否配置了可选的API密钥
- 等待下一次运行周期

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 GitHub Actions 提供的免费自动化服务
- 感谢各数据源提供的权威金价数据
- 感谢所有贡献者的支持

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [GitHub Issue](../../issues)
- 发送邮件至项目维护者

---

⭐ 如果这个项目对你有帮助，欢迎点个 Star！
