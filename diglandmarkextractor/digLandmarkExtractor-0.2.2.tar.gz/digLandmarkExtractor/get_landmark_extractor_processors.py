from digExtractor.extractor_processor import ExtractorProcessor
from digLandmarkExtractor.dig_landmark_extractor import DigLandmarkExtractor


def get_landmark_extractor_processor_for_rule_set(rule_set,
                                                  input_fields,
                                                  output_fields=None):
    if output_fields is None:
        output_fields = rule_set.names()
    extractor = DigLandmarkExtractor()
    extractor.set_rule_set(rule_set)
    extractor.set_metadata({"extractor": ""})
    extractor_processor = ExtractorProcessor()\
        .set_extractor(extractor)\
        .set_input_fields(input_fields)\
        .set_output_fields(output_fields)
    return extractor_processor


def get_landmark_extractor_processors(rule_set, input_fields):
    extractor_processors = list()
    for rule in rule_set.rules:
        output_field = rule.name
        extractor = DigLandmarkExtractor()
        extractor.set_rule(rule)
        extractor.set_metadata({"extractor": ""})
        extractor_processor = ExtractorProcessor()\
            .set_extractor(extractor)\
            .set_input_fields(input_fields)\
            .set_output_field(output_field)
        extractor_processors.append(extractor_processor)
    return extractor_processors
