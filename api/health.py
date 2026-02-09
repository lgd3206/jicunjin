"""
Vercel Health Check API
"""
import json


def handler(request):
    """健康检查端点"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'status': 'healthy',
            'service': 'gold-price-monitor',
            'version': '2.0.0',
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    }
