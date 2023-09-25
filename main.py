import sys

import auth
import tests
import excel_parser
import websocket

websocket_uri = 'wss://guilherme-turtera-q4uvy.ws.0mn.io/4'
bot_id = 'teste3226'

def main():
    _, tests_path, results_path = sys.argv

    test_cases = excel_parser.generate_test_cases_from_excel(tests_path)
    test_results = []
    for current_test in test_cases:
        try:    
            new_user = auth.create_new_user(websocket_uri, bot_id)
            ws = websocket.create_connection(websocket_uri)
            auth.authenticate_user_in_websocket(ws, new_user, bot_id)

            test_result = tests.run_test(ws, new_user, current_test['tests'])
            test_result['test_case'] = current_test['test_case']

        except:
            test_result = {
                "test_case": current_test['test_case'],
                "error": "falha não mapeada na realização do teste"
            }
        finally:
            test_results.append(test_result)
            ws.close()
    
    excel_parser.generate_simple_test_results(results_path, test_results)

main()