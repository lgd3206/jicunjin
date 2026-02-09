"""
极值价格提醒 - 实际应用示例
"""
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert
from config.settings import DB_PATH
from utils.logger import setup_logger


def example_1_basic_usage():
    """示例1: 基本使用"""
    print("\n" + "=" * 70)
    print("示例1: 基本使用 - 检查单个品种")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

    # 获取最新数据
    latest = db.get_latest_prices(limit=1)
    if not latest:
        print("❌ 数据库中没有数据\n")
        return

    product = latest[0]['product_name']
    current_price = latest[0]['price']

    # 检查触发条件
    result = alert_system.check_trigger_condition(product, current_price)

    # 输出结果
    print(f"品种: {product}")
    print(f"当前价格: {current_price}元/克")
    print(f"是否需要提醒: {'✅ 是' if result['should_alert'] else '❌ 否'}")
    print(f"提醒等级: {result['alert_level']}")

    if result['alert_reasons']:
        print(f"\n触发原因:")
        for reason in result['alert_reasons']:
            print(f"  - {reason}")

    print()


def example_2_custom_threshold():
    """示例2: 自定义下跌阈值"""
    print("\n" + "=" * 70)
    print("示例2: 自定义下跌阈值")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)

    # 创建多个提醒系统，使用不同的阈值
    alert_conservative = ExtremePriceAlert(db, drop_threshold_percent=10.0)  # 保守
    alert_balanced = ExtremePriceAlert(db, drop_threshold_percent=5.0)       # 平衡
    alert_aggressive = ExtremePriceAlert(db, drop_threshold_percent=2.0)     # 激进

    latest = db.get_latest_prices(limit=1)
    if not latest:
        print("❌ 数据库中没有数据\n")
        return

    product = latest[0]['product_name']
    current_price = latest[0]['price']

    print(f"品种: {product}")
    print(f"当前价格: {current_price}元/克\n")

    # 使用不同阈值检查
    result_conservative = alert_conservative.check_trigger_condition(product, current_price)
    result_balanced = alert_balanced.check_trigger_condition(product, current_price)
    result_aggressive = alert_aggressive.check_trigger_condition(product, current_price)

    print("不同阈值下的检查结果:")
    print(f"  保守策略 (10%): {'需要提醒' if result_conservative['should_alert'] else '无需提醒'}")
    print(f"  平衡策略 (5%):  {'需要提醒' if result_balanced['should_alert'] else '无需提醒'}")
    print(f"  激进策略 (2%):  {'需要提醒' if result_aggressive['should_alert'] else '无需提醒'}\n")


def example_3_batch_monitoring():
    """示例3: 批量监控多个品种"""
    print("\n" + "=" * 70)
    print("示例3: 批量监控多个品种")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

    # 获取所有品种的最新价格
    latest_prices = db.get_latest_prices(limit=100)
    if not latest_prices:
        print("❌ 数据库中没有数据\n")
        return

    # 提取品种和价格
    products = list(set(record['product_name'] for record in latest_prices))
    current_prices = {}
    for record in latest_prices:
        if record['product_name'] not in current_prices:
            current_prices[record['product_name']] = record['price']

    print(f"监控 {len(products)} 个品种\n")

    # 批量检查
    results = alert_system.batch_check_alerts(products, current_prices)

    # 获取摘要
    summary = alert_system.get_alert_summary(results)

    print(f"检查结果摘要:")
    print(f"  总检查数: {summary['total_checked']}")
    print(f"  触发提醒: {summary['total_triggered']}")
    print(f"  高等级: {summary['high_level']}")
    print(f"  中等级: {summary['medium_level']}\n")

    # 显示需要提醒的品种
    if summary['triggered_products']:
        print(f"需要提醒的品种:")
        for product in summary['triggered_products']:
            result = next(r for r in results if r['product_name'] == product)
            print(f"  - {product} (等级: {result['alert_level']})")
    else:
        print("所有品种都在正常范围内")

    print()


def example_4_alert_notification():
    """示例4: 提醒通知处理"""
    print("\n" + "=" * 70)
    print("示例4: 提醒通知处理")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

    latest = db.get_latest_prices(limit=1)
    if not latest:
        print("❌ 数据库中没有数据\n")
        return

    product = latest[0]['product_name']
    current_price = latest[0]['price']

    # 检查触发条件
    result = alert_system.check_trigger_condition(product, current_price)

    # 如果需要提醒，生成格式化消息
    if result['should_alert']:
        message = alert_system.format_alert_message(result)
        print("生成的提醒消息:")
        print(message)

        # 这里可以添加实际的通知逻辑
        # send_email(message)
        # send_wechat(message)
        # send_dingtalk(message)
    else:
        print(f"{product} 无需提醒\n")


def example_5_historical_analysis():
    """示例5: 历史数据分析"""
    print("\n" + "=" * 70)
    print("示例5: 历史数据分析")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db)

    latest = db.get_latest_prices(limit=1)
    if not latest:
        print("❌ 数据库中没有数据\n")
        return

    product = latest[0]['product_name']

    # 获取24小时极值
    extremes = alert_system.get_24h_extremes(product)

    if extremes:
        print(f"品种: {product}")
        print(f"\n24小时极值分析:")
        print(f"  最高价: {extremes['highest_price_24h']}元/克")
        print(f"  最低价: {extremes['lowest_price_24h']}元/克")
        print(f"  价格范围: {extremes['price_range']}元/克")
        print(f"  波动幅度: {(extremes['price_range'] / extremes['lowest_price_24h'] * 100):.2f}%")
        print(f"  数据点数: {extremes['data_points']}")

        # 获取统计信息
        stats = db.get_price_statistics(product, hours=24)
        if stats:
            print(f"\n统计信息:")
            print(f"  平均价: {stats['avg_price']}元/克")
            print(f"  最高价: {stats['max_price']}元/克")
            print(f"  最低价: {stats['min_price']}元/克")

    print()


def example_6_dynamic_threshold():
    """示例6: 动态阈值调整"""
    print("\n" + "=" * 70)
    print("示例6: 动态阈值调整")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

    latest = db.get_latest_prices(limit=1)
    if not latest:
        print("❌ 数据库中没有数据\n")
        return

    product = latest[0]['product_name']
    current_price = latest[0]['price']

    print(f"品种: {product}")
    print(f"当前价格: {current_price}元/克\n")

    # 测试不同的阈值
    thresholds = [1.0, 2.0, 3.0, 5.0, 10.0]

    print("不同阈值下的检查结果:")
    print("-" * 70)
    print(f"{'阈值':<10} {'需要提醒':<15} {'提醒等级':<15}")
    print("-" * 70)

    for threshold in thresholds:
        alert_system.set_drop_threshold(threshold)
        result = alert_system.check_trigger_condition(product, current_price)

        should_alert = "✅ 是" if result['should_alert'] else "❌ 否"
        alert_level = result['alert_level'].upper()

        print(f"{threshold}%{'':<6} {should_alert:<15} {alert_level:<15}")

    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 70)
    print("🔔 极值价格提醒 - 实际应用示例")
    print("=" * 70)

    try:
        example_1_basic_usage()
        example_2_custom_threshold()
        example_3_batch_monitoring()
        example_4_alert_notification()
        example_5_historical_analysis()
        example_6_dynamic_threshold()

        print("=" * 70)
        print("✅ 所有示例执行完成")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ 执行出错: {str(e)}\n")


if __name__ == "__main__":
    main()
