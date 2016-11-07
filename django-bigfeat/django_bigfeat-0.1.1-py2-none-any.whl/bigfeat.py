from django.db.models.fields import BigIntegerField
from django.core import checks
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

@deconstructible
class BigFeat(object):
    value = 0
    masks = {}
    
    def __init__(self, value, masks):
        self.value = int(value)
        self.masks = masks
        super(BigFeat, self).__init__()
    
    def __eq__(self, other):
        return (self.value == other.value) and (self.masks == other.masks)
    
    def __int__(self):
        return self.value
    
    def __repr__(self, *args, **kwargs):
        return hex(self.value)
    
    def __getattr__(self, name):
        name_ci = name.upper()
        feature_mask = self.masks.get(name_ci, None)
        if feature_mask is None:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__name__, name))
        else:
            return True if (self.value & feature_mask) else False
    
    def __setattr__(self, name, value):
        name_ci = name.upper()
        feature_mask = self.masks.get(name_ci, None)
        if feature_mask is None:
            super(BigFeat, self).__setattr__(name, value)
        else:
            self.value = (self.value | feature_mask) if value else (self.value & ~feature_mask)

class BigFeatField(BigIntegerField):
    description = _("Big (63 bits) boolean")
    
    def __init__(self, masks=None, *args, **kwargs):
        self.masks = masks
        kwargs.setdefault('default', BigFeat(0, masks))
        super(BigFeatField, self).__init__(*args, **kwargs)
    
    def check(self, **kwargs):
        errors = super(BigFeatField, self).check(**kwargs)
        errors.extend(self._check_masks_attribute(**kwargs))
        return errors
    
    def _check_masks_attribute(self, **kwargs):
        if not self.masks:
            return [
                checks.Error(
                    "BigFeatFields must define a 'masks' attribute.",
                    hint=None,
                    obj=self,
                    id='bigfeat.E001',
                ),
            ]
        return []
    
    def get_prep_value(self, value):
        return int(value)
    
    def from_db_value(self, value, expression, connection, context):
        return None if value is None else BigFeat(value, self.masks)
    
    def to_python(self, value):
        return None if value is None else BigFeat(super(BigFeatField, self).to_python(value), self.masks)
