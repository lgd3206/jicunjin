"""
定时监控脚本 - 每10分钟运行一次，包含防封策略和异常处理
"""
import time
import logging
import random
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import ConfigLoader
from email_alert_integration import EmailAlertIntegration


class ScheduledMonitor:
    """定时监控器 - 每10分钟运行一次"""

    # 常见的 User-Agent 列表，用于防止被识别为爬虫
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
    ]

    def __init__(self, env_path: str = '.env', check_interval: int = 600):
        """
        初始化定时监控器

        Args:
            env_path: .env 文件路径
            check_interval: 检查间隔（秒），默认 600 秒（10 分钟）
        """
        self.env_path = env_path
        self.check_interval = check_interval
        self.logger = self._setup_logger()
        self.config_loader = ConfigLoader(env_path)
        self.email_integration = EmailAlertIntegration(env_path)
        self.run_count = 0
        self.error_count = 0

        self.logger.info("=" * 70)
        self.logger.info("定时监控器已初始化")
        self.logger.info(f"检查间隔: {check_interval} 秒 ({check_interval // 60} 分钟)")
        self.logger.info("=" * 70)

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # 创建日志目录
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # 文件处理器
        file_handler = logging.FileHandler(
            'logs/scheduled_monitor.log',
            encoding='utf-8'
        )
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

    def get_random_user_agent(self) -> str:
        """获取随机 User-Agent"""
        return random.choice(self.USER_AGENTS)

    def get_random_delay(self, min_delay: float = 1.0, max_delay: float = 5.0) -> float:
        """获取随机延时"""
        return random.uniform(min_delay, max_delay)

    def simulate_price_check(self) -> List[Dict[str, Any]]:
        """
        模拟价格检查（实际应用中应从数据库查询）

        Returns:
            提醒结果列表
        """
        # 这是一个模拟函数，实际应用中应该：
        # 1. 从数据库查询最新价格
        # 2. 调用极值提醒系统检查条件
        # 3. 返回需要发送的提醒

        # 模拟提醒结果
        alert_results = [
            {
                'product_name': 'AU9999',
                'current_price': 380.20 + random.uniform(-5, 5),
                'should_alert': random.random() > 0.7,  # 30% 概率触发提醒
                'alert_level': 'high' if random.random() > 0.5 else 'medium',
                'alert_reasons': ['价格波动'],
                'extremes': {
                    'highest_price_24h': 385.50,
                    'lowest_price_24h': 375.00,
                    'price_range': 10.50,
                },
                'price_diff': {
                    'absolute_difference': 5.30,
                    'percentage_difference': 1.38,
                },
                'timestamp': datetime.now().isoformat()
            }
        ]

        return alert_results

    def check_and_send_alerts(self) -> bool:
        """
        检查价格并发送提醒

        Returns:
            是否成功
        """
        try:
            self.logger.info(f"\n[运行 #{self.run_count + 1}] 开始检查价格...")

            # 添加随机延时，防止频繁请求
            delay = self.get_random_delay(1.0, 3.0)
            self.logger.debug(f"添加随机延时: {delay:.2f} 秒")
            time.sleep(delay)

            # 获取随机 User-Agent（如果需要）
            user_agent = self.get_random_user_agent()
            self.logger.debug(f"使用 User-Agent: {user_agent[:50]}...")

            # 检查价格
            alert_results = self.simulate_price_check()
            self.logger.info(f"检查完成，获得 {len(alert_results)} 个结果")

            # 统计需要发送的提醒
            alerts_to_send = [r for r in alert_results if r.get('should_alert')]
            if alerts_to_send:
                self.logger.info(f"检测到 {len(alerts_to_send)} 个需要发送的提醒")

                # 发送邮件
                try:
                    all_results = self.email_integration.send_batch_alerts(alerts_to_send)
                    self.logger.info(f"邮件发送完成: {len(all_results)} 个品种")
                except Exception as e:
                    self.logger.error(f"邮件发送失败: {str(e)}")
                    self.error_count += 1
            else:
                self.logger.info("没有检测到需要发送的提醒")

            self.run_count += 1
            return True

        except Exception as e:
            self.logger.error(f"检查失败: {str(e)}")
            self.logger.exception("详细错误信息:")
            self.error_count += 1
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'run_count': self.run_count,
            'error_count': self.error_count,
            'success_rate': (self.run_count - self.error_count) / max(self.run_count, 1) * 100,
            'uptime': datetime.now().isoformat(),
        }

    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_statistics()
        self.logger.info("\n" + "=" * 70)
        self.logger.info("监控统计信息")
        self.logger.info("=" * 70)
        self.logger.info(f"总运行次数: {stats['run_count']}")
        self.logger.info(f"错误次数: {stats['error_count']}")
        self.logger.info(f"成功率: {stats['success_rate']:.1f}%")
        self.logger.info(f"最后更新: {stats['uptime']}")
        self.logger.info("=" * 70 + "\n")

    def run(self, max_runs: int = None):
        """
        启动定时监控

        Args:
            max_runs: 最大运行次数，None 表示无限运行
        """
        self.logger.info("启动定时监控...")
        self.logger.info(f"检查间隔: {self.check_interval} 秒")
        if max_runs:
            self.logger.info(f"最大运行次数: {max_runs}")
        else:
            self.logger.info("将无限运行，按 Ctrl+C 停止")

        try:
            while True:
                # 检查是否达到最大运行次数
                if max_runs and self.run_count >= max_runs:
                    self.logger.info(f"已达到最大运行次数 ({max_runs})，停止监控")
                    break

                # 执行检查
                self.check_and_send_alerts()

                # 每 10 次运行打印一次统计信息
                if self.run_count % 10 == 0:
                    self.print_statistics()

                # 等待下一次检查
                self.logger.info(f"等待 {self.check_interval} 秒后进行下次检查...")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("\n收到停止信号，正在关闭...")
            self.print_statistics()
            self.logger.info("监控已停止")
        except Exception as e:
            self.logger.error(f"监控异常: {str(e)}")
            self.logger.exception("详细错误信息:")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("定时监控脚本 - 每10分钟运行一次")
    print("=" * 70)

    # 创建监控器
    monitor = ScheduledMonitor(
        env_path='.env.example',  # 使用示例配置
        check_interval=600  # 10 分钟
    )

    # 启动监控（演示模式：运行 3 次）
    print("\n演示模式：将运行 3 次，每次间隔 10 秒")
    print("生产环境：将无限运行，每次间隔 10 分钟")
    print("\n按 Ctrl+C 停止监控\n")

    # 演示模式：运行 3 次，每次间隔 10 秒
    monitor.check_interval = 10  # 演示用：10 秒间隔
    monitor.run(max_runs=3)


if __name__ == "__main__":
    main()
