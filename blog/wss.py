import websocket
# ws = websocket.WebSocket()
# ws.connect("wss://api.bitfinex.com/ws", http_proxy_host="proxy_host_name", http_proxy_port=3128)


from websocket import create_connection
ws = create_connection("wss://api.bitfinex.com/ws")
print("Sending 'Hello, World'...")
ws.send("ping")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
