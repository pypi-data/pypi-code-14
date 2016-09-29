__author__ = 'mnowotka'

from tastypie import fields
from tastypie.resources import ALL
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from chembl_webservices.core.utils import NUMBER_FILTERS, CHAR_FILTERS, FLAG_FILTERS

try:
    from chembl_compatibility.models import TargetRelations
except ImportError:
    from chembl_core_model.models import TargetRelations

from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

#-----------------------------------------------------------------------------------------------------------------------

class TargetRelationsResource(ChemblModelResource):

    target_chembl_id = fields.CharField('target__chembl__chembl_id')
    related_target_chembl_id = fields.CharField('related_target__chembl__chembl_id')

    class Meta(ChemblResourceMeta):
        queryset = TargetRelations.objects.all()
        excludes = ['targrel_id']
        resource_name = 'target_relation'
        collection_name = 'target_relations'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name : resource_name})
        detail_uri_name = 'chembl_id'
        prefetch_related = ['target', 'target__chembl', 'related_target', 'related_target__chembl']

        fields = (
            'relationship',
        )

        filtering = {
            'target_chembl_id' : NUMBER_FILTERS,
            'related_target_chembl_id' : CHAR_FILTERS,
            'relationship': CHAR_FILTERS,
        }
        ordering = [field for field in filtering.keys() if not ('comment' in field or 'description' in field or 'canonical_smiles' in field) ]

#-----------------------------------------------------------------------------------------------------------------------
