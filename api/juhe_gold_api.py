"""
聚合数据API金价数据获取模块
提供上海黄金交易所和上海期货交易所的黄金价格数据
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


class JuheGoldAPI:
    """聚合数据黄金价格API封装"""

    def __init__(self, api_key: str, logger: Optional[logging.Logger] = None):
        self.api_key = api_key
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = 'http://web.juhe.cn/finance/gold'

    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """统一的API请求方法"""
        try:
            url = f'{self.base_url}/{endpoint}'
            request_params = {'key': self.api_key}
            if params:
                request_params.update(params)

            resp = requests.get(url, params=request_params, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                if data.get('resultcode') == '200':
                    return data.get('result')
                else:
                    error_code = data.get('error_code', 'unknown')
                    reason = data.get('reason', '未知错误')
                    self.logger.warning(f"{endpoint} API返回异常: [{error_code}] {reason}")
            else:
                self.logger.warning(f"{endpoint} HTTP状态码异常: {resp.status_code}")

        except Exception as e:
            self.logger.warning(f"{endpoint} 请求失败: {e}")

        return None

    def fetch_shanghai_gold(self) -> Optional[List[Dict]]:
        """
        获取上海黄金交易所价格
        包含：Au99.99、Au(T+D)、Ag(T+D)等品种
        """
        result = self._request('shgold')
        if result and isinstance(result, list) and len(result) > 0:
            # 聚合数据返回的是一个包含字典的列表，字典的key是数字
            gold_list = []
            first_item = result[0]
            if isinstance(first_item, dict):
                for key, value in first_item.items():
                    if isinstance(value, dict):
                        gold_list.append(value)

            if gold_list:
                self.logger.info(f"✓ 上海黄金交易所: 获取 {len(gold_list)} 个品种")
                return gold_list

        self.logger.warning("✗ 上海黄金交易所: 数据获取失败")
        return None

    def fetch_shanghai_futures(self) -> Optional[List[Dict]]:
        """
        获取上海期货交易所价格
        包含：沪金主力合约、各月合约

        返回数据格式：
        {
            "name": "黄金2406",
            "latestpri": "520.50",
            "change": "+2.50",
            "buypri": "520.48",
            "buyvol": "10",
            "sellpri": "520.52",
            "sellvol": "8",
            "tradvol": "12345",
            "open": "518.00",
            "lastclear": "518.00",
            "maxpri": "521.00",
            "minpri": "517.50",
            "position": "45678",
            "zengcang": "+123",
            "time": "2024-01-15 15:30:00"
        }
        """
        result = self._request('shfutures')
        if result and isinstance(result, list) and len(result) > 0:
            # 聚合数据返回的是一个包含字典的列表，字典的key是数字
            futures_list = []
            first_item = result[0]
            if isinstance(first_item, dict):
                for key, value in first_item.items():
                    if isinstance(value, dict):
                        # 只保留黄金期货，过滤掉白银期货
                        name = value.get('name', '')
                        if '黄金' in name or 'AU' in name.upper() or 'au' in name:
                            futures_list.append(value)

            if futures_list:
                self.logger.info(f"✓ 上海期货交易所: 获取 {len(futures_list)} 个黄金合约")
                return futures_list
            else:
                self.logger.warning("✗ 上海期货交易所: 未找到黄金合约数据")
                return None

        self.logger.warning("✗ 上海期货交易所: 数据获取失败")
        return None

    def fetch_all_gold_prices(self) -> Dict[str, Any]:
        """
        获取所有金价数据

        Returns:
            包含所有数据源的字典
        """
        self.logger.info("=" * 60)
        self.logger.info("开始获取聚合数据金价信息...")
        self.logger.info("=" * 60)

        all_data = {
            'shanghai_gold': self.fetch_shanghai_gold(),
            'shanghai_futures': self.fetch_shanghai_futures(),
            'timestamp': datetime.now().isoformat()
        }

        # 统计成功获取的数据源
        success_count = sum(1 for k, v in all_data.items() if k != 'timestamp' and v is not None)
        self.logger.info("=" * 60)
        self.logger.info(f"数据获取完成: {success_count}/2 个数据源成功")
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
            'au9999': None,  # 上海黄金交易所Au99.99
            'au_td': None,   # 黄金延期Au(T+D)
            'futures_main': None,  # 沪金主力合约
        }

        # 提取Au99.99价格
        if all_data['shanghai_gold'] and isinstance(all_data['shanghai_gold'], list):
            for item in all_data['shanghai_gold']:
                if isinstance(item, dict):
                    variety = str(item.get('variety', ''))
                    # 查找Au99.99
                    if 'Au99.99' in variety or 'AU99.99' in variety or '99.99' in variety:
                        try:
                            key_prices['au9999'] = {
                                'name': item.get('variety', 'Au99.99'),
                                'price': float(item.get('latestpri', 0)),
                                'open': float(item.get('openpri', 0)),
                                'high': float(item.get('maxpri', 0)),
                                'low': float(item.get('minpri', 0)),
                                'change': item.get('limit', '0%'),
                                'yesterday': float(item.get('yespri', 0)),
                                'volume': item.get('totalvol', '0'),
                                'update_time': item.get('time', '')
                            }
                            self.logger.info(f"✓ 成功提取Au99.99数据: {variety} = {key_prices['au9999']['price']} 元/克")
                            break
                        except (ValueError, TypeError) as e:
                            self.logger.warning(f"解析Au99.99数据失败: {e}")
                            continue

            # 查找Au(T+D)
            for item in all_data['shanghai_gold']:
                if isinstance(item, dict):
                    variety = str(item.get('variety', ''))
                    if 'Au(T+D)' in variety or 'AU(T+D)' in variety or 'T+D' in variety:
                        try:
                            key_prices['au_td'] = {
                                'name': item.get('variety', 'Au(T+D)'),
                                'price': float(item.get('latestpri', 0)),
                                'open': float(item.get('openpri', 0)),
                                'high': float(item.get('maxpri', 0)),
                                'low': float(item.get('minpri', 0)),
                                'change': item.get('limit', '0%'),
                                'yesterday': float(item.get('yespri', 0)),
                                'volume': item.get('totalvol', '0'),
                                'update_time': item.get('time', '')
                            }
                            self.logger.info(f"✓ 成功提取Au(T+D)数据: {variety} = {key_prices['au_td']['price']} 元/克")
                            break
                        except (ValueError, TypeError) as e:
                            self.logger.warning(f"解析Au(T+D)数据失败: {e}")
                            continue

        # 提取沪金主力合约
        if all_data['shanghai_futures'] and isinstance(all_data['shanghai_futures'], list):
            # 期货数据通常第一个就是主力合约，或者查找名称中包含"主力"的
            if len(all_data['shanghai_futures']) > 0:
                item = all_data['shanghai_futures'][0]
                if isinstance(item, dict):
                    try:
                        # 期货接口返回的字段名称不同
                        key_prices['futures_main'] = {
                            'name': item.get('name', '沪金主力'),
                            'price': float(item.get('latestpri', 0)),
                            'open': float(item.get('open', 0)),
                            'high': float(item.get('maxpri', 0)),
                            'low': float(item.get('minpri', 0)),
                            'change': item.get('change', '0'),
                            'yesterday': float(item.get('lastclear', 0)),
                            'volume': item.get('tradvol', '0'),
                            'update_time': item.get('time', '')
                        }
                        self.logger.info(f"✓ 成功提取期货主力数据: {item.get('name', '')} = {key_prices['futures_main']['price']} 元/克")
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"解析期货数据失败: {e}")

        return key_prices


# 使用示例
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 替换为你的API密钥
    api = JuheGoldAPI('YOUR_API_KEY', logger)

    # 获取所有金价数据
    all_data = api.fetch_all_gold_prices()

    # 获取关键金价数据
    key_prices = api.get_key_prices()

    print("\n" + "=" * 60)
    print("关键金价数据:")
    print("=" * 60)

    if key_prices['au9999']:
        print(f"\n📊 上海黄金交易所 Au99.99")
        print(f"   价格: {key_prices['au9999']['price']} 元/克")
        print(f"   涨跌: {key_prices['au9999']['change']}")
        print(f"   最高: {key_prices['au9999']['high']} 元/克")
        print(f"   最低: {key_prices['au9999']['low']} 元/克")

    if key_prices['au_td']:
        print(f"\n📈 黄金延期 Au(T+D)")
        print(f"   价格: {key_prices['au_td']['price']} 元/克")
        print(f"   涨跌: {key_prices['au_td']['change']}")

    if key_prices['futures_main']:
        print(f"\n🔮 沪金主力合约")
        print(f"   价格: {key_prices['futures_main']['price']} 元/克")
        print(f"   涨跌: {key_prices['futures_main']['change']}")
