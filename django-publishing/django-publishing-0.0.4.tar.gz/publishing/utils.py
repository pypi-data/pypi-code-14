# -*- coding: utf-8 -*-
from django.db.models import *


RELATED_SIMPLE_FIELDS = (
    BigIntegerField,
    BinaryField,
    BooleanField,
    CharField,
    CommaSeparatedIntegerField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    EmailField,
    FileField,
    FilePathField,
    FloatField,
    ImageField,
    IntegerField,
    GenericIPAddressField,
    NullBooleanField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SlugField,
    SmallIntegerField,
    TextField,
    URLField,
    UUIDField,
)


SIMPLE_FIELDS =  RELATED_SIMPLE_FIELDS + (ForeignKey, )

RELATION_FIELDS = (
    ManyToOneRel,
)

ADVANCED_RELATION_FIELDS = (
    OneToOneField,
)

BLACKLIST_FIELDS = (
    'draft',
    'is_draft',
    'draft_of',
    'has_draft',

    'uuid',
    '_order',
    'created',
    'modified',
)


def clone_fields(instance, duplicate, related=False, ignored_fields=[], ):
    # get all fields from model
    model_fields = instance._meta.get_fields()

    # set instance fields
    for field in model_fields:

        # set simple instance attribute
        if type(field) in SIMPLE_FIELDS and field.name not in BLACKLIST_FIELDS:
            if related and field.name in ignored_fields:
                # dont copy ignored fields, for example many_to_one relations
                continue
            else:
                setattr(instance, field.name, getattr(duplicate, field.name, None))

    # save instance after all simple fields were set, includes ForeignKey field
    # in case a field is set to not null.
    instance.save()

    for field in model_fields:
        # set relation fields
        if type(field) in RELATION_FIELDS and field.name not in BLACKLIST_FIELDS:
            instance, draft = clone_relations(instance, duplicate, field)

    instance.save()
    return instance


def clone_relations(instance, duplicate, field):
    related_instance_items = getattr(duplicate, field.name).all()

    # create draft or publish draft
    for item in related_instance_items:

        # existing draft
        if item.is_draft and item.draft_of:
            # update original item by draft value, don't update foreignkey for model itself
            ignored_fields = [field.remote_field.name, ]
            result_item = clone_fields(item.draft_of, item, related=True, ignored_fields=ignored_fields, )
            result_item.save()
        elif item.is_draft:
            # unpublished item
            print("CLONE RELATIONS NOT HANDLED (is_draft, not draft_of)")
        else:
            # create new draft item
            new_item = item.__class__()
            new_item = clone_fields(new_item, item)
            getattr(instance, field.name).add(new_item)
            new_item.is_draft = True
            new_item.draft_of = item
            new_item.save()

    return instance, duplicate
