# coding=utf-8

from .fields import Field, IntegerField, CharField, ChecksumField, DateField, DecimalField


class AbstractFile(object):
    def calculate_authentication_code(self, *fields):
        pass

    @property
    def fields(self):
        fields = [getattr(self, field) for field in self.__dict__]
        fields = [field for field in fields if isinstance(field, Field)]
        fields = sorted(fields, key=lambda field: field.position[0])
        return fields

    def serialize(self):
        serialized = "".join([field.serialize() for field in self.fields])
        return serialized + "\r\n"


class Master(AbstractFile):

    def __init__(self):
        # 1 CPF ou CNPJ | len 14 | 1-14 | int
        self.registration = IntegerField((1, 14))
        # 2 Inscrição Estadual | len 14 | 15-28 | str
        self.state_subscription = CharField((15, 28), "ISENTO")
        # 3 Razão Social | len 35 | 29-63 | str
        self.legal_name = CharField((29, 63))
        # 4 UF | len 2 | 64-65 | str
        self.state_code = CharField((64, 65))
        # 5 Classe de Consumo ou Tipo de Assinante | len 1 | 66-66 | int
        self.subscription_type = IntegerField(66)
        # 6 Fase ou Tipo de Utilização | len 1 | 67-67 | int
        self.utilization_type = IntegerField(67)
        # 7 Grupo de Tensão | len 2 | 68-69 | int
        self.tension_group = IntegerField((68, 69))
        # 8 Código de identificação do consumidor ou assinante | len 12 | 70-81 | str
        self.client_identification = CharField((70, 81))
        # 9 Data de emissão | len 8 | 82-89 | int
        self.emission_date = DateField((82, 89))
        # 10 Modelo | len 2 | 90-91 | int
        self.model = IntegerField((90, 91))
        # 11 Série | len 3| 92-94 | str
        self.serie = CharField((92, 94))
        # 12 Número | len 9 | 95-103 | int
        self.number = IntegerField((95, 103))
        # 13 Código de Autenticação Digital documento fiscal | len 32 | 104-135 | str
        self.fiscal_document_authentication_code = ChecksumField((104, 135), self, fields=['registration', 'number', 'total_amount', 'bcicms', 'icms'])
        # 14 Valor total (com 2 decimais) | len 12 | 136-147 | int
        self.total_amount = DecimalField((136, 147))
        # 15 BCICMS (com 2 decimais) | len 12 | 148-159 | int
        self.bcicms = DecimalField((148, 159))
        # 16 ICMS destacado (com 2 decimais) | len 12 | 160-171 | int
        self.icms = DecimalField((160, 171))
        # 17 Operações isentas ou não tributadas (com 2 decimais) | len 12 | 172-183 | int
        self.not_taxed_operations = DecimalField((172, 183))
        # 18 Outros valores (com 2 decimais) | len 12 | 184-195 | int
        self.other_amount = DecimalField((184, 195))
        # 19 Situação do documento | len 1 | 196-196 | str
        self.situation = CharField(196)
        # 20 Ano e Mês de referência de apuração | len 4| 197-200 | int
        self.year_month_apuration = DateField((197, 200), date_format="%y%m")
        # 21 Referência ao item da NF | len 9 | 201-209 | int
        self.invoice_item_reference = IntegerField((201, 209))
        # 22 Número do terminal telefônico ou Número da conta de consumo | len 12 | 210-221 | str
        self.phone_number = CharField((210, 221))
        # 23 Brancos - reservado para uso futuro | len 5 | 222-226 | str
        self.blanks = CharField((222, 226))
        # 24 Código de autenticação Digital do registro | len 32 | 227-258 | str
        self.digital_register_authentication_code = ChecksumField((227, 258), self)


class Item(AbstractFile):
    def __init__(self):
        # 1 CNPJ ou CPF | len 14 | 1-14 | int
        self.registration = IntegerField((1, 14))
        # 2 UF | len 2 | 15-16 | str
        self.state_code = CharField((15, 16))
        # 3 Classe de Consumo ou Tipo de Assinante | len 1 | 17-17 | int
        self.subscription_type = IntegerField(17)
        # 4 Fase ou Tipo de Utilização | len 1 | 18-18 | int
        self.utilization_type = IntegerField(18)
        # 5 Grupo de Tensão | len 2 | 19-20 | int
        self.tension_group = IntegerField((19, 20))
        # 6 Data de Emissão | len 8 | 21-28 | int
        self.emission_date = DateField((21, 28))
        # 7 Modelo | len 2 | 29-30 | str
        self.model = CharField((29, 30))
        # 8 Série | len 3 | 31-33 | str
        self.serie = CharField((31, 33))
        # 9 Número | len 9 | 34-42 | int
        self.number = IntegerField((34, 42))
        # 10 CFOP | len 4 | 43-46 | int
        self.cfop = IntegerField((43, 46))
        # 11 Item | len 3 | 47-49 | int
        self.item = IntegerField((47, 49))
        # 12 Código de serviço ou fornecimento | len 10 | 50-59 | str
        self.item_code = CharField((50, 59))
        # 13 Descrição do serviço ou fornecimento | len 40 | 60-99 | str
        self.item_description = CharField((60, 99))
        # 14 Código de classificação do item| len 4 | 100-103 | int
        self.item_classification = IntegerField((100, 103))
        # 15 Unidade | len 6 | 104-109 | str
        self.unit = CharField((104, 109))
        # 16 Quantidade contratada (com 3 decimais) | len 11 | 110-120 | int
        self.requested_quantity = DecimalField((110, 120), precision=3)
        # 17 Quantidade prestada ou fornecida (com 3 decimais) | len 11 | 121-131 | int
        self.provided_quantity = DecimalField((121, 131), precision=3)
        # 18 Total (com 2 decimais) | len 11 | 132-142 | int
        self.total_amount = DecimalField((132, 142))
        # 19 Desconto (com 2 decimais) | len 11 | 143-153 | int
        self.discount = DecimalField((143, 153))
        # 20 Acréscimo e Despesas Acessoriais (com 2 decimais) | len 11 | 154-164 | int
        self.accessory_expenses = DecimalField((154, 164))
        # 21 BC ICMS (com 2 decimais) | len 11 | 165-175 | int
        self.bcicms = DecimalField((165, 175))
        # 22 ICMS (com 2 decimais) | len 11 | 176-186 | int
        self.icms = DecimalField((176, 186))
        # 23 Operações Isentas ou não tributadas (com 2 decimais) | len 11 | 187-197 | int
        self.not_taxed_operations = DecimalField((187, 197))
        # 24 Outros valores que não compõe a BC do ICMS (com 2 decimais) | len 11 | 198-208 | int
        self.other_amount = DecimalField((198, 208))
        # 25 Alíquota do ICMS (com 2 decimais) | len 4 | 209-212 | int
        self.icms_aliquote = DecimalField((209, 212))
        # 26 Situação | len 1 | 213-213 | str
        self.situation = CharField(213)
        # 27 Ano e Mês de referência de apuração | len 4 | 214-217 | str
        self.year_month_apuration = DateField((214, 217), date_format="%y%m")
        # 28 Brancos - reservado para uso futuro | len 5 | 218-222 | str
        self.blanks = CharField((218, 222))
        # 29 Código de Autenticação Digital do registro | len 32 | 223-254 | str
        self.digital_register_authentication_code = ChecksumField((227, 258), self)


class Register(AbstractFile):
    def __init__(self):
        # 1 CNPJ ou CPF | len 14 | 1-14 | int
        self.registration = IntegerField((1, 14))
        # 2 IE | len 14 | 15-28 | str
        self.state_subscription = CharField((15, 28), "ISENTO")
        # 3 Razão Social | len 35 | 29-63 | str
        self.legal_name = CharField((29, 63))
        # 4 Logradouro | len 45 | 64-108 | str
        self.street = CharField((64, 108))
        # 5 Número | len 5 | 109-113 | int
        self.number = IntegerField((109, 113))
        # 6 Complemento | len 15 | 114-128 | str
        self.complement = CharField((114, 128))
        # 7 CEP | len 8 | 129-136 | int
        self.zip_code = IntegerField((129, 136))
        # 8 Bairro | len 15 | 137-151 | str
        self.neighborhood = CharField((137, 151))
        # 9 Município | len 30 | 152-181 | str
        self.city = CharField((152, 181))
        # 10 UF | len 2 | 182-183 | str
        self.state_code = CharField((182, 183))
        # 11 Telefone de contato | len 12 | 184-195 | int
        self.phone = IntegerField((184, 195))
        # 12 Código de Identificação do consumidor ou assinante | len 12 | 196-207 | str
        self.client_code = CharField((196, 207))
        # 13 Número do terminal telefônico ou Número de conta do consumo | len 12 | 208-219 | str
        self.contract_code = CharField((208, 219))
        # 14 UF de habilitação do terminal telefônico | len 2 | 220-221 | str
        self.contract_state = CharField((220, 221))
        # 15 Brancos - reservado para uso futuro | len 5 | 222-226 | str
        self.blanks = CharField((222, 226))
        # 16 Código de Autenticação Digital do registro | len 32 | 227-258 | str
        self.digital_register_authentication_code = ChecksumField((227, 258), self)
