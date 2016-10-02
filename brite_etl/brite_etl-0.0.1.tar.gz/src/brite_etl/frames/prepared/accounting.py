from brite_etl.abstracts import Frame
from brite_etl.utils import _btl


class Accounting(Frame):

    _config = {
        'name': 'accounting',
        'prepared': True
    }

    def endOfMonthSum(self):
        cols = [
            'changeInPaidCustomFee',
            'changeInPaidSystemFee',
            'endingAdvancedPremium'
        ]

        result = _btl(self.df[cols]).sum_cols(cols).value()
        return result
