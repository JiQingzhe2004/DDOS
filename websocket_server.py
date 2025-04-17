import asyncio
import websockets
import json
from datetime import datetime

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')
                msg_data = data.get('data')
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if msg_type == 'connect':
                    print(f"[{timestamp}] 新连接: 工具={msg_data['tool']}, IP={websocket.remote_address[0]}")
                elif msg_type == 'log':
                    print(f"[{timestamp}] 日志: {msg_data}")
                elif msg_type == 'heartbeat':
                    print(f"[{timestamp}] 心跳: {msg_data}")
                    await websocket.send(json.dumps({'type': 'heartbeat', 'data': 'pong'}))

                await websocket.send(json.dumps({'type': 'ack', 'data': f'已处理: {msg_type}'}))
            except json.JSONDecodeError:
                print(f"[{timestamp}] 无效消息: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"[{timestamp}] 客户端断开: IP={websocket.remote_address[0]}")

async def main():
    server = await websockets.serve(handle_connection, '0.0.0.0', 8765)
    print("WebSocket服务器运行在 ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())