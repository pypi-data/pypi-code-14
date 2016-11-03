# -*- coding: utf-8 -*-

from __future__ import absolute_import
import logging

log = logging.getLogger(__name__)


class SchemaConstructor(object):

    @classmethod
    def get_Ubicacion_schema(self, cfdi_version):
        cfdi_version = self.get_cfdi_version(cfdi_version)
        _versions = {
            '3.2': {
                'calle': {
                    'type': 'string',
                    'minlength': 1,
                },
                'noExterior': {
                    'type': 'string',
                    'minlength': 1,
                },
                'noInterior': {
                    'type': 'string',
                    'minlength': 1,
                },
                'colonia': {
                    'type': 'string',
                    'minlength': 1,
                },
                'localidad': {
                    'type': 'string',
                    'minlength': 1,
                },
                'referencia': {
                    'type': 'string',
                    'minlength': 1,
                },
                'municipio': {
                    'type': 'string',
                    'minlength': 1,
                },
                'estado': {
                    'type': 'string',
                    'minlength': 1,
                },
                'pais': {
                    'type': 'string',
                    'minlength': 1,
                },
                'codigoPostal': {
                    'type': 'mx_zipcode',
                }
            }
        }
        return self.get_schema_by_version(_versions, cfdi_version)

    @classmethod
    def get_UbicacionFiscal_schema(self, cfdi_version):
        cfdi_version = self.get_cfdi_version(cfdi_version)
        _versions = {}
        version_3_2 = self.get_Ubicacion_schema(cfdi_version)

        for field in ('calle', 'municipio', 'estado', 'pais', 'codigoPostal'):
            version_3_2[field]['required'] = True

        _versions['3.2'] = version_3_2
        return self.get_schema_by_version(_versions, cfdi_version)

    @classmethod
    def get_InformacionAduanera_schema(self, cfdi_version):
        cfdi_version = self.get_cfdi_version(cfdi_version)
        _versions = {
            '3.2': {
                'numero': {
                    'type': 'string',
                    'minlength': 1,
                    'required': True,
                },
                'fecha': {
                    'type': 'iso8601_date',
                    'required': True,
                },
                'aduana': {
                    'type': 'string',
                    'minlength': 1,
                },
            }
        }
        return self.get_schema_by_version(_versions, cfdi_version)

    @classmethod
    def get_Comprobante_schema(self, cfdi_version=None):
        cfdi_version = self.get_cfdi_version(cfdi_version)
        _versions = {
            '3.2': {
                'serie': {
                    'type': 'alphanumeric',
                    'minlength': 1,
                    'maxlength': 25,
                    'coerce': str,
                },
                'folio': {
                    'type': 'integer',
                    'min': 1,
                    'max': int('9' * 20)
                },
                'fecha': {
                    'type': 'iso8601_datetime',
                    'required': True,
                },
                'formaDePago': {
                    'type': 'string',
                    'required': True,
                },
                'condicionesDePago': {
                    'type': 'string',
                    'minlength': 1,
                },
                'subTotal': {
                    'type': 'importe',
                    'coerce': float,
                    'required': True,
                },
                'descuento': {
                    'type': 'importe',
                    'coerce': float,
                },
                'motivoDescuento': {
                    'type': 'string',
                    'minlength': 1,
                },
                'TipoCambio': {
                    'type': 'string',
                },
                'Moneda': {
                    'type': 'string',
                },
                'total': {
                    'type': 'importe',
                    'required': True,
                    'coerce': float,
                },
                'tipoDeComprobante': {
                    'type': 'string',
                    'allowed': ['ingreso', 'egreso', 'traslado'],
                    'required': True,
                },
                'metodoDePago': {
                    'type': 'string',
                    'minlength': 1,
                    'required': True,
                },
                'TipoCambio': {
                    'type': 'string',
                },
                'Moneda': {
                    'type': 'string',
                },
                'LugarExpedicion': {
                    'type': 'string',
                    'minlength': 1,
                    'required': True,
                },
                'NumCtaPago': {
                    'type': 'numeric',
                    'minlength': 4,
                },
                'FolioFiscalOrig': {
                    'type': 'string',
                },
                'SerieFolioFiscalOrig': {
                    'type': 'string',
                },
                'FechaFolioFiscalOrig': {
                    'type': 'iso8601_datetime',
                },
                'MontoFolioFiscalOrig': {
                    'type': 'importe',
                    'coerce': float,
                },
                'Emisor': {
                    'type': 'dict', 'required': True,
                    'schema': {
                        'DomicilioFiscal': {
                            'type': 'dict',
                            'schema': self.get_UbicacionFiscal_schema(cfdi_version),
                        },
                        'ExpedidoEn': {
                            'type': 'dict',
                            'required': True,
                            'schema': self.get_Ubicacion_schema(cfdi_version),
                        },
                        'RegimenFiscal': {
                            'type': ['string', 'list'],
                            'required': True,
                            'minlength': 1,
                            'schema': {
                                'type': 'string',
                            }
                        },
                        'rfc': {
                            'type': 'rfc',
                            'required': True,
                        },
                        'nombre': {
                            'type': 'string',
                            'minlength': 1,
                            'required': True,
                        },
                    }
                },
                'Receptor': {
                    'type': 'dict', 'required': True,
                    'schema': {
                        'Domicilio' : {
                            'type': 'dict',
                            'schema': self.get_Ubicacion_schema(cfdi_version),
                        },
                        'rfc': {
                            'type': 'rfc',
                            'required': True,
                        },
                        'nombre': {
                            'type': 'string',
                            'minlength': 1,
                            'required': True,
                        }
                    }
                },
                'Conceptos': {
                    'type': 'list',
                    'required': True,
                    'minlength': 1,
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'cantidad': {
                                'type': 'number',
                                'required': True,
                                'coerce': float,
                            },
                            'unidad': {
                                'type': 'string',
                                'minlength': 1,
                                'required': True,
                            },
                            'noIdentificacion': {
                                'type': 'string',
                                'minlength': 1,
                            },
                            'descripcion': {
                                'type': 'string',
                                'minlength': 1,
                                'required': True
                            },
                            'valorUnitario': {
                                'type': 'importe',
                                'required': True,
                                'coerce': float,
                            },
                            'importe': {
                                'type': 'importe',
                                'required': True,
                                'coerce': float,
                            },
                            'InformacionAduanera': {
                                'type': 'dict',
                                'schema': self.get_InformacionAduanera_schema(cfdi_version),
                            },
                            'CuentaPredial': {
                                'type': 'dict',
                                'schema': {
                                    'numero': {
                                        'type': 'string',
                                        'minlength': 1,
                                        'required': True
                                    }
                                }
                            },
                            'ComplementoConcepto': {
                                'type': 'dict',
                            }
                            # TODO: 'Parte': {}
                        }
                    }
                },
                'Impuestos': {
                    'type': 'dict',
                    'required': True,
                    'default': {},
                    'schema': {
                        'totalImpuestosRetenidos': {
                            'type': 'importe',
                            'coerce': float,
                        },
                        'totalImpuestosTrasladados': {
                            'type': 'importe',
                            'coerce': float,
                        },
                        'Retenciones': {
                            'type': 'list',
                            'minlength': 1,
                            'schema': {
                                'type': 'dict',
                                'schema': {
                                    'impuesto': {
                                        'type': 'string',
                                        'allowed': ['IVA', 'ISR'],
                                        'required': True,
                                    },
                                    'importe': {
                                        'type': 'importe',
                                        'required': True,
                                        'coerce': float,
                                    }
                                }
                            }
                        },
                        'Traslados': {
                            'type': 'list',
                            'minlength': 1,
                            'schema': {
                                'type': 'dict',
                                'schema': {
                                    'impuesto': {
                                        'type': 'string',
                                        'allowed': ['IVA', 'IEPS'],
                                        'required': True,
                                    },
                                    'importe': {
                                        'type': 'importe',
                                        'required': True,
                                        'coerce': float,
                                    },
                                    'tasa': {
                                        'type': 'importe',
                                        'required': True,
                                        'coerce': float,
                                    }
                                }
                            }
                        },
                    },

                },
                'Complemento': {'type': 'dict'},
            }
        }
        return self.get_schema_by_version(_versions, cfdi_version)

    @classmethod
    def get_schema(self, cfdi_version):
        self.cfdi_version = cfdi_version
        _versions = {
            '3.2': {
                'Comprobante': {
                    'type': 'dict', 'required': True,
                    'schema': self.get_Comprobante_schema(self.cfdi_version),
                },
            }
        }

        return self.get_schema_by_version(_versions, self.cfdi_version)

    @classmethod
    def get_cfdi_version(self, cfdi_version=None):
        if cfdi_version is None:
            return self.cfdi_version
        return cfdi_version

    @staticmethod
    def get_schema_by_version(versions, cfdi_version):
        try:
            return versions[cfdi_version]
        except KeyError:
            log.exception("CFDI version \"{}\" not supported.".format(cfdi_version))
            raise
