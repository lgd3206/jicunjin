"""
极值价格提醒模块 - 基于24小时极值的智能提醒系统
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager


class ExtremePriceAlert:
    """极值价格提醒系统"""

    def __init__(self, db: DatabaseManager, drop_threshold_percent: float = 5.0):
        """
        初始化极值价格提醒系统

        Args:
            db: 数据库管理器实例
            drop_threshold_percent: 下跌触发阈值（百分比），默认5%
        """
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.drop_threshold_percent = drop_threshold_percent
        self.alert_history = {}  # 存储提醒历史，避免重复提醒

    def get_24h_extremes(self, product_name: str) -> Optional[Dict[str, Any]]:
        """
        获取过去24小时的极值（最高价和最低价）

        Args:
            product_name: 品种名称

        Returns:
            包含极值信息的字典，格式：
            {
                'product_name': str,
                'highest_price_24h': float,  # 24小时最高价
                'lowest_price_24h': float,   # 24小时最低价
                'price_range': float,        # 价格范围
                'data_points': int,          # 数据点数
                'time_range': str            # 时间范围
            }
        """
        try:
            # 获取过去24小时的数据
            history = self.db.get_price_by_product(product_name, hours=24)

            if not history or len(history) == 0:
                self.logger.warning(f"未找到 {product_name} 的24小时数据")
                return None

            prices = [record['price'] for record in history]

            highest_price = max(prices)
            lowest_price = min(prices)
            price_range = highest_price - lowest_price

            return {
                'product_name': product_name,
                'highest_price_24h': round(highest_price, 2),
                'lowest_price_24h': round(lowest_price, 2),
                'price_range': round(price_range, 2),
                'data_points': len(history),
                'time_range': '24小时',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"获取24小时极值失败: {str(e)}")
            return None

    def calculate_price_difference(self, current_price: float, highest_price_24h: float) -> Dict[str, Any]:
        """
        计算当前价格与24小时最高价的差值

        Args:
            current_price: 当前价格
            highest_price_24h: 24小时最高价

        Returns:
            包含差值信息的字典，格式：
            {
                'current_price': float,
                'highest_price_24h': float,
                'absolute_difference': float,  # 绝对差值
                'percentage_difference': float, # 百分比差值
                'is_below_highest': bool       # 是否低于最高价
            }
        """
        absolute_diff = highest_price_24h - current_price
        percentage_diff = (absolute_diff / highest_price_24h * 100) if highest_price_24h != 0 else 0

        return {
            'current_price': round(current_price, 2),
            'highest_price_24h': round(highest_price_24h, 2),
            'absolute_difference': round(absolute_diff, 2),
            'percentage_difference': round(percentage_diff, 2),
            'is_below_highest': current_price < highest_price_24h
        }

    def check_trigger_condition(self, product_name: str, current_price: float) -> Dict[str, Any]:
        """
        检查是否满足触发条件

        触发条件：
        1. 当前价格是过去24小时的最低价
        2. 当前价格比24小时最高价下跌了X%（可配置）

        Args:
            product_name: 品种名称
            current_price: 当前价格

        Returns:
            包含触发判断结果的字典，格式：
            {
                'product_name': str,
                'current_price': float,
                'should_alert': bool,           # 是否需要发送提醒
                'alert_reasons': List[str],     # 触发原因列表
                'extremes': Dict,               # 24小时极值信息
                'price_diff': Dict,             # 价格差值信息
                'alert_level': str              # 提醒等级 ('low', 'medium', 'high')
            }
        """
        try:
            # 获取24小时极值
            extremes = self.get_24h_extremes(product_name)
            if not extremes:
                return {
                    'product_name': product_name,
                    'current_price': current_price,
                    'should_alert': False,
                    'alert_reasons': ['无法获取24小时数据'],
                    'extremes': None,
                    'price_diff': None,
                    'alert_level': 'none'
                }

            # 计算价格差值
            price_diff = self.calculate_price_difference(current_price, extremes['highest_price_24h'])

            alert_reasons = []
            alert_level = 'none'

            # 检查条件1：是否是24小时最低价
            if current_price <= extremes['lowest_price_24h']:
                alert_reasons.append(f"当前价格 {current_price} 是24小时最低价")
                alert_level = 'high'

            # 检查条件2：是否下跌超过阈值
            if price_diff['percentage_difference'] >= self.drop_threshold_percent:
                alert_reasons.append(
                    f"价格从24小时最高价 {extremes['highest_price_24h']} 下跌了 "
                    f"{price_diff['percentage_difference']}%（阈值: {self.drop_threshold_percent}%）"
                )
                if alert_level == 'none':
                    alert_level = 'medium'
                elif alert_level == 'medium':
                    alert_level = 'high'

            should_alert = len(alert_reasons) > 0

            result = {
                'product_name': product_name,
                'current_price': round(current_price, 2),
                'should_alert': should_alert,
                'alert_reasons': alert_reasons,
                'extremes': extremes,
                'price_diff': price_diff,
                'alert_level': alert_level,
                'timestamp': datetime.now().isoformat()
            }

            return result

        except Exception as e:
            self.logger.error(f"检查触发条件失败: {str(e)}")
            return {
                'product_name': product_name,
                'current_price': current_price,
                'should_alert': False,
                'alert_reasons': [f'检查失败: {str(e)}'],
                'extremes': None,
                'price_diff': None,
                'alert_level': 'none'
            }

    def set_drop_threshold(self, threshold_percent: float):
        """
        设置下跌触发阈值

        Args:
            threshold_percent: 下跌百分比阈值
        """
        if threshold_percent < 0:
            self.logger.warning("阈值不能为负数，使用默认值5%")
            self.drop_threshold_percent = 5.0
        else:
            self.drop_threshold_percent = threshold_percent
            self.logger.info(f"已设置下跌触发阈值为: {threshold_percent}%")

    def get_drop_threshold(self) -> float:
        """获取当前的下跌触发阈值"""
        return self.drop_threshold_percent

    def batch_check_alerts(self, products: List[str], current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        批量检查多个品种的提醒条件

        Args:
            products: 品种名称列表
            current_prices: 品种名称到当前价格的映射

        Returns:
            提醒结果列表
        """
        results = []

        for product in products:
            if product not in current_prices:
                self.logger.warning(f"未找到 {product} 的当前价格")
                continue

            current_price = current_prices[product]
            result = self.check_trigger_condition(product, current_price)
            results.append(result)

        return results

    def get_alert_summary(self, alert_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取提醒摘要

        Args:
            alert_results: 提醒结果列表

        Returns:
            提醒摘要信息
        """
        total_alerts = len(alert_results)
        triggered_alerts = [r for r in alert_results if r['should_alert']]
        high_level_alerts = [r for r in triggered_alerts if r['alert_level'] == 'high']
        medium_level_alerts = [r for r in triggered_alerts if r['alert_level'] == 'medium']

        return {
            'total_checked': total_alerts,
            'total_triggered': len(triggered_alerts),
            'high_level': len(high_level_alerts),
            'medium_level': len(medium_level_alerts),
            'triggered_products': [r['product_name'] for r in triggered_alerts],
            'high_level_products': [r['product_name'] for r in high_level_alerts],
            'timestamp': datetime.now().isoformat()
        }

    def format_alert_message(self, alert_result: Dict[str, Any]) -> str:
        """
        格式化提醒消息

        Args:
            alert_result: 提醒结果

        Returns:
            格式化的提醒消息
        """
        if not alert_result['should_alert']:
            return f"{alert_result['product_name']}: 无需提醒"

        message = f"\n{'='*60}\n"
        message += f"🔔 价格提醒 - {alert_result['product_name']}\n"
        message += f"{'='*60}\n"
        message += f"当前价格: {alert_result['current_price']}元/克\n"
        message += f"提醒等级: {alert_result['alert_level'].upper()}\n\n"

        message += "极值信息:\n"
        extremes = alert_result['extremes']
        message += f"  24小时最高价: {extremes['highest_price_24h']}元/克\n"
        message += f"  24小时最低价: {extremes['lowest_price_24h']}元/克\n"
        message += f"  价格范围: {extremes['price_range']}元/克\n\n"

        message += "价格差值:\n"
        price_diff = alert_result['price_diff']
        message += f"  与最高价差值: {price_diff['absolute_difference']}元/克\n"
        message += f"  下跌百分比: {price_diff['percentage_difference']}%\n\n"

        message += "触发原因:\n"
        for i, reason in enumerate(alert_result['alert_reasons'], 1):
            message += f"  {i}. {reason}\n"

        message += f"\n时间: {alert_result['timestamp']}\n"
        message += f"{'='*60}\n"

        return message
