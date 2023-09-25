import pandas as pd


def generate_test_cases_from_excel(excel_path: str):
    test_cases = pd.read_excel(excel_path)
    test_cases.columns = ['from', 'message', 'must_include', 'timeout_in_seconds']

    test_cases['from'] = test_cases['from'].fillna('')
    test_cases['message'] = test_cases['message'].fillna('')
    test_cases['must_include'] = test_cases['must_include'].fillna('')

    formatted_test_cases = []
    current_test_case = {}

    def check_valid_case(test_case: dict): 
        if not test_case.get('test_case'):
            raise Exception('É necessário passar o cenário antes dos casos de teste')

    def validate_user_line(user_line):
        if not user_line['message']:
            raise Exception(f"Célula B{user_line.name + 2} - necessária mensagem quando for o interação do usuário")

    def validate_bot_line(bot_line):
        if not bot_line['must_include']:
            raise Exception(f"Célula B{bot_line.name + 2} - necessária 'mensagem tem que incluir' quando for interação do bot")
        if not bot_line['timeout_in_seconds']:
            raise Exception(f"Célula B{bot_line.name + 2} - necessária 'tempo máximo de resposta (segundos)' quando for interação do bot")
        

    for i in range(test_cases.shape[0]):
        line = test_cases.iloc[i]
        if not line['from']:
            continue

        from_content = line['from'].lower().strip()
        if from_content.startswith('cenario:'):
            current_test_case = {}
            current_test_case['test_case'] = from_content
            current_test_case['tests'] = []
        
            formatted_test_cases.append(current_test_case)

        elif from_content == 'user':
            check_valid_case(current_test_case)
            validate_user_line(line)

            interaction = {
                "from": "user",
                "content": line['message'],
            }

            current_test_case['tests'].append(interaction)

        elif from_content == 'bot':
            check_valid_case(current_test_case)
            validate_bot_line(line)
            interaction = {
                "from": "bot",
                "must_include": line['must_include'],
                "timeout_in_seconds": line['timeout_in_seconds']
            }

            current_test_case['tests'].append(interaction)

        else:
            raise Exception(f'Entrada inválida na célula A{i+2}: {from_content}. Inputs válidos = [cenario:<CENARIO>, user, bot]')
        
    return formatted_test_cases

def generate_simple_test_results(results_path: str, test_results):
    result_df = pd.DataFrame(test_results)

    formatted_simple_result = []
    for i in range(result_df.shape[0]):
        line = result_df.iloc[i]
        
        test_case = line['test_case']
        user_identity = line['user']['identity']
        status = line['status']
        error = line['error']

        formatted_simple_result.append({
            "Caso de teste": test_case,
            "Id do usuário": user_identity,
            "Status": status,
            "Erro": error
        })
        
    df = pd.DataFrame(formatted_simple_result)
    df.to_excel(results_path)




    
