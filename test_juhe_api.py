"""
测试聚合数据API的不同接口地址
"""
import os
import requests

# 从环境变量获取API密钥
api_key = os.environ.get('JUHE_API_KEY')

if not api_key:
    print("错误：未设置 JUHE_API_KEY 环境变量")
    exit(1)

base_url = 'http://web.juhe.cn/finance/gold'

# 测试可能的期货接口地址
possible_endpoints = [
    'shfutures',  # 当前使用的（404错误）
    'futures',    # 简化版
    'shfe',       # 上海期货交易所缩写
    'qhjs',       # 期货交易所拼音缩写
    'shanghaifutures',  # 完整名称
]

print("=" * 60)
print("测试聚合数据API期货接口")
print("=" * 60)

for endpoint in possible_endpoints:
    url = f'{base_url}/{endpoint}'
    params = {'key': api_key}

    print(f"\n测试接口: {endpoint}")
    print(f"URL: {url}")

    try:
        resp = requests.get(url, params=params, timeout=10)
        print(f"HTTP状态码: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print(f"返回数据: {data}")

            if data.get('resultcode') == '200':
                print(f"✅ 成功！接口地址是: {endpoint}")
                result = data.get('result')
                if result:
                    print(f"数据类型: {type(result)}")
                    if isinstance(result, list) and len(result) > 0:
                        print(f"数据条数: {len(result)}")
                        print(f"第一条数据: {result[0]}")
                break
            else:
                error_code = data.get('error_code', 'unknown')
                reason = data.get('reason', '未知错误')
                print(f"❌ 失败: [{error_code}] {reason}")
        else:
            print(f"❌ HTTP错误: {resp.status_code}")

    except Exception as e:
        print(f"❌ 请求异常: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
