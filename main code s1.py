from funcoes_s1 import *

ativos=carregar_dados()

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
        ativos.append(cadastrar_ativo(ativos))
        salvar_dados(ativos)

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
            ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)
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
            ativo_encontrado = encontrar_ativo_por_id(id_a_excluir, ativos)

            if ativo_encontrado:
                ativos.remove(ativo_encontrado)
                salvar_dados(ativos)
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
                    ativo_encontrado = encontrar_ativo_por_id(id_ativo_vulneravel, ativos)

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
                ativo_encontrado = encontrar_ativo_por_id(id_ativo_add_vuln, ativos)

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
                        salvar_dados(ativos)
                        print(f'Vulnerabilidade "{nome_da_vulnerabilidade}" de nível "{nivel.name.lower()}" adicionada ao ativo {ativo_encontrado["nome"]} com sucesso!')
                else:
                    print('Ativo não encontrado.')

            elif opcao_vulnerabilidade == '3':
                print('Removendo vulnerabilidade...')

                id_ativo_del_vuln = pedir_id('Digite o ID do ativo que deseja remover a vulnerabilidade: ')
                ativo_encontrado = encontrar_ativo_por_id(id_ativo_del_vuln, ativos)

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
                            salvar_dados(ativos)
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