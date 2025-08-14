# Sistema Bancário em Python (DIO)

Projeto simples em **Python** inspirado no desafio da DIO “Criando um Sistema Bancário”.

## Recursos
- Cadastro de usuários (CPF único)
- Criação de contas (agência fixa `0001`) com **PIN de 4 dígitos**
- **Depósito, Saque e Transferência** entre contas
- **Extrato** com histórico de transações
- Listagem de usuários e contas
- Persistência opcional em JSON (defina `BANK_DATA_FILE`)

## Como executar
```bash
python3 bank.py
```
> Opcional (persistência):  
> No Linux/macOS:
> ```bash
> export BANK_DATA_FILE=bank_data.json
> python3 bank.py
> ```
> No Windows (PowerShell):
> ```powershell
> $env:BANK_DATA_FILE="bank_data.json"
> python bank.py
> ```

## Fluxo sugerido
1. **[1] Cadastrar usuário** → informe CPF, nome, data de nascimento e endereço.  
2. **[2] Criar conta** → associe o CPF e defina um **PIN (4 dígitos)**.  
3. **Transacionar:** Depósito, Saque, Transferência, Extrato.

## Regras
- Saque máximo por operação: **R$ 1.000,00**
- **Até 3 saques** por “dia” (contador reinicia a cada execução)
- Transferência exige saldo suficiente
- PIN é exigido para operações sensíveis

## Estrutura
```
dio-banking-system/
├─ bank.py
└─ README.md
```

## Como criar o repositório no GitHub (passo a passo)
```bash
# 1) Entre na pasta do projeto
cd dio-banking-system

# 2) Inicie o repositório
git init
git add .
git commit -m "feat: sistema bancário em Python (DIO)"

# 3) Crie o repositório na sua conta pelo GitHub (web) e copie a URL SSH/HTTPS
git remote add origin <URL_DO_SEU_REPO>
git branch -M main
git push -u origin main
```

## Melhorias que você pode implementar
- Validação de CPF
- Controle real de “dia” para limite de saques (por data)
- Interface com `argparse` ou `typer`
- Testes automatizados com `pytest`
- Interface gráfica (Tkinter/Streamlit) ou API (FastAPI)

---

Feito para ajudar no seu portfólio 😉
