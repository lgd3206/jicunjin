"""
邮件通知系统 - 测试脚本
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import ConfigLoader
from notifications.email_notifier import EmailNotifier
from email_alert_integration import EmailAlertIntegration


def test_config_loader():
    """测试配置加载器"""
    print("\n" + "=" * 60)
    print("测试 1: 配置加载器")
    print("=" * 60)

    try:
        config_loader = ConfigLoader('.env.example')
        print("✓ 配置加载成功")

        # 显示配置
        all_config = config_loader.get_all_config()
        print(f"\n邮件配置:")
        print(f"  - 邮箱类型: {all_config['email']['email_type']}")
        print(f"  - 邮箱地址: {all_config['email']['email_address']}")

        print(f"\n收件人配置:")
        print(f"  - 收件人数量: {len(all_config['recipients'])}")

        print(f"\n提醒配置:")
        print(f"  - 下跌阈值: {all_config['alert']['drop_threshold_percent']}%")
        print(f"  - 邮件通知: {'启用' if all_config['alert']['enable_email_notification'] else '禁用'}")
        print(f"  - 测试模式: {'启用' if all_config['alert']['test_mode'] else '禁用'}")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def test_email_notifier():
    """测试邮件通知器"""
    print("\n" + "=" * 60)
    print("测试 2: 邮件通知器初始化")
    print("=" * 60)

    try:
        config_loader = ConfigLoader('.env.example')
        email_config = config_loader.get_email_config()

        # 创建邮件通知器
        notifier = EmailNotifier(
            email_address=email_config['email_address'],
            app_password=email_config['app_password'],
            email_type=email_config['email_type']
        )

        print("✓ 邮件通知器初始化成功")
        print(f"  - 邮箱类型: {notifier.email_type}")
        print(f"  - SMTP服务器: {notifier.smtp_config['smtp_server']}")
        print(f"  - SMTP端口: {notifier.smtp_config['smtp_port']}")

        # 获取支持的邮箱类型
        supported_types = EmailNotifier.get_supported_email_types()
        print(f"\n支持的邮箱类型:")
        for email_type, description in supported_types.items():
            print(f"  - {email_type}: {description}")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False


def test_email_content_generation():
    """测试邮件内容生成"""
    print("\n" + "=" * 60)
    print("测试 3: 邮件内容生成")
    print("=" * 60)

    try:
        config_loader = ConfigLoader('.env.example')
        email_config = config_loader.get_email_config()

        notifier = EmailNotifier(
            email_address=email_config['email_address'],
            app_password=email_config['app_password'],
            email_type=email_config['email_type']
        )

        # 模拟提醒结果
        alert_result = {
            'product_name': 'AU9999',
            'current_price': 380.20,
            'alert_level': 'high',
            'extremes': {
                'highest_price_24h': 385.50,
                'lowest_price_24h': 380.20,
                'price_range': 5.30,
            },
            'price_diff': {
                'absolute_difference': 5.30,
                'percentage_difference': 1.38,
            },
            'alert_reasons': [
                '当前价格是24小时最低价',
                '价格下跌超过5%'
            ]
        }

        # 生成邮件内容
        subject, html_content = notifier._generate_email_content(alert_result)

        print("✓ 邮件内容生成成功")
        print(f"\n邮件主题: {subject}")
        print(f"HTML内容长度: {len(html_content)} 字符")

        # 检查HTML内容是否包含关键信息
        checks = [
            ('品种名称', 'AU9999' in html_content),
            ('当前价格', '380.20' in html_content),
            ('最高价', '385.50' in html_content),
            ('最低价', '380.20' in html_content),
            ('价格差值', '5.30' in html_content),
            ('提醒等级', 'HIGH' in html_content),
            ('触发原因', '最低价' in html_content),
        ]

        print("\n邮件内容检查:")
        all_passed = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
            if not result:
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试邮件提醒集成"""
    print("\n" + "=" * 60)
    print("测试 4: 邮件提醒集成")
    print("=" * 60)

    try:
        integration = EmailAlertIntegration('.env.example')
        print("✓ 邮件提醒集成初始化成功")

        # 显示配置摘要
        summary = integration.get_config_summary()
        print(summary)

        return True

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_alerts():
    """测试批量提醒"""
    print("\n" + "=" * 60)
    print("测试 5: 批量提醒处理")
    print("=" * 60)

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
                'should_alert': False,
                'alert_level': 'none',
                'alert_reasons': [],
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
            }
        ]

        print(f"处理 {len(alert_results)} 个提醒结果...")

        # 批量发送
        results = integration.send_batch_alerts(alert_results)

        print(f"✓ 批量处理完成")
        print(f"  - 需要发送提醒的品种: {len(results)}")

        for product_name, email_results in results.items():
            print(f"  - {product_name}: {len(email_results)} 个收件人")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("邮件通知系统 - 完整测试套件")
    print("=" * 60)

    tests = [
        ("配置加载器", test_config_loader),
        ("邮件通知器初始化", test_email_notifier),
        ("邮件内容生成", test_email_content_generation),
        ("邮件提醒集成", test_integration),
        ("批量提醒处理", test_batch_alerts),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} 测试异常: {str(e)}")
            results.append((test_name, False))

    # 显示测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {test_name}")

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
