#!/usr/bin/env python3
"""
Este script tem como objetivo facilitar a obtenção de dados do CEP através do
website da Correios.
"""

import json
import shelve
import requests
from bs4 import BeautifulSoup

__version__ = "1.0"
__author__ = "Emanuel A. Leite <androidel@openmailbox.org>"


class CepDatabase:

    """
    Esta classe controla o manuseio dos dados do banco de dados.
    """

    def __init__(self, filepath="ceps.shelf"):
        """
        Inicializa o banco de dados e as chaves com os respectivos valores
        padrões se os mesmos não existirem.
        """
        self._db = shelve.open(filepath or "ceps.shelf")
        if not self._db.get("last_cep"):
            self._db["last_cep"] = None
        if not self._db.get("ceps"):
            self._db["ceps"] = []

    def update_last_cep(self, value):
        """Atualiza o CEP."""
        self._db["last_cep"] = str(value).rjust(8, "0")

    def last_verified_cep(self):
        """Obtém o último CEP verificado."""
        return self._db["last_cep"]

    def store(self, cep):
        """Armazena os dados do CEP no banco de dados."""
        ceps = self._db.get("ceps")
        ceps.append(cep)
        self._db["ceps"] = ceps

    def get_all(self):
        """
        Obtém todos os CEPs do banco de dados.
        """
        return self._db.get("ceps")


class BaseRequestCep:

    """
    Esta classe possui a base necessária para o funcionamento das requisições e
    para a obtenção dos dados.
    """

    _url = ("http://www.buscacep.correios.com.br/sistemas/buscacep/"
            "detalhaCEP.cfm")
    """
    URL utilizada nas requisições dos dados do CEP.
    """
    _states = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )

    def get_state_by_initials(self, initials):
        """
        Obtém os dados de um estado específico pelas inicias do mesmo.
        """
        group_initials = tuple(state[0] for state in self._states)
        if initials not in group_initials:
            return
        index = group_initials.index(initials)
        return self._states[index]

    def search(self, cep):
        """
        Requisita os dados de um específico CEP pela Correios e retorna os
        seguintes dados:

        * Logradouro
        * Bairro
        * Cidade
        * Estado (UF e nome)
        * CEP (formatado em: "99999-999")
        """
        # CEP precisa ser uma string e ter 8 caracteres
        if not isinstance(cep, str) and len(cep) != 8:
            raise Exception("Erro de validação para o CEP: " + cep)
        # Requisita pelos dados
        request = requests.post(self._url, {"CEP": cep})
        if not all((request, request.ok)):
            raise Exception("Erro ao conectar-se com o servidor!")
        html = BeautifulSoup(request.text, "html.parser")
        # Obtém os dados de cada linha da tabela
        rows = html.select("table.tmptabela tr td")[:4]
        rows = tuple((r.get_text().strip() for r in rows))
        try:
            city, state = rows[2].split("/")
            state = self.get_state_by_initials(state)
            streetname, neighborhood, city, state, zipcode = (
                *rows[0:2], city, state, rows[3])
            return {
                "streetname": streetname,
                "neighborhood": neighborhood,
                "city": city,
                "state": {
                    "initials": state[0],
                    "name": state[1],
                },
                "zipcode": zipcode,
            }
        except IndexError:
            return


class RequestCep(BaseRequestCep):

    """
    Esta classe possui funcionalidades extras da classe `BaseRequestCep`.
    """

    _ceps = (
        (1000, 10000), (11000, 20000), (20000, 29000), (29000, 30000),
        (30000, 39991), (40000, 49000), (49000, 50000), (50000, 57000),
        (57000, 58000), (58000, 59000), (59000, 60000), (60000, 63991),
        (64000, 64991), (65000, 65991), (66000, 68891), (68900, 69000),
        (69000, 69300), (69400, 69900), (69300, 69400), (70000, 73700),
        (73700, 76800), (76800, 77000), (77000, 78000), (78000, 78900),
        (79000, 80000), (80000, 88000), (88000, 90000), (90000, 100000),
    )
    """
    São os prefixos dos CEPs nomeados para cada região ou estado do Brasil.

    https://pt.wikipedia.org/wiki/Código_de_Endereçamento_Postal#Estrutura_do_CEP
    """

    def download_all(self, dbfilepath="ceps.shelf"):
        """
        Pesquisa CEP por CEP verificando se existe ou não. Se existir, os
        dados do CEP atual são inseridos no banco de dados.
        """
        cepdb = CepDatabase(filepath=dbfilepath)
        last_cep = cepdb.last_verified_cep()
        if last_cep:
            last_cep = str(int(last_cep)+1).rjust(8, "0")
        for cep_range in self._ceps:
            start, end = cep_range
            if last_cep:
                start = int(last_cep[:5]) or start
            for prefix in range(start, end):
                prefix = str(prefix).rjust(5, "0")
                start = 0
                if last_cep:
                    start = int(last_cep[5:]) or 0
                for suffix in range(start, 1000):
                    suffix = str(suffix).rjust(3, "0")
                    cep = prefix + suffix
                    data = self.search(cep)
                    if data:
                        cepdb.store(data)
                        print(data)
                    else:
                        print("CEP {} não encontrado".format(cep))
                    cepdb.update_last_cep(cep)
                last_cep = None
            last_cep = None

    def _get_index(self, value):
        """
        Obtém o índice de `self._ceps` através do valor informado.
        """
        if not isinstance(value, int):
            if isinstance(value, str):
                value = int(value)
            else:
                raise Exception("Tipo de dado inválido!")
        for idx, cep in enumerate(self._ceps):
            start, end = cep
            if end > value >= start:
                return idx
        return


def generate_json(filepath="ceps.json", dbfilepath="ceps.shelf"):
    """
    Exporta os registros do banco de dados para um arquivo no formato
    JSON. Use `filepath` para alterar o caminho onde o arquivo será salvo.
    """
    filepath = filepath or "ceps.json"
    cepdb = CepDatabase(filepath=dbfilepath)
    data = cepdb.get_all()
    data = json.dumps(data, indent=4)
    open(filepath, "w").write(data)
