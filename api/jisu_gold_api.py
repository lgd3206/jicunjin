"""
极速数据API金价数据获取模块 - 完整版
整合所有金价数据源，为用户提供最全面的金价信息
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


class JisuGoldAPI:
    """极速数据黄金价格API封装"""

    def __init__(self, appkey: str, logger: Optional[logging.Logger] = None):
        self.appkey = appkey
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = 'https://api.jisuapi.com/gold'

    def _request(self, endpoint: str) -> Optional[Dict]:
        """统一的API请求方法"""
        try:
            url = f'{self.base_url}/{endpoint}?appkey={self.appkey}'
            resp = requests.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                if data.get('status') == 0:
                    return data.get('result')
                else:
                    self.logger.warning(f"{endpoint} API返回异常: {data.get('msg')}")
            else:
                self.logger.warning(f"{endpoint} HTTP状态码异常: {resp.status_code}")

        except Exception as e:
            self.logger.warning(f"{endpoint} 请求失败: {e}")

        return None

    def fetch_shanghai_gold(self) -> Optional[List[Dict]]:
        """
        获取上海黄金交易所价格
        包含：AU9999、黄金995、黄金延期、迷你黄金延期等
        """
        result = self._request('shgold')
        if result:
            self.logger.info(f"✓ 上海黄金交易所: 获取 {len(result)} 个品种")
            return result
        return None

    def fetch_shanghai_futures(self) -> Optional[List[Dict]]:
        """
        获取上海期货交易所价格
        包含：沪金主力合约、各月合约
        """
        result = self._request('shfutures')
        if result:
            self.logger.info(f"✓ 上海期货交易所: 获取 {len(result)} 个合约")
            return result
        return None

    def fetch_hongkong_gold(self) -> Optional[List[Dict]]:
        """获取香港黄金价格"""
        result = self._request('hkgold')
        if result:
            self.logger.info(f"✓ 香港黄金价格: 获取成功")
            return result
        return None

    def fetch_bank_gold(self) -> Optional[List[Dict]]:
        """
        获取银行账户黄金价格
        包含：工商银行人民币/美元账户金、银、铂金、钯金
        """
        result = self._request('bank')
        if result:
            self.logger.info(f"✓ 银行账户金价: 获取 {len(result)} 个品种")
            return result
        return None

    def fetch_london_gold(self) -> Optional[List[Dict]]:
        """获取伦敦金、银价格"""
        result = self._request('london')
        if result:
            self.logger.info(f"✓ 伦敦金银价格: 获取成功")
            return result
        return None

    def fetch_store_gold(self) -> Optional[List[Dict]]:
        """获取金店金价"""
        result = self._request('store')
        if result:
            self.logger.info(f"✓ 金店金价: 获取 {len(result)} 家金店")
            return result
        return None

    def fetch_all_gold_prices(self) -> Dict[str, Any]:
        """
        获取所有金价数据

        Returns:
            包含所有数据源的字典
        """
        self.logger.info("=" * 60)
        self.logger.info("开始获取所有金价数据...")
        self.logger.info("=" * 60)

        all_data = {
            'shanghai_gold': self.fetch_shanghai_gold(),
            'shanghai_futures': self.fetch_shanghai_futures(),
            'hongkong_gold': self.fetch_hongkong_gold(),
            'bank_gold': self.fetch_bank_gold(),
            'london_gold': self.fetch_london_gold(),
            'store_gold': self.fetch_store_gold(),
            'timestamp': datetime.now().isoformat()
        }

        # 统计成功获取的数据源
        success_count = sum(1 for v in all_data.values() if v is not None and v != all_data['timestamp'])
        self.logger.info("=" * 60)
        self.logger.info(f"数据获取完成: {success_count}/6 个数据源成功")
        self.logger.info("=" * 60)

        return all_data

    def get_key_prices(self) -> Dict[str, Any]:
        """
        获取关键金价数据（用于邮件提醒）

        Returns:
            精简的关键数据
        """
        all_data = self.fetch_all_gold_prices()

        key_prices = {
            'timestamp': all_data['timestamp'],
            'au9999': None,  # 上海黄金交易所AU9999
            'bank_gold': None,  # 工商银行账户金
            'london_gold': None,  # 伦敦金
            'futures_main': None,  # 沪金主力合约
            'store_gold': []  # 金店金价（前3家）
        }

        # 提取AU9999价格
        if all_data['shanghai_gold'] and isinstance(all_data['shanghai_gold'], list):
            for item in all_data['shanghai_gold']:
                if isinstance(item, dict) and 'AU9999' in str(item.get('variety', '')):
                    try:
                        key_prices['au9999'] = {
                            'name': item.get('variety', 'AU9999'),
                            'price': float(item.get('latestpri', 0)),
                            'open': float(item.get('openpri', 0)),
                            'high': float(item.get('maxpri', 0)),
                            'low': float(item.get('minpri', 0)),
                            'update_time': item.get('time', '')
                        }
                        break
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析AU9999数据失败: {e}")
                        continue

        # 提取工商银行账户金
        if all_data['bank_gold'] and isinstance(all_data['bank_gold'], list):
            for item in all_data['bank_gold']:
                if isinstance(item, dict) and item.get('typename') == '人民币账户黄金':
                    try:
                        key_prices['bank_gold'] = {
                            'name': '工商银行账户金',
                            'buy_price': float(item.get('buyprice', 0)),
                            'sell_price': float(item.get('sellprice', 0)),
                            'mid_price': float(item.get('midprice', 0)),
                            'high': float(item.get('maxprice', 0)),
                            'low': float(item.get('minprice', 0)),
                            'update_time': item.get('updatetime', '')
                        }
                        break
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析工商银行数据失败: {e}")
                        continue

        # 提取伦敦金价格
        if all_data['london_gold'] and isinstance(all_data['london_gold'], list):
            for item in all_data['london_gold']:
                if isinstance(item, dict) and '伦敦金' in str(item.get('variety', '')):
                    try:
                        key_prices['london_gold'] = {
                            'name': item.get('variety', '伦敦金'),
                            'price': float(item.get('price', 0)),
                            'update_time': item.get('time', '')
                        }
                        break
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析伦敦金数据失败: {e}")
                        continue

        # 提取沪金主力合约
        if all_data['shanghai_futures'] and isinstance(all_data['shanghai_futures'], list):
            for item in all_data['shanghai_futures']:
                if isinstance(item, dict) and '主力' in str(item.get('variety', '')):
                    try:
                        key_prices['futures_main'] = {
                            'name': item.get('variety', '沪金主力'),
                            'price': float(item.get('latestpri', 0)),
                            'open': float(item.get('openpri', 0)),
                            'high': float(item.get('maxpri', 0)),
                            'low': float(item.get('minpri', 0)),
                            'update_time': item.get('time', '')
                        }
                        break
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析期货数据失败: {e}")
                        continue

        # 提取金店金价（前3家）
        if all_data['store_gold'] and isinstance(all_data['store_gold'], list):
            for item in all_data['store_gold'][:3]:
                if isinstance(item, dict):
                    try:
                        key_prices['store_gold'].append({
                            'name': item.get('name', ''),
                            'price': float(item.get('price', 0)),
                            'unit': item.get('unit', '元/克'),
                            'update_time': item.get('time', '')
                        })
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析金店数据失败: {e}")
                        continue

        return key_prices


# 使用示例
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 替换为你的API密钥
    api = JisuGoldAPI('YOUR_API_KEY', logger)

    # 获取所有金价数据
    all_data = api.fetch_all_gold_prices()

    # 获取关键金价数据
    key_prices = api.get_key_prices()

    print("\n" + "=" * 60)
    print("关键金价数据:")
    print("=" * 60)

    if key_prices['au9999']:
        print(f"\n📊 上海黄金交易所 AU9999")
        print(f"   价格: {key_prices['au9999']['price']} 元/克")
        print(f"   最高: {key_prices['au9999']['high']} 元/克")
        print(f"   最低: {key_prices['au9999']['low']} 元/克")

    if key_prices['bank_gold']:
        print(f"\n🏦 工商银行账户金")
        print(f"   买入: {key_prices['bank_gold']['buy_price']} 元/克")
        print(f"   卖出: {key_prices['bank_gold']['sell_price']} 元/克")

    if key_prices['london_gold']:
        print(f"\n🌍 伦敦金")
        print(f"   价格: {key_prices['london_gold']['price']} 美元/盎司")

    if key_prices['store_gold']:
        print(f"\n💍 金店金价 (前3家)")
        for store in key_prices['store_gold']:
            print(f"   {store['name']}: {store['price']} {store['unit']}")
