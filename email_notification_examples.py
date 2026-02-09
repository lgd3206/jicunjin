"""
邮件通知系统 - 完整集成示例
演示如何将邮件通知与极值提醒系统完整集成
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import ConfigLoader
from email_alert_integration import EmailAlertIntegration


def example_1_basic_email_sending():
    """示例 1: 基础邮件发送"""
    print("\n" + "=" * 70)
    print("示例 1: 基础邮件发送")
    print("=" * 70)

    try:
        # 初始化集成
        integration = EmailAlertIntegration('.env.example')

        # 模拟一个提醒结果
        alert_result = {
            'product_name': 'AU9999',
            'current_price': 380.20,
            'should_alert': True,
            'alert_level': 'high',
            'alert_reasons': [
                '当前价格是24小时最低价',
                '价格下跌超过5%'
            ],
            'extremes': {
                'highest_price_24h': 385.50,
                'lowest_price_24h': 380.20,
                'price_range': 5.30,
                'data_points': 48
            },
            'price_diff': {
                'absolute_difference': 5.30,
                'percentage_difference': 1.38,
                'is_below_highest': True
            },
            'timestamp': '2024-01-15T10:30:00'
        }

        print("\n提醒信息:")
        print(f"  品种: {alert_result['product_name']}")
        print(f"  当前价格: {alert_result['current_price']}元/克")
        print(f"  提醒等级: {alert_result['alert_level'].upper()}")
        print(f"  触发原因: {', '.join(alert_result['alert_reasons'])}")

        # 发送邮件
        print("\n发送邮件...")
        results = integration.send_alert_emails(alert_result)

        if results:
            print(f"✓ 邮件发送完成")
            for email, success in results.items():
                status = "✓ 成功" if success else "✗ 失败"
                print(f"  {email}: {status}")
        else:
            print("未发送任何邮件（可能是测试模式或未配置收件人）")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


def example_2_batch_alerts():
    """示例 2: 批量提醒处理"""
    print("\n" + "=" * 70)
    print("示例 2: 批量提醒处理")
    print("=" * 70)

    try:
        integration = EmailAlertIntegration('.env.example')

        # 模拟多个提醒结果
        alert_results = [
            {
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
            },
            {
                'product_name': 'AU100G',
                'current_price': 3800.00,
                'should_alert': True,
                'alert_level': 'medium',
                'alert_reasons': ['价格下跌超过5%'],
                'extremes': {
                    'highest_price_24h': 3850.00,
                    'lowest_price_24h': 3800.00,
                    'price_range': 50.00,
                },
                'price_diff': {
                    'absolute_difference': 50.00,
                    'percentage_difference': 1.30,
                },
                'timestamp': '2024-01-15T10:30:00'
            },
            {
                'product_name': 'AU50G',
                'current_price': 1900.00,
                'should_alert': False,
                'alert_level': 'none',
                'alert_reasons': [],
                'extremes': {
                    'highest_price_24h': 1920.00,
                    'lowest_price_24h': 1900.00,
                    'price_range': 20.00,
                },
                'price_diff': {
                    'absolute_difference': 20.00,
                    'percentage_difference': 1.04,
                },
                'timestamp': '2024-01-15T10:30:00'
            }
        ]

        print(f"\n处理 {len(alert_results)} 个提醒结果...")

        # 显示提醒摘要
        print("\n提醒摘要:")
        for alert in alert_results:
            status = "✓ 需要提醒" if alert['should_alert'] else "✗ 无需提醒"
            print(f"  {status} | {alert['product_name']:8} | 价格: {alert['current_price']:8.2f} | 等级: {alert['alert_level']}")

        # 批量发送
        print("\n批量发送邮件...")
        all_results = integration.send_batch_alerts(alert_results)

        print(f"\n✓ 批量处理完成")
        print(f"  需要发送提醒的品种: {len(all_results)}")

        for product_name, email_results in all_results.items():
            success_count = sum(1 for v in email_results.values() if v)
            print(f"  {product_name}: {success_count}/{len(email_results)} 个收件人")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


def example_3_configuration_management():
    """示例 3: 配置管理"""
    print("\n" + "=" * 70)
    print("示例 3: 配置管理")
    print("=" * 70)

    try:
        # 加载配置
        config_loader = ConfigLoader('.env.example')

        print("\n配置信息:")

        # 邮件配置
        email_config = config_loader.get_email_config()
        print(f"\n邮件配置:")
        print(f"  邮箱类型: {email_config['email_type'].upper()}")
        print(f"  邮箱地址: {email_config['email_address']}")
        print(f"  授权码: {'已配置' if email_config['app_password'] else '未配置'}")

        # 收件人配置
        recipients = config_loader.get_recipient_emails()
        print(f"\n收件人配置:")
        print(f"  收件人数量: {len(recipients)}")
        for i, email in enumerate(recipients, 1):
            print(f"  {i}. {email}")

        # 提醒配置
        alert_config = config_loader.get_alert_config()
        print(f"\n提醒配置:")
        print(f"  下跌阈值: {alert_config['drop_threshold_percent']}%")
        print(f"  邮件通知: {'启用' if alert_config['enable_email_notification'] else '禁用'}")
        print(f"  测试模式: {'启用' if alert_config['test_mode'] else '禁用'}")

        # 数据库配置
        db_config = config_loader.get_database_config()
        print(f"\n数据库配置:")
        print(f"  数据库路径: {db_config['database_path']}")

        # 日志配置
        log_config = config_loader.get_log_config()
        print(f"\n日志配置:")
        print(f"  日志级别: {log_config['log_level']}")
        print(f"  日志文件: {log_config['log_file']}")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


def example_4_connection_testing():
    """示例 4: 连接测试"""
    print("\n" + "=" * 70)
    print("示例 4: 连接测试")
    print("=" * 70)

    try:
        integration = EmailAlertIntegration('.env.example')

        print("\n测试邮件连接...")
        if integration.test_email_connection():
            print("✓ 邮件连接测试成功！")
            print("  系统已准备好发送邮件")
        else:
            print("✗ 邮件连接测试失败")
            print("  请检查以下内容:")
            print("  1. 邮箱地址是否正确")
            print("  2. 应用授权码是否正确")
            print("  3. 网络连接是否正常")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


def example_5_error_handling():
    """示例 5: 错误处理"""
    print("\n" + "=" * 70)
    print("示例 5: 错误处理")
    print("=" * 70)

    print("\n演示各种错误处理场景...")

    # 场景 1: 配置文件不存在
    print("\n场景 1: 配置文件不存在")
    try:
        config_loader = ConfigLoader('nonexistent.env')
    except FileNotFoundError as e:
        print(f"✓ 正确捕获错误: {str(e)}")

    # 场景 2: 邮件配置不完整
    print("\n场景 2: 邮件配置不完整")
    try:
        config_loader = ConfigLoader('.env.example')
        # 模拟不完整的配置
        config_loader.config['EMAIL_ADDRESS'] = ''
        config_loader.validate_email_config()
    except ValueError as e:
        print(f"✓ 正确捕获错误: {str(e)}")

    # 场景 3: 收件人未配置
    print("\n场景 3: 收件人未配置")
    try:
        config_loader = ConfigLoader('.env.example')
        # 模拟未配置收件人
        config_loader.config['RECIPIENT_EMAILS'] = ''
        config_loader.validate_recipient_emails()
    except ValueError as e:
        print(f"✓ 正确捕获错误: {str(e)}")

    print("\n✓ 所有错误处理场景演示完成")


def example_6_workflow_integration():
    """示例 6: 完整工作流集成"""
    print("\n" + "=" * 70)
    print("示例 6: 完整工作流集成")
    print("=" * 70)

    print("\n这个示例展示如何在实际应用中集成邮件通知系统")
    print("\n工作流步骤:")
    print("  1. 初始化系统")
    print("  2. 加载配置")
    print("  3. 测试连接")
    print("  4. 检查极值提醒")
    print("  5. 发送邮件通知")
    print("  6. 记录日志")

    try:
        # 步骤 1: 初始化系统
        print("\n[步骤 1] 初始化系统...")
        integration = EmailAlertIntegration('.env.example')
        print("✓ 系统初始化完成")

        # 步骤 2: 加载配置
        print("\n[步骤 2] 加载配置...")
        config = integration.config
        print(f"✓ 配置加载完成 (收件人: {len(config['recipients'])})")

        # 步骤 3: 测试连接
        print("\n[步骤 3] 测试连接...")
        if integration.test_email_connection():
            print("✓ 连接测试成功")
        else:
            print("✗ 连接测试失败")
            return

        # 步骤 4: 检查极值提醒
        print("\n[步骤 4] 检查极值提醒...")
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
        print(f"✓ 检测到提醒: {alert_result['product_name']} (等级: {alert_result['alert_level']})")

        # 步骤 5: 发送邮件通知
        print("\n[步骤 5] 发送邮件通知...")
        results = integration.send_alert_emails(alert_result)
        if results:
            success_count = sum(1 for v in results.values() if v)
            print(f"✓ 邮件发送完成 ({success_count}/{len(results)} 成功)")
        else:
            print("✓ 邮件发送完成 (测试模式)")

        # 步骤 6: 记录日志
        print("\n[步骤 6] 记录日志...")
        print(f"✓ 日志已记录到: {config['log']['log_file']}")

        print("\n✓ 完整工作流执行成功！")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "=" * 70)
    print("邮件通知系统 - 完整集成示例")
    print("=" * 70)

    examples = [
        ("基础邮件发送", example_1_basic_email_sending),
        ("批量提醒处理", example_2_batch_alerts),
        ("配置管理", example_3_configuration_management),
        ("连接测试", example_4_connection_testing),
        ("错误处理", example_5_error_handling),
        ("完整工作流集成", example_6_workflow_integration),
    ]

    print("\n可用的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n运行所有示例...")

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ 示例执行失败: {str(e)}")

    print("\n" + "=" * 70)
    print("所有示例执行完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
