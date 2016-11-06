# coding: utf-8

from modeltranslation.translator import translator, TranslationOptions
from textflow.models import FlowObject


class FlowObjectTranslationOption(TranslationOptions):
    fields = ('text',)

translator.register(FlowObject, FlowObjectTranslationOption)
