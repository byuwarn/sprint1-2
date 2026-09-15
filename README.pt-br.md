# Gerenciador de Ativos e Vulnerabilidades de TI

*[Read in English](./README.md)*

Aplicação de linha de comando (CLI) em Python para cadastro e gerenciamento de ativos de TI e suas respectivas vulnerabilidades de segurança. Desenvolvido como projeto de estudo do curso de Cibersegurança, aplicando boas práticas de código (nomenclatura clara, funções com responsabilidade única, tratamento de erros sem exposição de dados internos).

## ✨ Funcionalidades

- **Cadastro de ativos**: registra ID, nome, responsável e status (Ativo / Inativo / Em manutenção), com validação de entradas
- **Listagem de ativos**: exibe todos os ativos cadastrados ou busca um específico por ID
- **Exclusão de ativos**: remove um ativo do sistema pelo ID
- **Gerenciamento de vulnerabilidades**: adiciona, lista e remove vulnerabilidades associadas a cada ativo, com nível de severidade (Baixo / Médio / Alto)
- **Persistência de dados**: os dados são salvos automaticamente em um arquivo `ativos.json`, e recarregados a cada execução

## 🫧 Tecnologias

- Python 3
- Módulos da biblioteca padrão: `json`, `enum`

## ✨ Estrutura do projeto

```
.
├── main code s1.py     # Ponto de entrada: menu interativo e fluxo principal
├── funcoes_s1.py         # Funções de negócio, validações e persistência de dados
├── .gitignore
└── README.md
```

> O arquivo `ativos.json` (dados salvos) é gerado automaticamente na primeira execução e não é versionado.

## 🫧 Como executar

Pré-requisito: Python 3.8 ou superior instalado.

```bash
git clone https://github.com/byuwarn/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python "main code s1.py"
```

O programa abre um menu interativo no terminal. Basta seguir as opções numeradas para cadastrar ativos, gerenciar vulnerabilidades e salvar os dados.

## ✨ Menu principal

```
1 - Cadastrar ativo
2 - Listar ativos
3 - Excluir ativo
4 - Editar vulnerabilidades
5 - Sair
```

Dentro da opção **4 (Editar vulnerabilidades)**, um submenu permite listar, adicionar e remover vulnerabilidades de um ativo específico.

## 🫧 Status do projeto

Projeto em desenvolvimento incremental (por sprints), com foco em:
- Nomenclatura clara e expressiva
- Funções com responsabilidade única
- Tratamento de erros sem exposição de dados internos
- Validação de entradas do usuário

**Sprint atual:** aplicação do checklist de Boas Práticas de Código (S2_01) — refatoração de funções com múltiplas responsabilidades.

## ✨ Licença

Projeto de estudo, livre para uso educacional.
