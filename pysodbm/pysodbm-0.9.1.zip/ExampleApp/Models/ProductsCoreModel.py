#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pysodbm import *
import datetime


class ProductsCoreModel(EsgentoModel):
    ESEAN = EsgentoModelField(u"ESEAN", int, None)
    PRODUCT_TYPE_ID = EsgentoModelField(u"", int, 1)
    SKU = EsgentoModelField(u"SKU", int, 0)
    EAN = EsgentoModelField(u"EAN", unicode, "")
    MANUFACTURER_ID = EsgentoModelField(u"Hersteller Id", int, 182)
    MANUFACTURER_SKU = EsgentoModelField(u"Hersteller SKU", unicode, "")
    MANUFACTURER_MSRP = EsgentoModelField(u"Hersteller MSRP", float, 0)
    PRICE = EsgentoModelField(u"Preis", float, 0)
    CALC_FACTOR = EsgentoModelField(u"Rundungsfaktor", float, 1.35)
    ROUND_FACTOR = EsgentoModelField(u"Berechnungsfaktor", float, 0.0001)
    OVERWRITE_CALC_FACTOR = EsgentoModelField(u"Berechnungsfaktor überschreiben", int, 0)
    TAX = EsgentoModelField(u"MwSt Satz", int, 1)
    UNITS_ID = EsgentoModelField(u"Mengeneinheit Id", int, 0)
    WEIGHT = EsgentoModelField(u"Gewicht", float, 0)
    WIDTH = EsgentoModelField(u"Breite", float, 0)
    HEIGHT = EsgentoModelField(u"Höhe", float, 0)
    LENGTH = EsgentoModelField(u"Länge", float, 0)
    INTRASTAT = EsgentoModelField(u"Zoll-Tarif Nummer", unicode, "")
    COUNTRY_OF_ORIGIN = EsgentoModelField(u"Ursprungsland", unicode, "")
    MOQ = EsgentoModelField(u"Mindestbestellmenge", float, 1)
    PU = EsgentoModelField(u"Verpackungseinheit Verkauf", float, 1)
    PURCHASE_PU = EsgentoModelField(u"Verpackungseinheit Einkauf", float, 0)
    NAME_TEXT_IDENTIFIER = EsgentoModelField(u"Text Identifier Name", unicode, "")
    SHORT_TEXT_IDENTIFIER = EsgentoModelField(u"Text Identifier Kurztext", unicode, "")
    LONG_TEXT_IDENTIFIER = EsgentoModelField(u"Text Identifier Langtext", unicode, "")
    STATUS = EsgentoModelField(u"Status", int, 0)
    CHECKED = EsgentoModelField(u"Gechecked", int, 0)
    WEBSHOP = EsgentoModelField(u"Webshop", int, 0)
    DIGITAL_PRODUCT = EsgentoModelField(u"Digitalprodukt", int, 0)
    FREE_SHIPMENT = EsgentoModelField(u"Versandkostenfrei", int, 0)
    NON_AMAZON = EsgentoModelField(u"Amazonverkauf", int, 0)
    SUCCESSOR_ESEAN = EsgentoModelField(u"Folgeprodukt", int, 0)
    REORDER_LEVEL = EsgentoModelField(u"", int, 0)
    UPDATED = EsgentoModelField(u"Geändert", datetime.datetime, None, extra="on update CURRENT_TIMESTAMP")
    CREATED = EsgentoModelField(u"Erstellt", datetime.datetime, dbNow)

    dbTableName = "products"

    dbPrimaryKey = EsgentoModelKey(
        fields={
            "ESEAN": ESEAN
        },
        primaryKey=True
    )
