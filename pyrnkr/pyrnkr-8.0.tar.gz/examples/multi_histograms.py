import numpy as np

from pyrnkr.widgets.models import BasicHistogram, StackedHistogram
from pyrnkr.formula.models import Trace
from pyrnkr.artifacts.models import App


class MultiHistogramsSampler(App):
    required_parameters = ['mu', 'sigma', 'samples']
    name = 'Normal Distribution Sampler'

    def _get_normal_trace(self, title, mu, sigma, samples):
        return Trace(
            title=title,
            x=np.random.normal(mu, sigma, samples).tolist(),
            trace_type=Trace.TYPE_HISTOGRAM
        )

    def _execute(self, parameters):
        mu, sigma = float(parameters['mu']), float(parameters['sigma'])
        samples = int(parameters['samples'])

        basic = BasicHistogram(trace=self._get_normal_trace(
            'Basic Histogram', mu, sigma, samples))

        stacked = StackedHistogram(traces=[
            self._get_normal_trace('Basic Histogram', mu, sigma, samples),
            self._get_normal_trace('Basic Histogram', mu, sigma, samples)
        ])

        return [
            [basic],
            [stacked]
        ]


def handler(event, context):
    return MultiHistogramsSampler().run(event)
