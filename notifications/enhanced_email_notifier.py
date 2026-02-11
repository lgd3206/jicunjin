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
                        {self._generate_futures_section(alert_data)}
                        {self._generate_store_gold_section(alert_data)}
                        {self._generate_recycle_section(alert_data)}
                        {self._generate_reasons_section(alert_data)}
                        {self._generate_tip_section()}
                    </div>

                    <div class="footer">
                        <p>这是一封自动生成的邮件，请勿直接回复。</p>
                        <p>数据来源：聚合数据API + 小小API | 发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
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
        au_td = data.get('au_td')

        if not au9999 and not au_td:
            return ""

        html = '<div class="section"><div class="section-title">🏛️ 上海黄金交易所</div>'

        # Au99.99
        if au9999:
            html += f"""
            <div class="price-card">
                <h4 style="margin-top:0; color:#667eea;">Au99.99</h4>
                <div class="price-row">
                    <span class="label">最新价:</span>
                    <span class="value">{au9999.get('price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">涨跌幅:</span>
                    <span class="value">{au9999.get('change', '0%')}</span>
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
                    <span class="label">成交量:</span>
                    <span class="value">{au9999.get('volume', '0')}</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{au9999.get('update_time', '')}</span>
                </div>
            </div>
            """

        # Au(T+D)
        if au_td:
            html += f"""
            <div class="price-card" style="margin-top:15px;">
                <h4 style="margin-top:0; color:#667eea;">Au(T+D) 黄金延期</h4>
                <div class="price-row">
                    <span class="label">最新价:</span>
                    <span class="value">{au_td.get('price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">涨跌幅:</span>
                    <span class="value">{au_td.get('change', '0%')}</span>
                </div>
                <div class="price-row">
                    <span class="label">开盘价:</span>
                    <span class="value">{au_td.get('open', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最高价:</span>
                    <span class="value">{au_td.get('high', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">最低价:</span>
                    <span class="value">{au_td.get('low', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">成交量:</span>
                    <span class="value">{au_td.get('volume', '0')}</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{au_td.get('update_time', '')}</span>
                </div>
            </div>
            """

        html += '</div>'
        return html

    def _generate_bank_gold_section(self, data: Dict) -> str:
        """生成银行账户金部分"""
        bank_prices = data.get('bank_prices', {})
        if not bank_prices or not any(bank_prices.values()):
            return ""

        html = '<div class="section"><div class="section-title">🏦 银行投资金条价格</div>'

        # 遍历所有银行
        for bank_code, bank_data in bank_prices.items():
            if bank_data:
                html += f"""
                <div class="price-card" style="margin-bottom:10px;">
                    <h4 style="margin-top:0; color:#667eea;">{bank_data['name']}</h4>
                    <div class="price-row">
                        <span class="label">价格:</span>
                        <span class="value">{bank_data['price']} 元/克</span>
                    </div>
                    <div class="price-row">
                        <span class="label">类型:</span>
                        <span class="value">{bank_data['type']}</span>
                    </div>
                </div>
                """

        html += '</div>'
        return html

    def _generate_london_gold_section(self, data: Dict) -> str:
        """生成伦敦金部分（聚合数据API不提供此数据）"""
        return ""

    def _generate_futures_section(self, data: Dict) -> str:
        """生成期货合约部分"""
        futures = data.get('futures_main')
        if not futures:
            return ""

        return f"""
        <div class="section">
            <div class="section-title">📈 上海期货交易所 - 沪金主力合约</div>
            <div class="price-card">
                <div class="price-row">
                    <span class="label">合约名称:</span>
                    <span class="value">{futures.get('name', '沪金主力')}</span>
                </div>
                <div class="price-row">
                    <span class="label">最新价:</span>
                    <span class="value">{futures.get('price', 0)} 元/克</span>
                </div>
                <div class="price-row">
                    <span class="label">涨跌幅:</span>
                    <span class="value">{futures.get('change', '0%')}</span>
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
                    <span class="label">成交量:</span>
                    <span class="value">{futures.get('volume', '0')}</span>
                </div>
                <div class="price-row">
                    <span class="label">更新时间:</span>
                    <span class="value">{futures.get('update_time', '')}</span>
                </div>
            </div>
        </div>
        """

    def _generate_store_gold_section(self, data: Dict) -> str:
        """生成品牌金店价格部分"""
        brand_prices = data.get('brand_prices', [])
        if not brand_prices:
            return ""

        rows = ""
        for item in brand_prices:
            bullion = item.get('bullion_price', '-')
            gold = item.get('gold_price', '-')
            platinum = item.get('platinum_price', '-')

            rows += f"""
            <tr>
                <td>{item.get('brand', '')}</td>
                <td style="color: #667eea; font-weight: bold;">{bullion}</td>
                <td style="color: #f39c12; font-weight: bold;">{gold}</td>
                <td style="color: #95a5a6;">{platinum}</td>
                <td style="font-size: 12px; color: #999;">{item.get('updated_date', '')}</td>
            </tr>
            """

        return f"""
        <div class="section">
            <div class="section-title">💍 品牌金店价格（前5家）</div>
            <table class="table">
                <thead>
                    <tr>
                        <th>品牌</th>
                        <th>金条价</th>
                        <th>黄金价</th>
                        <th>铂金价</th>
                        <th>更新日期</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">
                💡 提示：金店价格包含加工费和品牌溢价，通常高于批发价
            </p>
        </div>
        """

    def _generate_recycle_section(self, data: Dict) -> str:
        """生成黄金回收价格部分"""
        recycle_prices = data.get('recycle_prices', [])
        if not recycle_prices:
            return ""

        rows = ""
        for item in recycle_prices:
            gold_type = item.get('gold_type', '')
            price = item.get('recycle_price', '0')

            # 根据金类型设置不同颜色
            if '24K' in gold_type or '黄金' in gold_type:
                color = '#f39c12'
            elif '18K' in gold_type:
                color = '#e67e22'
            elif '14K' in gold_type:
                color = '#d35400'
            elif '钯金' in gold_type:
                color = '#95a5a6'
            elif '银' in gold_type:
                color = '#bdc3c7'
            else:
                color = '#667eea'

            rows += f"""
            <tr>
                <td>{gold_type}</td>
                <td style="color: {color}; font-weight: bold; font-size: 16px;">{price} 元/克</td>
                <td style="font-size: 12px; color: #999;">{item.get('updated_date', '')}</td>
            </tr>
            """

        return f"""
        <div class="section">
            <div class="section-title">♻️ 黄金回收价格（前5种）</div>
            <table class="table">
                <thead>
                    <tr>
                        <th>品种</th>
                        <th>回收价</th>
                        <th>更新日期</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">
                💡 提示：回收价格仅供参考，实际价格以回收商报价为准
            </p>
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
