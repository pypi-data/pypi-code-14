from numpy import zeros
from .explainers.esvalues import ESValuesExplainer

def explain(f, outNames, x, featureNames, *args):
    data = args[0] if len(args) > 0 else zeros(len(x))
    explainer = args[1] if len(args) > 1 else ESValuesExplainer()
    return explainer.explain(f, outNames, x, featureNames, data)
