"""
GitHub Actions 单次运行脚本 - 聚合数据版
使用聚合数据API获取上海黄金交易所和期货交易所的金价数据
"""
import os
import sys
import json
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import ConfigLoader
from api.juhe_gold_api import JuheGoldAPI
from api.xiaoxiao_gold_api import XiaoxiaoGoldAPI
from notifications.enhanced_email_notifier import EnhancedEmailNotifier

# 历史价格文件
PRICE_HISTORY_FILE = 'price_history.json'


def setup_logger() -> logging.Logger:
    """设置日志"""
    logger = logging.getLogger('gold_monitor')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
    return logger


def fetch_gold_price_fallback(logger: logging.Logger) -> Optional[Dict[str, Any]]:
    """
    备用金价获取（当极速数据API不可用时）
    使用免费的国际金价API
    """
    # 数据源1：gold-api.com
    try:
        resp = requests.get('https://api.gold-api.com/price/XAU', timeout=15)
        if resp.status_code == 200:
            gold_data = resp.json()
            usd_per_oz = gold_data.get('price')
            if usd_per_oz:
                resp2 = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=15)
                if resp2.status_code == 200:
                    cny_rate = resp2.json()['rates'].get('CNY', 7.1)
                else:
                    cny_rate = 7.1
                cny_per_gram = round(usd_per_oz * cny_rate / 31.1035, 2)
                logger.info(f"备用数据源获取成功: {cny_per_gram} 元/克")
                return {
                    'price': cny_per_gram,
                    'source': 'gold-api',
                    'timestamp': datetime.now().isoformat()
                }
    except Exception as e:
        logger.warning(f"备用数据源失败: {e}")

    # 数据源2：metals.dev
    try:
        resp = requests.get('https://api.metals.dev/v1/latest?api_key=demo&currency=CNY&unit=gram', timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            gold_price = data.get('metals', {}).get('gold')
            if gold_price:
                cny_per_gram = round(float(gold_price), 2)
                logger.info(f"备用数据源2获取成功: {cny_per_gram} 元/克")
                return {
                    'price': cny_per_gram,
                    'source': 'metals.dev',
                    'timestamp': datetime.now().isoformat()
                }
    except Exception as e:
        logger.warning(f"备用数据源2失败: {e}")

    # 手动设置价格（测试用）
    manual_price = os.environ.get('MANUAL_GOLD_PRICE')
    if manual_price:
        try:
            price = float(manual_price)
            logger.info(f"使用手动设置价格: {price} 元/克")
            return {
                'price': price,
                'source': 'manual',
                'timestamp': datetime.now().isoformat()
            }
        except ValueError:
            pass

    logger.error("所有备用数据源均失败")
    return None


def load_price_history(logger: logging.Logger) -> list:
    """加载历史价格记录"""
    if os.path.exists(PRICE_HISTORY_FILE):
        try:
            with open(PRICE_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"加载历史价格失败: {e}")
    return []


def save_price_history(history: list, logger: logging.Logger):
    """保存历史价格记录（只保留最近48条，即24小时 x 每30分钟1条）"""
    history = history[-48:]
    try:
        with open(PRICE_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        logger.info(f"已保存 {len(history)} 条历史价格记录")
    except Exception as e:
        logger.error(f"保存历史价格失败: {e}")


def analyze_price(current_price: float, history: list, threshold: float, logger: logging.Logger) -> Dict[str, Any]:
    """
    分析价格，判断是否需要发送提醒
    """
    if not history:
        logger.info("无历史数据，跳过分析")
        return {
            'product_name': 'AU9999',
            'current_price': current_price,
            'should_alert': False,
            'alert_reasons': ['首次运行，无历史数据'],
            'alert_level': 'none',
            'extremes': None,
            'price_diff': None,
            'timestamp': datetime.now().isoformat()
        }

    prices = [record['price'] for record in history]
    highest_price = max(prices)
    lowest_price = min(prices)
    price_range = highest_price - lowest_price

    absolute_diff = highest_price - current_price
    percentage_diff = round((absolute_diff / highest_price * 100), 2) if highest_price > 0 else 0

    extremes = {
        'highest_price_24h': highest_price,
        'lowest_price_24h': lowest_price,
        'price_range': round(price_range, 2),
        'data_points': len(history)
    }

    price_diff = {
        'absolute_difference': round(absolute_diff, 2),
        'percentage_difference': percentage_diff,
        'is_below_highest': current_price < highest_price
    }

    alert_reasons = []
    alert_level = 'none'

    # 条件1：当前价格是历史最低价
    if current_price <= lowest_price:
        alert_reasons.append(f"当前价格 {current_price} 元/克 是近24小时最低价")
        alert_level = 'high'

    # 条件2：价格下跌超过阈值
    if percentage_diff >= threshold:
        alert_reasons.append(
            f"价格从最高价 {highest_price} 元/克下跌了 {percentage_diff}%（阈值: {threshold}%）"
        )
        if alert_level == 'none':
            alert_level = 'medium'
        elif alert_level == 'medium':
            alert_level = 'high'

    # 条件3：价格大幅波动
    if price_range > 0 and (price_range / highest_price * 100) > 2:
        alert_reasons.append(f"24小时价格波动幅度较大: {round(price_range, 2)} 元/克")
        if alert_level == 'none':
            alert_level = 'low'

    should_alert = len(alert_reasons) > 0

    logger.info(f"分析结果: 当前价格={current_price}, 最高价={highest_price}, "
                f"最低价={lowest_price}, 下跌={percentage_diff}%, 需要提醒={should_alert}")

    return {
        'product_name': 'AU9999',
        'current_price': current_price,
        'should_alert': should_alert,
        'alert_reasons': alert_reasons,
        'alert_level': alert_level,
        'extremes': extremes,
        'price_diff': price_diff,
        'timestamp': datetime.now().isoformat()
    }


def send_email_alert(alert_result: Dict[str, Any], config: ConfigLoader, logger: logging.Logger) -> bool:
    """发送邮件提醒"""
    try:
        email_config = config.get_email_config()
        recipients = config.get_recipient_emails()
        alert_config = config.get_alert_config()

        if not alert_config['enable_email_notification']:
            logger.info("邮件通知已禁用")
            return False

        if not recipients:
            logger.warning("未配置收件人邮箱")
            return False

        if alert_config['test_mode']:
            logger.info(f"[测试模式] 模拟发送邮件到: {', '.join(recipients)}")
            return True

        notifier = EnhancedEmailNotifier(
            email_address=email_config['email_address'],
            app_password=email_config['app_password'],
            email_type=email_config['email_type']
        )

        results = notifier.send_batch_emails(recipients, alert_result)
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"邮件发送完成: 成功 {success_count}/{len(results)}")
        return success_count > 0

    except Exception as e:
        logger.error(f"发送邮件失败: {e}")
        return False


def main():
    """主函数 - 单次运行（聚合数据版）"""
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("积存金价格监控 - GitHub Actions 单次运行（聚合数据版）")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # 加载配置
    try:
        config = ConfigLoader()
    except Exception as e:
        logger.warning(f"加载 .env 文件失败 ({e})，将使用环境变量")
        config = ConfigLoader.__new__(ConfigLoader)
        config.env_path = '.env'
        config.config = {}
        config.load_config()

    # 获取下跌阈值
    alert_config = config.get_alert_config()
    threshold = alert_config['drop_threshold_percent']
    logger.info(f"下跌阈值: {threshold}%")

    # 获取聚合数据API密钥
    juhe_api_key = os.environ.get('JUHE_API_KEY')

    # 初始化金价数据
    current_price = None
    key_prices = {}

    if juhe_api_key:
        logger.info("=" * 60)
        logger.info("使用聚合数据API获取金价数据...")
        logger.info("=" * 60)

        try:
            # 使用聚合数据API获取所有金价
            juhe_api = JuheGoldAPI(juhe_api_key, logger)
            key_prices = juhe_api.get_key_prices()

            # 优先使用上海黄金交易所Au99.99价格
            if key_prices.get('au9999'):
                current_price = key_prices['au9999']['price']
                logger.info(f"✓ 使用上海黄金交易所Au99.99价格: {current_price} 元/克")
            # 其次使用黄金延期Au(T+D)价格
            elif key_prices.get('au_td'):
                current_price = key_prices['au_td']['price']
                logger.info(f"✓ 使用黄金延期Au(T+D)价格: {current_price} 元/克")
            # 最后使用期货主力合约价格
            elif key_prices.get('futures_main'):
                current_price = key_prices['futures_main']['price']
                logger.info(f"✓ 使用沪金主力合约价格: {current_price} 元/克")

        except Exception as e:
            logger.error(f"聚合数据API获取失败: {e}")

    # 获取银行金价数据（小小API - 完全免费）
    logger.info("=" * 60)
    logger.info("获取银行金价数据...")
    logger.info("=" * 60)

    bank_prices = {}
    brand_prices = []
    recycle_prices = []

    try:
        xiaoxiao_api = XiaoxiaoGoldAPI(logger)

        # 一次性获取所有数据（避免重复调用）
        all_xiaoxiao_data = xiaoxiao_api.fetch_all_gold_prices()

        if all_xiaoxiao_data:
            # 提取银行金价
            bank_gold_list = all_xiaoxiao_data.get('bank_gold_bar_price', [])
            if bank_gold_list:
                # 转换为key_bank_prices格式
                for item in bank_gold_list:
                    bank_name = item.get('bank', '')
                    price = float(item.get('price', 0))

                    if '工商银行' in bank_name or '工行' in bank_name:
                        bank_prices['icbc'] = {'name': bank_name, 'price': price, 'type': '投资金条'}
                    elif '建设银行' in bank_name or '建行' in bank_name:
                        bank_prices['ccb'] = {'name': bank_name, 'price': price, 'type': '投资金条'}
                    elif '中国银行' in bank_name or '中行' in bank_name:
                        bank_prices['boc'] = {'name': bank_name, 'price': price, 'type': '投资金条'}
                    elif '农业银行' in bank_name or '农行' in bank_name:
                        bank_prices['abc'] = {'name': bank_name, 'price': price, 'type': '投资金条'}
                    elif '浦发银行' in bank_name or '浦发' in bank_name:
                        bank_prices['spdb'] = {'name': bank_name, 'price': price, 'type': '投资金条'}
                    elif '平安' in bank_name:
                        bank_prices['pingan'] = {'name': bank_name, 'price': price, 'type': '投资金条'}

                if bank_prices:
                    key_prices['bank_prices'] = bank_prices
                    bank_count = sum(1 for v in bank_prices.values() if v)
                    logger.info(f"✓ 成功获取 {bank_count} 家银行金价")

                    # 如果没有上海金交所数据，使用工商银行金价作为当前价格
                    if current_price is None and bank_prices.get('icbc'):
                        current_price = bank_prices['icbc']['price']
                        logger.info(f"✓ 使用工商银行金条价格: {current_price} 元/克")

            # 提取品牌金店价格（前5家）
            brand_prices = all_xiaoxiao_data.get('precious_metal_price', [])[:5]
            if brand_prices:
                key_prices['brand_prices'] = brand_prices
                logger.info(f"✓ 成功获取 {len(brand_prices)} 家品牌金店价格")

            # 提取回收价格（前5种）
            recycle_prices = all_xiaoxiao_data.get('gold_recycle_price', [])[:5]
            if recycle_prices:
                key_prices['recycle_prices'] = recycle_prices
                logger.info(f"✓ 成功获取 {len(recycle_prices)} 种回收价格")

    except Exception as e:
        logger.warning(f"小小API获取失败: {e}")

    # 如果所有数据源都失败，使用备用数据源
    if current_price is None:
        logger.info("=" * 60)
        logger.info("使用备用数据源获取金价...")
        logger.info("=" * 60)

        price_data = fetch_gold_price_fallback(logger)
        if not price_data:
            logger.error("无法获取金价，本次运行结束")
            sys.exit(1)

        current_price = price_data['price']
        logger.info(f"当前金价: {current_price} 元/克 (来源: {price_data['source']})")

    # 加载历史价格
    history = load_price_history(logger)
    logger.info(f"历史记录: {len(history)} 条")

    # 分析价格
    alert_result = analyze_price(current_price, history, threshold, logger)

    # 将聚合数据API的关键金价添加到提醒结果中
    if key_prices:
        alert_result.update(key_prices)

    # 保存当前价格到历史
    history.append({
        'price': current_price,
        'source': 'juhe-api' if juhe_api_key else 'fallback',
        'timestamp': datetime.now().isoformat()
    })
    save_price_history(history, logger)

    # 判断是否需要发送提醒
    force_alert = os.environ.get('FORCE_ALERT', 'false').lower() == 'true'

    if force_alert:
        logger.info("=" * 60)
        logger.info("强制发送邮件模式（测试用）")
        logger.info("=" * 60)
        alert_result['should_alert'] = True
        alert_result['alert_level'] = 'TEST'
        if not alert_result.get('alert_reasons'):
            alert_result['alert_reasons'] = ['测试邮件 - 手动触发']

    if alert_result['should_alert']:
        logger.info(f"触发提醒! 等级: {alert_result['alert_level']}")
        for reason in alert_result['alert_reasons']:
            logger.info(f"  原因: {reason}")

        # 发送邮件
        send_email_alert(alert_result, config, logger)
    else:
        logger.info("价格正常，无需提醒")

    logger.info("=" * 60)
    logger.info("本次运行完成")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
