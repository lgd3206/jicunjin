"""
配置加载器 - 从 .env 文件读取配置
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """配置加载器 - 支持从 .env 文件读取配置"""

    def __init__(self, env_path: Optional[str] = None):
        """
        初始化配置加载器

        Args:
            env_path: .env 文件路径，如果为 None 则在当前目录查找
        """
        if env_path is None:
            # 在当前目录及上级目录查找 .env 文件
            env_path = self._find_env_file()

        self.env_path = env_path
        self.config = {}
        self.load_config()

    def _find_env_file(self) -> str:
        """查找 .env 文件"""
        # 优先查找当前目录
        if os.path.exists('.env'):
            return '.env'

        # 查找上级目录
        parent_dir = Path(__file__).parent.parent
        env_file = parent_dir / '.env'
        if env_file.exists():
            return str(env_file)

        # 如果找不到，返回默认路径
        return '.env'

    def load_config(self):
        """从 .env 文件加载配置"""
        if not os.path.exists(self.env_path):
            raise FileNotFoundError(f".env 文件不存在: {self.env_path}")

        with open(self.env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue

                # 解析 KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # 移除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值或默认值
        """
        return self.config.get(key, default)

    def get_email_config(self) -> Dict[str, str]:
        """获取邮件配置"""
        return {
            'email_type': self.get('EMAIL_TYPE', 'qq'),
            'email_address': self.get('EMAIL_ADDRESS', ''),
            'app_password': self.get('APP_PASSWORD', ''),
        }

    def get_recipient_emails(self) -> list:
        """获取收件人邮箱列表"""
        emails_str = self.get('RECIPIENT_EMAILS', '')
        if not emails_str:
            return []
        return [email.strip() for email in emails_str.split(',')]

    def get_alert_config(self) -> Dict[str, Any]:
        """获取提醒配置"""
        return {
            'drop_threshold_percent': float(self.get('DROP_THRESHOLD_PERCENT', '5.0')),
            'enable_email_notification': self.get('ENABLE_EMAIL_NOTIFICATION', 'true').lower() == 'true',
            'test_mode': self.get('TEST_MODE', 'false').lower() == 'true',
        }

    def get_database_config(self) -> Dict[str, str]:
        """获取数据库配置"""
        return {
            'database_path': self.get('DATABASE_PATH', 'gold_prices.db'),
        }

    def get_log_config(self) -> Dict[str, str]:
        """获取日志配置"""
        return {
            'log_level': self.get('LOG_LEVEL', 'INFO'),
            'log_file': self.get('LOG_FILE', 'logs/notifications.log'),
        }

    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            'email': self.get_email_config(),
            'recipients': self.get_recipient_emails(),
            'alert': self.get_alert_config(),
            'database': self.get_database_config(),
            'log': self.get_log_config(),
        }

    def validate_email_config(self) -> bool:
        """验证邮件配置是否完整"""
        email_config = self.get_email_config()

        if not email_config['email_address']:
            raise ValueError("EMAIL_ADDRESS 未配置")

        if not email_config['app_password']:
            raise ValueError("APP_PASSWORD 未配置")

        if email_config['email_type'] not in ['qq', '163']:
            raise ValueError(f"EMAIL_TYPE 必须是 'qq' 或 '163'，当前值: {email_config['email_type']}")

        return True

    def validate_recipient_emails(self) -> bool:
        """验证收件人邮箱是否配置"""
        recipients = self.get_recipient_emails()

        if not recipients:
            raise ValueError("RECIPIENT_EMAILS 未配置")

        return True

    def __repr__(self) -> str:
        """返回配置信息的字符串表示"""
        email_config = self.get_email_config()
        return (
            f"ConfigLoader(\n"
            f"  env_path={self.env_path}\n"
            f"  email_type={email_config['email_type']}\n"
            f"  email_address={email_config['email_address']}\n"
            f"  recipients={len(self.get_recipient_emails())} 个\n"
            f")"
        )
