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

def pedir_status(mensagem):

    status = None

    while status is None:

        try:
            print(f'''ATIVO - 1 \n INATIVO - 2 \n EM_MANUTENCAO - 3''')

            status_digitado = input(mensagem).strip()

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
    status = pedir_status('Digite o status do ativo: ')

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

def editar_ativo(ativos):

    id_ativo = pedir_id('Digite o ID do ativo que deseja editar: ')

    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

    if not ativo_encontrado:
        print('Nenhum ativo com este ID cadastrado.')
        return

    print(f'''Dados atuais do ativo:
    ID: {ativo_encontrado.id}
    Nome: {ativo_encontrado.nome}
    Responsável: {ativo_encontrado.responsavel}
    Status: {ativo_encontrado.status.name}
    ''')

    while True:
        print('1 - Editar responsável')
        print('2 - Editar status')
        print('3 - Voltar')

        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            novo_responsavel = pedir_info('Digite o novo nome do responsável pelo ativo: ')
            ativo_encontrado.responsavel = novo_responsavel
            print(f'Responsável atualizado com sucesso. Novo responsável: {novo_responsavel}')

        elif opcao == '2':
            novo_status=pedir_status('Digite o novo status do ativo: ')
            ativo_encontrado.status = novo_status
            print(f'Status do ativo atualizado com sucesso. Status atual: {novo_status.name}')

        elif opcao == '3':
            print('Voltando...')
            break

        else:
            print('Opção inválida.')

def excluir_ativo(ativos):
    if ativos:
        id_a_excluir = pedir_id('Digite o ID do ativo que deseja excluir: ')
        ativo_encontrado = encontrar_ativo_por_id(id_a_excluir, ativos)

        if ativo_encontrado:

            if confirmar_exclusao(ativo_encontrado):
                ativos.remove(ativo_encontrado)
                salvar_dados(ativos)
                print('Ativo excluído com sucesso!')
            else:
                print('Exclusão cancelada.')

        else:
            print('Ativo não encontrado.')

    else:
        print('Nenhum ativo cadastrado.')

def confirmar_exclusao(ativo):

    print(f'Tem certeza que deseja excluir o ativo "{ativo.nome}" (ID {ativo.id})?')
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == 'sim':
        return True
    else:
        return False

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