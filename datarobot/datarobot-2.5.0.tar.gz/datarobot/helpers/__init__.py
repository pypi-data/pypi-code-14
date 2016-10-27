from .partitioning_methods import *  # noqa


class RecommenderSettings(object):
    recommender_user_id = None
    recommender_item_id = None

    def __init__(self, recommender_user_id, recommender_item_id):
        self.recommender_user_id = recommender_user_id
        self.recommender_item_id = recommender_item_id

    def collect_payload(self):
        payload = {
            'recommender_user_id': self.recommender_user_id,
            'recommender_item_id': self.recommender_item_id
        }
        return payload


class AdvancedOptions(object):
    """
    Used when setting the target of a project to set advanced options of modeling process.

    Parameters
    ----------
    weights : string, optional
        The name of a column indicating the weight of each row
    response_cap : float in [0.5, 1), optional
        Quantile of the response distribution to use for response capping.
    blueprint_threshold : int, optional
        Number of hours models are permitted to run before being excluded from later autopilot
        stages
        Minimum 1
    seed : int
        a seed to use for randomization
    smart_downsampled : bool
        whether to use smart downsampling to throw away excess rows of the majority class.  Only
        applicable to classification and zero-boosted regression projects.
    majority_downsampling_rate : float
        the percentage between 0 and 100 of the majority rows that should be kept.  Specify only if
        using smart downsampling.  May not cause the majority class to become smaller than the
        minority class.

    Examples
    --------
    .. code-block:: python

        import datarobot as dr
        advanced_options = dr.AdvancedOptions(
            weights='weights_column',
            response_cap=0.7,
            blueprint_threshold=2,
            smart_downsampled=True, majority_downsampling_rate=75.0)

    """
    def __init__(self, weights=None, response_cap=None, blueprint_threshold=None,
                 seed=None, smart_downsampled=False, majority_downsampling_rate=None):
        self.weights = weights
        self.response_cap = response_cap
        self.blueprint_threshold = blueprint_threshold
        self.seed = seed
        self.smart_downsampled = smart_downsampled
        self.majority_downsampling_rate = majority_downsampling_rate

    def collect_payload(self):

        payload = dict(
            weights=self.weights,
            response_cap=self.response_cap,
            blueprint_threshold=self.blueprint_threshold,
            seed=self.seed,
            smart_downsampled=self.smart_downsampled,
            majority_downsampling_rate=self.majority_downsampling_rate
        )
        return payload
