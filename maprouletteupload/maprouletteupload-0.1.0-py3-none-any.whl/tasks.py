import geojson


def create_tasks(featurecollection, identifier_field='identifier',
        instruction_field='instruction', name_field='name'):

    for feature in featurecollection['features']:
        identifier = feature['properties'][identifier_field]
        instruction = feature['properties'][instruction_field]
        name = feature['properties'][name_field]
        del feature['properties']

        yield {
            'geometries': geojson.FeatureCollection([feature,]),
            'identifier': identifier,
            'instruction': instruction,
            'name': name,
        }
