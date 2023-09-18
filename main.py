import uuid
import json
from time import sleep

import websocket

import auth


websocket_uri = 'wss://guilherme-turtera-q4uvy.ws.0mn.io/4'
bot_id = 'teste3226'

# websocket_uri = '<URL DO SEU WEBSOCKET>'
# bot_id = '<ID DO SEU BOT>'
# appkey = 'dGVzdG1haW4zOmVhN2U1MDU2LWYwNmQtNDM0MS04Mzg1LWFiYmNmZWU4MjlkMw=='

def send_message(ws, content: dict) -> None:
    str_content = json.dumps(content)
    ws.send(str_content)
    

def receive_message(ws) -> dict:
    received_message = ws.recv()
    return json.loads(received_message)

def wait_response_message(ws) -> dict:
    is_response_message = False
    is_delay_content = True
    while not is_response_message or is_delay_content:
        res = receive_message(ws)

        is_response_message = (res['metadata'].get('#messageKind') == 'Response')
        is_delay_content = (type(res.get('content')) is dict and res['content'].get('state') == 'composing')        

    return res


print()
print("Conversa (CHAT) será mostrado abaixo:")

def run_test(ws, user: dict, expected_conversation: list) -> dict:
    test_result = {
        'user': user,
        'conversation': []
    }
    
    #### Timeout ainda não implementado
    for message in expected_conversation:
        if message['from'] == 'user':
            msg_to_send = {"id": f"{uuid.uuid4()}","to": f"{bot_id}@msging.net","type": "text/plain","content": f"{message['content']}","metadata": {}}
            print(f"  - User: {message['content']}")
            test_result['conversation'].append({'from': 'user', 'content': message})
            
            send_message(ws, msg_to_send)
        elif message['from'] == 'bot':
            res = wait_response_message(ws)    
            content = res['content']
            
            print(f'  - Bot: {content}')
            success_response = message['must_include'] in content
            test_result['conversation'].append({
                'from': 'bot', 
                'content': content, 
                'status': 'success' if success_response else 'failed', 
                'must_include': message['must_include'], 
                'timeout_in_seconds': message['timeout_in_seconds']
            })
            
            if not success_response:
                test_result['status'] = 'failed'
                return test_result
        else:
            raise Exception(f'{message["from"]} é inválido para a chave "from". Utilize "user" ou "bot"')
        
        sleep(0.5)
    
    test_result['status'] = 'success'
    return test_result
        

expected_conversation = [
    {
        "from": "user",
        "content": "oi",
    },
    {
        "from": "bot",
        "must_include": "Olá amigo!",
        "timeout_in_seconds": 10
    },
    {
        "from": "bot",
        "must_include": "Como você está?",
        "timeout_in_seconds": 10
    },
    {
        "from": "user",
        "content": "Muito bem, e você?"
    },
    {
        "from": "bot",
        "must_include": "Bem demais!",
        "timeout_in_seconds": 10
    }
]


new_user = auth.create_new_user(websocket_uri, bot_id)
print(f"Test user created = {new_user}")
ws = websocket.create_connection(websocket_uri)
auth.authenticate_user_in_websocket(ws, new_user, bot_id)

print('Simulando testes:')
print()
test_result = run_test(ws, new_user, expected_conversation)
print(test_result)
        
        
ws.close()
    
