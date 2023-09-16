import uuid
import websocket
import json

def _send_message(ws, content: dict) -> None:
    str_content = json.dumps(content)
    print(f'  - User: {str_content}')
    ws.send(str_content)
    

def _receive_message(ws) -> dict:
    received_message = ws.recv()
    print(f"  - Bot: {received_message}")
    return json.loads(received_message)


def _generate_custom_user_uuid(websocket_uri: str, bot_id: str):
    print("Criando usuário aleatório no chat:")
    print("  Conexão de verificação se o usuário já existe:")
    ws = websocket.create_connection(websocket_uri)

    password = "dGVzdGUxMjM="
    user_exists = True
    random_uuid = None
    
    while user_exists:
        random_uuid = uuid.uuid4()
        
        _send_message(ws, {'state': 'new'})
        res = _receive_message(ws)
        ws_id = res['id']
        
        check_auth_fail_collision = {"id":f"{ws_id}","state":"authenticating","from":f"{random_uuid}.{bot_id}@0mn.io/default","scheme":"plain","authentication":{"scheme":"plain","password":f"{password}"}}
        _send_message(ws, check_auth_fail_collision)
        res = _receive_message(ws)
        
        user_exists = res['state'] != "failed"
        
    print(f"  UUID gerado = {random_uuid}")
    print()
    
    ws.close()
    
    return random_uuid

def _configure_user_password(random_uuid: str, password: str, websocket_uri: str, bot_id: str) -> None:
    print("Configurando senha para o novo usuário:")
    ws = websocket.create_connection(websocket_uri)

    _send_message(ws, {'state': 'new'})
    res = _receive_message(ws)
    ws_id = res['id']

    pp_uuid = uuid.uuid4()
    msg_to_send = {"id":f"{ws_id}","state":"authenticating","from":f"{pp_uuid}@0mn.io/default","scheme":"guest","authentication":{"scheme":"guest"}}
    _send_message(ws, msg_to_send)
    _receive_message(ws)


    msg_to_send = {
    "id": f"{ws_id}",
    "method": "set",
    "from": f"{random_uuid}.{bot_id}@0mn.io/default",
    "pp": f"{pp_uuid}@0mn.io/default",
    "type": "application/vnd.lime.account+json",
    "uri": "/account",
    "resource": {
        "password": f"{password}",
        "extras": {
        "authType": "Dev"
        },
        "userIdentity": f"{random_uuid}.{bot_id}",
        "userPassword": f"{password}",
        "authType": "Dev"
    }
    }
    _send_message(ws, msg_to_send)
    res = _receive_message(ws)
    if res['status'] != "success":
        raise Exception(f"Falha na criação de um novo usuário aleatório: '{res}'")

    _send_message(ws, {"id":f"{ws_id}","state":"finishing"})
    _receive_message(ws)

    print()
    ws.close()

def create_new_user(websocket_uri: str, bot_id: str) -> dict:
    password = "dGVzdGUxMjM="
    
    custom_uuid = _generate_custom_user_uuid(websocket_uri, bot_id)
    _configure_user_password(custom_uuid, password, websocket_uri, bot_id)
    
    return {
        "identity": custom_uuid,
        "password": password,
        "scheme": "plain"
    }
    

    

    
        