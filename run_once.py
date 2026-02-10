"""
GitHub Actions 单次运行脚本 - 抓取实时金价并判断是否发送邮件提醒
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
from notifications.email_notifier import EmailNotifier

# 历史价格文件（用于在 GitHub Actions 无状态环境中持久化）
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


def fetch_bank_gold_prices(appkey: str, logger: logging.Logger) -> Optional[Dict[str, Any]]:
    """
    抓取各大银行金价（使用极速数据API）

    Args:
        appkey: 极速数据API密钥
        logger: 日志器

    Returns:
        {'banks': list, 'timestamp': str} 或 None
    """
    try:
        url = f'https://api.jisuapi.com/gold/bank?appkey={appkey}'
        resp = requests.get(url, timeout=15)

        if resp.status_code == 200:
            data = resp.json()
            logger.info(f"极速数据API返回: {data}")  # 调试日志

            # 注意：status 是数字 0，不是字符串 '0'
            if data.get('status') == 0 and data.get('result'):
                result = data['result']
                banks = []

                # 解析银行金价数据 - result 直接是列表
                for bank_data in result:
                    # 只处理人民币账户黄金
                    if bank_data.get('typename') == '人民币账户黄金':
                        banks.append({
                            'bank_name': '工商银行',  # API返回的是账户类型，不是银行名称
                            'buy_price': float(bank_data.get('buyprice', 0)),
                            'sell_price': float(bank_data.get('sellprice', 0)),
                            'update_time': bank_data.get('updatetime', '')
                        })

                if banks:
                    logger.info(f"成功获取银行金价数据")
                    return {
                        'banks': banks,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    logger.warning("API返回数据中未找到人民币账户黄金")
                    return None
            else:
                logger.warning(f"API返回状态异常: status={data.get('status')}, msg={data.get('msg')}")
                return None

        logger.warning(f"极速数据API HTTP状态码异常: {resp.status_code}")
        return None

    except Exception as e:
        logger.warning(f"获取银行金价失败: {e}")
        return None


def fetch_gold_price(logger: logging.Logger) -> Optional[Dict[str, Any]]:
    """
    抓取实时金价（使用多个数据源，确保可用性）

    Returns:
        {'price': float, 'source': str, 'timestamp': str} 或 None
    """
    # 数据源1：gold-api.com（免费，无需key，返回美元/盎司）+ exchangerate汇率
    try:
        # 获取金价（美元/盎司）
        resp = requests.get('https://api.gold-api.com/price/XAU', timeout=15)
        if resp.status_code == 200:
            gold_data = resp.json()
            usd_per_oz = gold_data.get('price')
            if usd_per_oz:
                # 获取美元兑人民币汇率
                resp2 = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=15)
                if resp2.status_code == 200:
                    cny_rate = resp2.json()['rates'].get('CNY', 7.1)
                else:
                    cny_rate = 7.1  # 备用汇率
                cny_per_gram = round(usd_per_oz * cny_rate / 31.1035, 2)
                logger.info(f"数据源1获取成功: {cny_per_gram} 元/克 (金价${usd_per_oz}/oz, 汇率{cny_rate})")
                return {
                    'price': cny_per_gram,
                    'source': 'gold-api',
                    'timestamp': datetime.now().isoformat()
                }
    except Exception as e:
        logger.warning(f"数据源1失败: {e}")

    # 数据源2：metals.dev（免费，无需key）
    try:
        resp = requests.get('https://api.metals.dev/v1/latest?api_key=demo&currency=CNY&unit=gram', timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            gold_price = data.get('metals', {}).get('gold')
            if gold_price:
                cny_per_gram = round(float(gold_price), 2)
                logger.info(f"数据源2获取成功: {cny_per_gram} 元/克")
                return {
                    'price': cny_per_gram,
                    'source': 'metals.dev',
                    'timestamp': datetime.now().isoformat()
                }
    except Exception as e:
        logger.warning(f"数据源2失败: {e}")

    # 数据源3：备用 - 从环境变量手动设置（用于测试）
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

    logger.error("所有数据源均失败")
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
    # 只保留最近48条记录
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

    Args:
        current_price: 当前价格
        history: 历史价格列表
        threshold: 下跌阈值百分比
        logger: 日志器

    Returns:
        提醒结果字典
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

    # 计算与最高价的差值
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

    # 条件3：价格大幅波动（范围超过2%）
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

        notifier = EmailNotifier(
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
    """主函数 - 单次运行"""
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("积存金价格监控 - GitHub Actions 单次运行")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # 加载配置
    try:
        config = ConfigLoader()
    except Exception as e:
        logger.warning(f"加载 .env 文件失败 ({e})，将使用环境变量")
        # 创建一个空的配置加载器，依赖环境变量
        config = ConfigLoader.__new__(ConfigLoader)
        config.env_path = '.env'
        config.config = {}
        config.load_config()

    # 获取下跌阈值
    alert_config = config.get_alert_config()
    threshold = alert_config['drop_threshold_percent']
    logger.info(f"下跌阈值: {threshold}%")

    # 获取银行金价（如果配置了API密钥）- 先测试这个
    bank_prices = None
    jisuapi_key = os.environ.get('JISUAPI_KEY')
    if jisuapi_key:
        logger.info("正在获取各大银行金价...")
        bank_prices = fetch_bank_gold_prices(jisuapi_key, logger)
        if bank_prices:
            logger.info(f"银行金价获取成功，共 {len(bank_prices['banks'])} 家银行")
        else:
            logger.warning("银行金价获取失败")
    else:
        logger.info("未配置 JISUAPI_KEY，跳过银行金价获取")

    # 抓取实时金价
    price_data = fetch_gold_price(logger)
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

    # 将银行金价添加到提醒结果中
    if bank_prices:
        alert_result['bank_prices'] = bank_prices['banks']

    # 保存当前价格到历史
    history.append({
        'price': current_price,
        'source': price_data['source'],
        'timestamp': price_data['timestamp']
    })
    save_price_history(history, logger)

    # 判断是否需要发送提醒
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
