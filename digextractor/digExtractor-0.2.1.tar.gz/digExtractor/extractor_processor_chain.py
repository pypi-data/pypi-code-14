

def execute_processor_chain(doc, processors):
    extracted_doc = reduce(processor_chain_reducer, iter(processors), doc)
    return extracted_doc


def processor_chain_reducer(doc, processor):
    return processor.extract(doc)
