# -*- coding: utf-8 -*-
from pyvalidation.validacao import valida_cpf, valida_cnpj

__author__ = 'rodrigo'


def test_valida_cpf():
    assert valida_cpf('38449278597') == True
    assert valida_cpf('473.523.334-28') == True
    assert valida_cpf('319.627.714-31') == True
    assert valida_cpf('290.744.619-30') == True
    assert valida_cpf('84121280288') == True
    assert valida_cpf('535.347.740-51') == True
    # Todos os cpfs abaixo são inválidos
    assert valida_cpf('535.347.740-52') == False
    assert valida_cpf('64110936735') == False
    assert valida_cpf('18535865168') == False
    assert valida_cpf('313830366839') == False
    assert valida_cpf('4876777752') == False
    assert valida_cpf('00000000000') == False
    assert valida_cpf('11111111111') == False
    assert valida_cpf('22222222222') == False
    assert valida_cpf('33333333333') == False
    assert valida_cpf('44444444444') == False
    assert valida_cpf('55555555555') == False
    assert valida_cpf('66666666666') == False
    assert valida_cpf('77777777777') == False
    assert valida_cpf('88888888888') == False
    assert valida_cpf('99999999999') == False
    assert valida_cpf('73551826849') == False
    assert valida_cpf('26847233696 ') == False
    assert valida_cpf(' ') == False
    assert valida_cpf('           ') == False
    assert valida_cpf(None) == False
    assert valida_cpf('') == False
    assert valida_cpf('dddd') == False
    assert valida_cpf('pppppp') == False


def test_valida_cnpj():
    tests = []
    assert valida_cnpj('25378864000172 ') == False
    assert valida_cnpj('67.312.201/0001-03') == True
    assert valida_cnpj('11.444.777/0001-61') == True
    assert valida_cnpj('86.452.146/0001-93') == True
    assert valida_cnpj('22.347.342/0001-15') == True
    assert valida_cnpj('98011495000159') == True
    assert valida_cnpj('63258135000171') == True
    assert valida_cnpj('41088284000105') == True
    assert valida_cnpj('10276193000161') == True
    assert valida_cnpj('10.276.193/0001-61') == True
    assert valida_cnpj('15.045.096/0001-81') == True

    # Todos os cnpjs abaixo são inválidos
    assert valida_cnpj('24.237.510/0001-46') == False
    assert valida_cnpj('77.780.552/0001-10') == False
    assert valida_cnpj('44.152.617/0001-26') == False
    assert valida_cnpj('86.866.620/0001-20') == False
    assert valida_cnpj('71.662.874/0002-52') == False
    assert valida_cnpj('38370784010112') == False
    assert valida_cnpj('12980192000193') == False
    assert valida_cnpj('75550581000135') == False
    assert valida_cnpj('00000000000000') == False
    assert valida_cnpj('11111111111111') == False
    assert valida_cnpj('22222222222222') == False
    assert valida_cnpj('33333333333333') == False
    assert valida_cnpj('44444444444444') == False
    assert valida_cnpj('55555555555555') == False
    assert valida_cnpj('66666666666666') == False
    assert valida_cnpj('77777777777777') == False
    assert valida_cnpj('88888888888888') == False
    assert valida_cnpj('99999999999999') == False
    assert valida_cnpj('3837078401011') == False

    assert valida_cnpj(' ') == False
    assert valida_cnpj('           ') == False
    assert valida_cnpj(None) == False
    assert valida_cnpj('') == False
    assert valida_cnpj('iiiiikkk') == False
