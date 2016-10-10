"""
Command update country.
"""

from django.core.management.base import BaseCommand
from ...tools import models, region
# pylint: disable=no-member


def update_regions(numeric_names):
    "Update regions"
    model = models.ALL['Region']
    m49_query = model.objects.filter(unsd_m49=True)
    index_old = set(m49_query.values_list('numeric', flat=True))
    index_new = set(numeric_names.keys())

    print('# Region entries; %s in db vs %s in source.' % (len(index_old),
                                                            len(index_new)))

    db_obsolete = index_old.difference(index_new)
    m49_query.filter(numeric__in=db_obsolete).update(obsolete=True)
    print('# %s DB Regions entries marked obsolete.' % len(db_obsolete))

    db_insert = index_new.difference(index_old)
    tmp = list()
    for entry in numeric_names.items():
        if entry[0] in db_insert:
            instance = model()
            instance.numeric = entry[0]
            instance.english = entry[1]
            instance.unsd_m49 = True
            tmp.append(instance)

    model.objects.bulk_create(tmp)
    print('# %s DB Region entries inserted.' % len(db_insert))

    db_update = index_new.intersection(index_old)
    update_count = 0
    by_numeric = dict()
    for instance in m49_query.filter(numeric__in=db_update):
        by_numeric[instance.numeric] = instance
        if instance.english != numeric_names[instance.numeric]:
            instance.english = numeric_names[instance.numeric]
            update_count += 1
            instance.save()

    print('# %s DB Region entries updated.' % update_count)
    return len(db_obsolete), len(db_insert), update_count

def update_region_chains(lookups, chains):
    "Update the region chains"
    model = models.ALL['RegionChain']
    db_exists = dict()
    db_insert = list()
    for instance in model.objects.all():
        key = (instance.upper.numeric, instance.lower.numeric)
        db_exists[key] = instance

    for chain in chains:
        if chain not in db_exists:
            upper = lookups[chain[0]]
            lower = lookups[chain[1]]
            db_insert.append(model(upper=upper, lower=lower))

    model.objects.bulk_create(db_insert)
    print('# %s DB Region chains entries inserted.' % len(db_insert))

    delete_count = 0
    for chain in db_exists:
        if chain not in chains:
            delete_count += 1
            db_exists[chain].delete()
    print('# %s DB Region chains entries removed.' % delete_count)
    return len(db_insert), delete_count


def update_region_reference(lookups):
    "Update region references"
    countries_by_numeric = dict()
    for instance in models.ALL['Country'].objects.all():
        countries_by_numeric[instance.numeric] = instance

    count = 0
    for numeric in lookups:
        if lookups[numeric].reference is None or \
           lookups[numeric].reference.numeric != int(numeric):
            if int(numeric) in countries_by_numeric:
                lookups[numeric].reference = countries_by_numeric[int(numeric)]
                count += 1
                lookups[numeric].save()

    print('# %s DB Region country references added.' % count)
    return count


def update():
    "Standard function to update data."
    print('#' * 80)
    print('# Update Regions')
    numeric_names, chains = region.get()
    update_regions(numeric_names)
    print('#' + ('-' * 79))
    lookups = {entry.numeric: entry for entry in models.Region.objects.all()}
    print('# Update Region Chains')
    update_region_chains(lookups, chains)
    print('#' + ('-' * 79))
    print('# Update Region Country References')
    update_region_reference(lookups)
    print('#' * 80)
    print('')

class Command(BaseCommand):
    """Update Countries"""
    help = "Update Country data."

    # pylint: disable=unused-argument
    def handle(self, *args, **kwargs):
        update()

