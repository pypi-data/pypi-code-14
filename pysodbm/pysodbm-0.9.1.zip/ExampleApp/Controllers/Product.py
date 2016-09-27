#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ExampleApp.Models.ProductsModel import ProductsModel, ProductsData
from pysodbm import EsgentoSingletonClass

__author__ = 'Marco Bartel'

class Product(EsgentoSingletonClass):
    esgentoModel = ProductsModel
    dataClass = ProductsData
