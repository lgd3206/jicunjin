"""
增强版邮件通知模块 - 整合所有金价数据源
为用户提供最全面的金价信息
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Dict, Any, Optional, List
from datetime import datetime


class EnhancedEmailNotifier:
    """增强版邮件通知器 - 支持多数据源金价展示"""

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
        self.email_address = email_address
        self.app_password = app_password
        self.email_type = email_type.lower()
        self.logger = logging.getLogger(__name__)

        if self.email_type not in self.SMTP_CONFIG:
            raise ValueError(f"不支持的邮箱类型: {email_type}")

        self.smtp_config = self.SMTP_CONFIG[self.email_type]

    def send_comprehensive_alert(self, recipient_email: str, alert_data: Dict[str, Any]) -> bool:
        """
        发送综合金价提醒邮件

        Args:
            recipient_email: 收件人邮箱
            alert_data: 包含所有金价数据的字典

        Returns:
            是否发送成功
        """
        try:
            subject, html_content = self._generate_comprehensive_email(alert_data)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')

            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            self._send_smtp(msg, recipient_email)

            self.logger.info(f"✓ 综合金价邮件已发送到: {recipient_email}")
            return True

        except Exception as e:
            self.logger.error(f"✗ 邮件发送失败: {str(e)}")
            return False

    def _generate_comprehensive_email(self, alert_data: Dict[str, Any]) -> tuple:
        """
        生成综合金价邮件内容

        Args:
            alert_data: 包含所有金价数据

        Returns:
            (主题, HTML内容)
        """
        alert_level = alert_data.get('alert_level', 'INFO').upper()
        current_price = alert_data.get('current_price', 0)

        # 邮件主题
        subject = f"🔔 金价提醒 - {alert_level} - {current_price}元/克"

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
                        max-width: 800px;
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
                    .section {{
                        margin-bottom: 30px;
                    }}
                    .section-title {{
                        font-size: 20px;
                        font-weight: bold;
                        color: #333;
                        margin-bottom: 15px;
                        padding-bottom: 10px;
                        border-bottom: 2px solid #667eea;
                    }}
                    .price-card {{
                        background-color: #f9f9f9;
                        border-left: 4px solid #667eea;
                        padding: 15px;
                        margin-bottom: 15px;
                        border-radius: 4px;
                    }}
                    .price-row {{
                        display: flex;
                        justify-content: space-between;
                        padding: 8px 0;
                        border-bottom: 1px solid #eee;
                    }}
                    .price-row:last-child {{
                        border-bottom: none;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #666;
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
                    .table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }}
                    .table th {{
                        background-color: #f0f0f0;
                        padding: 10px;
                        text-align: left;
                        border-bottom: 2px solid #667eea;
                        font-weight: bold;
                    }}
                    .table td {{
                        padding: 10px;
                        border-bottom: 1px solid #eee;
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
                    .tip {{
                        background-color: #e8f5e9;
                        border-left: 4px solid #4caf50;
                        padding: 15px;
                        margin-top: 20px;
                        border-radius: 4px;
                        font-size: 13px;
                        color: #2e7d32;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔔 金价综合提醒</h1>
                        <div class="alert-level">提醒等级: {alert_level}</div>
                    </div>

                    <div class="content">
                        {self._generate_alert_section(alert_data)}
                        {self._generate_shanghai_gold_section(alert_data)}
                        {self._generate_bank_gold_section(alert_data)}
                        {self._generate_london_gold_section(alert_data)}
                        {self._generate_futures_section(alert_data)}
                        {self._generate_store_gold_section(alert_data)}
                        {self._generate_reasons_section(alert_data)}
                        {self._generate_tip_section()}
                    </div>

                    <div class="footer">
                        <p>这是一封自动生成的邮件，请勿直接回复。</p>
                        <p>数据来源：极速数据API | 发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return subject, html_content

    def _generate_alert_section(self, data: Dict) -> str:
        """生成提醒概览部分"""
        current_price = data.get('current_price', 0)
        extremes = data.get('extremes', {})

        return f"""
        <div class="section">
            <div class="section-title">📊 价格概览</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">当前金价:</span>
                    <span class="value">{current_price} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">24小时最高价:</span>
                    <span class="value">{extremes.get('highest_price_24h', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">24小时最低价:</span>
                    <span class="value">{extremes.get('lowest_price_24h', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">价格波动:</span>
                    <span class="value">{extremes.get('price_range', 0)} 元/克</span>
                </div>
            </div>
        </div>
        """

    def _generate_shanghai_gold_section(self, data: Dict) -> str:
        """生成上海黄金交易所部分"""
        au9999 = data.get('au9999')
        if not au9999:
            return ""

        return f"""
        <div class="section">
            <div class="section-title">🏛️ 上海黄金交易所 AU9999</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">最新价:</span>
                    <span class="value">{au9999.get('price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">开盘价:</span>
                    <span class="value">{au9999.get('open', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最高价:</span>
                    <span class="value">{au9999.get('high', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最低价:</span>
                    <span class="value">{au9999.get('low', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{au9999.get('update_time', '')}</span>
                </div>
            </div>
        </div>
        """

    def _generate_bank_gold_section(self, data: Dict) -> str:
        """生成工商银行账户金部分"""
        bank_gold = data.get('bank_gold')
        if not bank_gold:
            return ""

        return f"""
        <div class="section">
            <div class="section-title">🏦 工商银行账户金</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">买入价:</span>
                    <span class="value" style="color: #4caf50;">{bank_gold.get('buy_price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">卖出价:</span>
                    <span class="value" style="color: #f44336;">{bank_gold.get('sell_price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">中间价:</span>
                    <span class="value">{bank_gold.get('mid_price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">今日最高:</span>
                    <span class="value">{bank_gold.get('high', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">今日最低:</span>
                    <span class="value">{bank_gold.get('low', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{bank_gold.get('update_time', '')}</span>
                </div>
            </div>
        </div>
        """

    def _generate_london_gold_section(self, data: Dict) -> str:
        """生成伦敦金部分"""
        london_gold = data.get('london_gold')
        if not london_gold:
            return ""

        return f"""
        <div class="section">
            <div class="section-title">🌍 伦敦金（国际金价）</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">价格:</span>
                    <span class="value">{london_gold.get('price', 0)} 美元/盎司</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{london_gold.get('update_time', '')}</span>
                </div>
            </div>
        </div>
        """

    def _generate_futures_section(self, data: Dict) -> str:
        """生成期货合约部分"""
        futures = data.get('futures_main')
        if not futures:
            return ""

        return f"""
        <div class="section">
            <div class="section-title">📈 沪金主力合约</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">最新价:</span>
                    <span class="value">{futures.get('price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">开盘价:</span>
                    <span class="value">{futures.get('open', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最高价:</span>
                    <span class="value">{futures.get('high', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最低价:</span>
                    <span class="value">{futures.get('low', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{futures.get('update_time', '')}</span>
                </div>
            </div>
        </div>
        """

    def _generate_store_gold_section(self, data: Dict) -> str:
        """生成金店金价部分"""
        stores = data.get('store_gold', [])
        if not stores:
            return ""

        rows = ""
        for store in stores:
            rows += f"""
            <tr>
                <td>{store.get('name', '')}</td>
                <td style="color: #667eea; font-weight: bold;">{store.get('price', 0)} {store.get('unit', '')}</td>
                <td>{store.get('update_time', '')}</td>
            </tr>
            """

        return f"""
        <div class="section">
            <div class="section-title">💍 金店金价（前3家）</div>
            <table class="table">
                <thead>
                    <tr>
                        <th>金店名称</th>
                        <th>价格</th>
                        <th>更新时间</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """

    def _generate_reasons_section(self, data: Dict) -> str:
        """生成触发原因部分"""
        reasons = data.get('alert_reasons', [])
        if not reasons:
            return ""

        reason_items = ''.join([f'<div class="reason-item">{reason}</div>' for reason in reasons])

        return f"""
        <div class="reasons">
            <h3>触发原因:</h3>
            {reason_items}
        </div>
        """

    def _generate_tip_section(self) -> str:
        """生成提示部分"""
        return """
        <div class="tip">
            <strong>💡 微信实时接收提醒:</strong><br>
            在微信中搜索"QQ邮箱提醒"小程序或公众号，绑定此邮箱账号，即可在微信上实时接收金价提醒邮件通知。
        </div>
        """

    def _send_smtp(self, msg: MIMEMultipart, recipient_email: str):
        """通过SMTP发送邮件"""
        try:
            server = smtplib.SMTP(
                self.smtp_config['smtp_server'],
                self.smtp_config['smtp_port'],
                timeout=10
            )
            server.starttls()
            server.login(self.email_address, self.app_password)
            server.send_message(msg, from_addr=self.email_address, to_addrs=recipient_email)
            server.quit()

        except smtplib.SMTPAuthenticationError:
            raise Exception("邮箱认证失败，请检查邮箱地址和应用授权码")
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP错误: {str(e)}")
        except Exception as e:
            raise Exception(f"邮件发送错误: {str(e)}")

    def send_batch_emails(self, recipient_emails: List[str], alert_data: Dict[str, Any]) -> Dict[str, bool]:
        """批量发送邮件"""
        results = {}
        for email in recipient_emails:
            results[email] = self.send_comprehensive_alert(email, alert_data)
        return results
