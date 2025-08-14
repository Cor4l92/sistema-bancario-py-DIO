Sistema Bancário em Python (DIO)

Projeto prático inspirado no desafio “Criando um Sistema Bancário com Python” da DIO.
Você constrói um sistema bancário em linha de comando (CLI) com cadastro de usuários e contas, transações (depósito, saque, transferência), extrato e persistência opcional em JSON.

🎯 O que é / Objetivo

Um app simples para simular operações bancárias e, ao mesmo tempo, praticar Python (estruturas de dados, funções, classes, validações) e conceitos de software (organização de código, persistência, UX de terminal).

✅ Funcionalidades

Cadastro de usuários (CPF único)

Criação de contas (agência padrão 0001) com PIN de 4 dígitos

Depósito, Saque (com limites), Transferência entre contas

Extrato com histórico de transações

Listagem de usuários e contas

Persistência opcional em arquivo JSON (BANK_DATA_FILE)

🧠 Regras de negócio

Saque máximo por operação: R$ 1.000,00

Até 3 saques por dia (contador reinicia a cada execução para simplificar)

Transferência e saque exigem saldo suficiente

Operações sensíveis pedem PIN correto

🛠️ Requisitos

Python 3.8+

Sistema operacional: Windows, Linux ou macOS

(Opcional) Editor/IDE à sua escolha

📦 Instalação (passo a passo)

Clone ou baixe este repositório

git clone <URL_DO_SEU_REPO>.git
cd <PASTA_DO_REPO>


Alternativa: baixe o .zip pelo GitHub e extraia.

(Opcional) Crie um ambiente virtual

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1


Dependências

Não há bibliotecas externas obrigatórias neste projeto.

▶️ Como executar
# Linux/macOS
python3 bank.py

# Windows
python bank.py

💾 Persistência opcional (JSON)

Se quiser salvar os dados entre execuções, defina a variável BANK_DATA_FILE:

# Linux/macOS
export BANK_DATA_FILE=bank_data.json
python3 bank.py

# Windows (PowerShell)
$env:BANK_DATA_FILE="bank_data.json"
python bank.py

🧭 Passo a passo de uso (fluxo sugerido)

Cadastrar usuário (opção 1) → informe CPF, nome, data de nascimento e endereço

Criar conta (opção 2) → associe a conta ao CPF e defina um PIN (4 dígitos)

Transacionar:

Depósito (3)

Saque (4)

Transferência (5)

Extrato (6)

Listar usuários/contas (7)

Sair (0) — se a persistência estiver ativa, os dados serão salvos no arquivo JSON.

🧪 Exemplos rápidos
Depósito
[3] Depositar
Número da conta: 1
PIN: ****
Valor do depósito: R$ 500
✅ Depósito realizado. Saldo atual: R$ 500,00

Saque
[4] Sacar
Número da conta: 1
PIN: ****
Valor do saque: R$ 100
✅ Saque realizado. Saldo atual: R$ 400,00

Transferência
[5] Transferir
Número da conta de ORIGEM: 1
PIN da conta de origem: ****
Número da conta de DESTINO: 2
Valor da transferência: R$ 150
✅ Transferência concluída. Saldo origem: R$ 250,00 | Saldo destino: R$ 150,00

Extrato
[6] Extrato
Número da conta: 1
PIN: ****

--- Extrato ---
DEPÓSITO               R$ 500,00
SAQUE                  R$ -100,00
TRANSFERÊNCIA-ENVIO    R$ -150,00
Saldo atual: R$ 250,00

🗂️ Estrutura do projeto
.
├─ bank.py        # Aplicação CLI
└─ README.md      # Este arquivo

🧩 Roadmap / Ideias de melhoria

Validação de CPF

Controle de limite diário por data real

Separar camadas (modelos/serviços/UI)

Testes com pytest

CLI com argparse/typer

API com FastAPI ou interface com Streamlit

Criptografia de PIN e logs de auditoria

❓ Dúvidas comuns

“O PIN precisa ter 4 dígitos?” Sim, apenas números e exatamente 4 dígitos.

“Não salvou meus dados ao sair.” Ative a persistência com BANK_DATA_FILE (veja seção de persistência).

“Posso ter contas para o mesmo CPF?” Sim, o CPF identifica o usuário; a conta tem número único.

📚 Referências

Desafio DIO: Criando um Sistema Bancário com Python

Repositório base da formação: digitalinnovationone/trilha-python-dio

📝 Licença

Este projeto é distribuído sob a licença MIT. Sinta-se à vontade para usar e melhorar.

👤 Autor

Feito por Sandro  — adaptado e estruturado para o desafio da DIO.
