"""
小小API - 银行金价数据获取模块
提供银行投资金条、黄金回收、品牌金店价格数据
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


class XiaoxiaoGoldAPI:
    """小小API黄金价格封装 - 完全免费"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = 'https://v2.xxapi.cn/api/goldprice'

    def fetch_all_gold_prices(self) -> Optional[Dict[str, Any]]:
        """
        获取所有金价数据

        Returns:
            包含银行金条、回收价格、品牌金店的字典
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            # 禁用SSL验证，添加重试
            resp = requests.get(
                self.base_url,
                headers=headers,
                timeout=15,
                verify=False  # 禁用SSL验证
            )

            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 200:
                    result = data.get('data', {})

                    # 统计数据
                    bank_count = len(result.get('bank_gold_bar_price', []))
                    recycle_count = len(result.get('gold_recycle_price', []))
                    brand_count = len(result.get('precious_metal_price', []))

                    self.logger.info(f"✓ 小小API: 获取成功")
                    self.logger.info(f"  - 银行金条: {bank_count} 家")
                    self.logger.info(f"  - 回收价格: {recycle_count} 种")
                    self.logger.info(f"  - 品牌金店: {brand_count} 家")

                    return result
                else:
                    self.logger.warning(f"小小API返回异常: {data.get('msg')}")
            else:
                self.logger.warning(f"小小API HTTP状态码异常: {resp.status_code}")

        except Exception as e:
            self.logger.warning(f"小小API请求失败: {e}")

        return None

    def get_bank_gold_prices(self) -> List[Dict[str, Any]]:
        """
        获取银行投资金条价格

        Returns:
            银行金条价格列表
        """
        all_data = self.fetch_all_gold_prices()
        if all_data:
            return all_data.get('bank_gold_bar_price', [])
        return []

    def get_recycle_prices(self) -> List[Dict[str, Any]]:
        """
        获取黄金回收价格

        Returns:
            回收价格列表
        """
        all_data = self.fetch_all_gold_prices()
        if all_data:
            return all_data.get('gold_recycle_price', [])
        return []

    def get_brand_prices(self) -> List[Dict[str, Any]]:
        """
        获取品牌金店价格

        Returns:
            品牌金店价格列表
        """
        all_data = self.fetch_all_gold_prices()
        if all_data:
            return all_data.get('precious_metal_price', [])
        return []

    def get_key_bank_prices(self) -> Dict[str, Any]:
        """
        获取关键银行金价（用于邮件提醒）

        Returns:
            精简的关键银行数据
        """
        bank_prices = self.get_bank_gold_prices()

        key_banks = {
            'icbc': None,  # 工商银行
            'ccb': None,   # 建设银行
            'boc': None,   # 中国银行
            'abc': None,   # 农业银行
            'spdb': None,  # 浦发银行
            'pingan': None # 平安银行
        }

        for item in bank_prices:
            bank_name = item.get('bank', '')
            price = float(item.get('price', 0))

            if '工商银行' in bank_name or '工行' in bank_name:
                key_banks['icbc'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 工商银行金条: {price} 元/克")

            elif '建设银行' in bank_name or '建行' in bank_name:
                key_banks['ccb'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 建设银行金条: {price} 元/克")

            elif '中国银行' in bank_name or '中行' in bank_name:
                key_banks['boc'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 中国银行金条: {price} 元/克")

            elif '农业银行' in bank_name or '农行' in bank_name:
                key_banks['abc'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 农业银行金条: {price} 元/克")

            elif '浦发银行' in bank_name or '浦发' in bank_name:
                key_banks['spdb'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 浦发银行金条: {price} 元/克")

            elif '平安' in bank_name:
                key_banks['pingan'] = {
                    'name': bank_name,
                    'price': price,
                    'type': '投资金条'
                }
                self.logger.info(f"✓ 平安银行金条: {price} 元/克")

        return key_banks


# 使用示例
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 创建API实例（无需密钥）
    api = XiaoxiaoGoldAPI(logger)

    # 获取所有金价数据
    all_data = api.fetch_all_gold_prices()

    if all_data:
        print("\n" + "=" * 60)
        print("银行投资金条价格:")
        print("=" * 60)
        for item in all_data.get('bank_gold_bar_price', []):
            print(f"{item['bank']}: {item['price']} 元/克")

        print("\n" + "=" * 60)
        print("品牌金店价格（前5家）:")
        print("=" * 60)
        for item in all_data.get('precious_metal_price', [])[:5]:
            print(f"{item['brand']}: 金条 {item['bullion_price']} | 黄金 {item['gold_price']} 元/克")

        print("\n" + "=" * 60)
        print("关键银行金价:")
        print("=" * 60)
        key_banks = api.get_key_bank_prices()
        for bank_code, data in key_banks.items():
            if data:
                print(f"{data['name']}: {data['price']} 元/克")
