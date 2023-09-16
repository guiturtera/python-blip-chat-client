import uuid
import websocket
import json

import auth

websocket_uri = '<YOUR WEBSOCKET_URI HERE>'
bot_id = '<YOUR BOT ID HERE>'

def send_message(ws, content: dict) -> None:
    str_content = json.dumps(content)
    print(f'  - User: {str_content}')
    ws.send(str_content)
    

def receive_message(ws) -> dict:
    received_message = ws.recv()
    print(f"  - Bot: {received_message}")
    return json.loads(received_message)

new_user = auth.create_new_user(websocket_uri, bot_id)
print(f"Test user created = {new_user}")

ws = websocket.create_connection(websocket_uri)
send_message(ws, {'state': 'new'})
ws_id = receive_message(ws)['id']

msg_to_send = {"id":f"{ws_id}","state":"authenticating","from":f"{new_user['identity']}.{bot_id}@0mn.io/default","scheme":"plain","authentication":{"scheme":"plain","password":"dGVzdGUxMjM="}}
send_message(ws, msg_to_send)
receive_message(ws)

msg_to_send = {"id":f"{ws_id}","method":"set","uri":"/presence","type":"application/vnd.lime.presence+json","resource":{"status":"available","routingRule":"promiscuous","echo":True}}
send_message(ws, msg_to_send)
receive_message(ws)

msg_to_send = {"id": f"{ws_id}","to": f"{bot_id}@msging.net","type": "text/plain","content": "oi","metadata": {}}
send_message(ws, msg_to_send)
receive_message(ws)
receive_message(ws)
receive_message(ws)
receive_message(ws)
receive_message(ws)

ws.close()


