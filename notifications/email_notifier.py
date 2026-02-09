"""
邮件通知模块 - 支持 QQ 邮箱和 163 邮箱的 SMTP 邮件发送
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Dict, Any, Optional, List
from datetime import datetime


class EmailNotifier:
    """邮件通知器"""

    # 邮箱配置
    SMTP_CONFIG = {
        'qq': {
            'smtp_server': 'smtp.qq.com',
            'smtp_port': 587,
            'description': 'QQ邮箱'
        },
        '163': {
            'smtp_server': 'smtp.163.com',
            'smtp_port': 587,
            'description': '163邮箱'
        }
    }

    def __init__(self, email_address: str, app_password: str, email_type: str = 'qq'):
        """
        初始化邮件通知器

        Args:
            email_address: 邮箱地址
            app_password: 应用授权码（不是邮箱密码）
            email_type: 邮箱类型 ('qq' 或 '163')
        """
        self.email_address = email_address
        self.app_password = app_password
        self.email_type = email_type.lower()
        self.logger = logging.getLogger(__name__)

        # 验证邮箱类型
        if self.email_type not in self.SMTP_CONFIG:
            raise ValueError(f"不支持的邮箱类型: {email_type}。支持: {list(self.SMTP_CONFIG.keys())}")

        self.smtp_config = self.SMTP_CONFIG[self.email_type]

    def send_alert_email(self, recipient_email: str, alert_result: Dict[str, Any]) -> bool:
        """
        发送价格提醒邮件

        Args:
            recipient_email: 收件人邮箱
            alert_result: 提醒结果字典

        Returns:
            是否发送成功
        """
        try:
            # 生成邮件内容
            subject, html_content = self._generate_email_content(alert_result)

            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')

            # 添加HTML内容
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # 发送邮件
            self._send_smtp(msg, recipient_email)

            self.logger.info(f"✓ 邮件已发送到: {recipient_email}")
            return True

        except Exception as e:
            self.logger.error(f"✗ 邮件发送失败: {str(e)}")
            return False

    def send_batch_emails(self, recipient_emails: List[str], alert_result: Dict[str, Any]) -> Dict[str, bool]:
        """
        批量发送邮件

        Args:
            recipient_emails: 收件人邮箱列表
            alert_result: 提醒结果字典

        Returns:
            发送结果字典 {邮箱: 是否成功}
        """
        results = {}

        for email in recipient_emails:
            results[email] = self.send_alert_email(email, alert_result)

        return results

    def _generate_email_content(self, alert_result: Dict[str, Any]) -> tuple:
        """
        生成邮件内容

        Args:
            alert_result: 提醒结果字典

        Returns:
            (主题, HTML内容)
        """
        product_name = alert_result['product_name']
        current_price = alert_result['current_price']
        alert_level = alert_result['alert_level'].upper()

        # 邮件主题
        subject = f"🔔 {product_name}金价提醒 - {alert_level}"

        # 获取极值信息
        extremes = alert_result['extremes']
        price_diff = alert_result['price_diff']

        # 生成HTML内容
        html_content = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: bold;
                    }}
                    .alert-level {{
                        display: inline-block;
                        background-color: rgba(255,255,255,0.3);
                        padding: 5px 15px;
                        border-radius: 20px;
                        font-size: 14px;
                        margin-top: 10px;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .info-box {{
                        background-color: #f9f9f9;
                        border-left: 4px solid #667eea;
                        padding: 15px;
                        margin-bottom: 20px;
                        border-radius: 4px;
                    }}
                    .info-row {{
                        display: flex;
                        justify-content: space-between;
                        padding: 12px 0;
                        border-bottom: 1px solid #eee;
                    }}
                    .info-row:last-child {{
                        border-bottom: none;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #333;
                        min-width: 120px;
                    }}
                    .value {{
                        color: #667eea;
                        font-weight: bold;
                        font-size: 16px;
                    }}
                    .highlight {{
                        background-color: #fff3cd;
                        padding: 2px 6px;
                        border-radius: 3px;
                    }}
                    .reasons {{
                        background-color: #f0f7ff;
                        border-left: 4px solid #0066cc;
                        padding: 15px;
                        margin-top: 20px;
                        border-radius: 4px;
                    }}
                    .reasons h3 {{
                        margin-top: 0;
                        color: #0066cc;
                    }}
                    .reason-item {{
                        margin: 8px 0;
                        color: #333;
                        padding-left: 20px;
                        position: relative;
                    }}
                    .reason-item:before {{
                        content: "✓";
                        position: absolute;
                        left: 0;
                        color: #0066cc;
                        font-weight: bold;
                    }}
                    .footer {{
                        background-color: #f5f5f5;
                        padding: 20px;
                        text-align: center;
                        font-size: 12px;
                        color: #999;
                        border-top: 1px solid #eee;
                    }}
                    .wechat-tip {{
                        background-color: #e8f5e9;
                        border-left: 4px solid #4caf50;
                        padding: 15px;
                        margin-top: 20px;
                        border-radius: 4px;
                        font-size: 13px;
                        color: #2e7d32;
                    }}
                    .wechat-tip strong {{
                        display: block;
                        margin-bottom: 8px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔔 {product_name}金价提醒</h1>
                        <div class="alert-level">提醒等级: {alert_level}</div>
                    </div>

                    <div class="content">
                        <div class="info-box">
                            <div class="info-row">
                                <span class="label">当前金价:</span>
                                <span class="value">{current_price}元/克</span>
                            </div>
                            <div class="info-row">
                                <span class="label">24小时最高价:</span>
                                <span class="value">{extremes['highest_price_24h']}元/克</span>
                            </div>
                            <div class="info-row">
                                <span class="label">24小时最低价:</span>
                                <span class="value">{extremes['lowest_price_24h']}元/克</span>
                            </div>
                            <div class="info-row">
                                <span class="label">价格范围:</span>
                                <span class="value">{extremes['price_range']}元/克</span>
                            </div>
                            <div class="info-row">
                                <span class="label">与最高价差值:</span>
                                <span class="value highlight">{price_diff['absolute_difference']}元/克 ({price_diff['percentage_difference']}%)</span>
                            </div>
                            <div class="info-row">
                                <span class="label">发送时间:</span>
                                <span class="value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                            </div>
                        </div>

                        <div class="reasons">
                            <h3>触发原因:</h3>
                            {''.join([f'<div class="reason-item">{reason}</div>' for reason in alert_result['alert_reasons']])}
                        </div>

                        <div class="wechat-tip">
                            <strong>💡 微信实时接收提醒:</strong>
                            在微信中搜索"QQ邮箱提醒"小程序或公众号，绑定此邮箱账号，即可在微信上实时接收金价提醒邮件通知。
                        </div>
                    </div>

                    <div class="footer">
                        <p>这是一封自动生成的邮件，请勿直接回复。</p>
                        <p>如有问题，请联系系统管理员。</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return subject, html_content

    def _send_smtp(self, msg: MIMEMultipart, recipient_email: str):
        """
        通过SMTP发送邮件

        Args:
            msg: 邮件对象
            recipient_email: 收件人邮箱
        """
        try:
            # 连接SMTP服务器
            server = smtplib.SMTP(
                self.smtp_config['smtp_server'],
                self.smtp_config['smtp_port'],
                timeout=10
            )

            # 启用TLS加密
            server.starttls()

            # 登录
            server.login(self.email_address, self.app_password)

            # 发送邮件
            server.send_message(msg, from_addr=self.email_address, to_addrs=recipient_email)

            # 关闭连接
            server.quit()

            self.logger.debug(f"SMTP连接已关闭")

        except smtplib.SMTPAuthenticationError:
            raise Exception("邮箱认证失败，请检查邮箱地址和应用授权码")
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP错误: {str(e)}")
        except Exception as e:
            raise Exception(f"邮件发送错误: {str(e)}")

    def test_connection(self) -> bool:
        """
        测试邮件连接

        Returns:
            连接是否成功
        """
        try:
            server = smtplib.SMTP(
                self.smtp_config['smtp_server'],
                self.smtp_config['smtp_port'],
                timeout=10
            )
            server.starttls()
            server.login(self.email_address, self.app_password)
            server.quit()

            self.logger.info(f"✓ {self.smtp_config['description']}连接成功")
            return True

        except Exception as e:
            self.logger.error(f"✗ 连接失败: {str(e)}")
            return False

    @staticmethod
    def get_supported_email_types() -> Dict[str, str]:
        """获取支持的邮箱类型"""
        return {
            key: config['description']
            for key, config in EmailNotifier.SMTP_CONFIG.items()
        }
