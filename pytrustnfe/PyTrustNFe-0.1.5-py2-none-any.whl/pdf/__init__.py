# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from super_table import PdfTable, PdfCell
from pytrustnfe import xml

inch = 28.34


class Danfe(object):

    objeto = None

    def __init__(self, objetoNFe):
        self.objeto = xml.sanitize_response(objetoNFe)[1]
        self.NFe = self.objeto.getchildren()[2]
        self.infNFe = self.NFe.getchildren()[0]
        self.ide = self.infNFe.getchildren()[0]
        self.emitente = self.infNFe.getchildren()[1]
        self.destinatario = self.infNFe.getchildren()[2]

    def gerar(self):
        table = PdfTable(columns=30, width=(20 * INCH)*1.7)

        table2 = PdfTable(columns=12)

        table2.add_cell(PdfCell('RECEBEMOS DE ISOCOMPÓSITOS EIRELI ME OS PRODUTOS \
    E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL ELETRÔNICA INDICADA AO LADO',
                        colspan=12))
        table2.add_cell(PdfCell('Data de Recebimento', colspan=2))
        table2.add_cell(PdfCell('Assinatura', colspan=10))

        table.add_cell(PdfCell(table2, colspan=10))
        table.add_cell(PdfCell(table2, colspan=20))

        table = table.render()

        doc = SimpleDocTemplate("ola.pdf", pagesize=A4, leftMargin=0,
                                rightMargin=0, topMargin=0, bottomMargin=0)
        doc.build([table])
