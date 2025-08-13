import re
import json
import requests
from typing import Optional, Dict


class Validator:


    @staticmethod
    def validar_cpf(cpf: str) -> bool:

        if not isinstance(cpf, str):
            raise ValueError("CPF deve ser uma string")

        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)

        # CPF precisa ter 11 dígitos
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calcular_digito(parcial: str, peso_inicial: int) -> str:
            soma = sum(int(d) * (peso_inicial - i) for i, d in enumerate(parcial))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        digito1 = calcular_digito(cpf[:9], 10)
        digito2 = calcular_digito(cpf[:10], 11)

        return cpf[-2:] == digito1 + digito2

    @staticmethod
    def validar_cep(cep: str) -> bool:


        if not isinstance(cep, str):
            raise ValueError("CEP deve ser uma string")

        cep_limpo = re.sub(r'\D', '', cep)

        if len(cep_limpo) != 8:
            return False

        return bool(re.fullmatch(r"\d{5}-?\d{3}", cep))

    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:

        if not isinstance(cnpj, str):
            raise ValueError("CNPJ deve ser uma string")

        cnpj = re.sub(r'\D', '', cnpj)

        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        def calcular_digito(parcial: str, pesos: list) -> str:
            soma = sum(int(d) * p for d, p in zip(parcial, pesos))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6] + pesos1

        digito1 = calcular_digito(cnpj[:12], pesos1)
        digito2 = calcular_digito(cnpj[:12] + digito1, pesos2)

        return cnpj[-2:] == digito1 + digito2


class ServicoCorreios:

    base_url = "https://viacep.com.br/ws"

    @staticmethod
    def validar_cep_api(cep: str) -> bool:
        try:
            cep_limpo = re.sub(r'\D', '', cep)

            if len(cep_limpo) != 8:
                return False

            url = f"{ServicoCorreios.base_url}/{cep_limpo}/json/"
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                return False

            data = response.json()

            return 'erro' not in data

        except (requests.RequestException, json.JSONDecodeError, Exception):
            return False
