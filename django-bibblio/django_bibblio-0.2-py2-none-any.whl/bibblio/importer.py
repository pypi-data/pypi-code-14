import logging
from .settings import MINIMAL_RELEVANCE

logger = logging.getLogger(__name__)


def process_keywords(bibblio_id_map, ignore_ids, keywords):
    """
    Process the keywords in the metadata
    """
    from .models import Metadata

    for keyword in keywords:
        if 'text' not in keyword:
            logger.error("Keyword record doesn't contain 'text'.")
            continue
        if 'relevance' not in keyword:
            logger.error("Keyword record for '%s' doesn't contain 'relevance'." % keyword['text'])
            continue
        mdata, created = Metadata.objects.get_or_create(text=keyword['text'], type='Keyword')
        if mdata.id in ignore_ids:
            logger.info("Skipping %s because it is ignored." % keyword['text'])
            continue
        if keyword['relevance'] < MINIMAL_RELEVANCE:
            logger.info("Skipping %s because its relevance (%s) is below %s." % (keyword['text'], keyword['relevance'], MINIMAL_RELEVANCE))
            continue
        bibblio_id_map.contentmetadata_set.create(
            content_type=bibblio_id_map.content_type,
            object_id=bibblio_id_map.object_id,
            bibblio_id=bibblio_id_map,
            metadata=mdata,
            relevance=keyword['relevance']
        )


def process_entities(bibblio_id_map, ignore_ids, entities):
    """
    Process the entities in the metadata
    """
    from .models import Metadata
    import json

    for entity in entities:
        if 'text' not in entity:
            logger.error("Entity record doesn't contain 'text'.")
            continue
        if 'relevance' not in entity:
            logger.error("Entity record for '%s' doesn't contain 'relevance'." % entity['text'])
            continue
        if 'type' not in entity:
            logger.error("Entity record for '%s' doesn't contain 'type'." % entity['text'])
            continue
        mdata, created = Metadata.objects.get_or_create(
            text=entity['text'],
            type=entity['type'],
            defaults={'linked_data': json.dumps(entity.get('linkedData', {}))})
        if mdata.id in ignore_ids:
            logger.info("Skipping %s because it is ignored." % entity['text'])
            continue
        if entity['relevance'] < MINIMAL_RELEVANCE:
            logger.info("Skipping %s because its relevance (%s) is below %s." % (entity['text'], entity['relevance'], MINIMAL_RELEVANCE))
            continue
        bibblio_id_map.contentmetadata_set.create(
            content_type=bibblio_id_map.content_type,
            object_id=bibblio_id_map.object_id,
            bibblio_id=bibblio_id_map,
            metadata=mdata,
            count=entity.get('count', 0),
            relevance=entity['relevance']
        )


def process_alignments(bibblio_id_map, ignore_ids, alignments):
    """
    Process the alignments in the metadata
    """
    from .models import Metadata
    import json

    for alignment in alignments:
        if 'text' not in alignment:
            logger.error("Alignment record doesn't contain 'text'.")
            continue
        level_data = {
            'levelCounts': alignment.get('levelCounts', []),
            'levels': alignment.get('levels', []),
        }
        mdata, created = Metadata.objects.get_or_create(
            text=alignment['text'],
            type='Alignment',
            defaults={'linked_data': json.dumps(alignment.get('linkedData', {}))})
        if mdata.id in ignore_ids:
            logger.info("Skipping %s because it is ignored." % alignment['text'])
            continue
        bibblio_id_map.contentmetadata_set.create(
            content_type=bibblio_id_map.content_type,
            object_id=bibblio_id_map.object_id,
            bibblio_id=bibblio_id_map,
            metadata=mdata,
            count=alignment.get('frequency', 0),
            relevance=0,
            additional_data=json.dumps(level_data)
        )


def process_concepts(bibblio_id_map, ignore_ids, concepts):
    """
    Process the concepts in the metadata
    """
    from .models import Metadata
    import json

    for concept in concepts:
        if 'text' not in concept:
            logger.error("Concept record doesn't contain 'text'.")
            continue
        if 'relevance' not in concept:
            logger.error("Concept record for '%s' doesn't contain 'relevance'." % concept['text'])
            continue
        mdata, created = Metadata.objects.get_or_create(
            text=concept['text'],
            type='Concept',
            defaults={'linked_data': json.dumps(concept.get('linkedData', {}))})
        if mdata.id in ignore_ids:
            logger.info("Skipping %s because it is ignored." % concept['text'])
            continue
        if concept['relevance'] < MINIMAL_RELEVANCE:
            logger.info("Skipping %s because its relevance (%s) is below %s." % (concept['text'], concept['relevance'], MINIMAL_RELEVANCE))
            continue
        bibblio_id_map.contentmetadata_set.create(
            content_type=bibblio_id_map.content_type,
            object_id=bibblio_id_map.object_id,
            bibblio_id=bibblio_id_map,
            metadata=mdata,
            count=0,
            relevance=concept['relevance']
        )


def process_metadata(bibblio_id_map, metadata):
    """
    Process the `metadata` part of the Bibblio record.
    """
    # Get rid of everything except what was marked "ignore" for this content
    #   That way we know to keep ignoring it.
    bibblio_id_map.contentmetadata_set.exclude(ignore=True).delete()

    ignore_ids = list(bibblio_id_map.contentmetadata_set.select_related().filter(ignore=True).values_list('metadata_id', flat=True))
    process_keywords(bibblio_id_map, ignore_ids, metadata.get('keywords', []))
    process_concepts(bibblio_id_map, ignore_ids, metadata.get('concepts', []))
    process_entities(bibblio_id_map, ignore_ids, metadata.get('entities', []))
    process_alignments(bibblio_id_map, ignore_ids, metadata.get('alignments', []))


def process_record(record, bibblio_id_map=None):
    """
    Process a Bibblio result record.

    record should be a dict
    """
    from .models import BibblioIDMap
    try:
        content_item_id = record['contentItemId']
        if bibblio_id_map is None:
            bibblio_id_map = BibblioIDMap.objects.get(bibblio_id=content_item_id)
    except BibblioIDMap.DoesNotExist:
        logger.error("Cannot find content for contentItemId='%s'." % content_item_id)
        return
    except KeyError:
        logger.error("Record is missing 'contentItemId'.")
        return
    try:
        metadata = record['metadata']
        process_metadata(bibblio_id_map, metadata)
    except KeyError:
        logger.error("Record is missing 'metadata'.")
        return
    except Exception as e:
        logger.error("Error processing metadata: %s" % e)
        return
