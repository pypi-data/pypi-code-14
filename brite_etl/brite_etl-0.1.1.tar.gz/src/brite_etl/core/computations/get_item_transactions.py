from brite_etl.decorators import get_frames, computation
import pandas as pd


@computation
@get_frames('revisions', 'property_items', 'revision_items', 'prepared.accounting')
def get_item_transactions(frames=None):
    """
    This function does "shift magic" to create item-level transactions
    """

    revisions = frames.get('revisions').df
    prop_items = frames.get('property_items').df
    revision_items = frames.get('revision_items').df

    revisions['commitDate'] = pd.to_datetime(revisions['commitDate'])
    revisions['revisionDate'] = pd.to_datetime(revisions['revisionDate'])
    revisions = revisions[['revisionId', 'commitDate', 'revisionDate', 'policyId', 'policyTermId', 'policyStatus',
                           'revisionState', 'createDate']]
    revisions.is_copy = False  # To shut up the SettingWithCopyWarning
    revisions['applyDate'] = revisions[['commitDate', 'revisionDate']].max(axis=1)

    columns = ['policyId', 'revisionId', 'policyTypeItemName', 'subLineName',
               'dateAdded', 'dateAddedMicro',
               'limit', 'writtenPremium', 'annualPremium',
               'deleted', 'policyTypeItemType', 'propertyId', 'manual']
    prop_items = prop_items[columns]
    revision_items = revision_items[columns]

    items = pd.concat([prop_items, revision_items])

    items = pd.merge(items, revisions)
    total_items = len(items)
    items = items.sort_values(['policyId', 'policyTypeItemName', 'dateAdded', 'dateAddedMicro', 'applyDate',
                               'revisionDate', 'createDate'])
    items = items.reset_index(drop=True)

    items_shifted = (
        items
        .groupby(['policyId', 'policyTypeItemName', 'dateAdded', 'dateAddedMicro'])
        .shift(1)
        [['limit', 'annualPremium', 'writtenPremium']]
    )

    items_shifted = items_shifted.rename(columns={'limit': 'prev_limit',
                                                  'annualPremium': 'prev_annualPremium',
                                                  'writtenPremium': 'prev_writtenPremium'})

    items_shifted = items_shifted.fillna(0.0)
    items = pd.concat([items, items_shifted], axis=1)

    assert len(items) == total_items

    # remove deleted items that were never real
    items = items[~((items.deleted == 1) & (items.prev_writtenPremium == 0.0))]

    items['trans_limit'] = items.limit - items.prev_limit
    items['trans_annualPremium'] = items.annualPremium - items.prev_annualPremium
    items['trans_writtenPremium'] = items.writtenPremium - items.prev_writtenPremium

    return items
