"""
邮件通知集成脚本 - 将极值提醒与邮件通知结合
"""
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import ConfigLoader
from notifications.email_notifier import EmailNotifier


class EmailAlertIntegration:
    """邮件提醒集成 - 将极值提醒与邮件通知结合"""

    def __init__(self, env_path: str = '.env'):
        """
        初始化邮件提醒集成

        Args:
            env_path: .env 文件路径
        """
        # 加载配置
        self.config_loader = ConfigLoader(env_path)
        self.config = self.config_loader.get_all_config()

        # 设置日志
        self.logger = self._setup_logger()

        # 初始化邮件通知器
        email_config = self.config['email']
        self.email_notifier = EmailNotifier(
            email_address=email_config['email_address'],
            app_password=email_config['app_password'],
            email_type=email_config['email_type']
        )

        self.logger.info("邮件提醒集成已初始化")

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(self.config['log']['log_level'])

        # 创建日志目录
        log_file = self.config['log']['log_file']
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def test_email_connection(self) -> bool:
        """测试邮件连接"""
        self.logger.info("开始测试邮件连接...")
        result = self.email_notifier.test_connection()

        if result:
            self.logger.info("✓ 邮件连接测试成功")
        else:
            self.logger.error("✗ 邮件连接测试失败")

        return result

    def send_alert_emails(self, alert_result: Dict[str, Any]) -> Dict[str, bool]:
        """
        发送提醒邮件

        Args:
            alert_result: 提醒结果字典（来自 ExtremePriceAlert）

        Returns:
            发送结果字典 {邮箱: 是否成功}
        """
        if not self.config['alert']['enable_email_notification']:
            self.logger.warning("邮件通知已禁用，跳过发送")
            return {}

        recipient_emails = self.config['recipients']

        if not recipient_emails:
            self.logger.warning("未配置收件人邮箱")
            return {}

        self.logger.info(f"准备发送提醒邮件到 {len(recipient_emails)} 个收件人")

        # 测试模式：不真正发送邮件
        if self.config['alert']['test_mode']:
            self.logger.info("测试模式已启用，不会真正发送邮件")
            results = {email: True for email in recipient_emails}
            self.logger.info(f"测试模式：模拟发送到 {len(results)} 个收件人")
            return results

        # 批量发送邮件
        results = self.email_notifier.send_batch_emails(recipient_emails, alert_result)

        # 统计结果
        success_count = sum(1 for v in results.values() if v)
        self.logger.info(f"邮件发送完成：成功 {success_count}/{len(results)}")

        return results

    def send_alert_for_product(
        self,
        product_name: str,
        current_price: float,
        alert_result: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        为特定品种发送提醒邮件

        Args:
            product_name: 品种名称
            current_price: 当前价格
            alert_result: 提醒结果字典

        Returns:
            发送结果字典
        """
        self.logger.info(f"处理 {product_name} 的提醒邮件（当前价格: {current_price}元/克）")

        if not alert_result.get('should_alert'):
            self.logger.info(f"{product_name} 不需要发送提醒")
            return {}

        self.logger.info(f"{product_name} 触发提醒条件，准备发送邮件")
        return self.send_alert_emails(alert_result)

    def send_batch_alerts(
        self,
        alert_results: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, bool]]:
        """
        批量发送提醒邮件

        Args:
            alert_results: 提醒结果列表

        Returns:
            发送结果字典 {品种: {邮箱: 是否成功}}
        """
        all_results = {}

        for alert_result in alert_results:
            if alert_result.get('should_alert'):
                product_name = alert_result.get('product_name', '未知品种')
                self.logger.info(f"发送 {product_name} 的提醒邮件")

                results = self.send_alert_emails(alert_result)
                all_results[product_name] = results

        return all_results

    def get_config_summary(self) -> str:
        """获取配置摘要"""
        email_config = self.config['email']
        recipients = self.config['recipients']
        alert_config = self.config['alert']

        summary = f"""
邮件提醒配置摘要
================

邮箱配置:
  - 邮箱类型: {email_config['email_type'].upper()}
  - 邮箱地址: {email_config['email_address']}
  - 应用授权码: {'已配置' if email_config['app_password'] else '未配置'}

收件人配置:
  - 收件人数量: {len(recipients)}
  - 收件人列表: {', '.join(recipients) if recipients else '未配置'}

提醒配置:
  - 下跌阈值: {alert_config['drop_threshold_percent']}%
  - 邮件通知: {'启用' if alert_config['enable_email_notification'] else '禁用'}
  - 测试模式: {'启用' if alert_config['test_mode'] else '禁用'}

数据库配置:
  - 数据库路径: {self.config['database']['database_path']}

日志配置:
  - 日志级别: {self.config['log']['log_level']}
  - 日志文件: {self.config['log']['log_file']}
"""
        return summary


def main():
    """主函数 - 演示如何使用邮件提醒集成"""
    print("=" * 60)
    print("邮件通知集成 - 演示脚本")
    print("=" * 60)

    try:
        # 初始化集成
        integration = EmailAlertIntegration()

        # 显示配置摘要
        print(integration.get_config_summary())

        # 测试邮件连接
        print("\n" + "=" * 60)
        print("测试邮件连接")
        print("=" * 60)
        if integration.test_email_connection():
            print("✓ 邮件连接测试成功！")
        else:
            print("✗ 邮件连接测试失败，请检查配置")
            return

        # 演示发送提醒邮件
        print("\n" + "=" * 60)
        print("演示发送提醒邮件")
        print("=" * 60)

        # 模拟一个提醒结果
        demo_alert_result = {
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

        print("\n模拟提醒结果:")
        print(f"  品种: {demo_alert_result['product_name']}")
        print(f"  当前价格: {demo_alert_result['current_price']}元/克")
        print(f"  提醒等级: {demo_alert_result['alert_level'].upper()}")
        print(f"  触发原因: {', '.join(demo_alert_result['alert_reasons'])}")

        # 发送邮件
        print("\n准备发送邮件...")
        results = integration.send_alert_emails(demo_alert_result)

        if results:
            print("\n邮件发送结果:")
            for email, success in results.items():
                status = "✓ 成功" if success else "✗ 失败"
                print(f"  {email}: {status}")
        else:
            print("未发送任何邮件（可能是测试模式或未配置收件人）")

        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
