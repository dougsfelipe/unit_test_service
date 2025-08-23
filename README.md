# Projeto de Validação com Pytest

## Status do Build

![CI](https://github.com/dougsfelipe/unit_test_service/actions/workflows/python-tests.yml/badge.svg)

## Cobertura de Testes

[![Coverage Status](https://coveralls.io/repos/github/dougsfelipe/unit_test_service/badge.svg)](https://coveralls.io/github/dougsfelipe/unit_test_service?branch=master)

Voce também pode checar o HTML de report usando esse [link](https://dougsfelipe.github.io/unit_test_service/?sort=result) o qual é feito o deploy via Github Pages sempre que for feito um commit.


Este projeto contém funções em Python com testes automatizados usando **Pytest** e integração contínua via **GitHub Actions**.

---

## 🚀 Funcionalidades

- Validação de CPF
- Validação de CEP
- Validação de CEP (Com API dos correios)
- Validação de CNPJ 

---

## 🧪 Testes

Os testes são escritos com [Pytest](https://docs.pytest.org/) e são executados automaticamente no GitHub Actions a cada `push` na branch `master`.

### ✅ Rodar os testes localmente:

```bash
pip install -r requirements.txt
pytest 
