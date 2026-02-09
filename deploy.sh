#!/bin/bash
# ============================================================================
# 金价监控系统 - Linux/Mac 一键部署脚本
# ============================================================================

set -e

echo ""
echo "============================================================================"
echo "金价监控系统 - Linux/Mac 一键部署脚本"
echo "============================================================================"
echo ""

# 获取当前目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/5] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "✗ 错误: 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi
python3 --version
echo "✓ Python 已安装"

echo ""
echo "[2/5] 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "✓ 虚拟环境已存在"
else
    python3 -m venv venv
    echo "✓ 虚拟环境已创建"
fi

echo ""
echo "[3/5] 激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -q -r requirements.txt
echo "✓ 依赖已安装"

echo ""
echo "[4/5] 配置系统..."
if [ -f ".env" ]; then
    echo "✓ .env 文件已存在"
else
    cp .env.example .env
    echo "✓ .env 文件已创建"
    echo ""
    echo "请编辑 .env 文件，填入以下信息:"
    echo "  - EMAIL_TYPE: qq 或 163"
    echo "  - EMAIL_ADDRESS: 你的邮箱地址"
    echo "  - APP_PASSWORD: 应用授权码"
    echo "  - RECIPIENT_EMAILS: 收件人邮箱"
    echo ""
    read -p "按 Enter 继续..."
fi

echo ""
echo "[5/5] 运行测试..."
python test_email_notification.py
if [ $? -ne 0 ]; then
    echo "✗ 测试失败，请检查配置"
    exit 1
fi
echo "✓ 测试通过"

echo ""
echo "============================================================================"
echo "部署完成！"
echo "============================================================================"
echo ""
echo "下一步:"
echo "1. 编辑 .env 文件，填入邮箱信息"
echo "2. 运行 python scheduled_monitor.py 进行监控"
echo "3. 或使用 cron 设置定时任务"
echo ""
echo "查看日志: tail -f logs/scheduled_monitor.log"
echo ""
