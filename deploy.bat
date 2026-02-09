@echo off
REM ============================================================================
REM 金价监控系统 - Windows 一键部署脚本
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo 金价监控系统 - Windows 一键部署脚本
echo ============================================================================
echo.

REM 获取当前目录
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)
echo ✓ Python 已安装

echo.
echo [2/5] 创建虚拟环境...
if exist venv (
    echo ✓ 虚拟环境已存在
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ✗ 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境已创建
)

echo.
echo [3/5] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ✗ 错误: 安装依赖失败
    pause
    exit /b 1
)
echo ✓ 依赖已安装

echo.
echo [4/5] 配置系统...
if exist .env (
    echo ✓ .env 文件已存在
) else (
    copy .env.example .env >nul
    echo ✓ .env 文件已创建
    echo.
    echo 请编辑 .env 文件，填入以下信息:
    echo   - EMAIL_TYPE: qq 或 163
    echo   - EMAIL_ADDRESS: 你的邮箱地址
    echo   - APP_PASSWORD: 应用授权码
    echo   - RECIPIENT_EMAILS: 收件人邮箱
    echo.
    pause
)

echo.
echo [5/5] 运行测试...
python test_email_notification.py
if errorlevel 1 (
    echo ✗ 测试失败，请检查配置
    pause
    exit /b 1
)
echo ✓ 测试通过

echo.
echo ============================================================================
echo 部署完成！
echo ============================================================================
echo.
echo 下一步:
echo 1. 编辑 .env 文件，填入邮箱信息
echo 2. 运行 scheduled_monitor.py 进行监控
echo 3. 或使用任务计划程序设置定时任务
echo.
echo 查看日志: type logs\scheduled_monitor.log
echo.
pause
