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

def pedir_nome():

    while True:
        try:
            nome_ativo = input('Digite o nome do ativo: ').strip()

            if not nome_ativo:
                raise DadoInvalidoError('Nome do ativo não pode ser vazio. Tente novamente.')
            if nome_ativo.isnumeric():
                raise DadoInvalidoError('Nome do ativo não pode ser composto apenas por números. Tente novamente.')
            break
        except DadoInvalidoError as erro:
            print(erro)

    return nome_ativo

def pedir_responsavel():

    while True:
        try:
            responsavel = input('Digite o nome do responsável pelo ativo: ').strip()

            if not responsavel:
                raise DadoInvalidoError('Nome do responsável não pode ser vazio. Tente novamente.')
            if responsavel.isnumeric():
                raise DadoInvalidoError('Nome do responsável não pode ser composto apenas por números. Tente novamente.')
            break
        except DadoInvalidoError as erro:
            print(erro)

    return responsavel

def pedir_status():

    status = None

    while status is None:

        try:
            print(f'''ATIVO - 1 \n INATIVO - 2 \n EM_MANUTENCAO - 3''')

            status_digitado = input('Digite o status do ativo: ').strip()

            if status_digitado == '1':
                status = StatusDoAtivo.ATIVO
            elif status_digitado == '2':
                status = StatusDoAtivo.INATIVO
            elif status_digitado == '3':
                status = StatusDoAtivo.EM_MANUTENCAO
            else:
                raise DadoInvalidoError('Status inválido. Tente novamente.')

        except DadoInvalidoError as erro:
            print(erro)

    return status

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

def pedir_id_disponivel(ativos):

    ID_do_ativo = pedir_id('Digite o ID do ativo: ')

    while True:
        try:
            if encontrar_ativo_por_id(ID_do_ativo, ativos) is not None:
                raise DadoInvalidoError('Já existe um ativo cadastrado com este ID. Tente outro.')
            
        except DadoInvalidoError as erro:
            print(erro)
            ID_do_ativo = pedir_id('Digite o ID do ativo: ')

        else:
            return ID_do_ativo

def cadastrar_ativo(ativos):

    ID_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_nome()
    responsavel = pedir_responsavel()
    status = pedir_status()

    print(f'''Ativo cadastrado com sucesso!
    Ativo cadastrado:ID {ID_do_ativo}
    Nome {nome_ativo}
    Status {status.name}
    Responsável {responsavel}
    ''')

    return {
        'id': ID_do_ativo,
        'nome': nome_ativo,
        'status': status,
        'responsavel': responsavel,
        'vulnerabilidades': []
    }

def encontrar_ativo_por_id(ID, ativos):
    for ativo in ativos:
        if ativo['id'] == ID:
            return ativo

    return None

def salvar_dados(ativos):
    
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