#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Bancário em Python (CLI)
--------------------------------
Recursos implementados:
- Cadastro de usuários (CPF único)
- Criação de contas (agência fixa 0001) com PIN de 4 dígitos
- Depósito
- Saque (com verificação de saldo e limites)
- Transferência entre contas
- Extrato
- Listagem de usuários e contas
- Persistência simples em JSON (opcional; padrão: memória)
Autor: Você (adaptado para o desafio DIO)
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from getpass import getpass

DATA_FILE = os.environ.get("BANK_DATA_FILE", "")  # se quiser persistir: export BANK_DATA_FILE=bank_data.json
AGENCIA_PADRAO = "0001"
LIMITE_SAQUE = 1000.0  # por operação
LIMITE_SAQUES_DIA = 3   # por dia (não implementa data real, apenas contador de sessão para simplicidade)

# -------------------------
# Modelos
# -------------------------

@dataclass
class Usuario:
    cpf: str
    nome: str
    data_nasc: str
    endereco: str  # "logradouro, nro - bairro - cidade/UF"

@dataclass
class Transacao:
    tipo: str  # "DEPÓSITO", "SAQUE", "TRANSFERÊNCIA-ENVIO", "TRANSFERÊNCIA-RECEB"
    valor: float

@dataclass
class Conta:
    numero: int
    agencia: str = AGENCIA_PADRAO
    cpf_titular: str = ""
    pin: str = "0000"
    saldo: float = 0.0
    extrato: List[Transacao] = field(default_factory=list)
    saques_hoje: int = 0

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de depósito deve ser positivo.")
        self.saldo += valor
        self.extrato.append(Transacao("DEPÓSITO", valor))

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de saque deve ser positivo.")
        if valor > LIMITE_SAQUE:
            raise ValueError(f"Saque máximo por operação: R$ {LIMITE_SAQUE:.2f}.")
        if self.saques_hoje >= LIMITE_SAQUES_DIA:
            raise ValueError("Limite de saques do dia atingido.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor
        self.saques_hoje += 1
        self.extrato.append(Transacao("SAQUE", -valor))

    def transferir(self, destino: "Conta", valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de transferência deve ser positivo.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para transferência.")
        self.saldo -= valor
        destino.saldo += valor
        self.extrato.append(Transacao("TRANSFERÊNCIA-ENVIO", -valor))
        destino.extrato.append(Transacao("TRANSFERÊNCIA-RECEB", valor))

# -------------------------
# "Repositório" simples em memória + persistência opcional JSON
# -------------------------

class Banco:
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}  # chave: cpf
        self.contas: Dict[int, Conta] = {}      # chave: numero da conta
        self._proximo_numero = 1

    # -------- Persistência --------
    def carregar(self, path: str) -> None:
        if not path or not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.usuarios = {u["cpf"]: Usuario(**u) for u in data.get("usuarios", [])}
        self.contas = {}
        for c in data.get("contas", []):
            cpy = c.copy()
            cpy["extrato"] = [Transacao(**t) for t in cpy.get("extrato", [])]
            self.contas[cpy["numero"]] = Conta(**cpy)
        self._proximo_numero = max(self.contas.keys(), default=0) + 1

    def salvar(self, path: str) -> None:
        if not path:
            return
        data = {
            "usuarios": [asdict(u) for u in self.usuarios.values()],
            "contas": [
                {
                    **{k: v for k, v in asdict(c).items() if k != "extrato"},
                    "extrato": [asdict(t) for t in c.extrato],
                }
                for c in self.contas.values()
            ],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # -------- Usuários e Contas --------
    def criar_usuario(self, cpf: str, nome: str, data_nasc: str, endereco: str) -> Usuario:
        if cpf in self.usuarios:
            raise ValueError("CPF já cadastrado.")
        user = Usuario(cpf=cpf, nome=nome, data_nasc=data_nasc, endereco=endereco)
        self.usuarios[cpf] = user
        return user

    def criar_conta(self, cpf_titular: str, pin: str) -> Conta:
        if cpf_titular not in self.usuarios:
            raise ValueError("CPF não encontrado. Cadastre o usuário antes.")
        if not (pin.isdigit() and len(pin) == 4):
            raise ValueError("PIN deve conter 4 dígitos numéricos.")
        numero = self._proximo_numero
        self._proximo_numero += 1
        conta = Conta(numero=numero, cpf_titular=cpf_titular, pin=pin)
        self.contas[numero] = conta
        return conta

    def autenticar_conta(self, numero: int, pin: str) -> Conta:
        conta = self.contas.get(numero)
        if not conta or conta.pin != pin:
            raise ValueError("Conta/PIN inválidos.")
        return conta

# -------------------------
# Interface de Linha de Comando
# -------------------------

def menu() -> str:
    print("\n=== Sistema Bancário DIO ===")
    print("[1] Cadastrar usuário")
    print("[2] Criar conta")
    print("[3] Depositar")
    print("[4] Sacar")
    print("[5] Transferir")
    print("[6] Extrato")
    print("[7] Listar usuários/contas")
    print("[0] Sair")
    return input("Escolha: ").strip()

def main():
    banco = Banco()
    if DATA_FILE:
        banco.carregar(DATA_FILE)

    while True:
        opc = menu()

        try:
            if opc == "1":
                cpf = input("CPF (somente números): ").strip()
                nome = input("Nome: ").strip()
                data_nasc = input("Data nasc (DD/MM/AAAA): ").strip()
                endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ").strip()
                user = banco.criar_usuario(cpf, nome, data_nasc, endereco)
                print(f"✅ Usuário criado: {user.nome} (CPF {user.cpf})")

            elif opc == "2":
                cpf = input("CPF do titular: ").strip()
                pin = getpass("Defina um PIN de 4 dígitos: ").strip()
                conta = banco.criar_conta(cpf, pin)
                print(f"✅ Conta criada: Agência {conta.agencia} | Número {conta.numero} | Titular CPF {conta.cpf_titular}")

            elif opc == "3":  # Depósito
                numero = int(input("Número da conta: ").strip())
                pin = getpass("PIN: ").strip()
                conta = banco.autenticar_conta(numero, pin)
                valor = float(input("Valor do depósito: R$ ").replace(",", ".").strip())
                conta.depositar(valor)
                print(f"✅ Depósito realizado. Saldo atual: R$ {conta.saldo:.2f}")

            elif opc == "4":  # Saque
                numero = int(input("Número da conta: ").strip())
                pin = getpass("PIN: ").strip()
                conta = banco.autenticar_conta(numero, pin)
                valor = float(input("Valor do saque: R$ ").replace(",", ".").strip())
                conta.sacar(valor)
                print(f"✅ Saque realizado. Saldo atual: R$ {conta.saldo:.2f}")

            elif opc == "5":  # Transferência
                origem_num = int(input("Número da conta de ORIGEM: ").strip())
                pin = getpass("PIN da conta de origem: ").strip()
                origem = banco.autenticar_conta(origem_num, pin)
                destino_num = int(input("Número da conta de DESTINO: ").strip())
                destino = banco.contas.get(destino_num)
                if not destino:
                    raise ValueError("Conta de destino não encontrada.")
                valor = float(input("Valor da transferência: R$ ").replace(",", ".").strip())
                origem.transferir(destino, valor)
                print(f"✅ Transferência concluída. Saldo origem: R$ {origem.saldo:.2f} | Saldo destino: R$ {destino.saldo:.2f}")

            elif opc == "6":  # Extrato
                numero = int(input("Número da conta: ").strip())
                pin = getpass("PIN: ").strip()
                conta = banco.autenticar_conta(numero, pin)
                print("\n--- Extrato ---")
                if not conta.extrato:
                    print("Não há movimentações.")
                else:
                    for t in conta.extrato:
                        sinal = "" if t.valor >= 0 else ""
                        print(f"{t.tipo:<24} R$ {t.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                print(f"Saldo atual: R$ {conta.saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            elif opc == "7":  # Listagens
                print("\n--- Usuários ---")
                for u in banco.usuarios.values():
                    print(f"{u.nome} | CPF: {u.cpf} | Nasc: {u.data_nasc} | End.: {u.endereco}")
                print("\n--- Contas ---")
                for c in banco.contas.values():
                    print(f"Agência {c.agencia} | Número {c.numero} | Titular CPF {c.cpf_titular} | Saldo R$ {c.saldo:.2f}")

            elif opc == "0":
                if DATA_FILE:
                    banco.salvar(DATA_FILE)
                    print(f"💾 Dados salvos em: {DATA_FILE}")
                print("Até mais!")
                break

            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
