import json
from enum import Enum

ARQUIVO_DADOS = 'ativos.json'

class DadoInvalidoError(Exception):
    pass

class StatusDoAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3

class NivelDaVulnerabilidade(Enum):
    BAIXO = 1
    MEDIO = 2
    ALTO = 3

def cadastrar_ativo():

    ID_do_ativo = pedir_id('Digite o ID do ativo: ')

    ativo = input('Digite o nome do ativo: ').strip()

    while encontrar_ativo_por_id(ID_do_ativo) is not None:
        print('Já existe um ativo cadastrado com este ID. Tente outro.')
        ID_do_ativo = pedir_id('Digite o ID do ativo: ')

    while not ativo:
        ativo = input('Digite o nome do ativo: ').strip()
        if not ativo:
                print('Nome do ativo não pode ser vazio. Tente novamente.')

    responsavel = input('Digite o nome do responsável pelo ativo: ').strip()

    while not responsavel:
        responsavel = input('Digite o nome do responsável pelo ativo: ').strip()
        if not responsavel:
            print('Nome do responsável não pode ser vazio. Tente novamente.')

    status = None

    while status is None:

        print(f'''ATIVO - 1 \n INATIVO - 2 \n EM_MANUTENCAO - 3''')

        status_digitado = input('Digite o status do ativo: ').strip()

        if status_digitado == '1':
            status = StatusDoAtivo.ATIVO
        elif status_digitado == '2':
            status = StatusDoAtivo.INATIVO
        elif status_digitado == '3':
            status = StatusDoAtivo.EM_MANUTENCAO
        else:
            print('Status inválido. Tente novamente.')
            continue

    print(f'''Ativo cadastrado com sucesso!
    Ativo cadastrado:ID {ID_do_ativo}
    Nome {ativo}
    Status {status.name}
    Responsável {responsavel}
''')

    return {
        'id': ID_do_ativo,
        'nome': ativo,
        'status': status,
        'responsavel': responsavel,
        'vulnerabilidades': []
    }

def encontrar_ativo_por_id(ID):
    for ativo in ativos:
        if ativo['id'] == ID:
            return ativo

    return None

def pedir_id(mensagem):

    while True:
        try:
            id_texto=input(mensagem).strip()

            if not id_texto:
                raise DadoInvalidoError('Este campo não pode ser vazio. Tente novamente.')

            if int(id_texto) <= 0:
                raise DadoInvalidoError('O ID não pode ser nulo ou negativo. Tente novamente.')

            return int(id_texto)

        except ValueError:
            print('Digite um número válido')

        except DadoInvalidoError as erro:
            print(erro)

def salvar_dados():
    
    lista_para_salvar = []

    try: 

        for ativo in ativos:
            ativo_formatado = ativo.copy()
            ativo_formatado['status'] = ativo_formatado['status'].value

            vulnerabilidades_formatadas = []

            for vulnerabilidade in ativo['vulnerabilidades']:
                copia_vulnerabilidade = vulnerabilidade.copy()
                copia_vulnerabilidade['nivel']=copia_vulnerabilidade['nivel'].value
                vulnerabilidades_formatadas.append(copia_vulnerabilidade)

            ativo_formatado['vulnerabilidades']=vulnerabilidades_formatadas
            lista_para_salvar.append(ativo_formatado)
            
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_para_salvar, arquivo, indent=4, ensure_ascii=False)

    except PermissionError:
        print('Erro de Persistência: Sem permissão para gravar no arquivo no computador.')

    except IOError:
        print(f'Erro de Persistência ao salvar os dados no arquivo.')

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados_brutos = json.load(arquivo)
            for ativo in dados_brutos:
                ativo['status'] = StatusDoAtivo(ativo['status'])

                for vulnerabilidade in ativo['vulnerabilidades']:
                    vulnerabilidade['nivel'] = NivelDaVulnerabilidade(vulnerabilidade['nivel'])

            return dados_brutos
            
    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print('Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...')
        return []

ativos = carregar_dados()

while True:

    print('MENU')
    print('1 - Cadastrar ativo')
    print('2 - Listar ativos')
    print('3 - Excluir ativo')
    print('4 - Editar vulnerabilidades')
    print('5 - Sair')

    try:
        opcao = input('Escolha uma opção: ').strip()
        
    except (EOFError, KeyboardInterrupt):
        print('Programa encerrado pelo usuário.')
        break

    except ValueError:
        print('Escolha uma opção válida.')
        continue

    if opcao == '1':
        ativos.append(cadastrar_ativo())
        salvar_dados()

    elif opcao == '2':

        todos_um = input('Deseja listar todos os ativos ou apenas um específico? (todos/um): ').strip()

        if todos_um == 'todos':
            if ativos:
                print('Listando ativos por ID, nome e responsável...')
                for ativo in ativos:
                    print(
                        f'''ID: {ativo['id']}
                        Nome: {ativo['nome']}
                        Status: {ativo['status'].name}
                        Responsável: {ativo['responsavel']}'''
                    )
            else:
                print('Nenhum ativo cadastrado.')

        elif todos_um == 'um':
            id_ativo = pedir_id('Digite o ID do ativo que deseja listar: ')
            ativo_encontrado = encontrar_ativo_por_id(id_ativo)
            if ativo_encontrado:
                print(
                    f'''ID: {ativo_encontrado['id']}
                    Nome: {ativo_encontrado['nome']}
                    Status: {ativo_encontrado['status'].name}
                    Responsável: {ativo_encontrado['responsavel']}'''
                )

            else:
                print('Ativo não encontrado.')

        else:
            print('Opção inválida. Tente novamente.')

    elif opcao == '3':
        if ativos:
            id_a_excluir = pedir_id('Digite o ID do ativo que deseja excluir: ')
            ativo_encontrado = encontrar_ativo_por_id(id_a_excluir)

            if ativo_encontrado:
                ativos.remove(ativo_encontrado)
                salvar_dados()
                print('Ativo excluído com sucesso!')
            else:
                print('Ativo não encontrado.')
        else:
            print('Nenhum ativo cadastrado.')

    elif opcao == '4':
        
        while True:
            print('Menu de vulnerabilidades:')
            print('1 - Listar vulnerabilidades')
            print('2 - Adicionar vulnerabilidade')
            print('3 - Remover vulnerabilidade')
            print('4 - Voltar ao menu principal')

            try:
                opcao_vulnerabilidade = input('Escolha uma opção: ').strip()

            except (EOFError, KeyboardInterrupt):
                print('Programa encerrado pelo usuário.')
                break

            except ValueError:
                print('Escolha uma opção válida.')
                continue

            if opcao_vulnerabilidade == '1':
                print('Listando vulnerabilidades...')
                todas_um = input('Deseja listar todas as vulnerabilidades ou apenas as de um ativo específico? (todas/um): ').strip()

                if todas_um == 'todas':
                    if ativos:
                        print('Listando todas as vulnerabilidades...')

                        for ativo in ativos:
                            if ativo['vulnerabilidades']:
                                print(f"Ativo: {ativo['nome']}")

                                for vulnerabilidade in ativo['vulnerabilidades']:
                                    print(
                                        f'''  Vulnerabilidade: {vulnerabilidade['nome da vulnerabilidade']}
                                        Nível: {vulnerabilidade['nivel'].name.lower()}'''
                                    )

                            else: 
                                print('Nenhuma vulnerabilidade cadastrada nos ativos.')
                                
                    else:
                        print('Nenhum ativo cadastrado.')

                elif todas_um == 'um':

                    id_ativo_vulneravel = pedir_id('Digite o ID do ativo que deseja listar as vulnerabilidades: ')
                    ativo_encontrado = encontrar_ativo_por_id(id_ativo_vulneravel)

                    if ativo_encontrado:

                        if not ativo_encontrado['vulnerabilidades']:
                            print('Este ativo não possui vulnerabilidades cadastradas.')

                        else:
                            print('Vulnerabilidades cadastradas:')
                            for vulnerabilidade in ativo_encontrado['vulnerabilidades']:
                                print(
                                    f'''Vulnerabilidade: {vulnerabilidade['nome da vulnerabilidade']}
                                    Nível: {vulnerabilidade['nivel'].name.lower()}'''
                                )
                        
                    else:
                        print('Ativo não encontrado.')

                else:
                    print('Opção inválida. Tente novamente.')

            elif opcao_vulnerabilidade == '2':
                print('Adicionando vulnerabilidade...')

                id_ativo_add_vuln = pedir_id('Digite o ID do ativo que deseja adicionar a vulnerabilidade: ')
                ativo_encontrado = encontrar_ativo_por_id(id_ativo_add_vuln)

                if ativo_encontrado:
                    nome_da_vulnerabilidade = input('Digite a vulnerabilidade que deseja adicionar: ').strip()

                    if not nome_da_vulnerabilidade:
                        print('Vulnerabilidade não pode ser vazia. Tente novamente.')
                    else:
                        nivel = None

                        while nivel is None:
                            print(f'''BAIXO - 1 \n MEDIO - 2 \n ALTO - 3''')

                            nivel_digitado = input('Digite o nível da vulnerabilidade: ').strip()

                            if nivel_digitado == '1':
                                nivel = NivelDaVulnerabilidade.BAIXO
                            elif nivel_digitado == '2':
                                nivel = NivelDaVulnerabilidade.MEDIO
                            elif nivel_digitado == '3':
                                nivel = NivelDaVulnerabilidade.ALTO
                            else:
                                print('Nível inválido. Tente novamente.')
                                continue

                        ativo_encontrado['vulnerabilidades'].append({
                            'nome da vulnerabilidade': nome_da_vulnerabilidade,
                            'nivel': nivel
                        })
                        salvar_dados()
                        print(f'Vulnerabilidade "{nome_da_vulnerabilidade}" de nível "{nivel.name.lower()}" adicionada ao ativo {ativo_encontrado["nome"]} com sucesso!')
                else:
                    print('Ativo não encontrado.')

            elif opcao_vulnerabilidade == '3':
                print('Removendo vulnerabilidade...')

                id_ativo_del_vuln = pedir_id('Digite o ID do ativo que deseja remover a vulnerabilidade: ')
                ativo_encontrado = encontrar_ativo_por_id(id_ativo_del_vuln)

                if ativo_encontrado:
                    if not ativo_encontrado['vulnerabilidades']:
                        print('Este ativo não possui vulnerabilidades cadastradas.')
                    else:
                        print('Vulnerabilidades cadastradas:')
                        for vulnerabilidade in ativo_encontrado['vulnerabilidades']:
                            print(f"- {vulnerabilidade['nome da vulnerabilidade']} (nível {vulnerabilidade['nivel']})")

                        nome_a_remover = input('Digite o nome da vulnerabilidade que deseja remover: ').strip()

                        vulnerabilidade_encontrada = {}

                        for vulnerabilidade in ativo_encontrado['vulnerabilidades']:
                            if vulnerabilidade['nome da vulnerabilidade'] == nome_a_remover:
                                vulnerabilidade_encontrada = vulnerabilidade

                        if vulnerabilidade_encontrada:
                            ativo_encontrado['vulnerabilidades'].remove(vulnerabilidade_encontrada)
                            salvar_dados()
                            print(f'Vulnerabilidade "{nome_a_remover}" removida do ativo {ativo_encontrado["nome"]} com sucesso!')
                        else:
                            print('Vulnerabilidade não encontrada. Tente novamente.')
                else:
                    print('Ativo não encontrado.')

            elif opcao_vulnerabilidade == '4':
                print('Voltando ao menu principal...')
                break

    elif opcao == '5':
        print('Saindo do programa...')
        break