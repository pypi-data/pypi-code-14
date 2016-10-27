from motorway.contrib.recurly_integration.ramps import RecurlyInvoiceRamp
from motorway.intersection import Intersection
from motorway.pipeline import Pipeline
import logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s%(levelname)-8s%(reset)s %(name)-32s %(processName)-32s %(blue)s%(message)s"
        }
    },
    'loggers': {
        'motorway': {
            'level': 'WARN',
            'handlers': ['console'],
            'propagate': False
        },
        'werkzeug': {
            'level': 'WARN',
            'handlers': ['console'],
            'propagate': False,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'colored'
        }
    },
    'root': {
        'level': 'WARN',
        'handlers': ['console']
    }

})



class PrintIntersection(Intersection):
    def process(self, message):
        print message
        self.ack(message)
        yield


class SamplePipeline(Pipeline):
    def definition(self):
        self.add_ramp(RecurlyInvoiceRamp, 'invoices')
        self.add_intersection(PrintIntersection, 'invoices')


SamplePipeline().run()