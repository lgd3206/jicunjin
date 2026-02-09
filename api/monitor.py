"""
Vercel Serverless Function - 金价监控 API
"""
import json
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from email_alert_integration import EmailAlertIntegration
except ImportError:
    EmailAlertIntegration = None


def handler(request):
    """处理 HTTP 请求"""

    # 处理 GET 请求 - 测试连接
    if request.method == 'GET':
        try:
            if EmailAlertIntegration is None:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'error',
                        'message': 'EmailAlertIntegration module not found'
                    })
                }

            integration = EmailAlertIntegration('.env')

            if integration.test_email_connection():
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'success',
                        'message': 'Connection test passed',
                        'timestamp': str(Path(__file__).stat().st_mtime)
                    })
                }
            else:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'error',
                        'message': 'Connection test failed'
                    })
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'error',
                    'message': f'Error: {str(e)}'
                })
            }

    # 处理 POST 请求 - 发送邮件
    elif request.method == 'POST':
        try:
            if EmailAlertIntegration is None:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'error',
                        'message': 'EmailAlertIntegration module not found'
                    })
                }

            # 解析请求体
            if isinstance(request.body, bytes):
                body = json.loads(request.body.decode('utf-8'))
            elif isinstance(request.body, str):
                body = json.loads(request.body)
            else:
                body = request.body

            integration = EmailAlertIntegration('.env')

            # 发送邮件
            results = integration.send_alert_emails(body)

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'success',
                    'message': 'Email sent successfully',
                    'results': results
                })
            }
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Invalid JSON in request body'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'error',
                    'message': f'Error: {str(e)}'
                })
            }

    # 其他方法
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'error',
                'message': 'Method not allowed'
            })
        }
