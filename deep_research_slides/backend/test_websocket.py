#!/usr/bin/env python3
"""WebSocket接続テストスクリプト"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket connected successfully")
            
            # 10秒間メッセージを待機
            try:
                for i in range(10):
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"Received: {data}")
            except asyncio.TimeoutError:
                print("No messages received within timeout")
            except Exception as e:
                print(f"Error receiving message: {e}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())