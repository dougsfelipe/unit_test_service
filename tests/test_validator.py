import pytest
from app.validator import Validator, ServicoCorreios
from unittest.mock import patch, Mock, MagicMock


@pytest.fixture
def validar():
    return Validator()

def servico():
    return ServicoCorreios()

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_correios_service(self):
    """Mock mais sofisticado do ServicoCorreios"""
    with patch('validator.ServicoCorreios') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.mark.parametrize("cpf_valido", [
    "529.982.247-25",
    "52998224725",
    "123.456.789-09"
])

def test_validar_cpf_valido(validar,cpf_valido):
    assert validar.validar_cpf(cpf_valido) == True

@pytest.mark.parametrize("cpf_invalido", [
    "11111111111",
    "12345678900",
    "000.000.000-00",
    "529.982.247",
    "abcdefghijk",

])

def test_validar_cpf_invalido(validar, cpf_invalido):
    assert validar.validar_cpf(cpf_invalido) == False

@pytest.mark.parametrize("cpf_formato_invalido", [
    52998224725,
    52998224725,
    12345678909
])

def test_validar_cpf_formato_invalido(validar, cpf_formato_invalido):
    with pytest.raises(ValueError):
        validar.validar_cpf(cpf_formato_invalido)


@pytest.mark.parametrize("cep_valido", [
    "12345-678",
    "12345678"
])

def test_validar_cep_valido(validar,cep_valido):
    assert validar.validar_cep(cep_valido) == True

@pytest.mark.parametrize("cep_invalido", [
    "1234-567",
    "12.345-678"
])

def test_validar_cep_invalido(cep_invalido, validar):
    assert validar.validar_cep(cep_invalido) == False

@pytest.mark.parametrize("cep_formato_invalido", [
    12345678,
    12345678
])

def test_validar_cep_formato_invalido(validar, cep_formato_invalido):
    with pytest.raises(ValueError):
        validar.validar_cep(cep_formato_invalido)



@pytest.mark.parametrize("cnpj_valido", [
    "04.252.011/0001-10",
    "04252011000110",
    "11.222.333/0001-81"  # válido fictício
])

def test_validar_cnpj_valido(cnpj_valido,validar):
    assert validar.validar_cnpj(cnpj_valido) == True

@pytest.mark.parametrize("cnpj_invalido", [
    "00.000.000/0000-00",   # repetido
    "11111111111111",       # repetido
    "12345678000100",       # dígitos errados
    "04.252.011/0001",      # incompleto
    "abcdefghijklll",       # letras
    "",                     # vazio
])

def test_validar_cnpj_invalido(cnpj_invalido,validar):
    assert validar.validar_cnpj(cnpj_invalido) == False

@pytest.mark.parametrize("cnpj_formato_invalido", [
    11111111111111,
    12345678000100,
    14252011000110
])

def test_validar_cnpj_formato_invalido(validar, cnpj_formato_invalido):
    with pytest.raises(ValueError):
        validar.validar_cnpj(cnpj_formato_invalido)

def test_cep_valido_api(mock_requests_get):
    # Simula resposta 200 e JSON sem "erro"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"cep": "12345-678"}
    mock_requests_get.return_value = mock_response

    s = servico()
    resultado = s.validar_cep_api("12345-678")

    assert resultado is True
    mock_requests_get.assert_called_once()


def test_cep_invalido_api(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"erro": True}  # sinaliza CEP inválido na API
    mock_requests_get.return_value = mock_response

    s = servico()
    resultado = s.validar_cep_api("00000-000")  # CEP qualquer inválido
    print(resultado)

    assert resultado is False
    mock_requests_get.assert_called_once()

def test_cep_api_excecao(mock_requests_get):
    # Simula exceção ao chamar requests.get
    mock_requests_get.side_effect = Exception("Erro na requisição")

    s = servico()
    resultado = s.validar_cep_api("99999-999")  # CEP qualquer

    print(resultado)

    # Espera que o método trate a exceção e retorne False
    assert resultado is False
    mock_requests_get.assert_called_once()
