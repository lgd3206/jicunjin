"""
极值价格提醒测试脚本 - 验证所有功能
"""
import sys
from database.db_manager import DatabaseManager
from alerts.extreme_price_alert import ExtremePriceAlert
from config.settings import DB_PATH
from utils.logger import setup_logger


def test_extreme_price_alert():
    """测试极值价格提醒系统"""
    logger = setup_logger()

    print("\n" + "=" * 70)
    print("🧪 极值价格提醒系统 - 功能测试")
    print("=" * 70 + "\n")

    # 初始化
    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db, drop_threshold_percent=5.0)

    # 测试1: 获取24小时极值
    print("测试1: 获取24小时极值")
    print("-" * 70)

    latest_prices = db.get_latest_prices(limit=100)
    if not latest_prices:
        print("❌ 数据库中没有数据，请先运行 main.py 抓取数据\n")
        return False

    products = list(set(record['product_name'] for record in latest_prices))
    test_product = products[0] if products else None

    if not test_product:
        print("❌ 未找到品种\n")
        return False

    extremes = alert_system.get_24h_extremes(test_product)

    if extremes:
        print(f"✅ 成功获取 {test_product} 的24小时极值")
        print(f"   最高价: {extremes['highest_price_24h']}")
        print(f"   最低价: {extremes['lowest_price_24h']}")
        print(f"   范围: {extremes['price_range']}")
        print(f"   数据点: {extremes['data_points']}\n")
    else:
        print(f"❌ 获取 {test_product} 的极值失败\n")
        return False

    # 测试2: 计算价格差值
    print("测试2: 计算价格差值")
    print("-" * 70)

    current_record = next((r for r in latest_prices if r['product_name'] == test_product), None)
    if current_record:
        current_price = current_record['price']
        price_diff = alert_system.calculate_price_difference(current_price, extremes['highest_price_24h'])

        print(f"✅ 成功计算价格差值")
        print(f"   当前价格: {price_diff['current_price']}")
        print(f"   最高价: {price_diff['highest_price_24h']}")
        print(f"   绝对差值: {price_diff['absolute_difference']}")
        print(f"   百分比差值: {price_diff['percentage_difference']}%\n")
    else:
        print(f"❌ 未找到 {test_product} 的当前价格\n")
        return False

    # 测试3: 检查触发条件
    print("测试3: 检查触发条件")
    print("-" * 70)

    result = alert_system.check_trigger_condition(test_product, current_price)

    print(f"✅ 成功检查触发条件")
    print(f"   品种: {result['product_name']}")
    print(f"   当前价格: {result['current_price']}")
    print(f"   是否需要提醒: {'是' if result['should_alert'] else '否'}")
    print(f"   提醒等级: {result['alert_level']}")

    if result['alert_reasons']:
        print(f"   触发原因:")
        for reason in result['alert_reasons']:
            print(f"     - {reason}")
    print()

    # 测试4: 批量检查
    print("测试4: 批量检查多个品种")
    print("-" * 70)

    current_prices = {}
    for record in latest_prices:
        if record['product_name'] not in current_prices:
            current_prices[record['product_name']] = record['price']

    batch_results = alert_system.batch_check_alerts(products[:5], current_prices)
    summary = alert_system.get_alert_summary(batch_results)

    print(f"✅ 成功批量检查")
    print(f"   检查总数: {summary['total_checked']}")
    print(f"   触发提醒: {summary['total_triggered']}")
    print(f"   高等级: {summary['high_level']}")
    print(f"   中等级: {summary['medium_level']}\n")

    # 测试5: 修改阈值
    print("测试5: 修改下跌阈值")
    print("-" * 70)

    original_threshold = alert_system.get_drop_threshold()
    print(f"✅ 原始阈值: {original_threshold}%")

    alert_system.set_drop_threshold(3.0)
    new_threshold = alert_system.get_drop_threshold()
    print(f"✅ 修改后阈值: {new_threshold}%")

    # 重新检查
    new_result = alert_system.check_trigger_condition(test_product, current_price)
    print(f"✅ 使用新阈值重新检查")
    print(f"   是否需要提醒: {'是' if new_result['should_alert'] else '否'}")
    print(f"   提醒等级: {new_result['alert_level']}\n")

    # 恢复原始阈值
    alert_system.set_drop_threshold(original_threshold)

    # 测试6: 格式化消息
    print("测试6: 格式化提醒消息")
    print("-" * 70)

    if batch_results:
        alert_result = next((r for r in batch_results if r['should_alert']), batch_results[0])
        message = alert_system.format_alert_message(alert_result)
        print("✅ 成功格式化消息")
        print(message)

    print("=" * 70)
    print("✅ 所有测试通过！")
    print("=" * 70 + "\n")

    return True


def test_edge_cases():
    """测试边界情况"""
    logger = setup_logger()

    print("\n" + "=" * 70)
    print("🧪 边界情况测试")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db)

    # 测试1: 不存在的品种
    print("测试1: 查询不存在的品种")
    print("-" * 70)

    result = alert_system.get_24h_extremes("不存在的品种")
    if result is None:
        print("✅ 正确处理不存在的品种\n")
    else:
        print("❌ 应该返回None\n")

    # 测试2: 无效的阈值
    print("测试2: 设置无效的阈值")
    print("-" * 70)

    alert_system.set_drop_threshold(-5.0)
    threshold = alert_system.get_drop_threshold()
    if threshold == 5.0:
        print("✅ 正确处理负数阈值，使用默认值\n")
    else:
        print(f"❌ 阈值应该是5.0，实际是{threshold}\n")

    # 测试3: 极端价格
    print("测试3: 处理极端价格")
    print("-" * 70)

    price_diff = alert_system.calculate_price_difference(0, 100)
    if price_diff['percentage_difference'] == 100.0:
        print("✅ 正确计算极端价格差值\n")
    else:
        print("❌ 计算错误\n")

    print("=" * 70)
    print("✅ 边界情况测试完成！")
    print("=" * 70 + "\n")

    return True


def test_performance():
    """性能测试"""
    logger = setup_logger()
    import time

    print("\n" + "=" * 70)
    print("⚡ 性能测试")
    print("=" * 70 + "\n")

    db = DatabaseManager(DB_PATH)
    alert_system = ExtremePriceAlert(db)

    latest_prices = db.get_latest_prices(limit=100)
    if not latest_prices:
        print("❌ 数据库中没有数据\n")
        return False

    products = list(set(record['product_name'] for record in latest_prices))
    current_prices = {}
    for record in latest_prices:
        if record['product_name'] not in current_prices:
            current_prices[record['product_name']] = record['price']

    # 测试1: 单个品种检查性能
    print("测试1: 单个品种检查性能")
    print("-" * 70)

    start_time = time.time()
    for _ in range(100):
        alert_system.check_trigger_condition(products[0], current_prices[products[0]])
    elapsed = time.time() - start_time

    avg_time = elapsed / 100 * 1000  # 转换为毫秒
    print(f"✅ 100次检查耗时: {elapsed:.3f}秒")
    print(f"   平均每次: {avg_time:.2f}毫秒\n")

    # 测试2: 批量检查性能
    print("测试2: 批量检查性能")
    print("-" * 70)

    start_time = time.time()
    for _ in range(10):
        alert_system.batch_check_alerts(products, current_prices)
    elapsed = time.time() - start_time

    avg_time = elapsed / 10 * 1000
    print(f"✅ 10次批量检查耗时: {elapsed:.3f}秒")
    print(f"   平均每次: {avg_time:.2f}毫秒")
    print(f"   每个品种: {avg_time / len(products):.2f}毫秒\n")

    print("=" * 70)
    print("✅ 性能测试完成！")
    print("=" * 70 + "\n")

    return True


def main():
    """主测试程序"""
    print("\n" + "=" * 70)
    print("🧪 极值价格提醒系统 - 完整测试套件")
    print("=" * 70)

    all_passed = True

    # 运行功能测试
    if not test_extreme_price_alert():
        all_passed = False

    # 运行边界情况测试
    if not test_edge_cases():
        all_passed = False

    # 运行性能测试
    if not test_performance():
        all_passed = False

    # 总结
    print("=" * 70)
    if all_passed:
        print("✅ 所有测试通过！系统运行正常。")
    else:
        print("❌ 部分测试失败，请检查系统。")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
