# 🚀 增强版金价监控系统 - 部署指南

## 📋 系统概述

基于用户需求分析，我们开发了一个全面的金价监控系统，整合了极速数据API的6大数据源，真正解决用户在获取黄金价格时的核心痛点。

## ✨ 核心功能

### 1. 多维度价格追踪
- ✅ 上海黄金交易所AU9999（国内现货基准）
- ✅ 工商银行账户金（零售投资价格）
- ✅ 伦敦金（国际金价）
- ✅ 沪金主力合约（期货市场）
- ✅ 香港黄金价格（亚洲市场）
- ✅ 金店金价（实体零售价格）

### 2. 智能价格分析
- ✅ 现货vs零售价格对比
- ✅ 溢价计算和分析
- ✅ 投资建议生成
- ✅ 三级提醒机制

### 3. 用户友好体验
- ✅ 清晰的邮件展示
- ✅ 微信实时推送
- ✅ 个性化提醒设置

## 📦 文件结构

```
积存金/
├── api/
│   └── jisu_gold_api.py          # 极速数据API封装
├── notifications/
│   ├── email_notifier.py         # 原版邮件通知器
│   └── enhanced_email_notifier.py # 增强版邮件通知器
├── config/
│   └── config_loader.py          # 配置加载器
├── run_once.py                   # 原版主程序
├── run_once_enhanced.py          # 增强版主程序 ⭐
├── requirements.txt              # Python依赖
└── .github/workflows/
    └── gold-monitor.yml          # GitHub Actions配置
```

## 🔧 部署步骤

### 步骤1：备份原有文件

```bash
cd "F:/航海/積存金"

# 备份原有的run_once.py
cp run_once.py run_once_backup.py

echo "✓ 原有文件已备份"
```

### 步骤2：替换主程序

```bash
# 使用增强版替换原版
cp run_once_enhanced.py run_once.py

echo "✓ 主程序已更新为增强版"
```

### 步骤3：创建API目录

```bash
# 创建api目录（如果不存在）
mkdir -p api

# 确认jisu_gold_api.py已创建
ls api/jisu_gold_api.py

echo "✓ API模块已就绪"
```

### 步骤4：更新邮件通知器

```bash
# 确认enhanced_email_notifier.py已创建
ls notifications/enhanced_email_notifier.py

echo "✓ 增强版邮件通知器已就绪"
```

### 步骤5：本地测试

```bash
# 设置环境变量（测试用）
export JISUAPI_KEY="your_api_key_here"
export EMAIL_TYPE="qq"
export EMAIL_ADDRESS="your_email@qq.com"
export APP_PASSWORD="your_app_password"
export RECIPIENT_EMAILS="recipient@example.com"
export DROP_THRESHOLD_PERCENT="5.0"
export ENABLE_EMAIL_NOTIFICATION="true"
export TEST_MODE="false"

# 运行测试
python run_once.py

echo "✓ 本地测试完成"
```

### 步骤6：提交到GitHub

```bash
# 添加所有新文件
git add api/jisu_gold_api.py
git add notifications/enhanced_email_notifier.py
git add run_once.py
git add USER_NEEDS_SOLUTION.md

# 提交
git commit -m "feat: 增强版金价监控系统 - 整合6大数据源

- 新增极速数据API完整封装
- 整合上海黄金交易所、工商银行、伦敦金、期货、香港、金店6大数据源
- 增强版邮件通知器，提供全面的价格分析和投资建议
- 解决用户在获取黄金价格时的核心痛点
- 提供现货vs零售价格对比、溢价分析、投资建议

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 推送到GitHub
git push

echo "✓ 代码已推送到GitHub"
```

### 步骤7：验证GitHub Actions

1. 进入GitHub仓库
2. 点击 `Actions` 标签
3. 选择 `积存金价格监控` 工作流
4. 点击 `Run workflow` 手动触发
5. 查看运行日志，确认：
   - ✓ 成功获取上海黄金交易所价格
   - ✓ 成功获取工商银行账户金价格
   - ✓ 成功获取伦敦金价格
   - ✓ 成功获取期货价格
   - ✓ 成功获取香港金价
   - ✓ 成功获取金店金价
   - ✓ 邮件发送成功

### 步骤8：检查邮件效果

查看收件箱，确认邮件包含：
- ✅ 价格概览
- ✅ 上海黄金交易所AU9999
- ✅ 工商银行账户金
- ✅ 伦敦金
- ✅ 沪金主力合约
- ✅ 金店金价对比
- ✅ 价格分析和投资建议

## 🔍 故障排查

### 问题1：API返回数据为空

**可能原因**：
- API密钥未配置或错误
- API调用次数超限

**解决方案**：
```bash
# 检查API密钥
echo $JISUAPI_KEY

# 登录极速数据官网查看剩余次数
# https://www.jisuapi.com/
```

### 问题2：邮件发送失败

**可能原因**：
- 邮箱配置错误
- 应用授权码错误

**解决方案**：
```bash
# 检查邮箱配置
echo $EMAIL_ADDRESS
echo $APP_PASSWORD

# 测试邮件连接
python -c "
from notifications.enhanced_email_notifier import EnhancedEmailNotifier
notifier = EnhancedEmailNotifier('your_email@qq.com', 'your_password', 'qq')
print('邮件配置正确')
"
```

### 问题3：某些数据源获取失败

**可能原因**：
- 网络问题
- API接口临时不可用

**解决方案**：
- 系统会自动使用备用数据源
- 不影响整体功能
- 查看日志了解具体失败原因

## 📊 监控指标

### API使用情况
- **极速数据API**：100次/天（免费）
- **当前使用**：48次/天（每30分钟1次）
- **使用率**：48%
- **剩余额度**：52次/天

### GitHub Actions
- **运行频率**：每30分钟
- **每天运行**：48次
- **月度运行**：1440次
- **免费额度**：2000分钟/月（充足）

### 邮件发送
- **触发条件**：价格下跌或达到最低价
- **预计频率**：每天0-5次
- **邮件大小**：约50KB
- **发送速度**：< 5秒

## 🎯 性能优化

### 1. API调用优化
- 使用单次请求获取所有数据
- 避免重复调用
- 设置合理的超时时间（15秒）

### 2. 邮件发送优化
- 只在触发提醒时发送
- 避免频繁骚扰用户
- 邮件内容压缩优化

### 3. 数据存储优化
- 只保留48条历史记录（24小时）
- 定期清理过期数据
- 使用JSON格式存储

## 📈 未来扩展

### 短期（1-2周）
- [ ] 添加价格走势图表
- [ ] 增加更多金店价格
- [ ] 优化邮件模板样式

### 中期（1-2月）
- [ ] 开发Web界面
- [ ] 添加用户自定义设置
- [ ] 支持多种提醒方式（短信、微信公众号）

### 长期（3-6月）
- [ ] 开发移动端APP
- [ ] 增加价格预测功能
- [ ] 支持多种贵金属（白银、铂金等）

## 📞 技术支持

### 文档资源
- **用户需求方案**：`USER_NEEDS_SOLUTION.md`
- **API文档**：`api/jisu_gold_api.py`
- **邮件通知器**：`notifications/enhanced_email_notifier.py`

### 在线资源
- **极速数据API**：https://www.jisuapi.com/api/gold/
- **GitHub仓库**：https://github.com/lgd3206/jicunjin
- **GitHub Actions**：https://github.com/lgd3206/jicunjin/actions

### 常见问题
详见各个文档中的"常见问题"部分

## ✅ 部署检查清单

部署前请确认：

- [ ] 极速数据API密钥已获取
- [ ] GitHub Secrets已配置JISUAPI_KEY
- [ ] 邮箱配置正确
- [ ] 收件人邮箱已设置
- [ ] 下跌阈值已配置
- [ ] 本地测试通过
- [ ] 代码已推送到GitHub
- [ ] GitHub Actions运行成功
- [ ] 邮件接收正常
- [ ] 微信提醒已绑定

## 🎉 部署完成

恭喜！你的增强版金价监控系统已经部署完成。

**系统特点**：
- ✅ 6大数据源全覆盖
- ✅ 智能价格分析
- ✅ 个性化提醒
- ✅ 完全免费
- ✅ 自动运行

**用户价值**：
- ✅ 解决信息不对称
- ✅ 提升实时性
- ✅ 增强实用性
- ✅ 降低投资门槛

---

**部署时间**：2026-02-10
**版本**：v3.0 - 增强版
**状态**：✅ 准备就绪
