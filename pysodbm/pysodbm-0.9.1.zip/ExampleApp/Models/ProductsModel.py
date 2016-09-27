#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pysodbm import EsgentoDataClass, EsgentoModelOneToOneRelation, \
    EsgentoModelOneToManyRelation, EsgentoModelManyToManyRelation

from .ProductsCoreModel import ProductsCoreModel

__author__ = 'Marco Bartel'


class ProductsModel(ProductsCoreModel):
    TAX_RATES = EsgentoModelOneToOneRelation(
        singletonClass="TaxRates",
        filter={
            "TAX_TYPE_ID": ProductsCoreModel.TAX
        }
    )

    SUPPLIERS = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasSupplier",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )
    NAME_TEXT = EsgentoModelOneToOneRelation(
        singletonClass="Text",
        filter={
            "IDENTIFIER": ProductsCoreModel.NAME_TEXT_IDENTIFIER
        },
        newObjectIfNotFound=True
    )
    SHORT_TEXT = EsgentoModelOneToOneRelation(
        singletonClass="Text",
        filter={
            "IDENTIFIER": ProductsCoreModel.SHORT_TEXT_IDENTIFIER
        },
        newObjectIfNotFound=True
    )

    LONG_TEXT = EsgentoModelOneToOneRelation(
        singletonClass="Text",
        filter={
            "IDENTIFIER": ProductsCoreModel.LONG_TEXT_IDENTIFIER
        },
        newObjectIfNotFound=True
    )

    SELLING_PLATFORMS = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasSellingPlatform",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    SELLING_PLATFORM_VERKAUF = EsgentoModelOneToOneRelation(
        singletonClass="SellingPlatform",
        filter={
            "ID": 1
        }
    )

    RESERVATIONS = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasReservation",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    STOCK = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasStock",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    STORAGE = EsgentoModelOneToManyRelation(
        singletonClass="StockHasStorage",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    MANUFACTURER = EsgentoModelOneToOneRelation(
        singletonClass="Manufacturer",
        filter={
            "ID": ProductsCoreModel.MANUFACTURER_ID
        }
    )

    MAIN_PICTURE = EsgentoModelManyToManyRelation(
        singletonClass="Picture",
        combiningClass="ProductHasPicture",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN,
            "MAINPICTURE": 1
        }
    )
    PICTURES = EsgentoModelManyToManyRelation(
        singletonClass="Picture",
        combiningClass="ProductHasPicture",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )
    LICENSES = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasLicense",
        filter={
            "PRODUCTS_SKU": ProductsCoreModel.SKU
        }
    )
    SLAVES = EsgentoModelManyToManyRelation(
        singletonClass="Product",
        combiningClass="ProductHasSlaves",
        relationName="SLAVE",
        filter={
            "MASTER_SKU": ProductsCoreModel.SKU
        }
    )
    UNIT = EsgentoModelOneToOneRelation(
        singletonClass="Unit",
        filter={
            "ID": ProductsCoreModel.UNITS_ID
        }
    )

    MASTER = EsgentoModelManyToManyRelation(
        singletonClass="Product",
        combiningClass="ProductHasSlaves",
        relationName="MASTER",
        filter={
            "SLAVE_SKU": ProductsCoreModel.SKU
        }
    )
    CARTS = EsgentoModelOneToManyRelation(
        singletonClass="CartHasProduct",
        filter={
            "PRODUCTS_SKU": ProductsCoreModel.SKU
        }
    )
    DELIVERY_DATE = EsgentoModelOneToOneRelation(
        singletonClass="ProductHasDeliveryDate",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    CATEGORIES = EsgentoModelManyToManyRelation(
        singletonClass="Category",
        combiningClass="ProductHasCategories",
        relationName="CATEGORY",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }

    )

    COSTS = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasCosts",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    FOLLOW_PRODUCT = EsgentoModelOneToOneRelation(
        singletonClass="Product",
        filter={
            "ESEAN": ProductsCoreModel.SUCCESSOR_ESEAN
        }
    )

    PACKAGE_UNITS = EsgentoModelOneToManyRelation(
        singletonClass="ProductHasPackageUnit",
        filter={
            "ESEAN": ProductsCoreModel.ESEAN
        }
    )

    TYPE = EsgentoModelOneToOneRelation(
        singletonClass="ProductsType",
        filter={
            "ID": ProductsCoreModel.PRODUCT_TYPE_ID
        }
    )


class ProductsData(EsgentoDataClass):
    esgentoModel = ProductsModel


