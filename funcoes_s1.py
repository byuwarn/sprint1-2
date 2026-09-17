import json
from enum import Enum

ARQUIVO_DADOS = 'ativos.json'

class Vulnerabilidade:
    def __init__(self, nome_vulnerabilidade, nivel):
        self.nome_vulnerabilidade = nome_vulnerabilidade
        self.nivel = nivel

    def para_dicionario(self):
        return {
            'nome da vulnerabilidade': self.nome_vulnerabilidade,
            'nivel': self.nivel.value
        }

class Ativo:

    def __init__(self, id, nome, responsavel, status):
        self.id = id
        self.nome = nome
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = []

    def para_dicionario(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'responsavel': self.responsavel,
            'status': self.status.value,
            'vulnerabilidades': [
                vulnerabilidade.para_dicionario() for vulnerabilidade in self.vulnerabilidades
            ]
        }

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

def validar_nome_responsavel(nome):
        
    if not nome:
        raise DadoInvalidoError('Este campo não pode ser vazio.')
    if nome.isnumeric():
        raise DadoInvalidoError('Este campo não pode ser composto apenas por números.')

def pedir_info(mensagem):

    info = None
    while info is None:

        info=input(mensagem).strip()

        try:
            validar_nome_responsavel(info)
            return info
        except DadoInvalidoError as erro:
            print(erro)
            info = None

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
    nome_ativo = pedir_info('Digite o nome do ativo: ')
    responsavel = pedir_info('Digite o nome do responsável pelo ativo: ')
    status = pedir_status()

    print(f'''Ativo cadastrado com sucesso!
    Ativo cadastrado:ID {ID_do_ativo}
    Nome {nome_ativo}
    Responsável {responsavel}
    Status {status.name}
    ''')

    return Ativo(ID_do_ativo, nome_ativo, responsavel, status)

def encontrar_ativo_por_id(ID, ativos):
    for ativo in ativos:

        if ativo.id == ID:
            return ativo

    return None

def salvar_dados(ativos):

    lista_para_salvar = []

    for ativo in ativos:

        lista_para_salvar.append(ativo.para_dicionario())

    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_para_salvar, arquivo, indent=4, ensure_ascii=False)

    except PermissionError:
        print('Erro de Persistência: Sem permissão para gravar no arquivo no computador.')
    except IOError:
        print('Erro de Persistência ao salvar os dados no arquivo.')

def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados_brutos = json.load(arquivo)

            ativos_carregados = []

            for ativo_dicionario in dados_brutos:

                vulnerabilidades_carregadas = []

                for vulnerabilidade_dicionario in ativo_dicionario['vulnerabilidades']:
                    nova_vulnerabilidade = Vulnerabilidade(
                        vulnerabilidade_dicionario['nome da vulnerabilidade'],
                        NivelDaVulnerabilidade(vulnerabilidade_dicionario['nivel'])
                    )
                    vulnerabilidades_carregadas.append(nova_vulnerabilidade)

                novo_ativo = Ativo(
                    ativo_dicionario['id'],
                    ativo_dicionario['nome'],
                    ativo_dicionario['responsavel'],
                    StatusDoAtivo(ativo_dicionario['status'])
                )

                novo_ativo.vulnerabilidades = vulnerabilidades_carregadas

                ativos_carregados.append(novo_ativo)

            return ativos_carregados

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print('Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...')
        return []