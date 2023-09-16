import uuid
import websocket
import json

import auth
from time import sleep

websocket_uri = '<URL DO SEU WEBSOCKET>'
bot_id = '<ID DO SEU BOT>'

def send_message(ws, content: dict) -> None:
    str_content = json.dumps(content)
    ws.send(str_content)
    

def receive_message(ws) -> dict:
    received_message = ws.recv()
    return json.loads(received_message)


def wait_response_message(ws) -> dict:
    is_response_message = False
    while not is_response_message:
        res = receive_message(ws)
        is_response_message = (res['metadata'].get('#messageKind') == 'Response')
                
    return res

new_user = auth.create_new_user(websocket_uri, bot_id)
print(f"Test user created = {new_user}")
ws = websocket.create_connection(websocket_uri)
auth.authenticate_user_in_websocket(ws, new_user, bot_id)


print()
print("Conversa (CHAT) será mostrado abaixo:")


messages_to_send = [
    {
        "content": "oi",
        "qtd_respostas": 3 
    },
    {
        "content": "Fazer comida",
        "qtd_respostas": 3
    }
]

for test_content in messages_to_send:
    msg_to_send = {"id": f"{uuid.uuid4()}","to": f"{bot_id}@msging.net","type": "text/plain","content": f"{test_content['content']}","metadata": {}}
    print(f"  - User: {test_content['content']}")
    send_message(ws, msg_to_send)
    
    for i in range(test_content['qtd_respostas']):
        res = wait_response_message(ws)['content']
        print(f'  - Bot: {res}')
    
    sleep(0.5)
        
        

message_id = uuid.uuid4()
msg_to_send = {"id": f"{message_id}","to": f"{bot_id}@msging.net","type": "text/plain","content": "oi","metadata": {}}
send_message(ws, msg_to_send)
receive_message(ws)
receive_message(ws)
receive_message(ws)
receive_message(ws)
# receive_message(ws)
# receive_message(ws)
# receive_message(ws)
# receive_message(ws)
# receive_message(ws)

