"""cubicweb-seda application package

Data Exchange Standard for Archival
"""

from cubicweb import neg_role

from cubes.compound import structure_def, skip_rtypes_set


def seda_profile_container_def(schema):
    """Define container for SEDAProfile"""
    return structure_def(schema, 'SEDAArchiveTransfer').items()


def iter_external_rdefs(eschema, skip_rtypes=skip_rtypes_set(['container'])):
    """Return an iterator on (rdef, role) of external relations from entity schema (i.e.
    non-composite relations).
    """
    for rschema, targets, role in eschema.relation_definitions():
        if rschema in skip_rtypes:
            continue
        for target_etype in targets:
            rdef = eschema.rdef(rschema, role, target_etype)
            if rdef.composite:
                continue
            yield rdef, role


def iter_all_rdefs(schema, container_etype):
    """Return an iterator on (rdef, role) of all relations of the compound graph starting from the
    given entity type, both internal (composite) and external (non-composite).
    """
    for etype, parent_rdefs in structure_def(schema, container_etype).items():
        for rtype, role in parent_rdefs:
            for rdef in schema[rtype].rdefs.values():
                yield rdef, neg_role(role)
        for rdef, role in iter_external_rdefs(schema[etype]):
                yield rdef, role
    for rdef, role in iter_external_rdefs(schema[container_etype]):
        yield rdef, role
